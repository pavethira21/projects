import streamlit as st
import cv2
import time
import numpy as np
from keras.models import load_model
from streamlit_option_menu import option_menu

def crop_image(imag,display=False):
    mask = imag ==0
    coords = np.array(np.nonzero(~mask))
    top_left = np.min(coords,axis =1)
    bottom_right = np.max(coords,axis=1)
    croped_image = imag[top_left[1]:bottom_right[1],top_left[1]:bottom_right[1]]
    kernel = np.ones((3,3))
    crp_image = cv2.morphologyEx(croped_image,cv2.MORPH_OPEN,kernel)
    return crp_image
with st.sidebar:
            selected = option_menu(
                menu_title=None,  # required
                options=["Prediction", "About"],  # required
                icons=["clipboard-data","book-half"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation = "horizontal",
                styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "20px"},
                
                "nav-link": {
                    "font-size": "20px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "black"},
                
                
            },
            
            )
left,mid = st.columns([1,3])
if selected == "Prediction": 
    with mid:
      st.title("BRAIN TUMOR DETECTION")
    model = load_model('D:/project/Brain_tumor_detection1.h5')
    classes = ['tumor gli','tumor men','no_tumor','tumor p']

    with mid:
        image=st.file_uploader(' ')
        but=st.button('predict')
    style={
        "title": {"color":"orange"},
        "file_Uploader" : {"padding":"1px"}
        }
    if but:
        if image is not None:
            with st.spinner('processing...'):
                time.sleep(5)
                file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
                opencv_image = cv2.imdecode(file_bytes, 1)
        
        
        
                # Displaying the image
                with mid:
                   opencv_image1 = cv2.resize(opencv_image, (300,300))
                   st.image(opencv_image1, channels="BGR")
                #st.write(opencv_image.shape)
                #Resizing the image
                opencv_img = crop_image(opencv_image)
                opencv_image = cv2.resize(opencv_img, (70,70))
                
                
                opencv_image.shape = (1,70,70,3)
                #st.write(opencv_image.shape)
                #opencv_img = np.asarray(opencv_image,dtype='float32')
                #st.write(opencv_img.shape)
                
                pred = model.predict(opencv_image)
                
                result = classes[np.argmax(pred)]
                with mid:
                    if result == 'tumor gli' or result == 'tumor men' or result == 'tumor p':
                        st.success("The system has detected presence of Tumor cells ")
                    if result =='no_tumor':
                        st.write("No tumor cells present ")
          
        else:
            st.error('upload a mri scan to predict')
    
if selected == "About":
    st.title('BRAIN TUMOR DETECTION')
    with mid:
        
        st.title('About Us')
    with st.container():
        st.write('This system helps you to know the presense of tumor cells in your brain')
        st.write('The system was developed with python programming language using packages such as Keras,numpy,cv2 .CNN model was used its accuracy is 97%')
        col1,col2=st.columns(2)
        with col1:
            acc = cv2.imread(r'D:/project/accuracy of model.png')
            st.image(acc)
            st.write('Training and Validation accuracy of the model')
        with col2:
            acc = cv2.imread(r'D:/project/loss of model.png')
            st.image(acc)
            st.write('Training and Validation loss of the model')