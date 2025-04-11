from flask import Flask, render_template, request
from pymysql import connections
import os
import argparse
import boto3
import logging
from dotenv import load_dotenv

# Load local environment variables (for local development)
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Function to download background image from private S3 using env config
def download_background_image():
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    object_key = os.environ.get("S3_OBJECT_KEY")
    local_file_path = "static/backgroundseneca.jpg"

    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not all([bucket_name, object_key, aws_access_key, aws_secret_key, aws_session_token]):
        logging.error("Missing S3 configuration in environment variables. Using default background image.")
        return "/static/default.jpg"  # Ensure this image exists locally

    logging.info(f"Using S3 bucket: {bucket_name}, object key: {object_key}")

    try:
        os.makedirs("static", exist_ok=True)
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            aws_session_token=aws_session_token,
            region_name=aws_region
        )
        s3.download_file(bucket_name, object_key, local_file_path)
        logging.info(f"Downloaded background image to {local_file_path}")
        return "/static/backgroundseneca.jpg"
    except Exception as e:
        logging.error(f"Failed to download background image from S3: {e}")
        return "/static/default.jpg"

# Download background image at container startup
background_image_path = download_background_image()

app = Flask(__name__)

# Load database environment variables
DBHOST = os.environ.get("DBHOST", "mysql")
DBUSER = os.environ.get("MYSQL_USER", "root")          # Updated
DBPWD = os.environ.get("MYSQL_PASSWORD", "password")   # Updated
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", 3306))
HEADER_NAME = os.environ.get("HEADER_NAME", "Clo835 Group 6")

# Connect to MySQL
try:
    logging.info(f"Connecting to MySQL at {DBHOST}:{DBPORT} as {DBUSER}")
    db_conn = connections.Connection(
        host=DBHOST,
        port=DBPORT,
        user=DBUSER,
        password=DBPWD,
        db=DATABASE
    )
    logging.info("MySQL connection successful.")
except Exception as db_error:
    logging.error(f"Failed to connect to MySQL: {db_error}")
    db_conn = None

# Routes
@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', bg=background_image_path, name=HEADER_NAME)

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', name=HEADER_NAME, bg=background_image_path)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    if db_conn is None:
        return "[ERROR] Database connection failed. Cannot add employee."

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

    return render_template('addempoutput.html', name=emp_name, bg=background_image_path)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", bg=background_image_path)

@app.route("/fetchdata", methods=['GET', 'POST'])
def FetchData():
    if db_conn is None:
        return "[ERROR] Database connection failed. Cannot fetch data."

    emp_id = request.form['emp_id']
    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
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
        logging.error(f"An error occurred while fetching data: {e}")
        return "An error occurred while fetching data."
    finally:
        cursor.close()

    return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                           lname=output["last_name"], interest=output["primary_skills"],
                           location=output["location"], bg=background_image_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    app.run(host='0.0.0.0', port=81, debug=True)
