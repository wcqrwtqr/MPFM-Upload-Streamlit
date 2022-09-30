import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from graphing import graphing_line_arg


def Gauges_data_Spartek(source_file, row=20):
    """Gauges_data_Spartek.

    Parameters
    ----------
    source_file :
        source_file
    row :
        row
    """
    """Gauges_data_Spartek.

    Parameters
    ----------
    source_file :
        source_file
    row :
        row
    """
    df = pd.read_csv(
        source_file,
        sep="\s+",
        header=None,
        skiprows=row,
        # names=["date", "time", "AMPM", "elpse", "pressure", "temperature"],
        names=["date", "time", "AMPM", "elpse", "pressure", "temperature"],
        engine="python",
    )
    range_data = df.index.tolist()
    df["date_time"] = df["date"] + " " + df["time"] + " " + df["AMPM"]
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0] : range_data_selection[1]]

    # Showing the graphs
    st.markdown(
        f'Max __Temperature__: {df_lst["temperature"].max()} - Max __Pressure__: {df_lst["pressure"].max()}'
    )
    st.markdown(f"*Available Data: {df_lst.shape[0]}")
    # st.markdown('Pressure Temperature Graph')

    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 15, 20, 30, 50])
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="text/csv"
        )
    with st.expander(label="Gauges Chart"):
        graphing_line_arg(df_lst, "date_time", st, ["pressure", "temperature"])


# ********************************************************************
# *************** Gauges Function for Metrolg Gauges******************
# ********************************************************************
def Gauges_data(source_file, row=20):
    """Gauges data processing generator

    :param source_file: file path
    :type source_file: string
    :param row: number of rows
    :type row: int

    :returns: None
    :rtype: None"""

    df = pd.read_csv(
        source_file,
        sep="[,\t]",
        header=None,
        skiprows=row,
        names=["date", "time", "pressure", "temperature"],
        engine="python",
    )
    range_data = df.index.tolist()
    df["date_time"] = df["date"] + " " + df["time"]
    # df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%y %H:%M:%S') ## new added
    # df['date_time']=pd.to_datetime(df['date'] + ' ' + df['time'], dayfirst=False)
    # position = df.columns.get_loc('time')
    # df['elapsed'] =  df.iloc[1:, position] - df.iat[0, position]

    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    # Creating the masked df from the index
    df_lst = df[range_data_selection[0] : range_data_selection[1]]
    # Showing the graphs
    st.markdown(
        f'Max __Temperature__: {df_lst["temperature"].max()} - Max __Pressure__: {df_lst["pressure"].max()}'
    )
    st.markdown(f"*Available Data: {df_lst.shape[0]}")

    with st.expander(label="Table of Data"):
        NN = st.selectbox("Interval", [1, 2, 5, 10, 15, 20, 30, 50])
        st.dataframe(df_lst.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data", data=df_lst.loc[:: int(NN)].to_csv(), mime="text/csv"
        )
    with st.expander(label="Gauges Chart"):
        # graphing the values of time, pressure and temperature using the function
        graphing_line_arg(df_lst, "date_time", st, ["pressure", "temperature"])


# ********************************************************************
# ************** MPFM Function ***************************************
# ********************************************************************


