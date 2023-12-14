"""Helper file. Not intended to be imported.
Used to read what's in the database"""

import os
import pandas as pd
import sqlalchemy

"""loads in the database using the same path as app.py"""
basedir = os.path.abspath(os.path.dirname(__file__))
engine = sqlalchemy.create_engine("sqlite:///" + os.path.join(basedir, 'db.sqlite'))

db_cols = pd.read_sql(sql = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name"
                      ,con=engine)

db_cols_list = db_cols["name"].tolist()

if __name__ == '__main__':
    for col in db_cols_list:
        print("\n\n\n"+col+"\n")
        print(pd.read_sql(sql=f"SELECT * FROM {col}",con=engine))
        print(pd.read_sql(sql=f'SELECT username,email,password FROM User',con=engine))
