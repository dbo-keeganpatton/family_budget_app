import streamlit as st 




def monthlySpendingBarchart(data, sort):
    st.vega_lite_chart(
        data,
        {
            "height": 380,
            "mark" : {"type":"bar", "cornerRadiusEnd":4},
            "encoding" : {
               
                "x" : {
                    "field":"month",
                    "sort" : sort,
                    "axis" :{"labelFontSize":16, "labelAngle":0, "title":False, "grid":False}
                },

                "y" : {
                    "aggregate":"sum",
                    "field":"value",
                    "axis":{"labelFontSize":16,  "title":False, "grid":False}
                },
                
                "color" : {
                    "field" : "expense", 
                    "type" : "nominal",
                    "legend" : {"orient":"bottom", "title":False, "labelFontSize":16}
                },

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
