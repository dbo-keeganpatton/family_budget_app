import os
import yaml
import psycopg2
import pandas as pd
import streamlit as st
import sqlalchemy as sa
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
pd.set_option('future.no_silent_downcasting', True)
from components.update_expense_db_widget import submit_updated_payment
from components.monthly_spending_barchart import monthlySpendingBarchart
from components.expense_trend_line_chart import expenseLineChart
from components.monthly_savings import monthlySavingsDonut
from components.bill_paid_donut import billsPaidDonut
from components.kpi_cards import kpiCards
from data.source import all_data


DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)


conn = st.connection("postgresql", type='sql', url=DATABASE_URL)
payments = conn.query("select * from fact_payment")


############################
#       Login Logic        #
############################

if 'authentication_status' not in st.session_state or not st.session_state['authentication_status']:
    st.info('Please Login from the Home page and try again.')
    st.switch_page("./app.py")

### Use this for DEV auth
with open('./auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


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
df, curr_df, bills_paid_chart_data, savings_chart_data, viz_data = all_data()   
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


##################################
#    Sidebar Filter Logic        #
##################################

# This is to create the sidebar, add each month name to a list and then we can use it to check against.
# I change the array to a set just so it can be only unique values.
# Default list is so the user can only start with a few bill types displayed, to reduce clutter.
month_filter_list = []
for i in df['month']:
    month_filter_list.append(i)



month_filter = set(month_filter_list)
default_list = ['groceries', 'electric', 'water', 'gas', 'baby']
bill_list = viz_data['expense'].unique()


##################################
#  KPI Metric Card Data Staging  #
##################################
def get_avg(df, expense_name):

    result = df[df['expense'] == expense_name].groupby('expense')['value'].mean()
    return round(float(result.squeeze()), 0) if not result.empty else 0.0


flex_spend_avg = get_avg(df, "flex_spend")
electric_avg = get_avg(df, "electric")
grocery_avg = get_avg(df, "groceries")
water_avg = get_avg(df, "water")


flex_spend_current_month = get_avg(curr_df, "flex_spend")
electric_current_month = get_avg(curr_df, "electric")
grocery_current_month = get_avg(curr_df, "groceries")
water_current_month = get_avg(curr_df, "water")


def find_percent_variance(curr_val, past_val):
    '''Just Calculates a variance'''
    
    if past_val == 0:  
        return 0.0 if curr_val == 0 else float('inf')
    var = curr_val - past_val
    diff = (var / past_val) * 100
    return round(diff, 0)


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
        
        ###############################
        #   Flex Spend add Widget     #
        ###############################

        submit_updated_payment()


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
            filtered_viz_data = viz_data[viz_data['month'].isin(selected_months) & viz_data['expense'].isin(selected_categories)]  
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

