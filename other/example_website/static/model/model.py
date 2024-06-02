import os
import re
import requests
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from googletrans import Translator
import torch
from PIL import Image
import matplotlib.pyplot as plt
import io
from TTS.api import TTS

"""Text-Generation > story_info"""

# def text_generation(title):
#     split_words = ['paragraph 1:', 'illustration 1:', 'paragraph 2:', 'illustration 2:', 'paragraph 3:', 'illustration 3:', 'paragraph 4:', 'illustration 4:']
#     model_name_or_path = "TheBloke/Llama-2-13B-chat-GGML"
#     model_basename = "llama-2-13b-chat.ggmlv3.q5_1.bin"
#     model_path = hf_hub_download(repo_id=model_name_or_path, filename=model_basename)
#     lcpp_llm = Llama(
#         model_path=model_path,
#         n_threads=2,
#         n_batch=512,
#         n_gpu_layers=32
#     )
#     lcpp_llm.params.n_gpu_layers
#     prompt = f'''
#     Taking Andersen's story as an example, write a 'very short' picture book story. It should includes four paragraphs (no more than 30 words) and illustration description in each paragraph.
#     Title: {title}.
#     Format please follows:
#         Title:
#         Paragraph 1:
#         Illustration 1:
#         Paragraph 2:
#         Illustration 2:
#         Paragraph 3:
#         Illustration 3:
#         Paragraph 4:
#         Illustration 4:
#     '''
#     while True:
#         print('RUN THE MODEL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
#         response = lcpp_llm(prompt=prompt, max_tokens=1200, temperature=0.5, top_p=0.95, repeat_penalty=1.2, top_k=150, echo=True)
#         full_story = response["choices"][0]["text"]
#         if all(full_story.lower().count(word.lower()) == 2 for word in split_words):
#             print(full_story)
#             return full_story

import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    pipeline,
    logging,
)
# from peft import LoraConfig
# from trl import SFTTrainer

import torch
import gc

def clear_memory():
    torch.cuda.empty_cache()
    gc.collect()

# Model from Hugging Face hub
base_model = "NousResearch/Llama-2-7b-chat-hf"

# New instruction dataset
guanaco_dataset = "mlabonne/guanaco-llama2-1k"

# Fine-tuned model
new_model = "llama-2-7b-chat-guanaco"

compute_dtype = getattr(torch, "float16")

quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=compute_dtype,
    bnb_4bit_use_double_quant=False,
)


model = AutoModelForCausalLM.from_pretrained(
    base_model,
    quantization_config=quant_config,
    device_map={"": 0}
)
model.config.use_cache = False
model.config.pretraining_tp = 1


tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

def text_generation(title):
    split_words = ['paragraph 1:', 'illustration 1:', 'paragraph 2:', 'illustration 2:', 'paragraph 3:', 'illustration 3:', 'paragraph 4:', 'illustration 4:']
    
    prompt = f'''
        Taking Andersen's story as an example, write a 'very short' picture book story in English. 
        Title: {title}.
        It should includes four paragraphs, please follow the output format:
            Title:
            Paragraph 1:
            Illustration 1:
            Paragraph 2:
            Illustration 2:
            Paragraph 3:
            Illustration 3:
            Paragraph 4:
            Illustration 4:
        '''

    while True:
        print('RUN THE MODEL!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=700,truncation=True)
        result = pipe(prompt)
        full_story = result[0]['generated_text']
        full_story = full_story.replace(prompt,'')
        clear_memory()  # Clear memory after generation
        
        if all(full_story.lower().count(word.lower()) == 2 for word in split_words):
            print(full_story)
            return full_story

def extract_story_info(text):
    split_words = ['paragraph 1:', 'illustration 1:', 'paragraph 2:', 'illustration 2:', 'paragraph 3:', 'illustration 3:', 'paragraph 4:', 'illustration 4:']
    keys = ['paragraph 1', 'illustration 1', 'paragraph 2', 'illustration 2', 'paragraph 3', 'illustration 3', 'paragraph 4', 'illustration 4']
    pattern = '|'.join(map(re.escape, split_words))
    pattern = f'(?i)({pattern})'
    split_text = re.split(pattern, text)
    split_text = [chunk.strip() for chunk in split_text if chunk.strip()]
    story_info = {}
    for i in range(len(keys)):
        key = keys[i]
        value = split_text[i * 2 + 1]
        story_info[key] = value
    if '\n' in story_info['illustration 4']:
        split_illustration = story_info['illustration 4'].split('\n')
        story_info['illustration 4'] = '\n'.join(split_illustration[:-1])
    return story_info

def translate_to_eng(title):
    translator = Translator()
    translation = translator.translate(title, dest='en')
    return translation.text

def generate_story(title):
    full_story = text_generation(title)
    story_info = extract_story_info(full_story)
    story_info['title'] = title
    return story_info

"""Text-to-Image > story_images"""

def text_to_images(story_info, user_access_token):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {user_access_token}"}
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content
    illustration_keys = ['illustration 1', 'illustration 2', 'illustration 3', 'illustration 4']
    images = []
    for illustration_key in illustration_keys:
        content = story_info[illustration_key]
        prompt = f'''
        Style: Joan Cornellà.
        Content: {content}
        '''
        image_bytes = query({"inputs": prompt})
        image = Image.open(io.BytesIO(image_bytes))
        images.append(image)
    return images

"""Translation > story_translation"""

def text_translations(story_info, lang):
    paragraph_keys = ['paragraph 1', 'paragraph 2', 'paragraph 3', 'paragraph 4']
    translations = []
    for paragraph_key in paragraph_keys:
        text = story_info[paragraph_key]
        translator = Translator()
        translation = translator.translate(text, dest=lang)
        translations.append(translation.text)
    return translations

"""Text-to-Speech> story_speeches"""

def text_to_speeches(story_translations, lang):
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
    paragraph_keys = ['paragraph 1', 'paragraph 2', 'paragraph 3', 'paragraph 4']
    speeches = []
    for i in range(4):
        text = story_translations[i]
        speech_file_path = f"{paragraph_keys[i]}.mp3"
        tts.tts_to_file(text=text, file_path=speech_file_path, speaker_wav="speaker.mp3", language=lang)
        speeches.append(speech_file_path)
    return speeches
