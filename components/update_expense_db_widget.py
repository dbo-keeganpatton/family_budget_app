import os
import streamlit as st
import pandas as pd
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)



st.set_page_config(
    page_title="Patton Family Budget",
    page_icon='💸',
    layout='wide',
    menu_items=None
)

conn = st.connection("postgresql", type="sql", url=DATABASE_URL)


###############################
#   Queries for Selections    #
###############################

expense_list_query = conn.query("select distinct expense from dim_expense")
expense_list_df = pd.DataFrame(expense_list_query)

month_list_query = conn.query("select distinct month from dim_calendar")
month_list_df = pd.DataFrame(month_list_query)

year_list_query = conn.query("""
    
    select distinct year from dim_calendar 
    where year between 2023 and extract(year from current_date)  
    
    """)
year_list_df = pd.DataFrame(year_list_query)


###############################
#         CRUD Logic          #
###############################
def update_payment(expense, year, month, value):
    try:

        with conn.session as session:
        # Streamlit requires a session to be accessed 
        # for CRUD actions to be committed to a DB
        # the session.execute() method also requires the 
        # query to be passed as a sqlalchemy.text() object.

            update_sql = text("""
            update fact_payment
                set value = case 
	                when expense in (
		                'groceries',
                        'gas',
                        'cat',
                        'savings',
                        'flex_spend',
                        'baby',
                        'skate') 
	                then value + :value
	                else :value
	                end,

	                paid = TRUE
                
                where
                    expense = :expense and 
                    month = :month and
                    mod(year_month_id / 100, 10000) = :year;
                """)

            session.execute(
                update_sql,
                params={
                    "value": value,
                    "expense": expense,
                    "month" : month,
                    "year": year
                }
            )

            session.commit()
            st.cache_data.clear()
            return True


    except Exception as e:
        st.error(f"Error updating payment: {str(e)}")
        return False




########################
#     Widget Logic     #
########################
@st.fragment
def submit_updated_payment():
    with st.form("Add Payment or Charge", clear_on_submit=True):
            st.subheader("Update Payment")
            
            with st.expander("Expand to view", expanded=False):
            ###############################
            #     Selections for User     #
            ###############################

                expense_category = st.selectbox("Expense Category", [i for i in expense_list_df['expense']])
                month_category = st.selectbox("Month", [i for i in month_list_df['month']])
                year_category = st.selectbox("Year", [i for i in year_list_df['year']])
                new_value = st.number_input("New Value", min_value=0.0)

                
                # Session Var
                submitted = st.form_submit_button("Confirm and Submit")
                

                if submitted:
                    if expense_category and year_category and month_category and new_value >= 0:
                        if update_payment(expense_category, year_category, month_category, new_value):
                            st.success("Payment updated successfully!")
                            

                    else:
                        st.warning("Please complete all fields")
                        

if __name__ == "__main__":
    submit_updated_payment()
