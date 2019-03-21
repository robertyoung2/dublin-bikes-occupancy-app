from flask import Flask

app = Flask(__name__)
app.secret_key = ***REMOVED***
from ouiflask import routes
