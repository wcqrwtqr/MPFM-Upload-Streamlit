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
from nodalanalysis import *
from nodal import *
from separator_sizing import *
from pressuredrop import *

def main():
    "Main function of the page"
    st.set_page_config(page_title="MPFM and Gauges", layout="wide")
    values = [
        "Main Page",
        "MPFM Upload",
        "Metrolog Gauges Upload",
        "Spartek Gauges Upload",
        "Nodal Analysis",
        "PVT-Correlation",
        "Separator sizing",
        "Well Test Analysis",
        "Loading Simulation",
        "Air-Oil Ratio",
        "Pressure drop",
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
        st.title("Oil field tool kit - Reservoir Engineering, MPFM, Memory gauges & Simulation")
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
                    filled in the at a duration\n
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


    # ============================================================
    # ====================Air Compressor Calculation==============
    # ============================================================
    # added air compressor calculcaiton
    if window_ANTICOR == "Air-Oil Ratio":
        st.title("Air-oil Ratio Calcuator 🔥")
        st.markdown(
            """
        This page is didcated to calcualte the percentage of the air to oil ratio to get
            the best air compressors capacity for the most efficient burning\n
        Ensure to get the rate between 10% and 20% to have a good burning
        """
        )
        with st.expander(label="Usage guidelines"):
            st.info(
                """ To get the air oil ratio update the following parameters\n
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
                lis_x = [100, 300, 500, 600, 700, 800, 900,
                    1000, 1200, 1500, 1800, 2000, 2300, 2500,
                    2700, 3000,]
                for rate in range(len(lis_x)):
                    new_air_rate = air_rate + lis_x[rate]
                    x = calculate_the_values_of_air(API_val, new_air_rate, oil_rate)
                    y.append(x)
                    xy.append(new_air_rate)
                fig = px.scatter(x=xy, y=y, title='Air oil Ratio for optimum burning' )
                fig.add_hrect(y0=10, y1=20, line_width=0, fillcolor='green', opacity=0.2)
                st.plotly_chart(fig)


    # ============================================================
    # ====================PVT corrleation==============
    # ============================================================
    if window_ANTICOR == "PVT-Correlation":
        st.title("PVT correlation")
        st.markdown(
            """
            This page is used to calculate the PVT parametes\n
            The calculations are computed based on the script done by https://github.com/yohanesnuwara/pyreservoir repositry\n
            Please visit his page and star his work
        """
        )

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
                    # col1, col2 = st.columns(2)
                    columns = ['Pressure (psi)', 'Temperature (°F)', 'Specific Gravity', 'Gas-oil ratio (scf/STB)','API','Bubble point (psi)','GOR (scf/STB)','FVF RB/STB', 'Isothermal Compressibility (microcip)', 'Viscosity (cp)']
                    df = pd.DataFrame(columns=columns)
                    df[columns[0]] = np.array([0])
                    df[columns[0]] = press_val
                    df[columns[1]] = temp_val
                    df[columns[2]] = sg_val
                    df[columns[3]] = Rsb_val
                    df[columns[4]] = API_val
                    df[columns[5]] = pbubble
                    df[columns[6]] = Rs
                    df[columns[7]] = Bo
                    df[columns[8]] = coil*1_000_000
                    df[columns[9]] = viscooil
                    st.dataframe(df)
                    st.markdown("""
                    * calculate bubble-point pressure using Vasquez and Beggs (1980)
                    * calculate isothermal compressibility using Vazquez and Beggs (1980); McCain et al (1988)
                    * calculate FVF using Vazquez and Beggs (1980); Levitan and Murtha (1999)
                    * calculate gas-oil ratio using Vazquez and Beggs (1980); Beggs and Robinson (1975)
                    """)

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
                    columns = ['Pressure (psi)', 'Temperature (°F)', 'Specific Gravity', 'z-factor', 'Density (lb/ft3)','FVF ft3/scf', 'Isothermal Compressibility (microcip)', 'Viscosity (cp)']
                    df = pd.DataFrame(columns=columns)
                    df[columns[0]] = np.array([0])
                    df[columns[0]] = press_val
                    df[columns[1]] = temp_val
                    df[columns[2]] = sg_val
                    df[columns[3]] = z_factor
                    df[columns[4]] = rhogas
                    df[columns[5]] = Bg
                    df[columns[6]] = cgas*1_000_000
                    df[columns[7]] = viscogas
                    st.dataframe(df)
                    st.markdown("""
                    * calculate pseudoproperties using Sutton (1985), Wichert and Aziz (1972)
                    * calculate z-factor using Dranchuk-Aboukassem (1975)
                    * calculate isothermal compressibility using Trube (1957) and Mattar (1975)
                    * calculate viscosity using Lee et al (1966)
                    """)

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
                    columns = ['Pressure (psi)', 'Temperature (°F)', 'Salinity', 'FVF (RB/STB)', 'Bubble-Point (psia)', 'Isothermal Compressibility (microcip)', 'Viscosity (cp)']
                    df = pd.DataFrame(columns=columns)
                    df[columns[0]] = np.array([0])
                    df[columns[0]] = press_val
                    df[columns[1]] = temp_val
                    df[columns[2]] = s_val
                    df[columns[3]] = Bw
                    df[columns[4]] = pbubble
                    df[columns[5]] = cw*1_000_000
                    df[columns[6]] = mu_w
                    st.dataframe(df)
                    st.markdown("""
                    * calculate water FVF using McCain et al (1989)
                    * calculate vapor (bubble-point) press_val using the classic Antoine (1888)
                    * calculate isothermal water compressibility using Osif (1988) and McCain (1989)
                    * calculate water viscosity using McCain (1989)
                    """)

    # ============================================================
    # ====================Well Test Analysis==============
    # ============================================================
    #
    if window_ANTICOR == "Well Test Analysis":
        st.title("Well Test Analysis")
        st.markdown(
            """
            This page is used to form well test analysis\n
            The calculations are computed based on the script done by https://github.com/yohanesnuwara/pyreservoir repositry\n
            please visit his page and star his work
        """)

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


    # ============================================================
    # ====================Nodal analysis==============
    # ============================================================
    if window_ANTICOR == "Nodal Analysis":
        st.title("Nodal Analysis IPR/VLR")
        st.markdown(
            """
            This page is for making nodal analysis acknowledgement for https://github.com/FreddyEcu-Ch/Oil-and-Gas-Resources Please visit his page and star his work
        """
        )

        ####################### IPR curve tab ################################
        with st.expander(label="Reservoir Inflow Behaviour - IPR Flow rates"):
            with st.form(key="file_form_nodalIPR"):
                col1, col2, col3 = st.columns(3)
                pr =col1.number_input(label="pr - Reservoir pressure (psia)", value=2900) #psi
                pb =col1.number_input(label="pb - Bubble point pressure (psia)", value=2500) #psi
                q_test =col2.number_input(label="q_test - Test oil flow rate (bpd)", value=1000) #bpd
                pwf_test =col2.number_input(label="pwf_test - Flowing bottom pressure of test (psia)", value=2000) #bpd
                method = col3.selectbox(
                    "select method",
                    ["Vogel", "IPR_compuesto", "Darcy"],)
                pwf_graph =np.array([4000, 3500, 3000, 2500, 1000, 0]) # TDOD make the streamlit
                pwf =col3.number_input(label="pwf - Flowing bottom pressure (psia)", value=1500) #np.array([4000, 3500, 3000, 2500, 1000, 0])
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    try:
                        col4, col5 = st.columns(2)
                        fig = IPR_curve_methods(q_test, pwf_test, pr, pwf_graph, pb, method)
                        x = aof(q_test, pwf_test, pr, pb)
                        PI = j(q_test, pwf_test, pr, pb)
                        q1 = qo_t(q_test, pwf_test,pr, pwf,pb)
                        q2 = qo_darcy(q_test, pwf_test, pr, pwf, pb)
                        q3 = qo_ipr_compuesto(q_test, pwf_test, pr, pwf, pb)
                        q4 = qo_vogel(q_test, pwf_test, pr, pwf, pb)
                        q5 = Qb(q_test, pwf_test, pr, pb, pb)
                        # Creating dataframe and putting all the values inside it
                        columns = ['AOF', 'PI', 'Qo', 'Qo_darcy', 'Qo_IPR', 'Qo_vogel', 'Qb_flow at bubble']
                        df = pd.DataFrame(columns=columns)
                        df[columns[0]] = np.array([0])
                        df[columns[0]] = x
                        df[columns[1]] = PI
                        df[columns[2]] = q1
                        df[columns[3]] = q2
                        df[columns[4]] = q3
                        df[columns[5]] = q4
                        df[columns[6]] = q5
                        st.dataframe(df)
                        st.write("---")
                        st.caption('Solving for rates 0 to 5000 with step of 1000 BBL/d')
                        st.pyplot(fig)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the MPFM")

        ####################### IPR with fluid propertry tab ################################
        with st.expander(label="Reservoir Inflow Behaviour - IPR Petrophysical and Fluid Properties"):
            with st.form(key="file_form_nodal"):
                col1, col2, col3 = st.columns(3)
                pr =col1.number_input(label="pr - Reservoir pressure (psia)", value=4000) #psi
                ko  =col1.number_input(label="Effective premeablity md", value=10)
                h  =col1.number_input(label="h Reservoir hieght ft", value=50)
                bo =col2.number_input(label="bo Formation volume factor rb/stb", value=1.2)
                uo =col2.number_input(label="uo Oil viscosity cp", value=1.2)
                re =col3.number_input(label="re Drainage radius ft", value=3000)
                rw =col3.number_input(label="rw Well radius ft", value=0.328)
                s  =col3.number_input(label="s Skin", value=0)
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    try:
                        q1 = j_darcy(ko, h, bo, uo, re, rw, s)
                        AOF = q1 * pr
                        st.subheader("Results for AOF and PI")
                        columns = ['AOF', 'PI']
                        df = pd.DataFrame(columns=columns)
                        df[columns[0]] = np.array([0])
                        df[columns[0]] = AOF
                        df[columns[1]] = q1
                        st.dataframe(df)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the MPFM")


        ####################### VLR tab ################################
        with st.expander(label="VLR"):
            with st.form(key="file_form_nodalp"):
                col1, col2, col3 = st.columns(3)
                THP = col1.number_input(label="THP - Pressure psi" , value=250 )#psia
                wc = col1.number_input(label="wc - water cut %" , value=0.75)
                sg_h2o = col1.number_input(label="SG" , value=1.04)
                API = col2.number_input(label="API" , value=30)
                Q = col2.number_input(label="Q - Flow rate bpd" , value=2500 )#bpd
                ID = col2.number_input(label="ID inch" , value=2.875 )#in
                tvd = col3.number_input(label="tvd - True vertical depth" , value=6000 )#ft
                md = col3.number_input(label="md - Measured depth" , value=6600 )#ft
                C = col3.number_input(label="C - Factor" , value=120)
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    try:
                        SG_Avg = sg_avg(API, wc, sg_h2o)
                        Gavg = gradient_avg(API, wc, sg_h2o)
                        Pg = Gavg * tvd
                        f = f_darcy(Q, ID, C)
                        Pf = f_darcy(Q, ID, C) * md * Gavg
                        po = THP + Pf + Pg
                        fig = vlp_curve(THP, API, wc, sg_h2o, md, tvd, ID, C)
                        # Creating dataframe and putting all the values inside it
                        columns = ['THP', 'SG avg', 'Gradient avg', 'Pressure due gravity', 'f friction', 'Pf Pressure due friction', 'Po Total Head']
                        df = pd.DataFrame(columns=columns)
                        df[columns[0]] = np.array([0])
                        df[columns[0]] = THP
                        df[columns[1]] = SG_Avg
                        df[columns[2]] = Gavg
                        df[columns[3]] = Pg
                        df[columns[4]] = f
                        df[columns[5]] = Pf
                        df[columns[6]] = po
                        st.dataframe(df)
                        st.pyplot(fig)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the MPFM")

        ####################### IPR vs VLP curve tab ################################
        with st.expander(label="IPR vs VLP"):
            with st.form(key="file_form_nodalvlp"):
                col1, col2 = st.columns(2)
                col1.subheader('IPR Data')
                pr =col1.number_input(label="pr - Reservoir pressure (psia)", value=4000) #psi
                pb =col1.number_input(label="pb - Bubble point pressure (psia)", value=3000) #psi
                pwf =col1.number_input(label="pwf - Flowing bottom pressure (psia)", value=4000) #np.array([4000, 3500, 3000, 2500, 1000, 0])
                q_test =col1.number_input(label="q_test - Test oil flow rate (bpd)", value=1500) #bpd
                pwf_test =col1.number_input(label="pwf_test - Flowing bottom pressure of test (psia)", value=2000) #bpd C = col1.number_input(label="C - Factor" , value=120)
                method = col1.selectbox(
                    "select method",
                    ["Vogel", "Darcy"],)
                col2.subheader('IPR Data')
                THP = col2.number_input(label="THP - Pressure psi" , value=250 )#psia
                sg_h2o = col2.number_input(label="SG" , value=1.04)
                wc = col2.number_input(label="wc - water cut %" , value=0.75)
                API = col2.number_input(label="API" , value=30)
                ID = col2.number_input(label="ID inch" , value=2.875 )#in
                md = col2.number_input(label="md - Measured depth" , value=6600 )#ft
                tvd = col2.number_input(label="tvd - True vertical depth" , value=6000 )#ft
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    try:
                        SG_Avg = sg_avg(API, wc, sg_h2o)
                        Gavg = gradient_avg(API, wc, sg_h2o)
                        Pg = Gavg * tvd
                        f = f_darcy(q_test, ID, C)
                        Pf = f_darcy(q_test, ID, C) * md * Gavg
                        x = aof(q_test, pwf_test, pr, pb)
                        PI = j(q_test, pwf_test, pr, pb)
                        po = THP + Pf + Pg
                        fig = IPR_vlp_curve(THP,API, wc, sg_h2o, md, tvd, ID, C, q_test, pwf_test,  pr, pb, method)
                        # Creating dataframe and putting all the values inside it
                        columns = ['THP', 'SG avg', 'Gradient avg', 'Pressure due gravity', 'f friction', 'Pf Pressure due friction', 'Po Total Head', 'AOF','PI']
                        df = pd.DataFrame(columns=columns)
                        df[columns[0]] = np.array([0])
                        df[columns[0]] = THP
                        df[columns[1]] = SG_Avg
                        df[columns[2]] = Gavg
                        df[columns[3]] = Pg
                        df[columns[4]] = f
                        df[columns[5]] = Pf
                        df[columns[6]] = po
                        df[columns[7]] = x
                        df[columns[8]] = PI
                        st.dataframe(df)
                        st.pyplot(fig)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the MPFM")

    # ============================================================
    # ====================Separator Sizing==============
    # ============================================================
    #
    if window_ANTICOR == "Separator sizing":
        st.title("Horizontal Three-Phase Separators")
        st.markdown(
            """
            This page is for sizing separator, many thanks to FreddyEcu-ch who made this happen by sharing his gihub repo\n
            https://github.com/FreddyEcu-Ch/Oil-and-Gas-Resources\n
            Please visit his page and star his work
        """
        )
        ####################### Separaotr beta chart ################################
        with st.expander(label="Separator Beta value"):
            image1 = Image.open(os.path.join(package_dir, "Thumbnail/beta.jpg"))
            st.image(image1, caption="Beta for seprator")
        with st.expander(label="Horizontal Three-Phase Separators"):
            with st.form(key="file_form_Hsizing"):
                image = Image.open(os.path.join(package_dir, "Thumbnail/threephase_separator.png"))
                st.image(image, caption="3 phase separator")
                st.subheader('Input parameters')
                st.write("---")
                col1, col2, col3, col4 = st.columns(4)
                qg =col1.number_input(label="Gas flow rate MMscfd", value=5 ) #MMscfd
                qo =col1.number_input(label="Oil flow rate bpd", value=5000 ) #bpd
                qw =col1.number_input(label="water flow rate bpd", value=3000 ) #bpd
                Api =col1.number_input(label="API", value=30)
                sg_gas =col2.number_input(label="Gas SG", value=0.6)
                sg_w =col2.number_input(label="Water SG", value=1.07)
                P =col2.number_input(label="Pressure psia", value=100 ) #psia
                T =col2.number_input(label="Temperatur F", value=90 ) #F
                Z =col3.number_input(label="Compress factor", value=0.99)
                uo =col3.number_input(label="Oil Viscosity cp", value=10 ) #cp
                uw= col3.number_input(label="Water viscosity cp", value=1)#cp
                ug =col3.number_input(label="Gas viscosity cp", value=0.013 ) #cp
                tro =col4.number_input(label="Retention time water min", value=10 ) #min
                trw =col4.number_input(label="Retention time oil  min", value=10 ) #min
                beta =col4.number_input(label="Beta Aw/A choose from graph", value=0.3 ) # from grpah
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    # load well-test data
                    try:
                        separator_trif_horizontal(qg, qo, qw, Api, sg_gas, sg_w, P, T, Z, uo , uw, ug, tro, trw, beta)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the Separator")

        ####################### Vertical 3 Phase Separator ##########################
        with st.expander(label="Vertical Three-Phase Separators"):
            with st.form(key="file_form_Vsizing"):
                image = Image.open(os.path.join(package_dir, "Thumbnail/vertical threephase_separator.png"))
                st.image(image, caption="Vertical 3 phase separator")
                st.subheader('Input parameters')
                st.write("---")
                # Data
                col1, col2, col3, col4 = st.columns(4)
                qg =col1.number_input(label="Gas flow rate MMscfd", value=5 ) #MMscfd
                qo =col1.number_input(label="Oil flow rate bpd", value=5000 ) #bpd
                qw =col1.number_input(label="water flow rate bpd", value=3000 ) #bpd
                Api =col1.number_input(label="API", value=30)
                sg_gas =col2.number_input(label="Gas SG", value=0.6)
                sg_w =col2.number_input(label="Water SG", value=1.07)
                P =col2.number_input(label="Pressure psia", value=100 ) #psia
                T =col2.number_input(label="Temperatur F", value=90 ) #F
                Z =col3.number_input(label="Compress factor", value=0.99)
                uo =col3.number_input(label="Oil Viscosity cp", value=10 ) #cp
                uw= col3.number_input(label="Water viscosity cp", value=1)#cp
                ug =col3.number_input(label="Gas viscosity cp", value=0.013 ) #cp
                tro =col4.number_input(label="Retention time water min", value=10 ) #min
                trw =col4.number_input(label="Retention time oil  min", value=10 ) #min
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    # load well-test data
                    try:
                        separator_trif_vertical(qg, qo, qw, Api, sg_gas, sg_w, P, T, Z, uo , uw, ug, tro, trw)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the Separtor")

        ####################### Horizontal 2 Phase Separator ##########################
        with st.expander(label="Horizontal Two-Phase Separators"):
            with st.form(key="file_form_H2sizing"):
                image = Image.open(os.path.join(package_dir, "Thumbnail/two_phase_separator.png"))
                st.image(image, caption="Horizontal 2 phase separator")
                st.subheader('Input parameters')
                st.write("---")
                # Data
                col1, col2, col3 = st.columns(3)
                qg =col1.number_input(label="Gas flow rate MMscfd", value=10 ) #MMscfd
                ql =col1.number_input(label="Oil flow rate bpd", value=2000 ) #bpd
                Api =col1.number_input(label="API", value=40)
                sg_gas =col2.number_input(label="Gas SG", value=0.6)
                P =col2.number_input(label="Pressure psia", value=1000 ) #psia
                T =col2.number_input(label="Temperatur F", value=60 ) #F
                z =col3.number_input(label="Compress factor", value=0.84)
                ug =col3.number_input(label="Gas viscosity cp", value=0.013 ) #cp
                tr =col3.number_input(label="Retention time water min", value=3 ) #min
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    try:
                        separator_bif_horizontal(qg, ql, Api, sg_gas, P, T, z, ug, tr)
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the Separtor")

        ####################### Vertical 2 Phase Separator ##########################
        with st.expander(label="Verical Two-Phase Separators"):
            with st.form(key="file_form_V2sizing"):
                image = Image.open(os.path.join(package_dir, "Thumbnail/vertical two phase.png"))
                st.image(image, caption="Vertical 2 phase separator")
                st.subheader('Input parameters')
                st.write("---")
                # Data
                col1, col2, col3 = st.columns(3)
                qg =col1.number_input(label="Gas flow rate MMscfd", value=10 ) #MMscfd
                qo =col1.number_input(label="Oil flow rate bpd", value=2000 ) #bpd
                Api =col1.number_input(label="API", value=40)
                sg_gas =col2.number_input(label="Gas SG", value=0.6)
                P =col2.number_input(label="Pressure psia", value=1000 ) #psia
                T =col2.number_input(label="Temperatur F", value=60 ) #F
                z =col3.number_input(label="Compress factor", value=0.84)
                ug =col3.number_input(label="Gas viscosity cp", value=0.013 ) #cp
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    # load well-test data
                    try:
                        separator_bif_vertical(qg, qo, Api, sg_gas, P, T, z, ug )
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the Separtor")



    # ============================================================
    # ====================Pressure Drop ==============
    # ============================================================
    #
    if window_ANTICOR == "Pressure drop":
        st.title("Pressure drop calculation")
        st.markdown(
            """
            This page is for presure drop calculation\n
            https://github.com/bsmeaton/PipePressureDrop.git\n
            Please visit his page and star his work
        """
        )
        ####################### Pressure drop ################################
        # with st.expander(label="Pipe Pressure drop"):
            # image1 = Image.open(os.path.join(package_dir, "Thumbnail/beta.jpg"))
            # st.image(image1, caption="Beta for seprator")
        with st.expander(label="Pipe pressure drop calulcator"):
            with st.form(key="file_form_pipedrop"):
                # image = Image.open(os.path.join(package_dir, "Thumbnail/threephase_separator.png"))
                # st.image(image, caption="3 phase separator")
                st.subheader('Input parameters')
                st.write("---")
                col1, col2, col3, col4 = st.columns(4)
                fluidkey = col1.selectbox("select fluid",
                                          ["Diesel25", "Diesel40", "HFO20", "HFO40", "HFO50",
                                           "HFO70", "HFO98", "Water", "TLX 304 oil 100",
                                           "TLX 304 oil 40", "Urea(32% solution)", "Natural Gas",
                                           "HFO (Gen Int)", "Natural Gas", "HFO 9", "HFO 180 40",
                                           "HFO 180 70",],)
                # viscosity =col4.number_input(label="Viscosity", value=0.3 ) # from grpah
                # denisty =col4.number_input(label="Density", value=0.7 ) # from grpah
                pipeno =col1.number_input(label="No of pipes", value=10 )
                # pipsize = col1.selectbox("select pipe type", ["Diesel25", "water", "etc"],)
                pipekey = col1.selectbox("select pipe type",
                                         ["DN300", "DN250", "DN251", "DN200", "DN150", "DN100",
                                          "DN25," "DN40," "DN50," "DN65," "DN80," "DN10," "omega",],)
                flowrate =col2.number_input(label="Flow rate in l/h", value=200 )
                pipelen =col2.number_input(label="Pipe length in m", value=5 )
                rr =col2.number_input(label="rr fraction", value=0.046 )
                st.write("---")
                submit = st.form_submit_button(label="Submit")
                if submit:
                    # load well-test data
                    try:
                        flowrate= float(flowrate) * float(2.778*10**-7)
                        viscosity = ""
                        density = ""
                        pdtotal = 0
                        with open("./Thumbnail/data/fluidlist.txt") as fluidfile:
                            for line in fluidfile:
                                if line.split(',')[0] == fluidkey:
                                    viscosity = float(line.split(',')[3])
                                    density = float(line.split(',')[1])
                                    # st.write('Found fluid: ' + fluidkey)
                        for x in range(0, pipeno):
                            # flowrate= float(("Choose pipe flow rate in l/hr for pipe "  + str(x+1) + ": "))*float(2.778*10**-7)
                            # pipekey = str(input("Choose Pipe Size for pipe " + str(x+1) + ": (e.g. DN80, DN100): "))
                            # print('Calculating ' + str(x+1) + ' of ' + str(pipeno) + ' pipes in piping system')
                            with open("./Thumbnail/data/pipelist.txt") as pipefile:
                                for line in pipefile:
                                    if line.split(',')[0] == pipekey:
                                        pipeid = float(line.split(',')[1])/1000
                                        # st.write('Found pipe: ' + pipekey )
                            # pipelen = float(input("Pipe length in m for pipe "  + str(x+1) + "?: "))
                            #fluidlist = np.atleast_1d(np.genfromtxt("fluidlist.txt", delimiter=",", dtype=None,comments='#'))
                            #pipelist = np.atleast_1d(np.genfromtxt("pipelist.txt", delimiter=",", dtype=None,comments='#'))
                            #print('\n \nList of pipe sizes in file (1-n)\n\n' + str(pipelist))
                            #print('\n \nList of fluid types in file (1-n) \n\n' + str(fluidlist))
                            pipelengtheqv = pipelen
                            head = 0
                            pd, velocity, reynum  = PressureDrop(pipelengtheqv,viscosity,flowrate,head,pipeid,rr,density)
                            pdtotal += pd
                            st.write('Pipe ID: ' + str(pipeid) + 'm')
                            st.write('Velocity: ' + str(velocity) + 'm/s')
                            st.write('Flowrate used for pipe '  + str(x+1) + ' is : ' + str(flowrate) + 'm^3/s')
                            st.write('Pressure drop for pipe '  + str(x+1) + " is :" + str(pd) + ' Bar\n')
                        st.write('Viscosity used is: ' + str(viscosity) + 'm^2/s')
                        st.write('Total Pressure drop is :' + str(pdtotal) + ' Bar')
                        # input("Press Enter to quit")
                    except Exception:
                        st.subheader("No data selected")
                        st.write("Select the correct data for the pipes")


if __name__ == "__main__":
    main()
