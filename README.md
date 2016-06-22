## About 

This script checks status of aws services in North America region and sends list of broken services to specified email address. It could be enhanced to monitor other regions as well.  Script runs in Docker container. Docker container contains also local smtp server based on postfix.

## Build docker image

	docker build -t <namespace>/monitor:<tag> .

for example:

	docker build -t enelen/monitor:v1 .

## Run docker container

Docker container supports next environment variables:
* **SMTP_SERVER**  - address of smtp server to use
* **FROM_ADDRESS** - script will send mails from this email address
* **TO_ADDRESS** - script will send mails to this email address

Example:

 	docker run -it -e TO_ADDRESS='test@test.com' -e FROM_ADDRESS='monitoring@test.com' enelen/monitor:v1 
