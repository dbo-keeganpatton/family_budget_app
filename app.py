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




##################################
#           Login Prompt        #
##################################

# with open('./auth.yaml') as file:
#    config = yaml.load(file, Loader=SafeLoader)

login_credentials = os.getenv('LOGIN_CREDENTIALS')

config = yaml.safe_load(login_credentials.strip())


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



