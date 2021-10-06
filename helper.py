import pandas as pd
import streamlit as st
import numpy as np
from graphing import graphing_line_2v, graphing_line_1v


def Gauges_data_Spartek(source_file, row=10):
    """ Gauges data processing generator

    :param source_file: file path
    :type source_file: string
    :param row: number of rows
    :type row: int

    :returns: None
    :rtype: None """

    df = pd.read_csv(source_file, sep='\s+', header=None, skiprows=row ,
                     names=['date', 'time','AMPM','elpse', 'pressure',
                            'temperature'], engine='python')
    range_data = df.index.tolist()
    df['date_time'] = df['date'] + " " + df['time'] + " " + df['AMPM']
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0]:range_data_selection[1]]
    # graphing the values of time, pressure and temperature using the function
    dx = graphing_line_2v(df_lst, 'date_time', 'pressure', 'temperature')
    # Showing the graphs 
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    st.markdown('Pressure Temperature Graph')

    with st.expander(label='Table of Data'):
        st.markdown('Full Data Table')
        st.dataframe(df_lst)
    with st.expander(label='Gauges Chart'):
        st.plotly_chart(dx)
    st.markdown(f'*Available Data: {df_lst.shape[0]}')

# ********************************************************************
# *************** Gauges Function for Metrolg Gauges******************
# ********************************************************************

def Gauges_data(source_file, row=10):
    """ Gauges data processing generator

    :param source_file: file path
    :type source_file: string
    :param row: number of rows
    :type row: int

    :returns: None
    :rtype: None """

    df = pd.read_csv(source_file, sep='[,\t]', header=None, skiprows=row , names=['date', 'time', 'pressure', 'temperature'], engine='python')
    range_data = df.index.tolist()
    df['date_time'] = df['date'] + " " + df['time']
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0]:range_data_selection[1]]
    # graphing the values of time, pressure and temperature using the function
    dx = graphing_line_2v(df_lst, 'date_time', 'pressure', 'temperature')
    # Showing the graphs 
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    st.markdown('Pressure Temperature Graph')

    with st.expander(label='Table of Data'):
        st.markdown('Full Data Table')
        st.dataframe(df_lst)
    with st.expander(label='Gauges Chart'):
        st.plotly_chart(dx)
    st.markdown(f'*Available Data: {df_lst.shape[0]}')

# ********************************************************************
# ************** MPFM Function ***************************************
# ********************************************************************

def MPFM_data(source_file):
    """ MPFM data processing generator

    :param source_file: file path
    :type source_file: string

    :returns: None
    :rtype: None """

    df = pd.read_csv(source_file, sep='\t')
    df.dropna(inplace=True, axis=1)
    # Masking
    range_data = df.index.tolist()
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0]:range_data_selection[1]]

    # Averages calculation
    avg_P           = np.average(df_lst['Pressure'])
    avg_T           = np.average(df_lst['Temperature'])
    avg_dP          = np.average(df_lst['dP'])
    avg_oilRate     = np.average(df_lst['Std.OilFlowrate'])
    avg_waterRate   = np.average(df_lst['WaterFlowrate'])
    avg_std_gasRate = np.average(df_lst['Std.GasFlowrate'])
    avg_act_gasRate = np.average(df_lst['Act.GasFlowrate'])
    avg_GOR         = np.average(df_lst['GOR(std)'])
    avg_WC          = np.average(df_lst['Std.Watercut'])
    avg_oilSG       = np.average(df_lst['OilDensity'])
    avg_waterSG     = np.average(df_lst['WaterDensity'])
    avg_gasSG       = np.average(df_lst['GasDensity'])
    avg_liquid      = avg_oilRate + avg_waterRate
    API             = (141.5/(avg_oilSG/1000) - 131.5)
    start           = df_lst['Clock'][range_data_selection[0]] + ' ' + df_lst['Date'][range_data_selection[0]]
    end             = df_lst['Clock'][range_data_selection[1]-1] + ' ' + df_lst['Date'][range_data_selection[1]-1]
    # Making the dataframe
    dict_summary = {'Start Time': start,
                    'End Time': end, 'WHP': avg_P, 'WHT': avg_T,
                    'Diff dP': avg_dP, 'Oil Rate': avg_oilRate, 'Water Rate': avg_waterRate,
                    'Liquid Rate': avg_liquid, 'Gas Rate': avg_std_gasRate,
                    'Actual Gas Rate': avg_act_gasRate, 'Total GOR': avg_GOR,
                    'Gas SG': avg_gasSG, 'Oil SG': avg_oilSG, 'Oil API': API,
                    'BSW': avg_WC, 'Water SG' : avg_waterSG}
    summary = pd.DataFrame([dict_summary])

    # Making the graphs
    ptd           = graphing_line_2v(df_lst, 'Clock', 'Pressure', 'dP')
    oil_GOR       = graphing_line_2v(df_lst, 'Clock', 'Std.OilFlowrate', 'GOR(std)')
    gas_oil       = graphing_line_2v(df_lst, 'Clock', 'Std.OilFlowrate', 'Std.GasFlowrate')
    oil_water_cum = graphing_line_2v(df_lst, 'Clock', 'Std.AccumOilVol', 'AccumWaterVol')

    # Drawing the graphs
    st.markdown(f'*Available Data: {df_lst.shape[0]}')
    with st.expander(label='Data Set'):
        st.dataframe(df_lst)
        st.download_button(label='Download data', data=df_lst.to_csv(), mime='text/csv')
    st.markdown('Average Table')
    st.dataframe(summary)
    st.download_button(label='Download Summary', data=summary.to_csv(), mime='text/csv')
    st.subheader('Summary of Data:')
    col1, col2, col3, col4 = st.columns(4)
    col1.subheader(f'Oil rate: {int(avg_oilRate)}')
    col2.subheader(f'Water rate: {int(avg_waterRate)}')
    gas_rate_float = "{:.4f}".format(avg_std_gasRate)
    col3.subheader(f'Gas rate: {float(gas_rate_float)}')
    col4.subheader(f'GOR: {int(avg_GOR)}')

    # Making the graphs
    with st.expander(label='Parameters Charts'):
        col6, col7 = st.columns(2)
        col6.plotly_chart(ptd)
        col7.plotly_chart(oil_GOR)
    with st.expander(label='Flow Rate Charts'):
        col8, col9 = st.columns(2)
        col8.plotly_chart(gas_oil)
        col9.plotly_chart(oil_water_cum)
    st.markdown(f'*Available Data: {df_lst.shape[0]}')



