
import streamlit as st

def billsPaidDonut(data, height):
   
    total_value = sum(data['value'])
    paid_value = sum(data[data['category']=="paid"]['value'])
    paid_percentage = round( (paid_value / total_value) * 100, 0)

    
    with st.container(height=height):
        st.vega_lite_chart(
            data,
            {
                "height": 250,
                "width": 250,
                "layer": [
                    
                    {
                        "mark": {"type": "arc", "innerRadius": 60},
                        "encoding": {
                            "theta": {"field": "value", "type": "quantitative"},
                            "color": {
                                "field": "category",
                                "type": "nominal",
                                "scale": {
                                    "domain": ["paid", "unpaid"],
                                    "range": ["#7DEFA1", "#C02F35"]
                                },
                                "legend": False
                            }
                        }
                    },
                    
                    {
                        "mark": {
                            "type": "text",
                            "align": "center",
                            "baseline": "middle",
                            "font": "sans-serif",
                            "fontSize": 24,
                            "color": "#EEEEEE"
                        },

                        "encoding": {
                            "text": {
                                "value": f"{paid_percentage:.0f}%"  # Display percentage of bills paid
                            }
                        }
                    }
                ],
                "title": {
                    "text": "Current Month Bills Paid",
                    "fontSize": 30,
                    "anchor": "middle",
                }
            },
            use_container_width=True
        )


if __name__ == "__main__":
    billsPaidDonut()

