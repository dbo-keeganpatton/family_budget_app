import gspread
import pandas as pd
import streamlit as st
pd.set_option('future.no_silent_downcasting', True)


# Authenticate using the svc account and get period data...
# will be a list of dictionaries and parse into a DataFrame.
# Ignore lsp for service_account method warning.
gc = gspread.service_account(filename='./secrets/secret.json')
sh = gc.open('Budget')
ws = sh.worksheet('Dashboard Data')
db_data = ws.get_all_records()
df = pd.DataFrame(db_data)
df.replace('', 0, inplace=True)



# This will be for getting the most current month for ELT...
# And current month tracking.
curr_month_data = sh.worksheets()
curr_mnt = curr_month_data[-2]

curr_data = curr_mnt.get("B15:F39")
curr_df = pd.DataFrame(curr_data)
curr_df.columns = curr_df.iloc[0]
curr_df = curr_df.drop(0).reset_index(drop=True)
curr_df['Value'] = pd.to_numeric(curr_df['Value'].dropna())

curr_paid_df = curr_df[curr_df['Paid']=='TRUE']


# These values will be used for a donut chart that shows...
# How close we are to paying all bills in the current month.
bills_paid_denom = curr_df['Value'].sum().round(2)
bills_paid_numer = curr_paid_df['Value'].sum().round(2)


bills_paid = pd.DataFrame({
    'paid':[bills_paid_numer],
    "denominator":[bills_paid_denom]
})


bills_paid['unpaid'] = bills_paid_denom - bills_paid_numer

bills_paid_chart_data = pd.DataFrame({
    'category': ['paid', 'unpaid'],
    'value' : [bills_paid['paid'][0], bills_paid['unpaid'][0]]
})



# Savings Donut chart Stage data 
savings_df = curr_df[curr_df['Bill']=='Minimum Savings']
savings_val = savings_df['Value'].sum()
savings_goal = 1000
savings_df = pd.DataFrame({"saved":[savings_val], "goal":[savings_goal]})

savings_chart_data = pd.DataFrame({
    'category': ['saved', 'goal'],
    'value' : [savings_df['saved'][0], savings_df['goal'][0]]
})





# Stage for Bar and Line viz     
viz_data = df.melt(id_vars=["Title"], var_name='Month', value_name='Value')
viz_data['Value'] = pd.to_numeric(viz_data['Value'])
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

barchart_df = df.drop(columns=['Title']).sum().reset_index()
barchart_df.columns = ['Month', 'Total']



# Slicer Filters
default_list = ['Groceries ', 'Electric', 'Water', 'Gas', 'Baby Food']
bill_list = viz_data['Title'].unique()



# KPI Card slices
# .loc ["Row Number", "Column to start from":]
flex_spend_avg = df.iloc[23, 1:].mean().round(2)
electric_avg = df.iloc[6, 1:].mean().round(2)
grocery_avg = df.iloc[2, 1:].mean().round(2)
water_avg = df.iloc[10, 1:].mean().round(2)

flex_spend_current_month = df.iloc[23, -1:].max()
electric_current_month = df.iloc[6, -1:].max()
grocery_current_month = df.iloc[2, -1:].max()
water_current_month = df.iloc[10, -1:].max()



def find_percent_variance(curr_val, past_val):
    
    var = curr_val - past_val
    diff = ((var / past_val) * 100).round(1)
    val = f"{diff}%"
    return val


# KPI Card Current variance values
flex_spend_current_month_var = find_percent_variance(flex_spend_current_month, flex_spend_avg)
electric_curr_month_var = find_percent_variance(electric_current_month, electric_avg)
grocery_current_month_var = find_percent_variance(grocery_current_month, grocery_avg)
water_current_month_var = find_percent_variance(water_current_month, water_avg )


# I do not like the standard colors for st.metric() indicators..
# They are not aligned with my theme and this is to overide them.
# I can not figure out how to affect the arrows so only the values will be colored
custom_css = """
    <style>
    /* Positive */
    div[data-testid="stMetricDelta"] div:first-child {
        color: #C02F35 !important;  
        font-size: 24px !important;
    }
    
    /* Negative */
    div[data-testid="stMetricDelta"] div:nth-child(2) {
        color: #7DEFA1 !important; 
        font-size: 24px !important;
    }
    </style>
    """


