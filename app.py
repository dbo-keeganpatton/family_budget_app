import gspread
import pandas as pd
import streamlit as st



# Authenticate using the svc account and get period data...
# will be a list of dictionaries and parse into a DataFrame.
# Ignore lsp for service_account method warning.
gc = gspread.service_account(filename='./secrets/secret.json')
sh = gc.open('Budget')
ws = sh.worksheet('Dashboard Data')
db_data = ws.get_all_records()
df = pd.DataFrame(db_data)
df.replace('', 0, inplace=True)



# Stage for viz     
viz_data = df.melt(id_vars=["Title"], var_name='Month', value_name='Value')
viz_data['Value'] = pd.to_numeric(viz_data['Value'])
month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]



# Slicer Filters
default_list = ['Groceries ', 'Electric', 'Water', 'Gas', 'Baby Food']
bill_list = viz_data['Title'].unique()



# KPI Card slices
# .loc ["Row Number", "Column to start from":]
flex_spend_avg = df.iloc[23, 1:].mean().round(2)
electric_avg = df.iloc[6, 1:].mean().round(2)
grocery_avg = df.iloc[2, 1:].mean().round(2)
water_avg = df.iloc[10, 1:].mean().round(2)

flex_spend_current_month = df.iloc[23, -1:].max().round(2)
electric_current_month = df.iloc[6, -1:].max().round(2)
grocery_current_month = df.iloc[2, -1:].max().round(2)
water_current_month = df.iloc[10, -1:].max().round(2)


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



######################
#     Streamlit      #
######################
def main():
    

    #####################
    #     KPI CARDS     #
    #####################
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(value=grocery_avg, label="Avg Grocery", delta=grocery_current_month_var, delta_color='inverse')

    with col2:
        st.metric(value=electric_avg, label="Avg Electric", delta=electric_curr_month_var, delta_color='inverse')
    
    with col3:
        st.metric(value=water_avg, label="Avg Water", delta=water_current_month_var, delta_color='inverse')

    with col4:
        st.metric(value=flex_spend_avg, label="Avg Flex Spend", delta=flex_spend_current_month_var, delta_color='inverse')
   

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
    

    

    ######################
    #     Bill Line      #
    ######################
    filtered_viz_data = viz_data[viz_data['Title'].isin(selected_categories)]
    st.vega_lite_chart(
        filtered_viz_data,
        {
            "mark" : "line",
            "encoding" : {
                
                "x" : {
                    "field":"Month", 
                    "type":"ordinal",
                    "sort" : month_list,
                    "axis" :{"labelFontSize":18, "labelAngle":-30, "title":False}
                
                },

                "y" : {
                    "field":"Value", 
                    "type":"quantitative",
                    "axis" :{"labelFontSize":18, "title":False}
                },
                
                "color" : {"field" : "Title", "type" : "nominal"}
            }
        },

        use_container_width=True
    )

    st.write(df)
    st.write(viz_data)
    


if __name__ == "__main__":

    
    st.set_page_config(
            page_title="Patton Family Budget",
            page_icon='💸',
            layout='wide',
            menu_items=None
        )
    
    main()

