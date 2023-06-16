from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = "0d6c0cb3b2b662ba13986fbff4f988e6"


from practico_07.sociosflask import routes