from flask import *
from flask_bootstrap import Bootstrap
import sys, operations

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
@app.route('/home')

def home():
    return render_template('home.html')

@app.route("/database")
def database():
    return render_template("database.html")

@app.route("/devices", methods=["POST", "GET"])
def devices():

    if request.method == 'POST':
        operations.dev_prepare_config(request.form)
    

    return render_template("devices.html", data=operations.show_config())


@app.route("/graphs")
def graphs():
    return render_template("graphs.html")

@app.route("/run", methods=["POST", "GET"])
def run():
    if request.method == 'POST':
       operations.run_tasks(request.form)
        
    return render_template("run.html")



if __name__ == "__main__":
    app.run(debug=True, port=4951)