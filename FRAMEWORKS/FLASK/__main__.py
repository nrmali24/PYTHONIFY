from flask import Flask,make_response
import sqlalchemy as sa
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists,create_database
from cors import CORS 


connection_url=f"{server}://{username}:{password}@{host}/{database}"
engine=create_engine(connection_url)

if database_exists(engine.url):
    create_database(engine.url)





app= Flask(__name__)
cors=CORS(app)
db=sqlalchemy(app)



@app.route("/")
def Home():
    return make_response({"status":"Success","message":"we are in the flask app"},200)


if __name__=="__main__":
    app.run(debug=True)

