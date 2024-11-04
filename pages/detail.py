import os
import yaml
import streamlit as st
from yaml.loader import SafeLoader
from data.source import all_data
import streamlit_authenticator as stauth



st.set_page_config(
    page_title="Detail",
    page_icon='🔎',
    layout='wide',
    menu_items=None
)



##################################
#         Login Check            #
##################################

if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.info('Please Login from the Home page and try again.')
    st.switch_page("./app.py")

# Use this for DEV auth
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





df, curr_df, bills_paid_chart_data, savings_chart_data, viz_data = all_data()


with st.sidebar:
    with st.container(border=True):
        st.page_link(
            "./pages/dashboard.py", 
            label="Return to Dashboard", 
            icon="📈", 
            use_container_width=True
        )
        

    st.write("________________")

    # Logout button
    authenticator.logout()


curr_df['paid'] = ["Yes" if i == True else "" for i in curr_df["paid"]]
curr_df['priority'] = ["Yes" if i == True else "" for i in curr_df["priority"]]
curr_df['value'] = ["" if i == None or i == 0 else i for i in curr_df["value"]]


# There is some reaaally not great stuff here for formatting...
# Since basic orientation options just don't exist in ST...
# I am forced to implement columns abusively to enforce order.
col1, col2 = st.columns(2)

with col1:

    # Hacky Header for center-content
    c1, c2, c3 = st.columns([2,1,2])
    with c1:
        st.write("")
    with c2:
        st.subheader("This Month")
    with c3:
        st.write("")

    st.data_editor(
        curr_df,
        height=800,
        disabled=True,
        hide_index=True,
        use_container_width=True
    )

with col2:

    # Hacky Header for center-content
    c4, c5, c6 = st.columns([2,1,2])
    with c4:
        st.write("")
    with c5:
        st.subheader("All Months")
    with c6:
        st.write("")

    st.data_editor(
        df,
        height=800,
        disabled=True,
        hide_index=True,
        use_container_width=True
    )
