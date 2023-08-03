from bardapi import Bard
import requests
from flask import Flask, request, jsonify
from keep_alive import keep_alive

token = "ZQg_XuFf4Z5tg3DvkLIVZTODiwvKzcDZiuaEWFS_u6m9BSk2saWvsA9YFRI2zGQXuW159A."
bard = Bard(token=token)

app = Flask(__name__)

keep_alive()

if __name__ == '__main__':
  app.run(port=6969)
