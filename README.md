# StoryVerse AI Hub: A Website for Fun Language Learning with AI-Generated Picture Books

**`June 5, 2024 / by Yu-Shin, Hu and collaborators (see report.pdf in document folder)`**


[**Click here to see the demo!**](https://www.youtube.com/watch?v=iFsHQ6Nd-lY)

<img src="https://github.com/yshyshyshyshysh/AI_PictureBooks_Web/assets/92580226/dd89184a-a209-4a3d-a3ad-90a3740d76bc" alt="preview" width="700">

## How to run

-   Go to website folder: `cd /home/webapp/AI_PictureBooks_Web/website`
-   Install the requirements: `pip install -r model/requirements.txt`
-   Update TTS: `pip install -U TTS`
-   Enter your firebase project's information in firebaseconfig.json
-   Run the website: `python3 app.py` 

## Frontend

-   [Savory – Free Multi Page HTML5 Portfolio Template](https://themewagon.com/themes/free-multi-page-html5-portfolio-template-free-download/)
-   Explore page: / (index.html)
-   Personal page: /profile (profile.html)
-   Registration page: /signup (signup.html)
-   Login page: /contact (contact.html)
-   Create page: /creator (creator.html)
-   Story page: /project (project.html)

## Backend
-   [Python Flask](https://flask.palletsprojects.com/en/3.0.x/)
-   [Firebase Javascript SDK](https://github.com/firebase/firebase-js-sdk)

## Database and API

-   See the attached file in document folder and [API functions](https://github.com/AdventrousAstronaut/web-app.git)
-   [Firebase](https://firebase.google.com/?gad_source=1&gclid=Cj0KCQjwsPCyBhD4ARIsAPaaRf04BXRmDV-fFAGqVLLoO-Uzz7vbM-pmjPZWeXg5kn3zOe8lNq30t28aAs--EALw_wcB&gclsrc=aw.ds)

## AI models

-   Text-Generation: [Llama-2-7b](https://huggingface.co/meta-llama/Llama-2-7b)
-   Text-to-Image: [stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
-   Text-to-Speech: [XTTS-v2](https://huggingface.co/coqui/XTTS-v2)


