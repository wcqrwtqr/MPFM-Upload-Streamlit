import streamlit as st
import os
from helper import Gauges_data, MPFM_data, Gauges_data_Spartek, daq_data
from PIL import Image
from simulation import Loadingtruck, setup
import simpy
from air_oil_ratio import calculate_the_values_of_air
import plotly.express as px



def main():
    "Main function of the page"
    st.set_page_config(page_title="MPFM and Gauges", layout="wide")
    values = [
        "Main Page",
        "MPFM Upload",
        "Metrolog Gauges Upload",
        "Spartek Gauges Upload",
        "DAQ Upload",
        "Loading Simulation",
        # "File Name",
        "Air-Oil Ratio",
    ]
    default_ix = values.index("Main Page")
    window_ANTICOR = st.sidebar.selectbox("Selection Window", values, index=default_ix)
    package_dir = os.path.dirname(os.path.abspath(__file__))

    # ============================================================
    # ====================Start Up Page===========================
    # ============================================================
    if window_ANTICOR == "Main Page":
        st.title("MPFM, MEMORY GAUGES & Simulation")
        st.subheader("👈🏼 Select service from menu bar")
        st.subheader("About the web site:")
        st.markdown(
            """
                    Upload row data from the MPFM ROXAR unit or from the Down hole memory gauges or csv files from the DAQ system and get
                    an instant graph and data set based on your requirements.\n
                    You can generate graphs and adjust it to the duration you desire and calculate the average values of the selected fields
                    then download it to csv.\n
                    The gauges used in our company are either __Metrolog__ or __Spartek__ and I made two sheets which can serve both conditions.\n
                    Also there is one page for simulating the loading of oil to trucks using loading stations which is a simple tool that 
                    can be used to get the total number of trucks by changing the variables such as:\n
                    - Number of loading stations.
                    - Number of trucks provided at a given time.
                    - Filling time.
                    - etc.
                    """
        )
        st.write("---")
        st.write(
            "Feel free to follow me in my YouTube channel for more video on data processing"
        )
        image = Image.open(os.path.join(package_dir, "Thumbnail/youtube.jpg"))
        st.image(image, caption="youtube channel")

    # ============================================================
    # ====================Spartek  Gauges=========================
    # ============================================================
    # Gauges Spartek
    if window_ANTICOR == "Spartek Gauges Upload":
        st.title("Down Hole Gauges _Spartek_ 🌡")
        st.markdown(
            """
                    The below is to manipulate __SPARTEK__ Down Hole Memory Gauges row data\n
                    The page can view the data, download the values after applying a reduction factor to excel
                    """
        )
        with st.expander(label="Upload row data guidelines"):
            st.warning(
                "Ensure the txt file belongs to Spartek gauges and has the format as below"
            )
            image = Image.open(os.path.join(package_dir, "Thumbnail/spartek.jpg"))
            st.image(image)
        source_data = st.file_uploader(
            label="Uplaod gauges data to web page", type=["csv", "log", "txt"]
        )
        st.write("---")
        try:
            Gauges_data_Spartek(source_data)
            col1, col2 = st.columns(2)
        except Exception:
            st.subheader("No Data available!!")
            st.write("Select correct data for Metrolog gauges")

    # ============================================================
    # ====================Metrolog Gauges=========================
    # ============================================================
    # Gauges Metrolg
    if window_ANTICOR == "Metrolog Gauges Upload":
        st.title("Down Hole Gauges _Metrolog_ 🌡")
        st.markdown(
            """
                    The below is to manipulate __METROLOG__ Down Hole Memory Gauges row data\n
                    The page can view the data, download the values after applying a reduction factor to excel
                    """
        )
        source_data = st.file_uploader(
            label="Uplaod gauges data to web page", type=["csv", "log", "txt"]
        )
        st.write("---")
        try:
            Gauges_data(source_data)
            col1, col2 = st.columns(2)
        except Exception:
            st.subheader("No Data available!!")
            st.write("Select correct data for Spartek gauges")

    # ============================================================
    # ====================MPFM Upload files=======================
    # ============================================================
    # MPFM Upload
    if window_ANTICOR == "MPFM Upload":
        st.title("Multi-phase Meter Data 🔬")
        st.markdown(
            """
                    The below is to view and the multi phase meter of type __ROXAR__ online \n
                    The page can view the data, download the summary values to excel and
                    graph the data using a custom graph up to 4 values.
                    """
        )
        source_data = st.file_uploader(
            label="Uplaod MPFM data to web page", type=["csv", "log", "txt"]
        )
        st.write("---")
        try:
            MPFM_data(source_data)
            col1, col2 = st.columns(2)
        except Exception:
            st.subheader("No data selected")
            st.write("Select the correct data for the MPFM")

    # ============================================================
    # ==================DATA Acquisition System===================
    # ============================================================
    # DAQ Upload
    if window_ANTICOR == "DAQ Upload":
        st.title("DAQ Data Acquisition System 💽")
        st.markdown(
            """
                    The below page is to view the Data Acquisition system of type __FEKETE__ or __FIELD NOTE__ online \n
                    The page can view the data, download the summary values to excel and graph the data using a custom graph up to 4 values
                    """
        )
        with st.expander(label="Upload row data guidelines"):
            st.warning(
                "Ensure the csv file has only one header and date start with yyy-mm-dd format"
            )
            image = Image.open(os.path.join(package_dir, "Thumbnail/DAQ data.jpg"))
            st.image(image)

        source_data = st.file_uploader(
            label="Uplaod MPFM data to web page", type=["csv", "log", "txt"]
        )
        st.write("---")
        try:
            daq_data(source_data)
        except Exception:
            st.subheader("No data selected")
            st.write("Select the correct data for the MPFM")

    # ============================================================
    # ===================Stimulation trucks=======================
    # ============================================================
    # Simulation of loading trucks
    if window_ANTICOR == "Loading Simulation":
        st.title("Trucks Loading Simulation 🚚")
        st.markdown(
            """
                    The below is to __simulate__ the number of trucks that can be loaded in a loading station \n
                    The input below is used to change the simulation variables and see the final results below
                    """
        )
        with st.expander(label="Usage guidelines"):
            st.info(
                """Choose the number of __loading stations__, __time to fill__ each
                    truck, __number of trucks__ provided at a certain time
                    and see the number of trucks that can be
                    filled in the at a duration

                Paramters:
                1- Number of loading stations
                2- Time of filling duration (in minutes)
                3- Number of trucks provided at any given time
                4- Loading duration (12 or 24 hours)
                    """
            )

        with st.form(key="simulation_form"):
            col1, col2, col3, col4 = st.columns(4)
            no_stations = int(col1.number_input("loading stations", 1))
            loading_time = int(col2.number_input("Loading time in minutes", 30, step=5))
            no_trucks = int(col3.number_input("No of trucks", 1))
            duration = int(col4.selectbox("Loading time in hours", [12, 24]))
            submit = st.form_submit_button(label="Submit")
            if submit:
                env = simpy.Environment()
                env.process(setup(env, no_stations, loading_time, 10, no_trucks))
                env.run(until=duration*60)

    if window_ANTICOR == "File Name":
        st.title("Name files for operation")
        st.markdown(
            """
        This page is to get a new file name for the different documents generated
        while doing operation in well testing such as Final report name convention,
        Down hole gauges data, final report for SWT, DST, SLS etc.
                    """
        )

        with st.form(key="file_form"):
            col1, col2, col3, col4 = st.columns(4)
            bu = col1.text_input(label="BU")
            bl = col2.text_input(label="BL")
            date_start = col3.date_input("Start date")
            date_end = col4.date_input("End date")
            client_name = col1.text_input(label="Clinet name")
            well_name = col2.text_input(label="Well name")
            job_id = col3.text_input(label="Job ID")
            service_desc = col4.text_input(label="Service")
            zone_desc = col1.text_input(label="Zone/DST")
            submit = st.form_submit_button(label="Submit")

            if submit:
                st.subheader("With job ID")
                st.write(
                    f'Final Report Format with ID : **"{job_id} {client_name} {well_name} {zone_desc} final report from {date_start} to {date_end}"**'
                )
                st.write(
                    f'Gauges Final Report Format : **"{job_id} {client_name} {well_name} {zone_desc} down hole gauges report from {date_start} to {date_end}"**'
                )
                st.write("---")
                st.subheader("Without job ID")
                st.write(
                    f'Final Report Format : **"{client_name} {well_name} {zone_desc} final report from {date_start} to {date_end}"**'
                )
                st.write(
                    f'Gauges Final Report Format : **"{client_name} {well_name} {zone_desc} down hole gauges report from {date_start} to {date_end}"**'
                )

    # ============================================================
    # ====================Air Compressor Calculation==============
    # ============================================================
    # added air compressor calculcaiton
    if window_ANTICOR == "Air-Oil Ratio":
        st.title("Air-oil Ratio Calcuator 🔥")
        st.markdown(
            """
        This page is didcated to calcualte the percentage of the air to oil ratio to get
            the best air compressors capacity for the most efficient burning

        Ensure to get the rate between 10% and 20% to have a good burning
        """
        )
        with st.expander(label="Usage guidelines"):
            st.info(
                """ To get the air oil ratio update the following parameters

                Paramters:
                1- Update the API
                2- Oil rate in bbl per day BBL/d
                3- Air rate in Cubic Feet Minute CFM
                """
            )

        with st.form(key="file_form"):
            col1, col2, col3 = st.columns(3)
            API_val = col1.number_input(label="API", step=0.5, value=25.5)
            oil_rate = col2.number_input(label="Oil Rate", step=100, value=2500)
            air_rate = col3.number_input(label="Air Rate", step=100, value=200)
            submit = st.form_submit_button(label="Submit")

            if submit:
                y = []
                xy = []
                lis_x = [
                    100,
                    300,
                    500,
                    600,
                    700,
                    800,
                    900,
                    1000,
                    1200,
                    1500,
                    1800,
                    2000,
                    2300,
                    2500,
                    2700,
                    3000,
                ]

                for rate in range(len(lis_x)):
                    new_air_rate = air_rate + lis_x[rate]
                    x = calculate_the_values_of_air(API_val, new_air_rate, oil_rate)
                    y.append(x)
                    xy.append(new_air_rate)

                fig = px.scatter(x=xy, y=y, title='Air oil Ratio for optimum burning' )
                # fig.add_hrect(y0=10, y1=20, line_width=0, fillcolor='green', opacity=0.2)
                st.plotly_chart(fig)




if __name__ == "__main__":
    main()
