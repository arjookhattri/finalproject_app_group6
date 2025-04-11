# finalproject_app_group6

# create SSH key 

```ssh-keygen``` 

# update aws credentials 

```aws configure```
```vim ~/.aws/credentials``` 
 
# create EKS cluster 

```eksctl create cluster -f  eks-cluster.yaml```

```curl -LO https://dl.k8s.io/release/v1.32.0/bin/linux/amd64/kubectl```

```sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl```

```rm -f ./kubectl```

```chmod 755 kubectl```

```kubectl get pods -A```

# delete the cluster 

```eksctl delete cluster -f  eks-cluster.yaml```  

# Install the required MySQL package

```sudo apt-get update -y```
```sudo apt-get install mysql-client -y```

# Running application locally

```pip3 install -r requirements.txt```
```sudo python3 app.py```

# Building and running 2 tier web application locally

### Building mysql docker image 
```docker build -t my_db -f Dockerfile_mysql . ```

### Building application docker image 
```docker build -t my_app -f Dockerfile . ```

### Running mysql
```docker run -d -e MYSQL_ROOT_PASSWORD=pw  my_db```

### Get the IP of the database and export it as DBHOST variable
```docker inspect <container_id>```


# Apply the manifests in order : 

```kubectl apply -f namespaces.yaml```
```kubectl apply -f configmap.yaml```
```kubectl apply -f secret.yaml```
```kubectl apply -f pvc.yaml```
```kubectl apply -f serviceaccount.yaml```
```kubectl apply -f rbac.yaml```
```kubectl apply -f mysql-deployment.yaml```
```kubectl apply -f mysql-service.yaml```
```kubectl apply -f flask-deployment.yaml```
```kubectl apply -f flask-service.yaml```

# create secret for ecr (edit AWS account and email)

```kubectl create secret -n final docker-registry ecr-secret   --docker-server=860572194478.dkr.ecr.us-east-1.amazonaws.com   --docker-username=AWS   --docker-password=$(aws ecr get-login-password --region us-east-1)   --docker-email=rgaraween@myseneca.ca```

# Check pods 

```kubectl get pods -n final```
