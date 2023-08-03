from bardapi import Bard
import requests
import flask
from threading import Thread
from flask import Flask, request, jsonify

app = Flask(__name__)

def runapp():
  app.run()

def keep_alive():
  Thread(target=runapp).start()
