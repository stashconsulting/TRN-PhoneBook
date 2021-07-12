# init a base image (Alpine is small Linux distro)
FROM python:3.9.5
# define the present working directory
WORKDIR /docker-flask-testsql
# copy the contents into the working dir
COPY . /docker-flask-testsql
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python","app.py"]
# define the port
EXPOSE 80/tcp