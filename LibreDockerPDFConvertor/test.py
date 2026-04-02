from flask import Flask,request,make_response,jsonify,send_file
import requests
import io

app=Flask(__name__)

CONVERTER_URL = "http://localhost:8000/convert"

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    user_file = request.files['file']
    try:
        files = {'file': (user_file.filename, user_file.stream, user_file.content_type)}
        response = requests.post(CONVERTER_URL, files=files, timeout=(600,600))
        if response.status_code == 200:
            return send_file(
                io.BytesIO(response.content),
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f"{user_file.filename.rsplit('.', 1)[0]}.pdf"
            )
        else:
            return jsonify({
                "error": "Conversion failed", 
                "details": response.text
            }), response.status_code

    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Converter service is offline"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the Flask gateway on a different port (e.g., 5000)
    app.run(host='0.0.0.0', port=5000)



    # F:\LibreDocker\requirements.txt