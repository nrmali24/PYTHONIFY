import json


# ! Gemini AI api key
try:
    with open ("/config/keys.json","r") as file:
        key=json.load(file)["gemini_key"]
except Exception as e:
    raise(str(e))



