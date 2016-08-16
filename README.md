#### Redwing: Python Type-Inference for CSV Files

This script takes in a piped CSV file and will infer data types.

It does a few other things, too, like determining max length for character fields.

It expects a CSV with a header row.

Currently, it works like this:


    redwing csvfile.csv

Output is a SQL creation script.

    CREATE TABLE tablename (
    id INTEGER,
    name VARCHAR(5)
    )
