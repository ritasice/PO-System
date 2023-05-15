import os
import json

with open("Routes/config.json") as config_file:
    config = json.load(config_file)


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLSERVER_IP = config.get('SQLSERVER_IP')
    SQLSERVER_USER = config.get('SQLSERVER_USER')
    SQLSERVER_PASS = config.get('SQLSERVER_PASS')

