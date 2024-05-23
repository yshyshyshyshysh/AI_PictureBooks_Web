from flask import Flask, request, jsonify, render_template
import getpass
import base64
from model.model import generate_story, text_translations, text_to_images, text_to_speeches
# import firebase_admin
# from firebase_admin import credentials, storage
app = Flask(__name__)

#  firebase
#  需要權限
# cred = credentials.Certificate("/home/webapp/AI_PictureBooks_Web/website/templates/firebaseconfig.json")  # replace with your service account key path
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'project-20240429.appspot.com'
# })
# bucket = storage.bucket()

"""Define Flask routes"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/creator')
def creator():
    return render_template('about.html')

@app.route('/components')
def components():
    return render_template('components.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/test_input')
def test():
    return render_template('test_input.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    title = data.get('title')
    language = data.get('language')
    token = data.get('token')
    
    # story_info = generate_story(title)
    # translation = text_translations(story_info, language)
    story_info = {'paragraph 1': "I was an ordinary boy, but one day I found a strange object in the forest. It was a toad's leg bone and it glowed with magic!", 'illustration 1': "A young boy holding a glowing toad's leg bone, standing in front of a giant tree. The background is filled with colorful leaves and flowers.", 'paragraph 2': 'When I touched the bone, I felt strange powers coursing through my body. Suddenly, I grew scales, wings, and a fiery breath!', 'illustration 2': 'A boy transformed into a dragon, standing on his hind legs with wings spread wide. He is surrounded by flames and smoke.', 'paragraph 3': 'Now I can breathe fire and fly through the skies! People call me the Spit Dragon because of my fiery breath. But sometimes I miss being a human boy.', 'illustration 3': 'A dragon flying over a village, with people looking up in amazement. The dragon has a sad expression on his face, longing for his former life as a human.', 'paragraph 4': "One day, I will find a way to turn back into a boy. Until then, I'll soar the skies and protect my forest home with my fiery breath!", 'illustration 4': 'A dragon perched on a branch of a tree, looking out over the landscape with a determined expression. The sun is setting in the background, casting warm colors across the scene.', 'title': 'I became a spit dragon'}
    image = text_to_images(story_info, token)
    # speak = text_to_speeches(translation, language)
    
    # with open(speak, 'rb') as audio_file:
    #     encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
    
    # return jsonify({
    #     'story': story_info,  # prefix-match hit
    #     'translation': translation,
    #     'image': image,
    #     'audio': encoded_audio
    # })
    image_url = []  # URL expiration time in seconds
    for i, img_data in enumerate(image):
        blob = bucket.blob(f"image_{i}.png")
        blob.upload_from_string(img_data, content_type='image/png')
        image_url.append.blob.generate_signed_url(expiration=3600)
    return jsonify({'story_download_url': image_url})

if __name__ == "__main__":
    app.run(debug=True, port=5001)