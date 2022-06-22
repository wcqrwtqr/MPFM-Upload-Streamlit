import streamlit as st

'''
This module help calculate the air/oil ratio for the burning process
'''

def convert_api_and_oil_rate_to_ton(api, oil):
    "This function will convert the data"
    if api != 0.0:
        x_api = 1000 * (141.5 / (api + 131.5))
        x_ton = x_api * (oil / 6.29) / 1000
    return x_ton


def convert_air_suupply_to_ton(air):
    "This function convert the air supply to ton"
    x_ton = air * 60 * 24 / 35.3147 * 1.225 / 1000
    return x_ton


def calculate_the_values_of_air(API_val, air_rate, oil_rate):
    # Check if the values are no zero
    conv_oil = convert_api_and_oil_rate_to_ton(API_val, oil_rate)
    conv_air = convert_air_suupply_to_ton(air_rate)

    if conv_oil != 0:
        air_oil_ratio = conv_air / conv_oil * 100
        if 10 <= air_oil_ratio <= 20:
            st.subheader(
                f"At oil rate {oil_rate} and air rate of \
                {air_rate} ratio is: {air_oil_ratio:.2f}% ✅"
            )
            return air_oil_ratio
        else:
            st.write(
                f"At oil rate {oil_rate} and air rate of \
                    {air_rate} ratio is: {air_oil_ratio:.2f}% 🚫"
            )
            return air_oil_ratio
