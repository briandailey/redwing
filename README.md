#### Redwing: Python Type-Inference for CSV Files

This script reads CSV file and infers data types.

It does a few other things, too, like determining max length for character fields.

It expects a CSV with a header row.

Currently, it works like this:


    redwing csvfile.csv --tablename=tablename

Output is a SQL creation script.

    CREATE TABLE tablename (
    id INTEGER,
    name VARCHAR(5)
    )
