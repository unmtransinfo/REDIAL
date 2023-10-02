# REDIAL
This repository contains ML models for predicting Anti-SARS-CoV-2 Activities (`Live Virus Infectivity`, `Viral Entry`, `Viral Replication`) and for performing Similarity Search<br/>
- Website: http://drugcentral.org/Redial

## Installation with Docker
To run the application on your system, you need docker installed. You can run the app directly using docker by using the following command to do so

    docker-compose -f docker-compose-prod.yml --env-file .env.prod up --build -d

You can leave out `-d` flag if you do not wish to run in detached mode

> Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to check out the running server.

> Note: You will need to create a new file .env.prod, which will contain environment variables (secret keys) for the project

GID=501
    USER=appuser
    IMAGE_NAME=redial-2023

#### Adding AWS project configuration for S3 bucket access
You need to add AWS configuration files (credentials, config) for the project code to use the necessary model files, and other static files available on S3 buckets.
For this, you need to use steps mentioned on this [link](https://aws.amazon.com/cli/) to configure AWS CLI. 
***You need to have your AWS account details for this step.***

## Deployment on AWS
With the current AWS structure, we need to create an EC2 instance to run the docker container, and Route 53 to use DNS service.

 - With EC2 instance, the Github repository can be connected to AWS to
   maintain CI/CD (Amazon Linux Image). 
 - The Route 53 needs to be connected to the existing (or new?) domain name, and needs some DNS information as input, which is provided by domain name provider (Varies for providers).

After the EC2 is created, connect using the SSH client option (you need the `.pem` file generated during EC2 initialization to connect using this option), or directly using the console
On successful connection, install docker, docker-compose and git on the instance using the following commands

> Note: If you want to allow traffic over HTTP and HTTPS, make sure to check the options under **Network Settings** while creating EC2 instance.

### Installing Docker

    sudo yum install docker 
    sudo service docker start 
    sudo usermod -a -G docker ec2-user

Use the command below to auto start docker

    sudo chkconfig docker on

### Installing Git

    sudo yum install -y git

### Installing Docker Compose

    sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

Finally, after the required installations, reboot the instance by using

    sudo reboot
    
This will reboot the EC2 instance, thereby closing the shell connection that was established. 
In order to perform the further steps, connect to the instance again.

Now that Git and Docker are installed on the EC2 instance, clone the repository using 

    git clone <repository URL>
Change the current directory to access the files in the repository cloned in the step above. 

To run the server on production, simply run the bash script called ***deploy.sh*** using

    bash deploy.sh
    
The above command will spin up the docker containers and attach them to the ports exposed by the container. 

The server can now be accessed using the public IP of the EC2 instance.

> Note: You will only be able to access the server over HTTP, make sure to use http in URL instead of https

## Requesting domain name and adding SSL certificates to the server
To request a domain and add SSL certificate to the server, you need to follow these steps:-  
 1. [Requesting domain from Route53](#requesting-domain-from-route53)
 2. [Requesting certificate from ACM](#requesting-certificate-from-acm)
 3. [Creating CloudFront distribution ID to link to EC2 instance](#creating-cloudfront-distribution)
 4. [Adding Alias name records to Route53](#adding-alias-name-records-to-route53)
 5. [Verifying certificates from EC2 instance](#verifying-certificates-from-ec2-instance)

### Requesting domain from Route53
Go to Route53 in AWS console, under Registered domains register a new domain name that you want to use with your server (you need to check if the domain is available, if not, choose a different domain name). 

### Requesting certificate from ACM

To connect a domain name and add SSL certificates to access the server over HTTPS, you need to request a public certificate from [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/). Enter fully qualified domain name that you wish to request.
> Note: Click on **Add another name to this certificate** and make sure to add the domain name prefixed with `www.`

After requesting the certificate, you need to add CNAME records to Route53 and wait for validation of certificate by Amazon.

### Creating CloudFront distribution
On the AWS console, open CloudFront service, and create new distribution.

**Configuration for distribution:** 

 - Origin domain - *Public IPv4 DNS of EC2 instance which needs to be
   linked to the domain name*
- Name - *Distribution name*
- Viewer protocol policy - *Redirect HTTP to HTTPS*
- Allowed HTTP methods - *GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE*
- Cache policy - *CachingDisabled*
- Origin request policy - *AllViewer*
- Alternate domain name (CNAME) - Add two records, (a) DOMAIN_NAME (b) www.DOMAIN_NAME

And finally link the requested certificate from ACM to the distribution under ***Custom SSL certificate***, and create distribution.

### Adding Alias name records to Route53
Go to Route53 entry of your domain name, and add two A records, which need to be alias to the created CloudFront distribution. 
First record with empty record name, and the second record name will be `www`

### Verifying certificates from EC2 instance
After linking the instance and certificate using the distribution, connect to the EC2 instance either using shell access, or using the console

 - Make sure `nginx` is installed, or use

        sudo yum install nginx
    to install

- Install certbot

```
sudo python3 -m venv /opt/certbot
sudo /opt/certbot/bin/pip install --upgrade pip
sudo /opt/certbot/bin/pip install certbot certbot-nginx
sudo ln -s /opt/certbot/bin/certbot /usr/bin/certbot
```
- Request certificate installation using

    ```
    certbot certonly --nginx
    ``` 
and enter the details on the prompt

Once validation is complete, the certificates have been installed, and network traffic will work over HTTPS.
