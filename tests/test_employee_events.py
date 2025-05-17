import pytest
from pathlib import Path

# Figure out where our project root is (two levels up from this test file)
project_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def db_path():
    # Construct the full path to the database file
    # If it's missing, one of the tests below will catch it
    return project_root / "python-package" / "employee_events" / "employee_events.db"


def test_db_exists(db_path):
    # Let’s make sure the database file is actually there
    assert db_path.is_file(), f"The database file does not exist: {db_path}"


@pytest.fixture
def db_conn(db_path):
    # Open a connection to the SQLite database file
    from sqlite3 import connect
    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    # Grab a list of all table names from the database
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [x[0] for x in name_tuples]


def test_employee_table_exists(table_names):
    # Make sure the 'employee' table exists in the database
    assert "employee" in table_names, "Table 'employee' does not exist in the database"


def test_team_table_exists(table_names):
    # Make sure the 'team' table exists in the database
    assert "team" in table_names, "Table 'team' does not exist in the database"


def test_employee_events_table_exists(table_names):
    # And don’t forget the one that tracks the actual events
    assert "employee_events" in table_names, "Table 'employee_events' does not exist in the database"
