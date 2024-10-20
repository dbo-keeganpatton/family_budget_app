import os
import yaml
import pandas as pd
import streamlit as st
from yaml.loader import SafeLoader
pd.set_option('future.no_silent_downcasting', True)
from components.monthly_spending_barchart import monthlySpendingBarchart
from components.expense_trend_line_chart import expenseLineChart
from components.monthly_savings import monthlySavingsDonut
from components.bill_paid_donut import billsPaidDonut
from components.kpi_cards import kpiCards
from data.transform import transformData
import streamlit_authenticator as stauth

st.set_page_config(
    page_title="Patton Family Budget",
    page_icon='💸',
    layout='wide',
    menu_items=None
)



############################
#       Login Logic        #
############################

if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.info('Please Login from the Home page and try again.')
    st.switch_page("./app.py")

## Use this for DEV auth
with open('./auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


 # Use this for PROD Auth
 # log_cred = os.environ.get("LOGIN_CREDENTIALS")
 # config = yaml.load(log_cred, Loader=SafeLoader)


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)



# All Data used in main app can be sourced from transform.py
# They are transformed to fit visuals in this file and returned as
# themselves by the function 'transformData()'
df, bills_paid_chart_data, savings_chart_data, viz_data = transformData()   
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


##################################
#    Sidebar Filter Logic        #
##################################

# This is to create the sidebar, add each month name to a list and then we can use it to check against.
# I change the array to a set just so it can be only unique values.
# Default list is so the user can only start with a few bill types displayed, to reduce clutter.
month_filter_list = []
for i in df.columns:
    if i != 'Title':
        month_filter_list.append(i)
    else:
        pass

month_filter = set(month_filter_list)
default_list = ['Groceries ', 'Electric', 'Water', 'Gas', 'Baby Food']
bill_list = viz_data['Title'].unique()



##################################
#  KPI Metric Card Data Staging  #
##################################

# .loc ["Row Number", "Column to start from":]
# Display will be current average from all data, and the indicator will 
# show the variance of our current months value for that category compared to the average.
flex_spend_avg = df.iloc[23, 1:].mean().round(2)
electric_avg = df.iloc[6, 1:].mean().round(2)
grocery_avg = df.iloc[2, 1:].mean().round(2)
water_avg = df.iloc[10, 1:].mean().round(2)

flex_spend_current_month = df.iloc[23, -1:].max()
electric_current_month = df.iloc[6, -1:].max()
grocery_current_month = df.iloc[2, -1:].max()
water_current_month = df.iloc[10, -1:].max()

def find_percent_variance(curr_val, past_val):
    '''Just Calculates a variance'''
    var = curr_val - past_val
    diff = ((var / past_val) * 100).round(1)
    val = diff
    return val

flex_spend_current_month_var = find_percent_variance(flex_spend_current_month, flex_spend_avg)
electric_curr_month_var = find_percent_variance(electric_current_month, electric_avg)
grocery_current_month_var = find_percent_variance(grocery_current_month, grocery_avg)
water_current_month_var = find_percent_variance(water_current_month, water_avg )




######################################
#     Streamlit App Starts Here      #
######################################
def main():
    
        
    #####################
    #     KPI CARDS     #
    #####################
    kpiCards(
        grocery_avg, grocery_current_month_var,
        electric_avg, electric_curr_month_var,
        water_avg, water_current_month_var,
        flex_spend_avg, flex_spend_current_month_var
    ) 

    st.write("____________________")

    ######################
    #      Sidebar       #
    ######################
    with st.sidebar:
       

        # Detail Page Link
        with st.container(border=True):

            st.page_link(
                './pages/detail.py',
                label="View Raw Data",
                icon="🗂️",
                use_container_width=True
            )


        st.title('Category')
        selected_categories = st.multiselect(
            'Select Categories:',
            options=bill_list,
            default=[i for i in default_list if i in bill_list],
            help="""click anywhere in the selection box below
            to filter the report to specific expense categories.
            """,
            label_visibility='collapsed'

        )


        st.title('Month')
        selected_months = st.multiselect(
            "Select Month:",
            options=month_filter,
            default=[i for i in month_filter],
            label_visibility='collapsed'
        )
        
        
        st.write("______________")

        # Logout button
        authenticator.logout()


    ##############################
    #       Curr Month Viz       #
    ##############################
    cur1, cur2 = st.columns(2)

    with cur1:
        billsPaidDonut(data=bills_paid_chart_data, height=300)
        
    with cur2:
        monthlySavingsDonut(data=savings_chart_data, height=300)
        

    ##############################
    #      Seond Row Viz's       #
    ##############################
    viz1, viz2 = st.columns(2)
    
    with viz1:
        with st.container(height=400):
            ######################
            #     Bill Line      #
            ######################
            filtered_viz_data = viz_data[viz_data['Month'].isin(selected_months) & viz_data['Title'].isin(selected_categories)]  
            expenseLineChart(data=filtered_viz_data, sort=month_list) 

    with viz2:
            ######################
            #       Bar Chart    #
            ######################
        with st.container(height=400):
            monthlySpendingBarchart(data=filtered_viz_data, sort=month_list) 



################################
#     End Streamlit App        #
################################
if __name__ == "__main__":

        main()

