from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    grades = data.get('grades', [])
    average = sum(grades) / len(grades) if grades else 0
    return jsonify({'average': average})

if __name__ == '__main__':
    app.run(debug=True)
