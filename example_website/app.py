from flask import Flask, request, jsonify, render_template
import getpass
import base64
from static.model.model import generate_story, text_translations, text_to_images, text_to_speeches
app = Flask(__name__)

"""Define Flask routes"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def page1():
    return render_template('page1.html')

# @app.route('/get_results', methods=['POST'])
# def get_results():
#     # Get input data from frontend
#     data = request.json
#     input1 = data.get('input1')
#     input2 = data.get('input2')
#     # AI function here?
#     image_url = f"https://example.com/image?input1={input1}&input2={input2}"
#     return jsonify({'image_url': image_url})

@app.route('/generate_story', methods=['POST'])
def generate_story_route():
    data = request.json
    title = data.get('title')
    story = generate_story(title)
    return jsonify({'story': story})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
    