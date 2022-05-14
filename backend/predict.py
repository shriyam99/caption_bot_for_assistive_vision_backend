import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from collections import defaultdict
import gc
import string
import nltk

from keras.preprocessing.image import img_to_array, array_to_img, load_img
from keras.applications.vgg19 import preprocess_input
from keras.applications.vgg19 import VGG19
from keras.models import Model

IMG_DIM = (224,224,3)
vgg19 = VGG19(weights='imagenet',include_top=True, input_shape=IMG_DIM)
vgg19.layers.pop()
vggModel = Model( vgg19.input,vgg19.layers[-1].output)
imagemap = {}
1

def getImageFeature(path):
    temp = preprocess_input( img_to_array( load_img( os.path.join(path), target_size=IMG_DIM[:2] )) )
    return vggModel.predict(np.expand_dims(temp,axis=0))[0]

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
word_counter = defaultdict(int)

table = str.maketrans('', '', string.punctuation,)

def getData():
    allimage = os.listdir('/Users/magicpin/Downloads/Images')
    data = pd.read_csv('/Users/magicpin/Downloads/captions.txt', sep='\t',header=None, names= ['image','caption'])
    data.caption = data.image.apply(lambda x: x.split(',')[1])
    data.image = data.image.apply( lambda x: x.split('jpg')[0]+'jpg' )
    data['avail'] = data.image.apply( lambda x: x in allimage )
    data = data[ data.avail==True ]
    data = data.dropna()
    return data

def preprocesCaption( caption):
    caption = caption.lower() #to lower case
    caption = caption.translate(table) #remove punctuations
    caption = caption.split() # convert to words
    caption = [ w for w in caption if len(w) > 1 ] #remove dangling 'a' and 's'
    caption = [ w for w in caption if w.isalpha()  ] #keep only words with alphabets
    caption = [ lemmatizer.lemmatize(w) for w in caption ]
    for w in caption: word_counter[w]+=1
    return ' '.join(caption)

def getWords():
    data = getData()
    words = set()
    words.update( ('<S>','</S>') )
    mx = []
    images = defaultdict(list)
    for img in tqdm(data.image.unique()):
        for comment in data[data.image == img ].caption.values:
            caption = preprocesCaption(comment)
            caption = [ w for w in caption.split() if word_counter[w]>=10 ]  #taking words whose count atleast 10
            words.update( caption )
            mx.append( len(caption)+2 )
            images[img].append( '<S> '+" ".join(caption)+' </S>' )
    
    return words

def getWordToInd():
    word_to_ind = {}
    words = getWords()
    for i,w in enumerate(words):
        word_to_ind[w] = i+1
    return word_to_ind
    


def getIndToWord():
    ind_to_word = {}
    words = getWords()
    for i,w in enumerate(words):
        ind_to_word[w] = i+1
    return ind_to_word
    