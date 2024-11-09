import os
import pandas as pd
import streamlit as st
import psycopg2
pd.set_option('future.no_silent_downcasting', True)



# DEV Local DB
DATABASE_URL = os.getenv("DATABASE_URL")

# PROD DB 
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)


@st.cache_data
def all_data():
    
    # Database Connection
    conn = st.connection("postgresql", type='sql', url=DATABASE_URL)

    ####################################
    #         Trend Data Pull          #
    ####################################
    trend = conn.query("select month, expense, value from fact_payment")
    df = pd.DataFrame(trend)


    ####################################
    #    Current Month Data Pull       #
    ####################################
    curr = conn.query("""
        select 
        pa.month, 
        pa.expense, 
        pa.value, 
        pa.paid , 
        de.priority 
        from fact_payment as pa
        left join dim_expense as de 
            on de.expense  = pa.expense 
        where year_month_id = ( select max(year_month_id) from fact_payment)
        """)

    curr_df = pd.DataFrame(curr)


    #########################################
    #       Donut Charts Data Staging       #   
    #########################################

    # These values will be used for a donut chart that shows
    # How close we are to paying all bills in the current month.
    # For the vega donut charts, it is important that a dataframe with two columns,
    # labeled 'category' and 'value' be used. 
    # Here we stage a boolean 'category' of whether bills are marked as Paid or Unpaid.
    # The value for both is then assigned.
    curr_paid = conn.query("""
    select 
    month, expense, value, paid 
    from fact_payment
    where 
    year_month_id = ( select max(year_month_id) from fact_payment )
    and paid = true
    """)    
    curr_paid_df = pd.DataFrame(curr_paid)


    bills_paid_denom = curr_df['value'].sum()
    bills_paid_numer = curr_paid_df['value'].sum()
    bills_paid = pd.DataFrame({ 'paid':[bills_paid_numer], "denominator":[bills_paid_denom] })
    bills_paid['unpaid'] = bills_paid_denom - bills_paid_numer
    bills_paid_chart_data = pd.DataFrame({ 'category': ['paid', 'unpaid'], 'value' : [bills_paid['paid'][0], bills_paid['unpaid'][0]] })


    # Same rules as above apply regarding vega-lite donut chart configuration.
    # Goal is static 1000 currently.
    savings_goal = 1000
    savings_df = curr_df[curr_df['expense']=='Minimum Savings']
    savings_val = savings_df['value'].sum()
    savings_df = pd.DataFrame({"saved":[savings_val], "goal":[savings_goal]})
    savings_chart_data = pd.DataFrame({ 'category': ['saved', 'goal'], 'value' : [savings_df['saved'][0], savings_df['goal'][0]] })



    #########################################
    #       Trend Charts Data Staging       #   
    #########################################

    # Data is pivoted to assist with summarization.
    # viz_data is for the line chart.
    # barchart_df is for the bar chart.
    viz_data = df.copy()
    viz_data['value'] = pd.to_numeric(viz_data['value'])

    
    return df, curr_df, bills_paid_chart_data, savings_chart_data, viz_data

if __name__ == "__main__":
    all_data()
