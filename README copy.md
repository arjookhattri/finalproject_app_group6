# Install the required MySQL package

sudo apt-get update -y
sudo apt-get install mysql-client -y

# Running application locally
pip3 install -r requirements.txt
sudo python3 app.py
# Building and running 2 tier web application locally
### Building mysql docker image 
```docker build -t my_db -f Dockerfile_mysql . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

### Create a network
```docker network create clo835 || true```

### Running mysql
```docker run -d --name mydb --network clo835 -e MYSQL_DATABASE=employees -e MYSQL_ROOT_PASSWORD=password -p 3306:3306  my_db```


```
### Example when running DB runs as a docker container and app is running locally
```
export DBHOST=mydb
export DBPORT=3306
export DBUSER=root
export DATABASE=employees
export DBPWD=password
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=
export AWS_REGION=us-east-1


### Run the application, make sure it is visible in the browser
```docker run -p 81:81  -e DBHOST=$DBHOST -e DBPORT=$DBPORT -e  DBUSER=$DBUSER -e DBPWD=$DBPWD  my_app```
 docker run -d --name flaskapp-container --network clo835 -p 81:81 \
-e DBHOST=$DBHOST \
-e DBPORT=$DBPORT \
-e DATABASE=$DATABASE \
-e DBUSER=$DBUSER \
-e DBPWD=$DBPWD \
-e S3_BUCKET_NAME=$S3_BUCKET_NAME \
-e S3_OBJECT_KEY=$S3_OBJECT_KEY \
-e AWS_REGION=$AWS_REGION \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
-e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN \
my_app