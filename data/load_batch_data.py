import pandas as pd
import sqlite3 as sql

cal_df = pd.read_csv('./schemas/dim_calendar.csv')
expense_df = pd.read_csv('./schemas/dim_expense.csv')
payment_df = pd.read_csv('./schemas/fact_payment.csv')

conn = sql.connect('./database.db')


# cal_df.to_sql('dim_calendar', conn, if_exists='append', index=False)
# expense_df.to_sql('dim_expense', conn, if_exists='append', index=False)
# payment_df.to_sql('fact_payment', conn, if_exists='append', index=False)


conn.close()
