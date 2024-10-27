import os
import gspread.auth
from gspread.utils import ValueRenderOption
import streamlit as st
import gspread
import json

# Auth and Worksheet Retrieval
#secret_path = './data/secrets/secret.json'
#with open(secret_path, 'r') as f:
#    secret = f.read()
#    gcp_credentials_dict = json.loads(secret)
#
# Use this for PROD auth
secret = os.getenv('GCP_SERVICE_ACCOUNT')
gcp_credentials_dict = json.loads(secret)
    





gc = gspread.auth.service_account_from_dict(gcp_credentials_dict)
sh = gc.open('Budget')
curr_month_data = sh.worksheets()
curr_mnt = curr_month_data[-2]

# Session Variables
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False
if 'confirmation' not in st.session_state:
    st.session_state['confirmation'] = False
if 'flex_spend_formula' not in st.session_state:
    st.session_state['flex_spend_formula'] = None

# Input Form
def input_form():
    with st.form("Add Payment or Charge", clear_on_submit=True):
        st.subheader("Add Flex Charge")
        
        with st.expander("expand to view", expanded=False):
            if 'Flexible Spending' in curr_mnt.row_values(39):

                # Retrieve the formula if it hasn't been loaded already
                if st.session_state['flex_spend_formula'] is None:
                    st.session_state['flex_spend_formula'] = curr_mnt.row_values(
                        39, value_render_option=ValueRenderOption.formula
                    )[2]

                flex_charge = st.number_input(label="Amount")

                # Submit button for initial form submission
                submitted = st.form_submit_button("Add Charge")

                if submitted and flex_charge:
                    adjusted_formula = f"{st.session_state['flex_spend_formula']}+{flex_charge}".replace("++", "+")
                    st.session_state['submitted'] = True
                    st.session_state['adjusted_formula'] = adjusted_formula
                    st.session_state['flex_charge'] = flex_charge

                if st.session_state['submitted']:
                    st.warning("You are adding a flex charge, are you sure?")
                    st.session_state['confirmation'] = st.form_submit_button("Confirm Charge")
                    
                    if st.session_state['confirmation']:
                        # Update Google Sheets only on confirmation
                        curr_mnt.update_cell(39, 3, st.session_state['adjusted_formula'])
                        st.success("Charge added successfully!")
                        
                        # Reset the session state for the form
                        st.session_state['submitted'] = False
                        st.session_state['confirmation'] = False
                        st.session_state['flex_spend_formula'] = None
                        st.session_state['flex_charge'] = ""
                        st.rerun()
            else:
                st.error("Wrong Row Selected in Update.py for Flex Spend")


if __name__ == "__main__":
    input_form()
