from flask import Flask, render_template, request
from pymysql import connections
from datetime import datetime   # datetime import 
import os
import random
import argparse

app = Flask(__name__)

# Environment Variables from Secret or ConfigMap
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("MYSQL_USER", "root")
DBPWD = os.environ.get("MYSQL_PASSWORD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", 3306))

HEADER_NAME = os.environ.get("HEADER_NAME", "Your Name Here")
BACKGROUND_IMAGE_URL = os.environ.get("BACKGROUND_IMAGE_URL", "")
print(f"[LOG] Background image URL: {BACKGROUND_IMAGE_URL}")

# MySQL Connection
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

# Color config
color_codes = {
    "red": "#e74c3c",
    "green": "#16a085",
    "blue": "#89CFF0",
    "blue2": "#30336b",
    "pink": "#f4c2c2",
    "darkblue": "#130f40",
    "lime": "#C1FF9C",
}
SUPPORTED_COLORS = ",".join(color_codes.keys())
COLOR_FROM_ENV = os.environ.get('APP_COLOR', "lime")
COLOR = random.choice(list(color_codes.keys()))

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', color=color_codes[COLOR], bg=BACKGROUND_IMAGE_URL, name=HEADER_NAME)

@app.route("/about", methods=['GET','POST'])  # changing the about route to make sure background image show
def about():
    return render_template('about.html', color=color_codes[COLOR], name=HEADER_NAME, bg=BACKGROUND_IMAGE_URL, now=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    print("Employee added:", emp_name)
    return render_template('addempoutput.html', name=emp_name, color=color_codes[COLOR])

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", color=color_codes[COLOR])

@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']
    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
        else:
            return "No employee found with ID: " + emp_id
    except Exception as e:
        print(e)
        return "An error occurred while fetching data."
    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"],
                           location=output["location"], color=color_codes[COLOR])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()

    if args.color:
        print("Color from command line argument =", args.color)
        COLOR = args.color
    elif COLOR_FROM_ENV:
        print("Color from environment variable =", COLOR_FROM_ENV)
        COLOR = COLOR_FROM_ENV
    else:
        print("Using random color:", COLOR)

    if COLOR not in color_codes:
        print("Invalid color. Choose from:", SUPPORTED_COLORS)
        exit(1)

    app.run(host='0.0.0.0', port=81, debug=True)
