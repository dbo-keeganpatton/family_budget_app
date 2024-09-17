import streamlit as st 


# After alot of headache with the st.metric class, I just decided
# to make a custom function using html/css and normal strings to make indicators that fit our needs.
def colored_metric(label, value, delta, delta_color):
        delta_sign = "+" if delta > 0 else ""
        html = f"""
            <div style="font-size: 24px; color: #888;">{label}</div>
            <div style="font-size: 36px; font-weight: bold;">{value}</div>
            <div style="font-size: 24px; color: {delta_color};">
            {delta_sign} {delta} %
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)


def get_delta_color(delta):
    return "#C02F35" if float(delta) >= 0 else "#7DEFA1" 




def kpiCards (grocery_avg, grocery_current_month_var, electric_avg, electric_curr_month_var, water_avg, water_current_month_var, flex_spend_avg, flex_spend_current_month_var):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        colored_metric(label="Avg Grocery", value=grocery_avg, delta=grocery_current_month_var, delta_color=get_delta_color(grocery_current_month_var))

    with col2:
        colored_metric(label="Avg Electric", value=electric_avg, delta=electric_curr_month_var, delta_color=get_delta_color(electric_curr_month_var))
    
    with col3:
        colored_metric(label="Avg Water", value=water_avg, delta=water_current_month_var, delta_color=get_delta_color(water_current_month_var))

    with col4:
        colored_metric(label="Avg Flex Spend", value=flex_spend_avg, delta=flex_spend_current_month_var, delta_color=get_delta_color(flex_spend_current_month_var))
   


if __name__ == "__main__":

    kpiCards()

