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
grocery_avg = df.iloc[2, 1:].mean()




######################
#     Streamlit      #
######################
def main():
    
    st.title("Patton Family Budget")
    
    
    st.metric(value=grocery_avg, label="Avg Grocery")

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

