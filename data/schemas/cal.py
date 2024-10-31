import pandas as pd
import calendar

start_year = 2020
end_year = 2100

# List to store calendar data
calendar_data = []

# Loop through each year and month in the specified range
for year in range(start_year, end_year + 1):
    for month in range(1, 13):

        # Create the Year_Month_Id in the format YYYYMM
        year_month_id = year * 100 + month
        
        # Get month name from the calendar module
        month_name = calendar.month_name[month]
        
        # Append data for each month
        calendar_data.append({
            "Year_Month_Id": year_month_id,
            "Month_Nbr": month,
            "Month": month_name,
            "Year": year
        })

calendar_df = pd.DataFrame(calendar_data)

calendar_df.to_csv("dim_calendar.csv", index=False)
