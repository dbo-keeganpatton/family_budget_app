import gspread
from gspread.auth import service_account, service_account_from_dict
import pandas as pd
import json
import os
pd.set_option('future.no_silent_downcasting', True)
from google.oauth2.service_account import Credentials



def source_data():
    

    ####################################
    #         Trend Data Pull          #
    ####################################
    # Source data is located on a specific page where data is aggregated across all months.
    # This will be used for trend visuals and KPI cards.
    
    # IMPORTANT!! Since the app is executed from the project root, the secret path for GCP
    # must be set to route from that location.
    # secret = './data/secrets/secret.json'
    
    # Use this for PROD auth
    secret = os.getenv('GCP_SERVICE_ACCOUNT')
    gcp_credentials_dict = json.loads(secret)
    

    
    gc = gspread.service_account_from_dict(gcp_credentials_dict)
    sh = gc.open('Budget')
    ws = sh.worksheet('Dashboard Data')
    db_data = ws.get_all_records()
    df = pd.DataFrame(db_data)
    df.replace('', 0, inplace=True)
    

    ####################################
    #    Current Month Data Pull       #
    ####################################
    # Current month data should always be the last sheet in the index of the workbook.
    # For not it is the second to last, this will change after 12/01/2024.
    
    curr_month_data = sh.worksheets()
    curr_mnt = curr_month_data[-2]
    curr_data = curr_mnt.get("B15:F39")
    curr_df = pd.DataFrame(curr_data)
    curr_df.columns = curr_df.iloc[0]
    curr_df = curr_df.drop(0).reset_index(drop=True)
    curr_df['Value'] = pd.to_numeric(curr_df['Value'].dropna())


    return df, curr_df


if __name__ == "__main__":
    source_data()
