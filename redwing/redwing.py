import re
import csv
import fileinput
from StringIO import StringIO
from sqlalchemy.schema import CreateTable
from sqlalchemy import Table, MetaData, Column, create_engine
from sqlalchemy.types import Integer, Numeric, Date, String, Text


# The int and numeric regex will exclude
# numbers that seem to be zero-padded.
int_regex = re.compile('^([-1-9](?=[0-9])[\d]*|[0-9])$')

# numeric includes anything that also includes a decimal
numeric_regex = re.compile('^((-?0(\.\d*)?)|(-?[1-9\.]\d*(\.\d*)?))$')
date_regex = re.compile('[\d]{1,2}\/[\d]{1,2}\/[\d]{2,4}')


class DataType(object):
    """ Detect a data type and return a SQLAlchemy SQL data type. """
    def test_type(self, value):
        raise NotImplemented

    def to_sql(self):
        raise NotImplemented


class IntegerDataType(DataType):
    def test_type(self, value):
        return bool(int_regex.match(value)) or len(value) == 0

    def to_sql(self, data_column):
        return Integer


class NumericDataType(DataType):
    def test_type(self, value):
        return bool(numeric_regex.match(value)) or len(value) == 0

    def to_sql(self, data_column):
        return Numeric


class DateDataType(DataType):
    def test_type(self, value):
        return bool(date_regex.match(value))

    def to_sql(self, data_column):
        return Date


class StringDataType(DataType):
    def test_type(self, value):
        return len(value) < 256

    def to_sql(self, data_column):
        return String(data_column.max_length)


class TextDataType(DataType):
    """ Default type. Always returns true. """
    def test_type(self, value):
        return True

    def to_sql(self, data_column):
        return Text


# The order here is important.
DEFAULT_TYPECHECKS = [IntegerDataType(),
    NumericDataType(),
    DateDataType(),
    StringDataType(),
    TextDataType()]


class DataColumn(object):
    name = ''
    max_length = 0

    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return self.name

    def update_length(self, length):
        if self.max_length < length:
            self.max_length = length

    def get_slugified_name(self):
        value = self.name
        value = re.sub('[^\w\s-]', '', value).strip().lower()
        return re.sub('[-\s]+', '-', value)


class DataScanner(object):

    def __init__(self, typechecks=DEFAULT_TYPECHECKS, filename=None):
        if filename is None:
            self.reader = csv.reader(fileinput.input())
        else:
            self.reader = csv.reader(open(filename, 'r'))

        self.typechecks = typechecks
        self.data_columns = []

    def scan(self):
        for i, row in enumerate(self.reader):
            if i == 0:
                for h in row:
                    self.data_columns.append(DataColumn(h))
                continue

            for j, value in enumerate(row):
                # some data has blank spaces. ignore it.
                # TODO - make this optional.
                value = value.strip()

                column = self.data_columns[j]
                column.update_length(len(value))

                # if we've already fallen down the tunnel to the
                # default data type, no need to retest everything again.
                if getattr(column, 'is_{data_type}'.format(data_type=self.typechecks[-1].__class__.__name__), False):
                    continue
                for typecheck in self.typechecks:
                    target_attr = 'is_%s' % typecheck.__class__.__name__
                    is_data_type = getattr(column, target_attr, None)
                    if is_data_type is None:
                        # has not been tested. test it!
                        if typecheck.test_type(value):
                            setattr(column, target_attr, True)
                            break
                        else:
                            setattr(column, target_attr, False)
                            continue
                    elif is_data_type is False:
                        continue
                    else:
                        # was tested, passed before, confirm.
                        setattr(column, target_attr, typecheck.test_type(value))
                        break

    def get_sql_column_types(self):
        sql_column_types = []
        for column in self.data_columns:
            for typecheck in self.typechecks:
                if getattr(column, 'is_%s' % typecheck.__class__.__name__, False) is True:
                    # print("%s\t%s\t%s" % (header.name, typecheck.__class__.__name__, header.max_length))
                    sql_column_types.append(Column(column.get_slugified_name(), typecheck.to_sql(column)))
        return sql_column_types

    def get_sql_to_string(self, tablename=None):
        if tablename is None:
            tablename = 'tablename'

        buf = StringIO()

        def dump(sql, *multiparams, **params):
            buf.write(sql.__str__() + ";\n")

        engine = create_engine('postgres://', strategy='mock', executor=dump)
        table_args = [tablename, MetaData()] + self.get_sql_column_types()
        t = Table(*table_args)
        table_sql = CreateTable(t).compile(engine)
        return table_sql
