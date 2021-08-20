import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_DB_URL = os.getenv('DB_CONN')
app.config['SQLALCHEMY_DATABSE_URI'] = SQLALCHEMY_DB_URL
db = SQLAlchemy(app)


@app.before_first_request
def setup():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
