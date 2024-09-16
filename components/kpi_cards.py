import streamlit as st 



def kpiCards (grocery_avg, grocery_current_month_var, electric_avg, electric_curr_month_var, water_avg, water_current_month_var, flex_spend_avg, flex_spend_current_month_var):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(value=grocery_avg, label="Avg Grocery", delta=grocery_current_month_var, delta_color='off')

    with col2:
        st.metric(value=electric_avg, label="Avg Electric", delta=electric_curr_month_var, delta_color='off')
    
    with col3:
        st.metric(value=water_avg, label="Avg Water", delta=water_current_month_var, delta_color='off')

    with col4:
        st.metric(value=flex_spend_avg, label="Avg Flex Spend", delta=flex_spend_current_month_var, delta_color='off')
   
    


if __name__ == "__main__":

    kpiCards()

