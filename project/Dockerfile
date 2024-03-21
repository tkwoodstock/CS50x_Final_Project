## example build command: docker build -f Dockerfile -t <image_name> .

# get python 3.7 (built on top of linux distro)
FROM python:3.10-slim

# set the working directory 
WORKDIR /flask_app

# get the flask project into the working directory 
# (run build command from inside project/ directory)
COPY . /flask_app

# get requirements
RUN python -m pip install -r requirements.txt

# run flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
