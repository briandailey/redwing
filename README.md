#### Redwing: Python Type-Inference for CSV Files

Yes, I'm aware this requires some serious cleanup.

This script takes in a piped CSV file and will infer data types. The philosphy is that you provide a list of types that create a fall-down scenario. If it doesn't match the first type, then it falls down to the next. The default type is Text.

It does a few other things, too, like determining max length for character fields.

It expects a CSV with a header row.

Currently, it works like this:

In:

    cat mycsvfile.csv | python redwing.py

Out:

    CREATE TABLE tablename (
    id INTEGER,
    name VARCHAR(5)
    )
