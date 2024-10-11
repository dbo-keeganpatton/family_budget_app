from gspread.auth import service_account, service_account_from_dict
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


gc = gspread.service_account_from_dict(gcp_credentials_dict)
sh = gc.open('Budget')
curr_month_data = sh.worksheets()
curr_mnt = curr_month_data[-2]



#########################################
#              Input Form               #
#########################################
with st.form("Add Payment or Charge"):
    st.subheader("Add Flex Charge")
    
    with st.expander("expand to view"):
         

        if 'Flexible Spending' in curr_mnt.row_values(39):
            
            
            flex_spend_formula = curr_mnt.row_values(39, value_render_option=ValueRenderOption.formula)[2]

            if st.form_submit_button:
                flex_charge = st.text_input(label="Amount")

                adjusted_formula = flex_spend_formula.replace(")", f"+{flex_charge})")
                
                update_action = curr_mnt.update_cell(39, 3, adjusted_formula)
                

            else:
                pass
        
            st.form_submit_button()

        else:
            
            print("Wrong Row Selected in Update.py for Flex Spend")


    
