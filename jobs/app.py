from flask import Flask, render_template, g
import sqlite3

#create an app instance using Flask constructor
PATH = 'db/jobs.sqlite'

app = Flask(__name__)

# connection to the databse
def open_connection():
    connection=getattr(g, '_connection', None)
    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row
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

#making sure the connection is closed
@app.teardown_appcontext
def close_connection(exception):
    connection=getattr(g, '_connection', None)
    if connection!=None:
        connection.close()


#basic route
@app.route('/')
@app.route('/jobs')
def jobs():
    jobs=execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


@app.route('/job/<job_id>')
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)
