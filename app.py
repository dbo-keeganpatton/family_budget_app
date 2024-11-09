
# Login Imports
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os


st.set_page_config(
    page_title="Patton Family Budget",
    page_icon='💸',
    layout='wide',
    menu_items=None
)


# Explicitly invoke config toml for deployement
os.environ["STREAMLIT_CONFIG_DIR"] = "./.streamlit"


##################################
#           Login Prompt        #
##################################

# DEV Auth
#with open('./auth.yaml') as file:
#    config = yaml.load(file, Loader=SafeLoader)

# PROD Auth
log_cred = os.environ.get("LOGIN_CREDENTIALS")
config = yaml.load(log_cred, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
) 
 
name, authentication_status, username = authenticator.login()
    
if authentication_status:
    authenticator.login('unrendered')
    st.success(f"Welcome {name}")
    st.switch_page("pages/dashboard.py")

elif authentication_status is False:
    st.error('Username/password is incorrect')
elif authentication_status is None:
    st.warning('Please enter your username and password') 



