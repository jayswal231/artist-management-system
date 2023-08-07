from django.db import connection

def execute_query(query, params=None):
    with connection.cursor() as cursor:
        if params is None:
            cursor.execute(query)
        else:
            cursor.execute(query, params)
        result = cursor.fetchall()
    return result