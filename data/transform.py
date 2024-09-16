import pandas as pd
from .source import source_data


# sourc_data UDF just returns the two dataframes ['df', 'curr_df']
# df is the data for historical data
# curr_df is data for current month data.
df, curr_df = source_data()



def transformData(df=df, curr_df=curr_df):

    #########################################
    #       Donut Charts Data Staging       #   
    #########################################

    # These values will be used for a donut chart that shows
    # How close we are to paying all bills in the current month.
    # For the vega donut charts, it is important that a dataframe with two columns,
    # labeled 'category' and 'value' be used. 
    # Here we stage a boolean 'category' of whether bills are marked as Paid or Unpaid.
    # The value for both is then assigned.
    curr_paid_df = curr_df[curr_df['Paid']=='TRUE']
    bills_paid_denom = curr_df['Value'].sum().round(2)
    bills_paid_numer = curr_paid_df['Value'].sum().round(2)

    bills_paid = pd.DataFrame({ 'paid':[bills_paid_numer], "denominator":[bills_paid_denom] })
    bills_paid['unpaid'] = bills_paid_denom - bills_paid_numer
    bills_paid_chart_data = pd.DataFrame({ 'category': ['paid', 'unpaid'], 'value' : [bills_paid['paid'][0], bills_paid['unpaid'][0]] })



    # Same rules as above apply regarding vega-lite donut chart configuration.
    # Goal is static 1000 currently.
    savings_goal = 1000
    savings_df = curr_df[curr_df['Bill']=='Minimum Savings']
    savings_val = savings_df['Value'].sum()
    savings_df = pd.DataFrame({"saved":[savings_val], "goal":[savings_goal]})
    savings_chart_data = pd.DataFrame({ 'category': ['saved', 'goal'], 'value' : [savings_df['saved'][0], savings_df['goal'][0]] })



    #########################################
    #       Trend Charts Data Staging       #   
    #########################################

    # Data is pivoted to assist with summarization.
    # viz_data is for the line chart.
    # barchart_df is for the bar chart.
    viz_data = df.melt(id_vars=["Title"], var_name='Month', value_name='Value')
    viz_data['Value'] = pd.to_numeric(viz_data['Value'])

    barchart_df = df.drop(columns=['Title']).sum().reset_index()
    barchart_df.columns = ['Month', 'Total']

    
    return df, bills_paid_chart_data, savings_chart_data, viz_data, barchart_df



if __name__ == "__main__":
    transformData()
