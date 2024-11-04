import streamlit as st


conn = st.connection("postgresql", type="sql")
expense_category = st.text_input("Expense Category")
new_value = st.number_input("New Value", min_value=0.0)

def update_payment(expense, value):
    try:
        conn.query(
            """
            UPDATE fact_payment
            SET value = :value,
                paid = TRUE
            WHERE expense = :expense;
            """,
            params={
                "value": value,
                "expense": expense
            }
        )
        return True
    except Exception as e:
        st.error(f"Error updating payment: {str(e)}")
        return False



if st.button("Update Payment"):
    if expense_category and new_value >= 0:
        if update_payment(expense_category, new_value):
            st.success("Payment updated successfully!")
    else:
        st.warning("Please enter both expense category and value")

