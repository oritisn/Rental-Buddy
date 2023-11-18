"""Used to read what's in the database"""

import os
import pandas as pd
import sqlalchemy
"""loads in the database using the same path as app.py"""
basedir = os.path.abspath(os.path.dirname(__file__))
engine = sqlalchemy.create_engine("sqlite:///" + os.path.join(basedir, 'db.sqlite'))

df=pd.read_sql("SELECT * FROM User",con=engine)
print(df)