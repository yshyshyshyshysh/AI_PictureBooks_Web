from flask import Flask, request, jsonify, render_template
import getpass
import base64
from model.model import generate_story, text_translations, text_to_images, text_to_speeches, translate_to_eng
import firebase_admin
# import google-cloud-firestore
from firebase_admin import credentials, storage, firestore
from io import BytesIO
from PIL import Image
import random
import string
import os
import json
from datetime import timedelta
import shutil


app = Flask(__name__)

#  firebase
cred = credentials.Certificate("/home/webapp/AI_PictureBooks_Web/website/templates/firebaseconfig.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mywebsite-vivian.appspot.com'
})
bucket = storage.bucket()

# db=firestore.client()
# collection_ref = db.collection('item')
# doc_ref = collection_ref.add("shi")

"""Define Flask routes"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/creator')
def test():
    return render_template('creator.html')

@app.route('/creator', methods=['POST'])
def creator():
    data = request.json
    title = data.get('title')
    language = data.get('language')  # es
    token = data.get('token')  # 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
    uid = data.get('uid')
    storyToken = data.get('storyToken')

    data = {
        "title": "小牛天上飛1",
        "From_To": "Eng:Chinese",
        "image_urls": ["https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/Rabbit%20flying%20in%20the%20sky%2Fimage_0.jpg?alt=media&token=95529af0-33be-4682-a0d6-5c5f13a2946c","https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/Rabbit%20flying%20in%20the%20sky%2Fimage_0.jpg?alt=media&token=95529af0-33be-4682-a0d6-5c5f13a2946c","https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/Rabbit%20flying%20in%20the%20sky%2Fimage_0.jpg?alt=media&token=95529af0-33be-4682-a0d6-5c5f13a2946c",
        "https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/Rabbit%20flying%20in%20the%20sky%2Fimage_0.jpg?alt=media&token=95529af0-33be-4682-a0d6-5c5f13a2946c"
        ],
        "paragraphs": [
            "一只小兔子总是夢想著飞行，所以他制作了翼膜，然後跳下地面。",
            "兔子一飛一舞，高飞到云海上，發現了天空中的其他生物。",
            "兔子感謝自己制作的翼膜，現在可以飞上天空。",
            "但是他知道，有時候也要返回地面，繼續努力成長。"
        ],
        "translations": [
            "A little rabbit always dreamed of flying, so he made a wing membrane and jumped off the ground.",
            "The rabbit fluttered and flew to the sea of ​​clouds and found other creatures in the sky.",
            "The rabbit thanks to the wing membrane he made, and now he can fly into the sky.",
            "But he knew that sometimes he had to return to the ground and continue to work hard."
        ],
        "speech_urls": [
            "https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/audio%2Fdramatic-background-music-for-short-videos-1-minute-little-alicia-155718.mp3?alt=media&token=92424fd6-1d15-4956-a21d-2e2860b38a0a",
            "https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/audio%2Fdramatic-background-music-for-short-videos-1-minute-little-alicia-155718.mp3?alt=media&token=92424fd6-1d15-4956-a21d-2e2860b38a0a",
            "https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/audio%2Fdramatic-background-music-for-short-videos-1-minute-little-alicia-155718.mp3?alt=media&token=92424fd6-1d15-4956-a21d-2e2860b38a0a",
            "https://firebasestorage.googleapis.com/v0/b/mywebsite-vivian.appspot.com/o/audio%2Fdramatic-background-music-for-short-videos-1-minute-little-alicia-155718.mp3?alt=media&token=92424fd6-1d15-4956-a21d-2e2860b38a0a"
        ],
        "uid": uid,
        "storyToken": storyToken
    }
    # return jsonify(data)

    title_eng = translate_to_eng(title)
    story_info = generate_story(title)
    print("...SUCCESSFULLY generated story")
    print(story_info)

    translation = text_translations(story_info, language)
    print("...SUCCESSFULLY generated translation")
    print(translation)

    image = text_to_images(story_info, token)
    print("...SUCCESSFULLY generated image")

    speeches = text_to_speeches(translation, language)
    print("...SUCCESSFULLY generated speeches")

    story_data = {
        'title': title,
        'story': story_info,
        'translation': translation
    }
    print("...check infomation")
    print(story_data)


    json_blob = bucket.blob(f'{title_eng}/{title_eng}.json')
    json_blob.upload_from_string(json.dumps(story_data), content_type='application/json')
    json_url = json_blob.generate_signed_url(timedelta(days=365))

    image_url = []
    for i, img in enumerate(image):
        img_bytes = BytesIO()
        try:
            img.save(img_bytes, format='PNG')
        except Exception as e:
            print(f"Error saving image {i}: {e}")
            continue
        img_bytes.seek(0)
        blob = bucket.blob(f'{title_eng}/image_{i}.jpg')
        blob.upload_from_file(img_bytes, content_type='image/jpg')
        image_url.append(blob.generate_signed_url(timedelta(days=365)))

    mp3_urls = []
    for i, speech_file in enumerate(speeches):
        blob = bucket.blob(f'{title_eng}/paragraph_{i}.mp3')
        blob.upload_from_filename(speech_file)
        mp3_token = blob.generate_signed_url(timedelta(days=365))
        mp3_urls.append(mp3_token)
    for i in range(4):
        i = i + 1
        os.remove(f'/home/webapp/AI_PictureBooks_Web/website/model/speech/paragraph {i}.mp3')

    language_info = f'中文翻譯成{language}'
    log_blob = bucket.blob('story_logs.json')
    log_data = json.loads(log_blob.download_as_text()) if log_blob.exists() else []
    log_entry = {
        'title': title,
        'From_To': language_info,
        'title_eng': title_eng,
        'story_url': json_url,
        'image_urls': image_url,
        'speech_urls': mp3_urls,
        'uid': uid,
        "storyToken": storyToken
    }

    paragraphs = [v for k, v in story_data["story"].items() if k.startswith("paragraph")]

    log_data.append(log_entry)
    log_blob.upload_from_string(json.dumps(log_data), content_type='application/json')

    print("...check infomation")
    print(log_entry)
    
    # https://firebasestorage.googleapis.com/v0/b/webapp-ecc1b.appspot.com/o/story_logs.json?alt=media&token=1560ce88-e76f-473f-a38d-d7caec27c511


    retData = {
        "title": title,
        "From_To": "Eng:Chinese",
        "paragraghs": paragraphs,
        "translations": story_data["translation"],
        "image_urls": image_url,
        "speech_urls": mp3_urls,
        "uid": uid,  # Replace with actual UID
        "storyToken": storyToken  # Replace with actual storyToken
    }

    # return jsonify({'story': json_url,'image_urls': image_url})
    # return jsonify({'speech': mp3_urls})
    return jsonify(retData)

if __name__ == "__main__":
    app.run(debug=True, port=8080)