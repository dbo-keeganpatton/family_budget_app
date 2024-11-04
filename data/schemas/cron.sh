# Populate a new months data in fact_payment on the 1st of each month
PGPASSWORD='password' /usr/bin/psql -U username -d database -c "SELECT populate_new_month_fact_payment();"


# Backup the database each night
PGPASSWORD='password' pg_dump -U username -h localhost -F c -b -v -f "/home/user/database_backups/db_name/db_$(date +\%Y-\%m-\%d).sql" database_name

