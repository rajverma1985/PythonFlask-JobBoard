from flask import Flask, render_template

#create an app instance using Flask constructor

app = Flask(__name__)


#basic route
@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')
