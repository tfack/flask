FROM python:3.10.4-slim-bullseye

#make and change to a working directory inside the container
WORKDIR /usr/src/flask-project

#copy all the files into this directory including requirements.txt
COPY . .

#we upgrade pip to the latest version
RUN pip3 install --upgrade pip

#run pip and install all the packages in requirements.txt - you can specify specific versions this way
RUN pip3 install -r requirements.txt

#default command
CMD python app.py