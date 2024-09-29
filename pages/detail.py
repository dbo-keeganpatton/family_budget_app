import streamlit as st
from data.source import source_data


st.set_page_config(
    page_title="Detail",
    page_icon='🔎',
    layout='wide',
    menu_items=None
)

df, curr_df = source_data()


curr_df['Paid'] = ["Yes" if i == "TRUE" else "" for i in curr_df["Paid"]]
curr_df['Priority'] = ["Yes" if i == "TRUE" else "" for i in curr_df["Priority"]]
curr_df['Value'] = ["" if i == None or i == 0 else i for i in curr_df["Value"]]


# There is some reaaally not great stuff here for formatting...
# Since basic orientation options just don't exist in ST...
# I am forced to implement columns abusively to enforce order.
col1, col2 = st.columns(2)

with col1:

    # Hacky Header for center-content
    c1, c2, c3 = st.columns([2,1,2])
    with c1:
        st.write("")
    with c2:
        st.subheader("This Month")
    with c3:
        st.write("")

    st.data_editor(
        curr_df,
        height=800,
        disabled=True,
        hide_index=True,
        use_container_width=True
    )

with col2:

    # Hacky Header for center-content
    c4, c5, c6 = st.columns([2,1,2])
    with c4:
        st.write("")
    with c5:
        st.subheader("All Months")
    with c6:
        st.write("")

    st.data_editor(
        df,
        height=800,
        disabled=True,
        hide_index=True,
        use_container_width=True
    )
