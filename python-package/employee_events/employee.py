from .query_base import QueryBase

class Employee(QueryBase):

    name = "employee"

    def names(self):
        # Grab all employees from the database with full names and IDs
        # We mash together first and last name for display purposes
        sql_query = """
                       SELECT first_name || ' ' || last_name AS full_name, employee_id
                       FROM employee
                """
        return self.query(sql_query)

    def username(self, id):
        # Given an employee ID, this pulls their full name from the database
        sql_query = f"""
                    SELECT first_name || ' ' || last_name AS full_name
                    FROM employee
                    WHERE employee_id = {id}
                """
        return self.query(sql_query)

    def model_data(self, id):
        # This is where we fetch the data we want to feed into our model
        # It grabs total counts of good and bad events for one employee
        sql_query = f"""
               SELECT SUM(positive_events) AS positive_events,
                      SUM(negative_events) AS negative_events
               FROM {self.name}
               JOIN employee_events USING({self.name}_id)
               WHERE {self.name}.{self.name}_id = {id}
           """

        return self.pandas_query(sql_query)