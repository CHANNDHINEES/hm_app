ENV_LINK = "https://a44450945f5e04816a392a73fae9bc18-1065398358.ap-southeast-2.elb.amazonaws.com"
USER_POOL_ID = "ap-southeast-2_OUg9hqyf4"
CLIENT_ID = "3diqopiha1h5djmvii62kgti38"
REDIRECT_URI = f"{ENV_LINK}/home"
AUTH_DOMAIN = "https://rpm.auth.ap-southeast-2.amazoncognito.com"
AUTHORIZATION_URL = f"{AUTH_DOMAIN}/login?client_id={CLIENT_ID}&response_type=code&scope=email+openid+phone+profile&redirect_uri={REDIRECT_URI}"
TOKEN_URL = f"{AUTH_DOMAIN}/oauth2/token"
USER_INFO_URL = f"{AUTH_DOMAIN}/oauth2/userInfo"
REGION = "ap-southeast-2"
PATIENT_VITALS_API_URL = "https://yzbuzi7mxi.execute-api.ap-southeast-1.amazonaws.com/prod/vitals"


