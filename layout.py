import streamlit as st
import os
from helper import Gauges_data, MPFM_data, Gauges_data_Spartek, daq_data
from PIL import Image
from simulation import Loadingtruck, setup
import simpy

def main():
    st.set_page_config(page_title='MPFM and Gauges', layout='wide')
    values         = ['Choose Data', 'MPFM Upload', 'Metrolog Gauges Upload', 'Spartek Gauges Upload','DAQ Upload', 'Loading Simulation']
    default_ix     = values.index('Choose Data')
    window_ANTICOR = st.sidebar.selectbox('Selection Window', values, index = default_ix)
    package_dir    = os.path.dirname(os.path.abspath(__file__))

    if window_ANTICOR == 'Choose Data':
        st.title('MPFM, MEMORY GAUGES & Simulation')
        st.title('👈🏼 Choose data from menu bar')
        st.write('---')
        image = Image.open(os.path.join(package_dir, 'Thumbnail/youtube.jpg'))
        st.subheader('About the web site:')
        st.markdown('''
                    Upload row data (ASCII) from the MPFM ROXAR unit or from the Down hole memory gauges and get
                    an instant graph and data set based on your requirements.\n
                    The gauges used in our company are either Metrolog or Spartek and I made two sheets which can serve both conditions.\n
                    Also a tab for simulating the loading of oil to trucks using loading stations which is a simple tool that 
                    can be used to get the number of trucks by changing the variables such as:\n
                    - Number of loading stations.
                    - Number of trucks provided at a given time.
                    - Filling time.
                    - etc.
                    ''')
        st.write('---')
        st.write("You can find the data discussed in my youtube channel")
        st.image(image, caption='youtube channel')

# Gauges Spartek
    if window_ANTICOR == 'Spartek Gauges Upload':
        st.title('Down Hole Gauges _Spartek_ 🌡')
        st.write('---')
        st.markdown('''
                    The below is to manipulate __SPARTEK__ Down Hole Memory Gauges row data\n
                    The page can view the data, download the values after applying a reduction factor to excel
                    ''')
        source_data = st.file_uploader(label='Uplaod gauges data to web page', type=['csv', 'log', 'txt'])
        st.write('---')
        try:
            Gauges_data_Spartek(source_data)
            col1, col2 = st.columns(2)
        except Exception:
            st.subheader('No Data available!!')
            st.write('Select correct data for Metrolog gauges')

# Gauges Metrolg
    if window_ANTICOR == 'Metrolog Gauges Upload':
        st.title('Down Hole Gauges _Metrolog_ 🌡')
        st.write('---')
        st.markdown('''
                    The below is to manipulate __METROLOG__ Down Hole Memory Gauges row data\n
                    The page can view the data, download the values after applying a reduction factor to excel
                    ''')
        source_data = st.file_uploader(label='Uplaod gauges data to web page', type=['csv', 'log', 'txt'])
        st.write('---')
        try:
            Gauges_data(source_data)
            col1, col2 = st.columns(2)
        except Exception:
            st.subheader('No Data available!!')
            st.write('Select correct data for Spartek gauges')


# MPFM Upload
    if window_ANTICOR == 'MPFM Upload':
        st.title('Multiphase Meter Data 🔬')
        st.write('---')
        st.markdown('''
                    The below is to view and the multiphase meter of type __ROXAR__ online \n
                    The page can view the data, download the summary values to excel and
                    graph the data using a custom graph up to 4 values.
                    ''')
        source_data = st.file_uploader(label='Uplaod MPFM data to web page', type=['csv', 'log', 'txt'])
        st.write('---')
        try:
            MPFM_data(source_data)
            col1, col2 = st.columns(2)
        except Exception:
            st.subheader('No data selected')
            st.write('Select the correct data for the MPFM')


# DAQ Upload
    if window_ANTICOR == 'DAQ Upload':
        st.title('DAQ Data 🔬')
        st.write('---')
        st.markdown('''
                    The below is to view and the multiphase meter of type __ROXAR__ online \n
                    The page can view the data, download the summary values to excel and graph the data using a custom graph up to 4 values
                    ''')
        source_data = st.file_uploader(label='Uplaod MPFM data to web page', type=['csv', 'log', 'txt'])
        st.write('---')
        try:
            daq_data(source_data)
        except Exception:
            st.subheader('No data selected')
            st.write('Select the correct data for the MPFM')

# Simulation of loading trucks
    if window_ANTICOR == 'Loading Simulation':
        st.title('Trucks Loading Simulation 🚚')
        st.write('---')
        st.markdown('''
                    The below is to __simulate__ the number of trucks that can be loaded in a loading station \n
                    The input below is used to change the simulation variables and see the final results below
                    ''')
        with st.form(key='simulation_form'):
            col1, col2, col3, col4 = st.columns(4)
            no_stations   = int(col1.number_input('loading stations', 1))
            loading_time  = int(col2.number_input('Loading time in minutes', 30, step = 5))
            no_trucks     = int(col3.number_input('No of trucks', 1))
            duration      = int(col4.selectbox('Loading time in minutes', [720, 1440]))
            submit = st.form_submit_button(label='Submit')
        env = simpy.Environment()
        env.process(setup(env, no_stations, loading_time, 10, no_trucks))
        env.run(until=duration)


if __name__ == '__main__':
    main()
