import gspread.auth
from gspread.utils import ValueRenderOption
import streamlit as st
import gspread
import json



#########################################
#       Auth and Worksheet Gettin       #
#########################################
secret_path = './data/secrets/secret.json'
with open(secret_path, 'r') as f:
    secret = f.read()
    gcp_credentials_dict = json.loads(secret)


gc = gspread.auth.service_account_from_dict(gcp_credentials_dict)
sh = gc.open('Budget')
curr_month_data = sh.worksheets()
curr_mnt = curr_month_data[-2]



#########################################
#            Session Vars               #
#########################################
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

if 'confirmation' not in st.session_state:
    st.session_state['confirmation'] = False


#########################################
#              Input Form               #
#########################################
def input_form():

    with st.form("Add Payment or Charge"):
        st.subheader("Add Flex Charge")
        
        with st.expander("expand to view"):
             

            if 'Flexible Spending' in curr_mnt.row_values(39):
                
                
                flex_spend_formula = curr_mnt.row_values(39, value_render_option=ValueRenderOption.formula)[2]

                if st.form_submit_button:
                    flex_charge = st.text_input(label="Amount").strip()

                    
                    # For some reason this f-string adds a double '++' to each new charge...
                    # I cannot figure out why this is happening so I am just going to replace instances..
                    # of double '++' to single '+', hacky and lame.
                    adjusted_formula = f"{flex_spend_formula}+{flex_charge}".replace("++", "+")
                    
                    update_action = curr_mnt.update_cell(39, 3, adjusted_formula)
                    


                else:
                    pass
            
                # Here we set the submission value in the session state..
                # This is to track if there has been an action taken for response from the app.
                submitted = st.form_submit_button()

                # Check if the session has captured our submission.
                if submitted:
                    st.session_state['submitted'] = True
                    st.session_state['flex_charge'] = flex_charge


                if st.session_state['submitted']:
                    st.warning("You are adding a flex charge, are you sure?")
                    st.session_state['confirmation'] = st.button("Confirm Charge")

                    if not st.session_state['confirmation']:
                        return




            else:
                
                print("Wrong Row Selected in Update.py for Flex Spend")


    