######################
#     Streamlit      #
######################
def main():
   

    

    # This if for the st.metric() custom coloring. 
    st.markdown(custom_css, unsafe_allow_html=True)
    #####################
    #     KPI CARDS     #
    #####################
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(value=grocery_avg, label="Avg Grocery", delta=grocery_current_month_var, delta_color='off')

    with col2:
        st.metric(value=electric_avg, label="Avg Electric", delta=electric_curr_month_var, delta_color='off')
    
    with col3:
        st.metric(value=water_avg, label="Avg Water", delta=water_current_month_var, delta_color='off')

    with col4:
        st.metric(value=flex_spend_avg, label="Avg Flex Spend", delta=flex_spend_current_month_var, delta_color='off')
   

    st.write("____________________")

    ######################
    #      Sidebar       #
    ######################
    with st.sidebar:
        selected_categories = st.multiselect(
            'Select Categories:',
            options=bill_list,
            default=[i for i in default_list if i in bill_list],
            help="""click anywhere in the selection box below
            to filter the report to specific expense categories.
            """
        )
    

    
    ##############################
    #       Curr Month Viz       #
    ##############################
    cur1, cur2, cur3 = st.columns(3)

    with cur1:
        with st.container(height=300):
            st.vega_lite_chart(
                bills_paid_chart_data,
                {
                    "height": 250,
                    "width": 250,
                    "mark": {"type":"arc", "innerRadius":60},
                    "encoding": {
                        "theta": {"field":"value", "type":"quantitative"},
                        "color": {
                            "field":"category", 
                            "type":"nominal",
                            "scale": {
                                    "domain":["paid", "unpaid"],
                                    "range":["#7DEFA1", "#C02F35"]
                                },
                            "legend" : False 
                        }
                    },

                    "title": {
                        "text": "Current Month Bills Paid",  
                        "fontSize": 30,  
                        "anchor": "middle",  
                    }

                },
                use_container_width=True
            )


    with cur2:
        with st.container(height=300):
            st.vega_lite_chart(
                savings_chart_data,
                {
                    "height": 250,
                    "width": 250,
                    "mark": {"type":"arc", "innerRadius":60},
                    "encoding": {
                        "theta": {"field":"value", "type":"quantitative"},
                        "color": {
                            "field":"category", 
                            "type":"nominal",
                            "scale": {
                                    "domain":["saved", "goal"],
                                    "range":["#7DEFA1", "#C02F35"]
                                },
                            "legend" : False 
                        }
                    },

                    "title": {
                        "text": "Monthly Savings Goal",  
                        "fontSize": 30,  
                        "anchor": "middle",  
                    }

                },
                use_container_width=True
            )


    with cur3:
        with st.container(height=300):
            st.write("Current Debt to be Paid")



    ##############################
    #      Seond Row Viz's       #
    ##############################
    viz1, viz2 = st.columns(2)

    
    
    with viz1:
        with st.container(height=400):
        ######################
        #     Bill Line      #
        ######################
            filtered_viz_data = viz_data[viz_data['Title'].isin(selected_categories)]
            st.vega_lite_chart(
                filtered_viz_data,
                {
                    "height": 360,
                    "mark" : "line",
                    "encoding" : {
                        
                        "x" : {
                            "field":"Month", 
                            "type":"ordinal",
                            "sort" : month_list,
                            "axis" :{"labelFontSize":16, "labelAngle":-30, "title":False}
                        
                        },

                        "y" : {
                            "field":"Value", 
                            "type":"quantitative",
                            "axis" :{"labelFontSize":16, "title":False, "grid":False}
                        },
                        
                        "color" : {
                            "field" : "Title", 
                            "type" : "nominal",
                            "legend" : {"orient":"bottom", "title":False, "labelFontSize":16}
                        },
                        

                    },
                    
                    "title": {
                        "text": "Expense Trends",  
                        "fontSize": 30,  
                        "anchor": "middle",  
                    }

                },

                use_container_width=True
            )

   


    with viz2:
        ##########################
        #       Bar Chart        #
        ##########################
        with st.container(height=400):
            st.vega_lite_chart(
                barchart_df,
                {
                    "height": 380,
                    "mark" : {"type":"bar", "cornerRadiusEnd":4},
                    "encoding" : {
                       
                        "x" : {
                            "field":"Month",
                            "sort" : month_list,
                            "axis" :{"labelFontSize":16, "labelAngle":0, "title":False, "grid":False}
                        },

                        "y" : {
                            "aggregate":"sum",
                            "field":"Total",
                            "axis":{"labelFontSize":16,  "title":False, "grid":False}
                        },

                        "color" : {"value":"#7DEFA1"}
                            
                    },

                    "title": {
                        "text": "Monthly Spending",  
                        "fontSize": 30,  
                        "anchor": "middle",  
                    }
                },

                use_container_width=True
            )

    


if __name__ == "__main__":

    
    st.set_page_config(
            page_title="Patton Family Budget",
            page_icon='💸',
            layout='wide',
            menu_items=None
        )
    
    main()

