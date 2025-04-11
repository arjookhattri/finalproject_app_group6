
# Final Project - Group 6: Flask + MySQL on EKS

This project demonstrates a full-stack deployment of a Flask application with a MySQL backend using Amazon EKS and Docker. 
The application integrates with AWS S3 for background images and is designed to run in both containerized and Kubernetes environments.

#install Kubectl and eksctl 

```curl -LO https://dl.k8s.io/release/v1.32.0/bin/linux/amd64/kubectl```

```sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl```

```rm -f ./kubectl```

```chmod 755 kubectl```

# update aws credentials 

## Prerequisites

- AWS Cloud9 or EC2 instance with IAM role access
- AWS CLI configured
- Docker installed
- `eksctl` and `kubectl` installed

```eksctl create addon   --name aws-ebs-csi-driver   --cluster group6-final-project-eks   --region us-east-1```
---

## 1. AWS Credential Configuration

### Disable Cloud9 Managed Credentials
```bash
aws cloud9 update-environment --environment-id $C9_PID --managed-credentials-action DISABLE
```

### Remove and Edit AWS Credentials
```bash
rm -vf ${HOME}/.aws/credentials
nano ~/.aws/credentials
```

---

## 2. Install Required Tools

### Install `eksctl`
```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

### Install `kubectl`
```bash
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

---

## 3. EKS Cluster Setup

### Create the EKS Cluster
```bash
eksctl create cluster -f eks-cluster.yaml
```

### Create EBS CSI Addon
```bash
eksctl create addon   --name aws-ebs-csi-driver   --cluster group6-final-project-eks   --region us-east-1
```

### Update kubeconfig
```bash
aws eks update-kubeconfig --name group6-final-project-eks --region us-east-1
```

### Check Cluster Status
```bash
kubectl cluster-info
```

---

## 4. Deploy Kubernetes Resources

### Apply Resources in Order
```bash
kubectl apply -f namespaces.yaml -n final
kubectl apply -f pvc.yaml -n final
kubectl apply -f configmap.yaml -n final
kubectl apply -f secret.yaml -n final
kubectl apply -f mysql-deployment.yaml -n final
kubectl apply -f mysql-service.yaml -n final
kubectl apply -f flask-deployment.yaml -n final
kubectl apply -f flask-service.yaml -n final
```


## 5. ECR Secret Creation (replace email and AWS account)
```bash
kubectl create secret -n final docker-registry ecr-secret   --docker-server=813634909417.dkr.ecr.us-east-1.amazonaws.com   --docker-username=AWS   --docker-password=$(aws ecr get-login-password --region us-east-1)   --docker-email=akhattri@myseneca.ca
```

### Apply RBAC and Service Account
```bash
kubectl apply -f rbac.yaml -n final
kubectl apply -f serviceaccount.yaml -n final
```

---

## 6. Verify Deployment

### Check Pods and Services
```bash
kubectl get pods -n final
kubectl get svc -n final
```

---

## 7. Docker Build & Local Test (Optional)

### Build Docker Images
```bash
docker build -t my_db -f Dockerfile_mysql .
docker build -t my_app -f Dockerfile .
```

### Create Docker Network
```bash
docker network create clo835 || true
```

### Run MySQL Container
```bash
docker run -d --name mydb --network clo835   -e MYSQL_DATABASE=employees   -e MYSQL_ROOT_PASSWORD=password   -p 3306:3306 my_db
```

### Export Environment Variables
```bash
export DBHOST=mydb
export DBPORT=3306
export DBUSER=root
export DBPWD=my-secret
export DATABASE=employees
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_SESSION_TOKEN=
export S3_BUCKET_NAME=clo835s3bucketgroup6
export S3_OBJECT_KEY=backgroundseneca.jpg
```

### Run Flask App Locally in Docker
```bash
docker run -d --name flaskapp-container --network clo835 -p 81:81   -e DBHOST=$DBHOST   -e DBPORT=$DBPORT   -e DATABASE=$DATABASE   -e DBUSER=$DBUSER   -e DBPWD=$DBPWD   -e S3_BUCKET_NAME=$S3_BUCKET_NAME   -e S3_OBJECT_KEY=$S3_OBJECT_KEY   -e AWS_REGION=$AWS_REGION   -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID   -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY   -e AWS_SESSION_TOKEN=$AWS_SESSION_TOKEN   my_app
```
#To show the log entry of backgorung image
kubectl logs flask-app-6bc6d48fdc-2lfd4 -n final 
---

## 8. Delete the Cluster (Optional)
```bash
eksctl delete cluster -f eks-cluster.yaml
```

---

## Authors

- **Arjoo Khattri**  
- **Final Project Group 6 – CLO835**  

---

## License

MIT License – see `LICENSE.md` for details.
