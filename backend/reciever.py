import pika, sys, os
import numpy as np
from PIL import Image
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
from predict1 import *

MAX_SEQ_LEN = 17

def main():
    model = tf.keras.models.load_model('my_model')

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    
    def prepare_image(img):
        img = Image.open(img)
        img = img.resize((224, 224))
        img = np.array(img)
        img = np.expand_dims(img, 0)
        return img
    
    def getNextWords(image,in_text,word_to_ind,ind_to_word,n=1):
        sequence =  [word_to_ind[w] for w in in_text.split()]
        sequence = pad_sequences([sequence],MAX_SEQ_LEN)
        print(model.predict([image,sequence],verbose=0))
        yhat = model.predict([image,sequence],verbose=0)
        topn = yhat.argsort()[0][-1*n:][::-1]
        probs = yhat[0][topn]
        return [ (ind_to_word[i],p) for i,p in zip(topn,probs) ]

    def predict_caption(image_path):
        image = np.expand_dims(getImageFeature(image_path),axis=0)
        word_to_ind = getWordToInd()
        ind_to_word = getIndToWord()
        in_text = '<S>'
        i = 0
        while i in range(17):
            nw = getNextWords(image,in_text,word_to_ind,ind_to_word,n=1)[0][0]
            in_text += ' '+nw
            if nw == "</S>":
                break
        return in_text


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print(image_caption(body))


    channel.basic_consume(queue='test', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)