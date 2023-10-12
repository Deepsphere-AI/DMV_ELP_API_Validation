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

import redis
from DMV_ELP_Bigquery_Read import profanity,fword_guideline,previously_denied,denied_pattern
import os
from DMV_ELP_Read_TLS_Certificate import get_ca_cert


def redis_load(request):
    try:

        vAR_ca_cert_path = get_ca_cert(os.environ["GCS_BUCKET_NAME"], os.environ["TLS_CERTIFICATE_PATH"])
        redis_client = redis.Redis(host=os.environ["REDIS_IP"], port=int(os.environ["REDIS_PORT"]), decode_responses=True,password=os.environ["REDIS_AUTH"],ssl=True,ssl_ca_certs=vAR_ca_cert_path)
        # a = ['b1','b2']
        # r.sadd('fooset', *a)

        # print(r.scard('fooset'))
        # print(redis_client.smembers('ELP_DENIED_PATTERN'))
        # print(type(redis_client.smembers('ELP_DENIED_PATTERN')))
        # conf = '111111'
        # for res in redis_client.smembers('ELP_DENIED_PATTERN'):
        #     print(res)
        # print(r.sismember('fooset','b3'))

        profanity_list = profanity()
        redis_client.sadd('ELP_BADWORDS',*profanity_list)

        print('ELP_BADWORDS LOADED SUCCESSFULLY')

        fword_guideline_list = fword_guideline()
        redis_client.sadd('ELP_FWORD_GUIDELINES',*fword_guideline_list)

        print('ELP_FWORD_GUIDELINES LOADED SUCCESSFULLY')

        previously_denied_list = previously_denied()
        redis_client.sadd('ELP_PREVIOUSLY_DENIED',*previously_denied_list)

        print('ELP_PREVIOUSLY_DENIED LOADED SUCCESSFULLY')

        denied_pattern_list = denied_pattern()
        redis_client.sadd('ELP_DENIED_PATTERN',*denied_pattern_list)

        print('ELP_DENIED_PATTERN LOADED SUCCESSFULLY')

        return {"Message":"Redis Data Loaded Successfully..!"}

    except BaseException as e:
        print("Error on loading redis data - ",str(e))
        return {"Error Message": str(e)}