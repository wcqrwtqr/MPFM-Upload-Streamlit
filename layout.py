import streamlit as st
import os
from helper import Gauges_data, MPFM_data, Gauges_data_Spartek
from PIL import Image

def main():
    st.set_page_config(page_title='ASCII files Upload Page', layout='wide')
    st.title('Roxar MPFM unit and Downhole Memory gauges log file grapher')
    values = ['Choose Data','MPFM Upload', 'Metrolog Gauges Upload','Spartek Gauges Upload']
    default_ix = values.index('Choose Data')
    window_ANTICOR = st.sidebar.selectbox('Selection Window', values, index=default_ix)
    package_dir = os.path.dirname(os.path.abspath(__file__))

    if window_ANTICOR == 'Choose Data':
        st.title('👈🏼 Choose data from menu bar')
        image = Image.open(os.path.join( package_dir,'Thumbnail/youtube.jpg'))
        st.subheader('About the website:')
        st.write('Upload row data (ASCII) from the MPFM ROXAR unit or from the Down hole memory gauges and get an instant graph and data set based on your requirements the gauges used in our company are either Metrolog or Spartek and I made two sheets which can serve both conditions')
        st.write("You can find the data discussed in my youtube channel and I've added the ")
        st.image(image, caption = 'youtube channel')

# Gauges Spartek
    if window_ANTICOR == 'Spartek Gauges Upload':
        source_data = st.file_uploader(label='Uplaod gauges data to web page', type=['csv', 'log', 'txt'])
        try:
            st.title('Down Hole Gauges Data')
            Gauges_data_Spartek(source_data)
            col1, col2 = st.columns(2)
            image = Image.open(os.path.join(package_dir,'Thumbnail/Gauges data thumbnail.jpg'))
            col1.image(image, caption='youtube', width=100)
            col2.markdown('See my youtube on this data: https://youtu.be/C6oz96OLCCg')
        except Exception:
            st.title('No Data available!!')
            st.subheader('Select previous data')
# Gauges Metrolg
    if window_ANTICOR == 'Metrolog Gauges Upload':
        source_data = st.file_uploader(label='Uplaod gauges data to web page', type=['csv', 'log', 'txt'])
        try:
            st.title('Down Hole Gauges Data')
            Gauges_data(source_data)
            col1, col2 = st.columns(2)
            image = Image.open(os.path.join(package_dir,'Thumbnail/Gauges data thumbnail.jpg'))
            col1.image(image, caption='youtube', width=100)
            col2.markdown('See my youtube on this data: https://youtu.be/C6oz96OLCCg')
        except Exception:
            st.title('No Data available!!')
            st.subheader('Select correct data for Spartek gauges')


# MPFM Upload
    if window_ANTICOR == 'MPFM Upload':
        source_data = st.file_uploader(label='Uplaod MPFM data to web page', type=['csv', 'log', 'txt'])
        try:
            st.title('Multiphase Meter Data')
            st.text('Uploaded data')
            MPFM_data(source_data)
            col1, col2 = st.columns(2)
            image = Image.open(os.path.join(package_dir,'Thumbnail/MPFM data thumbnail.jpg'))
            col1.image(image, caption='youtube', width=100)
            col2.markdown('See my youtube on this data:https://youtu.be/sctzeSaUL2c')
        except Exception:
            st.title('Wrong data selected')
            st.subheader('Select the correct data for the MPFM')


if __name__ == '__main__':
    main()
