import json
import os
import azure.functions as func
import pyodbc
import datetime

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def convert_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()

connection_string = os.environ["AzSQLConnString"]

@app.route(route="GetAllBlogEntries")
def GetAllBlogEntries(req: func.HttpRequest) -> func.HttpResponse:
    with pyodbc.connect(connection_string) as conn:
        with conn.cursor() as cursor:
            # Execute a SQL query
            cursor.execute("SELECT TOP 10 * FROM Blog")
            rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
            data = []
            columns = [column[0] for column in cursor.description]
            for row in rows:
                data.append(dict(zip(columns, row)))

            # Convert the list of dictionaries to JSON
            json_data = json.dumps(data, indent=4, default=convert_datetime)

    # Return the JSON data as the response
    return func.HttpResponse(json_data, mimetype="application/json")