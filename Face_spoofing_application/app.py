import base64
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save-image', methods=['POST'])
def save_image():
    data_url = request.json['dataURL']
    image_data = base64.b64decode(data_url.split(',')[1])
    with open('snapshot.png', 'wb') as f:
        f.write(image_data)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run()