def MPFM_data(source_file):
    """MPFM data processing generator

    :param source_file: file path
    :type source_file: string

    :returns: None
    :rtype: None"""

    df = pd.read_csv(source_file, sep="\t")
    df.dropna(inplace=True, axis=1)
    # Masking
    range_data = df.index.tolist()
    # Create a new column combining the date and time
    df["date_time"] = df["Date"] + " " + df["Clock"]
    header_list = df.columns.tolist()
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )
    # Creating the masked df from the index
    df_header = st.sidebar.multiselect(
        "Data Columns", header_list, default=header_list[:-12]
    )
    df_lst = df[range_data_selection[0] : range_data_selection[1]]
    # used a another dataframe df_lst2 instead of using the same df_lst so the
    # graph are not affected when using the multi select (df_header) which will
    # affect the rest of the graphs
    df_lst2 = df_lst[df_header]

    # Averages calculation
    avg_P = np.average(df_lst["Pressure"])
    avg_T = np.average(df_lst["Temperature"])
    avg_dP = np.average(df_lst["dP"])
    avg_oilRate = np.average(df_lst["Std.OilFlowrate"])
    avg_waterRate = np.average(df_lst["WaterFlowrate"])
    avg_std_gasRate = np.average(df_lst["Std.GasFlowrate"])
    avg_act_gasRate = np.average(df_lst["Act.GasFlowrate"])
    avg_GOR = np.average(df_lst["GOR(std)"])
    avg_WC = np.average(df_lst["Std.Watercut"])
    avg_oilSG = np.average(df_lst["OilDensity"])
    avg_waterSG = np.average(df_lst["WaterDensity"])
    avg_gasSG = np.average(df_lst["GasDensity"])
    avg_liquid = avg_oilRate + avg_waterRate
    API = 141.5 / (avg_oilSG / 1000) - 131.5
    # start           = df_lst['Clock'][range_data_selection[0]] + ' ' + df_lst['Date'][range_data_selection[0]]
    # end             = df_lst['Clock'][range_data_selection[1]-1] + ' ' + df_lst['Date'][range_data_selection[1]-1]
    start = (
        df_lst["date_time"][range_data_selection[0]]
        + " "
        + df_lst["Date"][range_data_selection[0]]
    )
    end = (
        df_lst["date_time"][range_data_selection[1] - 1]
        + " "
        + df_lst["Date"][range_data_selection[1] - 1]
    )
    # Making the dataframe
    dict_summary = {
        "Start Time": start,
        "End Time": end,
        "WHP": avg_P,
        "WHT": avg_T,
        "Diff dP": avg_dP,
        "Oil Rate": avg_oilRate,
        "Water Rate": avg_waterRate,
        "Liquid Rate": avg_liquid,
        "Gas Rate": avg_std_gasRate,
        "Actual Gas Rate": avg_act_gasRate,
        "Total GOR": avg_GOR,
        "Gas SG": avg_gasSG,
        "Oil SG": avg_oilSG,
        "Oil API": API,
        "BSW": avg_WC,
        "Water SG": avg_waterSG,
    }
    summary = pd.DataFrame([dict_summary])

    st.markdown(f"*Available Data: {df_lst2.shape[0]}")
    gas_rate_float = "{:.4f}".format(avg_std_gasRate)
    st.markdown(
        f"Data Average Values : Oil rate __*{int(avg_oilRate)}*__ / Gas rate __{gas_rate_float}__ / GOR __{int(avg_GOR)}__"
    )
    st.markdown(
        f'Data Max Values : Oil rate __{int(df_lst["Std.OilFlowrate"].max())}__ / Gas rate __{df_lst["Std.GasFlowrate"].max()}__ / GOR __{int(df_lst["GOR(std)"].max())}__'
    )
    # Making the graphs
    with st.expander(label="Parameters Charts"):
        col6, col7 = st.columns(2)
        graphing_line_arg(df_lst, "date_time", col6, ["Pressure", "dP"])
        graphing_line_arg(df_lst, "date_time", col7, ["Std.OilFlowrate", "GOR(std)"])

    # making the average table along with a graph
    with st.expander(label="Average table"):
        # Select the columns that we need to see the average and graph for it
        avg_selection = st.multiselect("select header", header_list[2:-1])
        col6, col8, col7 = st.columns(3)
        if avg_selection != []:
            col6.write("Average table 👇🏼")
            col7.write("Graph here 👇🏼")
        col6.dataframe(df_lst[avg_selection].mean())
        graphing_line_arg(df_lst, "date_time", col7, avg_selection)
        st.download_button(
            "Download Average table",
            data=df_lst[avg_selection].mean().to_csv(),
            mime="text/csv",
        )

    # Showing the data set with the needed columns
    with st.expander(label="Data Set"):
        NN = st.selectbox("Interval", [1, 5, 10, 15, 20, 30])
        st.write("👈🏼 Add/Remove from the sidebar list")
        st.dataframe(df_lst2.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst2.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data",
            data=df_lst2.loc[:: int(NN)].to_csv(),
            mime="text/csv",
        )
    with st.expander(label="Summary table"):
        st.markdown("Average Table")
        st.dataframe(summary)
        st.download_button(
            label="Download Summary", data=summary.to_csv(), mime="text/csv"
        )

    with st.expander(label="Custom Graph"):
        SS = st.multiselect("Select Headers", header_list[2:-2])
        graphing_line_arg(df_lst, "date_time", st, SS)

    with st.expander(label="Custom Graph 2"):
        com = st.multiselect("Select headers", header_list[2:-2])
        graphing_line_arg(df_lst, "date_time", st, com)

    with st.expander(label="Correlation"):
        selector = st.multiselect("select one", header_list[2:-2])
        cmp = st.selectbox(
            "select one",
            ["coolwarm", "BuPu", "coolwarm_r", "magma", "magma_r", "tab10"],
        )
        fig, ax = plt.subplots()
        ax = sns.heatmap(df_lst[selector].corr(), cmap=cmp, annot=True)
        st.pyplot(fig)
        st.plotly_chart(fig)


