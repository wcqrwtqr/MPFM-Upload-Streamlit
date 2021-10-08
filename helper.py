import pandas as pd
import streamlit as st
import numpy as np
from graphing import graphing_line_2v, graphing_line_1v, graphing_line_3v, graphing_line_4v, apply_Graphs




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
        NN = st.selectbox('Interval', [1, 2, 5, 10, 15, 20, 30, 50])
        st.dataframe(df_lst.loc[::int(NN)])
        st.markdown(f'*Available Data: {df_lst.loc[::int(NN)].shape[0]}')
        st.download_button(label='Download data', data=df_lst.loc[::int(NN)].to_csv(), mime='text/csv')
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
        NN = st.selectbox('Interval', [1, 2, 5, 10, 15, 20, 30, 50])
        st.dataframe(df_lst.loc[::int(NN)])
        st.markdown(f'*Available Data: {df_lst.loc[::int(NN)].shape[0]}')
        st.download_button(label='Download data', data=df_lst.loc[::int(NN)].to_csv(), mime='text/csv')
        # st.dataframe(df_lst)
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
    header_list = df.columns.tolist()
    range_data_selection = st.slider('Range:', min_value=min(range_data),
                                     max_value=max(range_data),
                                     value=(min(range_data), max(range_data)))
    # Creating the masked df from the index
    # df_header = st.multiselect('Data Columns', header_list, default=header_list)
    df_header = st.sidebar.multiselect('Data Columns', header_list, default=header_list)
    df_lst = df[range_data_selection[0]:range_data_selection[1]]
    # used a another dataframe df_lst2 instead of using the same df_lst so the graph are not affected when using the multi select (df_header) which will affect the rest of the graphs
    df_lst2 = df_lst[df_header]

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

    st.markdown(f'*Available Data: {df_lst2.shape[0]}')
    gas_rate_float = "{:.4f}".format(avg_std_gasRate)
    # st.subheader(f'Data Summary : Oil rate _{int(avg_oilRate)}_ / __Gas rate__ _{gas_rate_float}_ / GOR _{int(avg_GOR)}_')
    st.markdown(f'Data Summary : Oil rate __*{int(avg_oilRate)}*__ / Gas rate __{gas_rate_float}__ / GOR __{int(avg_GOR)}__')
    # st.write('---')
    # Making the graphs
    with st.expander(label='Parameters Charts'):
        col6, col7 = st.columns(2)
        col6.plotly_chart(ptd)
        col7.plotly_chart(oil_GOR)


    # Drawing the graphs
    with st.expander(label='Data Set'):
        NN = st.selectbox('Interval', [1, 5, 10, 15, 20, 30, 60, 120])
        st.dataframe(df_lst2.loc[::int(NN)])
        st.markdown(f'*Available Data: {df_lst2.loc[::int(NN)].shape[0]}')
        st.download_button(label='Download data', data=df_lst2.loc[::int(NN)].to_csv(), mime='text/csv')
    with st.expander(label='Summary table'):
        st.markdown('Average Table')
        st.dataframe(summary)
        st.download_button(label='Download Summary', data=summary.to_csv(), mime='text/csv')
    # st.write('---')

    with st.expander(label='Custom Graph'):
        SS = st.multiselect('Select up to 4 Headers', header_list[2:])
        apply_Graphs(SS,df_lst,header_list)

    with st.expander(label='Custom Graph 2'):
        com = st.multiselect('Select headers',header_list[2:])
        apply_Graphs(com,df_lst,header_list)




