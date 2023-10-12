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



def Pre_Request_Validation(request_json):
    vAR_error_message = ""

    if 'licencePlateConfig' in request_json:
        vAR_configuration = request_json['licencePlateConfig']
    else:
        vAR_error_message =vAR_error_message+ "### Mandatory Parameter licencePlateConfig is missing"
        return {"Error Message":vAR_error_message}

    vAR_strlen = len(vAR_configuration)
    for char in vAR_configuration:
        if char=='/':
            vAR_strlen = vAR_strlen-0.5
    print('CONFIGURATION - ',vAR_configuration)
    print('LENGTH - ',vAR_strlen)
    
    if vAR_strlen>8:
        vAR_error_message = vAR_error_message+"### ELP Configuration can not be more than 8 characters"

    if len(request_json['licencePlateConfig'].strip())==0:
        vAR_error_message = vAR_error_message+"### ELP Configuration can not be processed for empty string"

    
    
    return {"Error Message":vAR_error_message}
