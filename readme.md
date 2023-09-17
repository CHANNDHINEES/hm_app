Description:

Front end code for health monitoring app

Steps to set up:

1) Create virtual environment and activate. Install packages from requirements.txt
```
pip install -r requirements.txt
```
2) Set up .env file with the below for register_patients_callbacks.py
```commandline
AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY='AWS_SECRET_ACCESS_KEY'
```
3) Start app

```commandline
python index.py
```
4) Current Implemented functionalities

- AWS Cognito based login - based on the user type attribute we will decide patient or staff

- Front end and back end of Adding users is done - Staff users can add users. Add user functionality will add users to the cognito user group

- Front end for adding patient vitals is done
- All users passwords are set "Aa@123456"

