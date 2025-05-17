from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Define where the database lives
# In this case, it's right next to this file
db_path = Path(__file__).parent.absolute() / "employee_events.db"


class QueryMixin:
    # This one gives you a DataFrame straight from your SQL string
    def pandas_query(self, sql_query):
        connection = connect(db_path)
        result = pd.read_sql_query(sql_query, connection)
        connection.close()
        return result

    # If you want raw tuples instead of a DataFrame, use this
    def query(self, sql_query):
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(sql_query).fetchall()
        connection.close()
        return result


# Just return a SQL string from your function and it'll handle the rest

def query(func):
    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result

    return run_query
