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

from google.cloud import bigquery
import pandas as pd
import datetime
import os

def GetConfigDetails(vAR_config):
    vAR_client = bigquery.Client()
    vAR_response_table_name = "DMV_ELP_MLOPS_RESPONSE"
    vAR_sql =(
        "select * from `"+ os.environ["GCP_PROJECT_ID"]+"."+os.environ["GCP_BQ_SCHEMA_NAME"]+"."+vAR_response_table_name+"`"+" where LICENSE_PLATE_CONFIG='"+vAR_config+"' and MODEL='GPT'"
    )

    vAR_df = vAR_client.query(vAR_sql).to_dataframe()

    

    if len(vAR_df)==0:
      vAR_data_dict={"errorCode":104,"errorDescription":"No record found for given ELP Configuration.Try with different one."}
      return vAR_data_dict
    else:

      vAR_data_dict = vAR_df.to_dict(orient='records')[0]

      if vAR_data_dict["RECOMMENDATION"].lower()=='denied':
        vAR_data_dict["Denial_Reason"] = vAR_data_dict["REASON"]
      elif vAR_data_dict["RECOMMENDATION"].lower()=='accepted':
        vAR_data_dict["Denial_Reason"] = None


      print('vAR_data_dict - ',vAR_data_dict)
      print('type vAR_data_dict - ',type(vAR_data_dict))

      vAR_data_dict.pop('CREATED_DT', None)
      vAR_data_dict.pop('CREATED_USER', None)
      vAR_data_dict.pop('UPDATED_DT', None)
      vAR_data_dict.pop('UPDATED_USER', None)

      vAR_data_dict["approved_Or_Denied"] = vAR_data_dict.pop('RECOMMENDATION', None)
      vAR_data_dict["recommended_Configuration_Reason"] = vAR_data_dict.pop('RECOMMENDATION_REASON', None)

      vAR_data_dict.pop('REQUEST_ID', None)
      vAR_data_dict.pop('REASON', None)
      vAR_data_dict.pop('REQUEST_DATE', None)
      vAR_data_dict.pop('SG_ID', None)
      vAR_data_dict.pop('LICENSE_PLATE_DESC', None)
      vAR_data_dict.pop('DOUBLE_OR_SINGLE', None)
      vAR_data_dict.pop('LICENSE_PLATE', None)
      vAR_data_dict.pop('TYPE', None)
      vAR_data_dict.pop('ORDER_PAYMENT_DATE', None)
      vAR_data_dict.pop('ORDER_PLACED_OFFICE_ID', None)
      vAR_data_dict.pop('VIN', None)
      vAR_data_dict.pop('ORDER_NUMBER_CODE', None)
      vAR_data_dict.pop('ORDER_DEST_OFFICE_ID', None)
      vAR_data_dict.pop('ORDER_GROUP_ID', None)
      vAR_data_dict.pop('REGISTERED_OWNER_NAME', None)
      vAR_data_dict.pop('REGISTERED_OWNER_ADDRESS', None)
      vAR_data_dict.pop('REGISTERED_OWNER_CITY', None)
      vAR_data_dict.pop('REGISTERED_OWNER_ZIP', None)
      vAR_data_dict.pop('TECH_ID', None)
      vAR_data_dict.pop('PLATE_CODE', None)
      vAR_data_dict.pop('BADWORDS_CLASSIFICATION', None)
      vAR_data_dict.pop('GUIDELINE_FWORD_CLASSIFICATION', None)
      vAR_data_dict.pop('PREVIOUSLY_DENIED_CLASSIFICATION', None)
      vAR_data_dict.pop('RULE_BASED_CLASSIFICATION', None)
      vAR_data_dict.pop('OVERALL_SCORE', None)
      vAR_data_dict.pop('ERROR_MESSAGE', None)
      vAR_data_dict.pop('PLATE_TYPE_COUNT', None)
      vAR_data_dict.pop('PLATE_TYPE_MAX_COUNT_FLG', None)
      vAR_data_dict.pop('RUN_ID', None)
      vAR_data_dict.pop('REQUEST_FILE_NAME', None)

      

      

      # Convert keys to camel case
      vAR_final_dict = {to_camel_case(k): v for k, v in vAR_data_dict.items()}

      return vAR_final_dict






def to_camel_case(dict_key_str):
    vAR_components = dict_key_str.lower().split('_')
    # combine first word with capitalized version of the rest
    return vAR_components[0] + ''.join(x.title() for x in vAR_components[1:])



