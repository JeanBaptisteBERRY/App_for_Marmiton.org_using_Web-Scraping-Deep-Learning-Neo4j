# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
    


def image_ingredient(image_path):
    
    import numpy as np
    from googletrans import Translator
    from keras.models import load_model
    from keras.applications import imagenet_utils
    from keras.preprocessing.image import img_to_array
    from keras.preprocessing.image import load_img
    
    translator = Translator()
    
    inputShape = (224, 224)
    image = load_img(image_path, target_size=inputShape)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    preprocess = imagenet_utils.preprocess_input
    image = preprocess(image)
    
    model = load_model('model_VGG16.h5')
    
    preds = model.predict(image)
    preds_en = imagenet_utils.decode_predictions(preds)[0][0][1]
    
    preds_fr = translator.translate(preds_en, dest='fr')
    preds_fr_word = (str(preds_fr).split('text'))[1].split(',')[0][1:]
    
    return preds_fr_word