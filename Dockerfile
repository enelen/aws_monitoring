FROM alpine:3.4
MAINTAINER Eugene Nelen <eugene@nelen.org.ua>

# Install packages
RUN apk add --update python py-pip py-libxml2 build-base python-dev libxslt-dev postfix

# Copy python code
COPY requirements.txt /src/requirements.txt
COPY monitor.py /src/monitor.py
COPY entry.sh /src/entry.sh

# Install python packages
RUN pip install -r /src/requirements.txt

#Environment variables
ENV SMTP_SERVER   "localhost"
ENV FROM_ADDRESS  "monitoring@test.com"
ENV TO_ADDRESS    ""

ENTRYPOINT ["/bin/ash","/src/entry.sh"]

