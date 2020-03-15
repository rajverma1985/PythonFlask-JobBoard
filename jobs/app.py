from flask import Flask, render_template, g
import sqlite3
#create an app instance using Flask constructor
PATH = 'db/jobs.sqlite'
app = Flask(__name__)

# connection to the databse
def open_connection():
    connection=getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3(PATH)
    connection.row_factory=sqlite3.Row
    return connection

#function to run the query

def execute_sql(sql, values=(), commit=False, single=False):
    connection=open_connection()
    cursor=connection.execute(sql, values)
    if commit==True:
        results=connection.commit()
    else:
        results= cursor.fetchone() if single else cursor.fetchall()
    cursor.close()
    return results

@app.teardown_appcontext
def close_connection(exception):
    connection=getattr(g, '_connection', None)
    if connection!=None:
        connection.close()





#basic route
@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')
