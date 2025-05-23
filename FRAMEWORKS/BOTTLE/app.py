from app import Bottle
app=Bottle()

@app.route('/')
def home():
    return "Hello, Bottle!"

@app.route('/hello/<name>')
def greet(name):
    return f"Hello, {name}!"

if __name__=="__main__":
    app.run(host="localhost",port=5000,debug=True)