FROM python:3.6.1-alpine

LABEL Maintainer="Ioannis Gkinis - giannisginis53@gmail.com"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /shorty/requirements.txt

WORKDIR /shorty

RUN pip3 install -r requirements.txt

COPY . /shorty

ENTRYPOINT [ "python3" ]

CMD [ "run.py" ]