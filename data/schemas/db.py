####################################
#        SCHEMA QUERIES            #
####################################

dim_calendar_schema = """
CREATE TABLE dim_calendar (
    year_month_id INTEGER PRIMARY KEY,
    month_nbr INTEGER NOT NULL,
    month TEXT NOT NULL,
    year INTEGER NOT NULL
)
"""

dim_expense_schema = """
CREATE TABLE dim_expense (
    expense TEXT PRIMARY KEY,
    value INTEGER,
    priority BOOLEAN NOT NULL
)
"""

fact_payment_schema = """
CREATE TABLE fact_payment (
    date DATE NOT NULL,
    month TEXT NOT NULL,
    year_month_id INTEGER,
    expense TEXT,
    value INTEGER NOT NULL,
    paid BOOLEAN NOT NULL,
    FOREIGN KEY (year_month_id) REFERENCES dim_calendar (year_month_id),
    FOREIGN KEY (expense) REFERENCES dim_expense (expense)
)
"""

add_column = """
ALTER TABLE dim_expense
ADD COLUMN current_ind BOOLEAN
"""


#####################################
#        Stored Procedures          #
#####################################

populate_new_month = """
CREATE OR REPLACE FUNCTION public.populate_new_month_fact_payment()
 RETURNS void
 LANGUAGE plpgsql
AS $function$
DECLARE new_year_month_id INTEGER;
BEGIN
																		    -- Determine the next year_month_id 
																			-- based on the current date
	SELECT year_month_id
    INTO new_year_month_id
    FROM dim_Calendar
    WHERE year_month_id = (EXTRACT(YEAR FROM CURRENT_DATE) * 100 + EXTRACT(MONTH FROM CURRENT_DATE));

																		    -- Insert new rows into fact_payment with updated month 
																			-- and year_month_id from dim_Calendar
    INSERT INTO fact_payment (date, month, year_month_id, expense, value, paid)
    SELECT
        CURRENT_DATE,                           							-- Record the current date of insertion
        dc.month,                               							-- Use the month name from dim_Calendar
        dc.year_month_id,                       							-- Use the new year_month_id from dim_Calendar
        fp.expense,                             							-- Expense category from the previous month
        CASE WHEN de.static_ind THEN fp.value ELSE 0 END,  						-- Keep value if static, otherwise set to 0
        false                                   							-- Reset paid to false for the new month
    FROM fact_payment AS fp
    INNER JOIN dim_expense AS de ON fp.expense = de.expense
    INNER JOIN dim_Calendar AS dc ON dc.year_month_id = new_year_month_id
    WHERE fp.year_month_id = new_year_month_id - 1;    						-- Filter by the previous month
END;
$function$;
"""

####################################
#          ELT Actions             #
####################################
add_expense = """

UPDATE fact_payment
SET value = :value,
	paid = TRUE
WHERE 
	expense = :expense and 
	month = :month and
	mod(year_month_id / 100, 10000) = :year;

"""



