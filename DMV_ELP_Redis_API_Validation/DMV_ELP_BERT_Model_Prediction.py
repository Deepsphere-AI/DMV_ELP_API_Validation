"""
-----------------------------------------------------------------------------------------------------------------------------------------------------

© Copyright 2022, California, Department of Motor Vehicle, all rights reserved.
The source code and all its associated artifacts belong to the California Department of Motor Vehicle (CA, DMV), and no one has any ownership
and control over this source code and its belongings. Any attempt to copy the source code or repurpose the source code and lead to criminal
prosecution. Don't hesitate to contact DMV for further information on this copyright statement.

Release Notes and Development Platform:
The source code was developed on the Google Cloud platform using Google Cloud Functions serverless computing architecture. The Cloud
Functions gen 2 version automatically deploys the cloud function on Google Cloud Run as a service under the same name as the Cloud
Functions. The initial version of this code was created to quickly demonstrate the role of MLOps in the ELP process and to create an MVP. Later,
this code will be optimized, and Python OOP concepts will be introduced to increase the code reusability and efficiency.
____________________________________________________________________________________________________________
Development Platform                | Developer       | Reviewer   | Release  | Version  | Date
____________________________________|_________________|____________|__________|__________|__________________
Google Cloud Serverless Computing   | DMV Consultant  | Ajay Gupta | Initial  | 1.0      | 09/18/2022

-----------------------------------------------------------------------------------------------------------------------------------------------------

"""

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras

import requests

from transformers import TFBertModel,  BertConfig, BertTokenizerFast, TFAutoModel
import time
import json
import traceback
import os





# Name of the BERT model to use
model_name = 'bert-base-uncased'

# Max length of tokens
max_length = 128


# Load transformers config and set output_hidden_states to False
config = BertConfig.from_pretrained(model_name)

# Load BERT tokenizer
tokenizer = BertTokenizerFast.from_pretrained(pretrained_model_name_or_path = model_name, config = config)


def BERT_Model_Result(vAR_input_text):
    
    
    
    vAR_input_text = vAR_input_text.replace('/','')
    vAR_input_text = vAR_input_text.replace('*','')
    vAR_target_columns = ["TOXIC","SEVERE_TOXIC","OBSCENE","THREAT","INSULT","IDENTITY_HATE"]
    
    

    tokenizer_start_time = time.time()

    
    
    vAR_test_x = tokenizer(
    text=vAR_input_text,
    add_special_tokens=True,
    max_length=max_length,
    truncation=True,
    padding='max_length', 
    return_tensors='tf',
    return_token_type_ids = False,
    return_attention_mask = True,
    verbose = True)

    print("---Bert Model tokenizer loading time %s seconds ---" % (time.time() - tokenizer_start_time)) 

    start_time = time.time()


    # Method for h5 format
     
    # MODEL_PATH = "gs://"+os.environ["GCS_BUCKET_NAME"]+"/"+os.environ["BERT_MODEL_LOAD_PATH"]
    # FS = gcsfs.GCSFileSystem()
    # with FS.open(MODEL_PATH, 'rb') as model_file:
    #      model_gcs = h5py.File(model_file, 'r')
    #      vAR_load_model = tf.keras.models.load_model(model_gcs,compile=False)

    # Method for pb format

    # vAR_load_model = keras.models.load_model("gs://"+os.environ["GCS_BUCKET_NAME"]+"/"+os.environ["BERT_MODEL_LOAD_PATH"])

    # Method for json format
    
    # load json and create model
    # json_file = open("gs://"+os.environ["GCS_BUCKET_NAME"]+"/"+os.environ["BERT_MODEL_LOAD_PATH"]+'/model.json', 'r')
    # loaded_model_json = json_file.read()
    # json_file.close()
    # vAR_load_model = model_from_json(loaded_model_json)
    # # load weights into new model
    # vAR_load_model.load_weights("gs://"+os.environ["GCS_BUCKET_NAME"]+"/"+os.environ["BERT_MODEL_LOAD_PATH"]+'/model.h5')
    # print("Loaded model from disk")

    # evaluate loaded model on test data
    # optimizer = Adam(lr=1e-5, decay=1e-6)
    # vAR_load_model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    
    
    

    # vAR_model_result = vAR_load_model.predict(x={'input_ids': vAR_test_x['input_ids'], 'attention_mask': vAR_test_x['attention_mask']},batch_size=32)
    

    vAR_url = os.environ["TF_SERVING_URL"]
    vAR_attention_mask_list = vAR_test_x['attention_mask'].numpy().flatten().tolist()
    vAR_input_ids_list = vAR_test_x['input_ids'].numpy().flatten().tolist()
    vAR_request = {'instances': [{'attention_mask':vAR_attention_mask_list,'input_ids':vAR_input_ids_list}]}

    vAR_model_result = requests.post(vAR_url, json = vAR_request)

    print('vAR_model_result - ',vAR_model_result.text)
    print('vAR_model_result type- ',type(vAR_model_result.text))


    print('vAR_model_result type- ',type(vAR_model_result))
    print('vAR_model_result - ',vAR_model_result)

    vAR_model_result = vAR_model_result.json()["predictions"]

    print("---Bert Model loading time %s seconds ---" % (time.time() - start_time))

    
    vAR_result_data = pd.DataFrame(vAR_model_result,columns=vAR_target_columns)
    vAR_target_sum = (np.sum(vAR_model_result)).round(2)
    vAR_result_data.index = pd.Index(['Percentage'],name='category')
    vAR_result_data = vAR_result_data.astype(float).round(2)
    
    # If Highest probability more than 50%, then configuration is denied

    vAR_max_prob = np.array(vAR_model_result).max()
    print('arg max val - ',vAR_max_prob)

    if (vAR_max_prob)>=0.5:
        return False,vAR_result_data,vAR_target_sum
    else:
        return True,vAR_result_data,vAR_target_sum
