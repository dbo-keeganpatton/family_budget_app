import streamlit as st 




def monthlySpendingBarchart(data, sort):
    st.vega_lite_chart(
        data,
        {
            "height": 380,
            "mark" : {"type":"bar", "cornerRadiusEnd":4},
            "encoding" : {
               
                "x" : {
                    "field":"Month",
                    "sort" : sort,
                    "axis" :{"labelFontSize":16, "labelAngle":0, "title":False, "grid":False}
                },

                "y" : {
                    "aggregate":"sum",
                    "field":"Total",
                    "axis":{"labelFontSize":16,  "title":False, "grid":False}
                },

                "color" : {"value":"#7DEFA1"}
                    
            },

            "title": {
                "text": "Monthly Spending",  
                "fontSize": 30,  
                "anchor": "middle",  
            }
        },

        use_container_width=True
    )


if __name__ == "__main__":
    monthlySpendingBarchart()
