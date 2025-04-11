from flask import Flask, render_template, request
from datetime import datetime
import os
import random
import argparse
import boto3
# from pymysql import connections  # Uncomment only when MySQL is running

app = Flask(__name__)

# ----------------------- ENV VARIABLES -----------------------
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("MYSQL_USER", "root")
DBPWD = os.environ.get("MYSQL_PASSWORD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
DBPORT = int(os.environ.get("DBPORT", 3306))

HEADER_NAME = os.environ.get("HEADER_NAME", "Your Name Here")
BACKGROUND_IMAGE_URL = os.environ.get("BACKGROUND_IMAGE_URL", "")
print(f"[LOG] Background image URL: {BACKGROUND_IMAGE_URL}")

# ----------------------- COLORS -----------------------
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

# ----------------------- DOWNLOAD IMAGE FUNCTION -----------------------
def download_background_image(background_url):
    if background_url:
        print(f"[LOG] Downloading image from: {background_url}")
        try:
            s3 = boto3.client('s3')
            bucket_name = background_url.split('/')[2].split('.')[0]
            key = '/'.join(background_url.split('/')[3:])
            os.makedirs("static", exist_ok=True)
            s3.download_file(bucket_name, key, 'static/background.jpg')
        except Exception as e:
            print(f"[ERROR] Failed to download background image: {e}")

# ----------------------- ROUTES -----------------------

@app.route("/")
def index():
    download_background_image(BACKGROUND_IMAGE_URL)
    return render_template("about.html", name=HEADER_NAME, bg=BACKGROUND_IMAGE_URL, now=datetime.now().strftime("%Y-%m-%d %H:%M"))

@app.route("/about", methods=['GET','POST'])
def about():
    download_background_image(BACKGROUND_IMAGE_URL)
    return render_template('about.html', color=color_codes[COLOR], name=HEADER_NAME, bg=BACKGROUND_IMAGE_URL, now=datetime.now().strftime("%Y-%m-%d %H:%M"))

# ----------------------- TEMP DISABLED MYSQL ROUTES -----------------------

@app.route("/addemp", methods=['POST'])
def AddEmp():
    return "MySQL features disabled for local testing."

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return "MySQL features disabled for local testing."

@app.route("/fetchdata", methods=['GET','POST'])
def FetchData():
    return "MySQL features disabled for local testing."

# ----------------------- MAIN -----------------------

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
