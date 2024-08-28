# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:57:19 2023

@author: PAVITHRA
"""

import streamlit as st
import os
import cv2
import time
import numpy as np
from keras.models import load_model,Model
from streamlit_option_menu import option_menu
from tensorflow.keras.applications.vgg19 import VGG19, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
BASEC_DIR = 'D:/research/dataset'
with open(os.path.join(BASEC_DIR, 'Flickr8k.lemma.token.txt'), 'r') as f:
    
    captions_doc = f.read()
from tqdm.notebook import tqdm
mapping = {}
# process lines
for line in tqdm(captions_doc.split('\n')):
    # split the line by comma(,)
    tokens = line.split(' ')
    if len(line) < 2:
        continue
    image_id, caption = tokens[0], tokens[1:]
    # remove extension from image ID
    image_id = image_id.split('.')[0]
    # convert caption list to string
    caption = " ".join(caption)
    # create list if needed
    if image_id not in mapping:
        mapping[image_id] = []
    # store the caption
    mapping[image_id].append(caption)
def clean(mapping):
    for key, captions in mapping.items():
        for i in range(len(captions)):
        # take one caption at a time
            caption = captions[i]
            # preprocessing steps
            # convert to lowercase
            caption = caption.lower()
            # delete digits, special chars, etc., 
            caption = caption.replace('[^A-Za-z]', '')
            # delete additional spaces
            caption = caption.replace('\s+', ' ')
            # add start and end tags to the caption
            caption = 'startseq ' + " ".join([word for word in caption.split() if len(word)>1]) + ' endseq'
            captions[i] = caption
clean(mapping)

FE_model = VGG19()
FE_model = Model(inputs=FE_model.inputs, outputs=FE_model.layers[-2].output)

def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None
all_captions = []
for key in mapping:
    for caption in mapping[key]:
        all_captions.append(caption)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_captions)
vocab_size = len(tokenizer.word_index) + 1

def predict_caption(model, image, tokenizer, max_length):
    # add start tag for generation process
    in_text = 'startseq'
    # iterate over the max length of sequence
    for i in range(max_length):
        # encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad the sequence
        sequence = pad_sequences([sequence], max_length)
        # predict next word
        yhat = model.predict([image, sequence], verbose=0)
        # get index with high probability
        yhat = np.argmax(yhat)
        # convert index to word
        word = idx_to_word(yhat, tokenizer)
        # stop if word not found
        if word is None:
            break
        # append word as input for generating next word
        in_text += " " + word
        # stop if we reach end tag
        if word == 'endseq':
            break
    return in_text

#%%
left,mid = st.columns([1,3])
max_length=33
model = load_model('D:/research/vgg19model.h5')
with mid:
    st.title("CAPTION GENERATION AND INTERPRETATION SYSTEM")
    image=st.file_uploader(' ')
    image1 = image
    but=st.button('generate')
style={
    "title": {"color":"orange"},
    "file_Uploader" : {"padding":"1px"}
    }
if but:
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    image = cv2.resize(image,(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    print(image.shape)
    image = preprocess_input(image)
    feature_image = FE_model.predict(image, verbose=0)
    caption=predict_caption(model, feature_image, tokenizer, max_length)
    cap=caption.strip("startseqendseq")
    print(caption)
    with mid:
        st.image(image1,channels='RGB')
        st.write(cap)