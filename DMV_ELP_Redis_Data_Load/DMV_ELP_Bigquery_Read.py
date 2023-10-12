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
import os

vAR_client = bigquery.Client()

def profanity():
    vAR_direct_profanity_sql = "SELECT upper(BADWORD_DESC) as BADWORD_DESC FROM `"+os.environ["GCP_PROJECT_ID"]+"."+os.environ["GCP_BQ_SCHEMA_NAME"]+".DMV_ELP_BADWORDS`"
    vAR_query_job = vAR_client.query(vAR_direct_profanity_sql)
    vAR_results = vAR_query_job.result()
    profanity_list = []
    for row in vAR_results:
        profanity_list.append(row.get('BADWORD_DESC'))
    return profanity_list

def fword_guideline():
    vAR_fword_guideline_sql = "SELECT upper(CONFIGURATION) as CONFIGURATION FROM `"+os.environ["GCP_PROJECT_ID"]+"."+os.environ["GCP_BQ_SCHEMA_NAME"]+".DMV_ELP_CONFIGURATION_GUIDELINES` Where upper(APPROVED_OR_DENIED)='DENIED'"
    vAR_query_job = vAR_client.query(vAR_fword_guideline_sql)
    vAR_results = vAR_query_job.result()
    fword_guideline_list = []
    for row in vAR_results:
        fword_guideline_list.append(row.get('CONFIGURATION'))
    return fword_guideline_list

def previously_denied():
    vAR_pd_sql = "SELECT RTRIM(upper(PREVIOUSLY_DENIED_CONFIG)) as PREVIOUSLY_DENIED_CONFIG FROM `"+os.environ["GCP_PROJECT_ID"]+"."+os.environ["GCP_BQ_SCHEMA_NAME"]+".DMV_ELP_PREVIOUSLY_DENIED_CONFIGURATION` "
    vAR_query_job = vAR_client.query(vAR_pd_sql)
    vAR_results = vAR_query_job.result()
    pd_list = []
    for row in vAR_results:
        pd_list.append(row.get('PREVIOUSLY_DENIED_CONFIG'))
    return pd_list


def denied_pattern():
    vAR_pattern_sql = "SELECT REGEX_CONFIGURATION FROM `"+os.environ["GCP_PROJECT_ID"]+"."+os.environ["GCP_BQ_SCHEMA_NAME"]+"..DMV_ELP_DENIED_PATTERN`"
    vAR_query_job = vAR_client.query(vAR_pattern_sql)
    vAR_results = vAR_query_job.result()
    pattern_list = []
    for row in vAR_results:
        pattern_list.append(row.get('REGEX_CONFIGURATION'))
    return pattern_list