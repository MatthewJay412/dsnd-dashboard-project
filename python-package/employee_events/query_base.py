from .sql_execution import QueryMixin

class QueryBase(QueryMixin):

    name = ""

    def names(self):
        # Just a placeholder for now, returns an empty list
        # Real implementations override this to fetch actual names
        return []

    def event_counts(self, id):
        # Pulls event counts for a given ID, grouped by date
        # Great for charting trends or building timelines
        sql_query = f"""
                    SELECT event_date,
                           SUM(positive_events) AS positive_events,
                           SUM(negative_events) AS negative_events
                    FROM {self.name}
                    JOIN employee_events USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY event_date
                    ORDER BY event_date
                    """
        return self.pandas_query(sql_query)

    def notes(self, id):
        # Grabs all notes tied to the given entity (employee or team)
        # Gives you the full note history with dates
        sql_query = f"""
                    SELECT note_date, note
                    FROM notes
                    JOIN {self.name} USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    """
        return self.pandas_query(sql_query)
