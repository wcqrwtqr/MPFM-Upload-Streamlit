import streamlit as st
import os
from helper import Gauges_data, MPFM_data, Gauges_data_Spartek, daq_data
from PIL import Image
from simulation import Loadingtruck, setup
import simpy
from air_oil_ratio import calculate_the_values_of_air
import plotly.express as px
from pvtcorrelation import *
from wellanalysis import *
import pandas as pd


def main():
    "Main function of the page"
    st.set_page_config(page_title="MPFM and Gauges", layout="wide")
    values = [
        "Main Page",
        "MPFM Upload",
        "Metrolog Gauges Upload",
        "Spartek Gauges Upload",
        "Well Test Analysis",
        "PVT-Correlation",
        "Loading Simulation",
        "Air-Oil Ratio",
        # "DAQ Upload",
        # "File Name",
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


    # ============================================================
    # ====================PVT corrleation==============
    # ============================================================
    # added air compressor calculcaiton
    if window_ANTICOR == "PVT-Correlation":
        st.title("PVT correlation")
        st.markdown(
            """
            This page is used to calculate the PVT parametes
            The calculations are computed based on the script done by

            https://github.com/yohanesnuwara/pyreservoir repositry

            Please visit his page and star his work
        """
        )
        # with st.expander(label="Usage guidelines"):
        #     st.info(
        #         """ To get the OIL parameters
        #         Paramters:
        #         1- xxxx
        #         2- xxxx
        #         3- xxxx
        #         """
        #     )

        with st.expander(label="OIL PVT"):
            with st.form(key="file_form"):
                col1, col2, col3, col4 = st.columns(4)
                sg_val = col1.number_input(label="SG", step=0.10, value=0.75)
                temp_val = col2.number_input(label="Temperature F", step=5, value=150)
                Rsb_val = col3.number_input(label="Solution GOR", step=10, value=300)
                API_val = 141.5 / (sg_val) - 131.5
                press_val = col4.number_input(label="Pressure psi", step=10, value=300)
                submit = st.form_submit_button(label="Submit")

                if submit:
                    # calculate bubble-point pressure using Vasquez and Beggs (1980)
                    pbubble = oil_pbubble(Rsb_val, sg_val ,API_val, temp_val)
                    # calculate isothermal compressibility using Vazquez and Beggs (1980); McCain et al (1988)
                    coil = oil_compressibility(press_val, pbubble, temp_val, API_val, Rsb_val, sg_val)
                    # calculate FVF using Vazquez and Beggs (1980); Levitan and Murtha (1999)
                    Bo = oil_fvf(pbubble, API_val, Rsb_val, sg_val, temp_val, press_val)
                    # calculate gas-oil ratio using Vazquez and Beggs (1980)
                    Rs = gasoilratio(press_val, pbubble, sg_val, API_val, temp_val, Rsb_val)
                    # calculate gas-oil ratio using Vazquez and Beggs (1980); Beggs and Robinson (1975)
                    viscooil = oil_mu(press_val, pbubble, sg_val, API_val, temp_val, Rs)
                    col1, col2 = st.columns(2)
                    col1.subheader('Your Input:')
                    col1.write('Pressure                     : {} psia'.format(press_val))
                    col1.write('Temperature                  : {} °F'.format(temp_val))
                    col1.write('Specific Gravity             : {}'.format(sg_val))
                    col1.write('Gas-oil ratio @ Bubble-point : {} scf/STB'.format(Rsb_val))
                    col1.write('Oil gravity                  : {:.2f} API \n'.format(API_val))

                    col2.subheader('PVT Output:')
                    col2.write('Bubble-point Pressure        : {:.2f} psi'.format(pbubble))
                    col2.write('Gas-oil ratio                : {:.2f} scf/STB'.format(Rs))
                    col2.write('FVF                          : {:.2f} RB/STB'.format(Bo))
                    col2.write('Isothermal compressibility   : {:.2f} microsip'.format(coil * 1E+6))
                    col2.write('Viscosity                    : {:.3f} cp'.format(viscooil))

        with st.expander(label="Gas PVT"):
            with st.form(key="file_form_gas"):
                col1, col2, col3, col4, col5 = st.columns(5)
                press_val = col1.number_input(label="Pressure psi", step=10, value=2000)
                temp_val = col2.number_input(label="Temperature F", step=5, value=110)
                sg_val = col3.number_input(label="SG", step=0.10, value=0.7)
                h2s_val = col4.number_input(label="HS %", step=0.01, value=0.07)
                co2_val = col5.number_input(label="Co2 %", step=0.01, value=0.07)
                submit = st.form_submit_button(label="Submit")

                if submit:
                    # calculate pseudoproperties using Sutton (1985), Wichert and Aziz (1972)
                    P_pc, T_pc, P_pr, T_pr = gas_pseudoprops(temp_val, press_val, sg_val, h2s_val, co2_val)

                    # calculate z-factor using Dranchuk-Aboukassem (1975)
                    pseudo_rho, z_factor = gas_zfactor(T_pr, P_pr)

                    # calculate density
                    rhogas = gas_density(temp_val, press_val, sg_val, z_factor)

                    # calculate gas FVF
                    Bg = gas_fvf(z_factor, temp_val, press_val)

                    # calculate isothermal compressibility using Trube (1957) and Mattar (1975)
                    cgas = gas_compressibility(T_pr, P_pr, pseudo_rho, z_factor, P_pc)

                    # calculate viscosity using Lee et al (1966)
                    viscogas = gas_mu(temp_val, rhogas, sg_val)

                    col1, col2 = st.columns(2)
                    col1.subheader('Your Input:')
                    col1.write('Pressure                   : {} psia'.format(press_val))
                    col1.write('Temperature                : {} °F'.format(temp_val))
                    col1.write('Specific Gravity           : {:.2f}'.format(sg_val))
                    col1.write('H2S Mole Fraction          : {}'.format(h2s_val))
                    col1.write('CO2 Mole Fraction          : {} \n'.format(co2_val))

                    col2.subheader('PVT Output:')
                    col2.write('z-factor                   : {:.4f}'.format(z_factor))
                    col2.write('Density                    : {:.2f} lb/ft3'.format(rhogas))
                    col2.write('FVF                        : {:.3f} res ft3/scf'.format(Bg))
                    col2.write('Isothermal compressibility : {:.3f} microsip'.format(cgas * 1E+6))
                    col2.write('Viscosity                  : {:.4f} cp'.format(viscogas))


        with st.expander(label="Water PVT"):
            with st.form(key="file_form_water"):
                col1, col2, col3, col4, col5 = st.columns(5)
                press_val = col1.number_input(label="Pressure psi", step=10, value=2000)
                temp_val = col2.number_input(label="Temperature F", step=5, value=110)
                s_val = col3.number_input(label="Salinity, wt%", step=1, value=5)
                submit = st.form_submit_button(label="Submit")

                if submit:
                    # calculate water FVF using McCain et al (1989)
                    Bw = water_fvf(temp_val, press_val)

                    # calculate vapor (bubble-point) press_val using the classic Antoine (1888)
                    pbubble = water_pbubble(temp_val)

                    # calculate isothermal water compressibility using Osif (1988) and McCain (1989)
                    cw = water_compressibility(temp_val, press_val, s_val, Bw)

                    # calculate water viscosity using McCain (1989)
                    mu_w = water_mu(temp_val, press_val, s_val)

                    col1, col2 = st.columns(2)
                    col1.subheader('Your Input:')
                    col1.write('Pressure                     : {} psia'.format(press_val))
                    col1.write('Temperature                  : {} °F'.format(temp_val))
                    col1.write('Salinity                     : {} \n'.format(s_val / 100))

                    col2.subheader('PVT Output:')
                    col2.write('FVF                          : {:.4f} RB/STB'.format(Bw))
                    col2.write('Bubble-Point Press_val        : {:.3f} psia'.format(pbubble))
                    col2.write('Isothermal Compressibility   : {:.4f} microsip'.format(cw * 1E+6))
                    col2.write('Viscosity                    : {:.4f} cp'.format(mu_w))

    # ============================================================
    # ====================Well Test Analysis==============
    # ============================================================
    #
    if window_ANTICOR == "Well Test Analysis":
        st.title("Well Test Analysis")
        st.markdown(
            """
            This page is used to form well test analysis
            The calculations are computed based on the script done by

            https://github.com/yohanesnuwara/pyreservoir repositry

            Please visit his page and star his work
        """
        )

        with st.expander(label="Constant Rate Drawdown Test"):
            with st.form(key="file_form_analysis"):
                col1, col2, col3= st.columns(3)
                poro = col1.number_input(label="Porosity", step=0.10, value=0.15) # Porosity
                rw =col1.number_input(label="Wellbore Radius ft", step=0.10, value=0.333)  # Wellbore radius, ft
                h = col2.number_input(label="Reservoir thickness ft", step=1, value=32) # Reservoir thickness, ft
                # ct = col2.number_input(label="Total Compressibilitym, sip", step=0.10, value=12E-06)  # Total compressibility, sip
                ct = col2.number_input(label="Total Compressibilitym, sip",step=0.00001, value=0.000012)  # Total compressibility, sip
                mu_oil = col3.number_input(label="Oil viscosity, cp", step=1, value=2)  # Total compressibility, sip
                pi = col2.number_input(label="Reservoir Inital Pressure, psi", value=2500) # Initial reservoir pressure, psia
                Bo =col1.number_input(label="Oil FVF, RB/STB", value=0.133) # Oil FVF, RB/STB
                q = col3.number_input(label="well rate", value=1000)
                your_guess =  col3.number_input(label="guess time index", value=30)
                source_data = st.file_uploader(
                    label="Upload drawdown file", type=["csv", "log", "txt"]
                )
                st.write("---")
                submit = st.form_submit_button(label="Submit")

                if submit:
                    # load well-test data
                    try:
                        df = pd.read_csv(source_data, sep=",")
                        t = df['t'].values
                        p = df['p'].values
                        # I modified the function below to return the st.pyplot(fig) and draw a graph
                        constant_rate_drawdown_test(t, p, q, Bo, mu_oil, h, poro, ct, rw, pi, your_guess)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the MPFM")



if __name__ == "__main__":
    main()
