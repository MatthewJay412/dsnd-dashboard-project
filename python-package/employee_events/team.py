from .query_base import QueryBase

class Team(QueryBase):

    name = "team"

    def names(self):
        # Grab all teams from the database with their names and IDs
        sql_query = f"""
                    SELECT team_name, team_id
                    FROM {self.name}
                    """
        return self.query(sql_query)

    def username(self, id):
        # Given a team ID, this pulls the team name from the database
        sql_query = f"""
                        SELECT team_name
                        FROM {self.name}
                        WHERE team_id = {id}
                    """
        return self.query(sql_query)

    def model_data(self, id):
        # This builds a dataset showing the total positive and negative events per employee on a team
        # It’s meant to feed into an ML model or dashboard visualization
        sql_query = f"""
            SELECT positive_events, negative_events
            FROM (
                SELECT employee_id,
                       SUM(positive_events) AS positive_events,
                       SUM(negative_events) AS negative_events
                FROM {self.name}
                JOIN employee_events
                    USING({self.name}_id)
                WHERE {self.name}.{self.name}_id = {id}
                GROUP BY employee_id
            )
        """
        return self.pandas_query(sql_query)
