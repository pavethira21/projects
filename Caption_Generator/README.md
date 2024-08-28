The project aims at building a Image Captioning system that will
automatically generate the caption for the given input image. It
involves challenging task of generating a human readable textual description of an image. 
It involves natural language processing and
computer vision. These caption helps the user to know the essential
information of the image.
The system is built using Deep Neural network models. The
model is divided into two parts the encoder and the decoder. The
encoder extracts the features from the image , the last layer of the
encoder is connected to the decoder which generate a caption for the
image. Pretrained CNN and RNN models are used to build the model. From the feature
vectors obtained from models such as VGG19 and inception-V3 the
LSTM model generate sequence of words.
The dataset used to train the model is flickr8k dataset. This
dataset consists of 8091 images from flickr and each image has 5
captions that describe the actions in the image .

DATASET
The dataset used for this study is flickr8k dataset which consists
about 8091 images with each image having 5 captions that provide
clear descriptions of the salient entities and events. The Data set
was complied by P.Young, M.Hodosh and J.Hockenmaier. This
dataset is preprocessed and then applied in the model.
 *Pre-processing
1. Image Dataset
The images are loaded by using load img method after loading all
the image the image pixels are then converted into array as the
model can only process an array value and not a pixel value, then the
images are reshaped into 4d image.The images are further processed
by using a predefined function preprocess input .
2. Caption Data
The caption are loaded and then each caption is separated from its
index value and stored in a dictionary with its index as key. All
the words in the captions are separated and stored. The words are
written in lower case using the function .lower() for better quality
All the special character and numbers that are present in the captions are removed along with extra spacing.
Then finally the words are bounded by a start and end tag to indicate the starting and
ending of the caption.