from flask import Flask
from config.config import key
import google.generativeai as genai   # type: ignore

#! New Config without sessions
def create_app():
    app = Flask(__name__,template_folder='/templates')
    return app


#initializing app
app=create_app()

genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-pro')

