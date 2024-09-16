import streamlit as st


def expenseLineChart(data, sort):
    st.vega_lite_chart(
        data,
        {
            "height": 360,
            "mark" : "line",
            "encoding" : {
                
                "x" : {
                    "field":"Month", 
                    "type":"ordinal",
                    "sort" : sort,
                    "axis" :{"labelFontSize":16, "labelAngle":-30, "title":False}
                
                },

                "y" : {
                    "field":"Value", 
                    "type":"quantitative",
                    "axis" :{"labelFontSize":16, "title":False, "grid":False}
                },
                
                "color" : {
                    "field" : "Title", 
                    "type" : "nominal",
                    "legend" : {"orient":"bottom", "title":False, "labelFontSize":16}
                },
                

            },
            
            "title": {
                "text": "Expense Trends",  
                "fontSize": 30,  
                "anchor": "middle",  
            }

        },

        use_container_width=True
    )



if __name__ == "__main__":
    expenseLineChart()