# ********************************************************************
# ************** DAQ Function ***************************************
# ********************************************************************


def daq_data(source_file):
    """DAQ data processing generator

    :param source_file: file path
    :type source_file: string

    :returns: None
    :rtype: None"""

    df = pd.read_csv(source_file)
    df.dropna(inplace=True, axis=1)
    df["date_time"] = df["Date"] + " " + df["Time"]
    # Masking
    range_data = df.index.tolist()
    header_list = df.columns.tolist()
    range_data_selection = st.slider(
        "Range:",
        min_value=min(range_data),
        max_value=max(range_data),
        value=(min(range_data), max(range_data)),
    )

    # Creating the masked df from the index
    df_header = st.sidebar.multiselect("Data Columns", header_list, default=header_list)
    df_lst = df[range_data_selection[0] : range_data_selection[1]]
    # used a another dataframe df_lst2 instead of using the same df_lst so the
    # graph are not affected when using the multi select (df_header) which will
    # affect the rest of the graphs
    df_lst2 = df_lst[df_header]
    st.markdown(f"*Available Data: {df_lst2.shape[0]}")

    # making the average table along with a graph
    with st.expander(label="Average table"):
        # Select the columns that we need to see the average and graph for it
        avg_selection = st.multiselect("select header", header_list[2:-1])
        col6, col7 = st.columns(2)
        if avg_selection != []:
            col6.write("Average table 👇🏼")
            col7.write("Graph here 👇🏼")
        col6.dataframe(df_lst[avg_selection].mean())
        graphing_line_arg(df_lst, "date_time", col7, avg_selection)
        st.download_button(
            "Download Average table",
            data=df_lst[avg_selection].mean().to_csv(),
            mime="text/csv",
        )

    # Showing the Data set and removing any unwanted columns
    with st.expander(label="Data Set"):
        # Select the interval that will reduce the number of rows
        NN = st.selectbox("Interval", [1, 5, 10, 15, 20, 30, 60, 120])
        st.write("👈🏼 Add/Remove from the sidebar list")
        st.dataframe(df_lst2.loc[:: int(NN)])
        st.markdown(f"*Available Data: {df_lst2.loc[::int(NN)].shape[0]}")
        st.download_button(
            label="Download data",
            data=df_lst2.loc[:: int(NN)].to_csv(),
            mime="text/csv",
        )

    # Custom graph 1
    with st.expander(label="Custom Graph"):
        col4, col5 = st.columns(2)
        SS = st.multiselect("Select Headers", header_list[2:-2])
        graphing_line_arg(df_lst, "date_time", st, SS)

    # Custom graph 2
    with st.expander(label="Custom Graph 2"):
        com = st.multiselect("Select headers", header_list[2:])
        graphing_line_arg(df_lst, "date_time", st, com)
