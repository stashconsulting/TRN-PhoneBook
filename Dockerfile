# init a base image (Alpine is small Linux distro)
FROM python:3.9.5
# define the present working directory
WORKDIR /docker-flask-testsql

COPY requirements.txt /docker-flask-testsql/

RUN pip install -r requirements.txt


# copy the contents into the working dir
COPY . /docker-flask-testsql

ENTRYPOINT [ "./docker-entrypoint.sh" ]

# define the port
EXPOSE 8080


