#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/tyler/flask_app/CS50x_Final_Project/app/")

from app import app as application
#application.secret_key = ''

if __name__ == "__main__":
    application.run()
