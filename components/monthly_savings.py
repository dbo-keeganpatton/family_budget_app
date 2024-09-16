import streamlit as st


def monthlySavingsDonut(data, height):
    with st.container(height=height):
                st.vega_lite_chart(
                    data,
                    {
                        "height": 250,
                        "width": 250,
                        "mark": {"type":"arc", "innerRadius":60},
                        "encoding": {
                            "theta": {"field":"value", "type":"quantitative"},
                            "color": {
                                "field":"category", 
                                "type":"nominal",
                                "scale": {
                                        "domain":["saved", "goal"],
                                        "range":["#7DEFA1", "#C02F35"]
                                    },
                                "legend" : False 
                            }
                        },

                        "title": {
                            "text": "Monthly Savings Goal",  
                            "fontSize": 30,  
                            "anchor": "middle",  
                        }

                    },
                    use_container_width=True
                )


if __name__ == "__main__":
    monthlySavingsDonut()
