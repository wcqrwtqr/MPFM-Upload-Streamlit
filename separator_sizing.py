#!/usr/bin/env python3
import pandas as pd
import numpy as np
from math import isclose, sqrt
import streamlit as st


# Function to size a three-phase horizontal separator
def separator_trif_horizontal(qg, qo, qw, Api, sg_gas, sg_w, P, T, Z, uo , uw, ug, tro, trw, beta, dm_g=100, dm_o=200, dm_w=500 ):
    '''
    This function to size a three-phase horizontal separator
    '''
    # Oil density
    pho_o = 62.4 * (141.5 / (131.5 + Api))
    # Water density
    pho_g = 2.7 * sg_gas * P / (Z * (T + 460))
    # Calculate difference in specific gravities
    sg_o = 141.5 / (Api + 131.5)
    delta_sg = sg_w -  sg_o
    cd = 0.34
    df = pd.DataFrame()
    # Iterate until the cd value converges
    while True:
        vt = 0.0119 * ((pho_o - pho_g) / pho_g * (dm_g / cd))**0.5
        re = (0.0049 * pho_g * dm_g * vt) / ug
        cd_cal = 24 / re + 3 / re**0.5 + 0.34
        df1 = pd.DataFrame({'cd':[cd], 'Vt':[vt], 'Re':[re], 'Cd_cal':[cd_cal]})
        df = pd.concat([df, df1])
        cd = cd_cal
        row = np.array(df.iloc[-1, :])
        # st.write(row)
        if isclose(row[0], row[-1], abs_tol=0.001) is True:
            # st.write('inside the break')
            break
    # st.write(f" Iterations Table: \n{df.to_markdown()}")
    st.dataframe(df)
    cd = df.iloc[-1, -1]
    # Calculate maximum oil pad thickness (ho_max)
    ho_max = 1.28E-3 * (tro * delta_sg * dm_w**2 / 10)
    # Calculate Aw/A
    Aw_A = 0.5 * ((qw * trw) / (tro * qo + trw * qw))
    # Determine beta from the figure using the AW/A value
    st.write(f'Aw/A equals = {Aw_A} please update the beta and run again ☝🏼 ')
    # beta = float(input(f'Enter the value of beta read from figure 6. If AW/A is {Aw_A}->'))
    # Calculate dmax
    d_max = ho_max / beta
    dLeff =  420 * (((T + 460) * Z * qg) / P) *\
    ((pho_g / (pho_o - pho_g)) * (cd / dm_g))**0.5
    # Calculate combinations of d, Leff for d less than dmax to satisfy the oil and water time constraints
    d2Leff = 1.42 * (qw * trw + qo * trw)
    # Create resulst table
    tabla = pd.DataFrame()
    tabla['d(in)'] = np.arange(60, d_max + 1, 12)
    tabla['Gas_Leff(ft)'] =  dLeff / tabla['d(in)']
    tabla['Liq_Leff(ft)'] = d2Leff / tabla['d(in)']**2
    tabla['Lss(ft)'] = np.where(tabla['Gas_Leff(ft)'] > tabla['Liq_Leff(ft)'],\
                                tabla['Gas_Leff(ft)'] + (tabla['d(in)'] / 12),\
                                (4 / 3) * tabla['Liq_Leff(ft)'])
    tabla['SR'] = (12 * tabla['Lss(ft)']) / tabla['d(in)']
    tabla_res = tabla.loc[tabla['SR'] > 3]
    # st.table(f"\nResults Table: \n {tabla.to_markdown()}")
    st.dataframe(tabla)
    st.write("\nOptimal Results Table:\n Engineers must select a slenderness radius between 3 and 5")
    st.dataframe(tabla_res)
    # return tabla_res


# Function to size a two-phase vertical separator
def separator_trif_vertical(qg, qo, qw, Api, sg_gas, sg_w, P, T, z, uo, uw, ug, tro, trw, dm_g=100, dm_o=200, dm_w=500):
    # Oil density
    pho_o = 62.4 * (141.5 / (131.5 + Api))
    # Gas density
    pho_g = 2.7 * sg_gas * P / (z * (T + 460))
    delta_SG = 1.07 - (141.5 / (Api + 131.5))
    cd = 0.34
    df = pd.DataFrame()
    # Iterate until the cd value converges
    while True:
        vt = 0.0119 * ((pho_o - pho_g) / pho_g * (dm_g / cd))**0.5
        re = (0.0049 * pho_g * dm_g * vt) / ug
        cd_cal = 24 / re + 3 / re**0.5 + 0.34
        df1 = pd.DataFrame({'cd':[cd], 'Vt':[vt], 'Re':[re], 'Cd_cal':[cd_cal]})
        df = pd.concat([df, df1])
        cd = cd_cal
        row = np.array(df.iloc[-1, :])
        if isclose(row[0], row[-1], abs_tol=0.001) is True:
            break
    # print(f" Iterations Table: \n{df.to_markdown()}")
    st.write(" Iterations Table:")
    st.dataframe(df)
    cd = df.iloc[-1, -1]
    # Minimum diameter due to gas
    d_min_gas = sqrt(5040 * (((T + 460) * z * qg) / P) * \
                     ((pho_g / (pho_o - pho_g)) * (cd / dm_g))**0.5)
    # Minimum diameter due to oil
    d_min_oil = sqrt(6690 * ((qo * uo)) / ((dm_w)**2 * (delta_SG)))
    # Minimum diameter due to water
    d_min_water = sqrt(6690 * ((qw * uw)) / ((dm_o)**2 * (delta_SG)))
    # Minimum diameter to size the separator
    d_min = round(max([d_min_gas, d_min_oil, d_min_water]))
    df = pd.DataFrame()
    df['d(in)'] = np.arange(d_min + 1, d_min + 20, 6)
    df['h_liq(in)'] = (tro * qo + trw * qw) / (0.12 * df['d(in)']**2)
    df['Lss(ft)'] = np.where(df['d(in)'] <= 36, (df['h_liq(in)'] + 76) / 12,\
                             (df['h_liq(in)'] + df['d(in)'] + 40) / 12)
    df['SR'] = (12 * df['Lss(ft)']) / df['d(in)']
    st.write("\nOptimal Results Table:\n Engineers must select a slenderness radius between 1.5 and 3")
    st.dataframe(df)
    # return df


# Function to size a two-phase horizontal separator
def separator_bif_horizontal(qg, ql, Api, sg_gas, P, T, z, ug, tr, dm=140):
    '''
    Function to size a two-phase horizontal separator
    '''
    # Liquid density
    pho_l = 62.4 * (141.5 / (131.5 + Api))
    # Gas density
    pho_g = 2.7 * sg_gas * P / (z * (T + 460))
    cd = 0.34
    df = pd.DataFrame()
    # Iterate until the cd value converge
    while True:
        vt = 0.0119 * ((pho_l - pho_g) / pho_g * (dm / cd))**0.5
        re = (0.0049 * pho_g * dm * vt) / ug
        cd_cal = 24 / re + 3 / re**0.5 + 0.34
        df1 = pd.DataFrame({'cd':[cd], 'Vt':[vt], 'Re':[re], 'Cd_cal':[cd_cal]})
        df = pd.concat([df, df1])
        cd = cd_cal
        row = np.array(df.iloc[-1, :])
        if isclose(row[0], row[-1], abs_tol=0.001) is True:
            break
    st.write(" Iterations Table:")
    st.dataframe(df)
    cd = df.iloc[-1, -1]
    dLeff = 420 * (((T + 460) * z * qg) / P) *\
    ((pho_g / (pho_l - pho_g)) * (cd / dm))**0.5
    tr = [tr]
    dia = [24, 30, 36, 42, 48]
    tabla = pd.DataFrame()
    # Looping to create results table
    for t in tr:
        for diam in dia:
            tabla1 = pd.DataFrame({'tr(min)': [t], 'd(in)': [diam]})
            tabla = pd.concat([tabla, tabla1])
    tabla['Gas_Leff(ft)'] = dLeff / tabla['d(in)']
    tabla['Liq_Leff(ft)'] = (tabla['tr(min)'] * 2000) / (tabla['d(in)']**2 * 0.7)
    tabla['Lss(ft)'] = np.where(tabla['Gas_Leff(ft)'] > tabla['Liq_Leff(ft)'],\
                                tabla['Gas_Leff(ft)'] + (tabla['d(in)'] / 12),\
                                (4 / 3) * tabla['Liq_Leff(ft)'])
    tabla['12LSS/d'] = (12 * tabla['Lss(ft)']) / tabla['d(in)']
    st.write('Results Table:')
    st.dataframe(tabla)
    st.write("\nOptimal Results Table: \n Engineers must select a slenderness radius between 3 and 4")
    # Slice the results table, considering conditions to get the best dimension of the separator
    tabla_res = tabla.loc[(tabla['12LSS/d'] > 2.9) & (tabla['12LSS/d'] < 4)]
    st.dataframe(tabla_res)
    # return tabla_res



# Function to size a two-phase vertical separator
def separator_bif_vertical(qg, ql, Api, sg_gas, P, T, z, ug, dm=140):
    # Liquid density
    pho_l = 62.4 * (141.5 / (131.5 + Api))
    # Gas density
    pho_g = 2.7 * sg_gas * P / (z * (T + 460))
    cd = 0.34
    df = pd.DataFrame()
    # Iterate until the cd value converge
    while True:
        vt = 0.0119 * ((pho_l - pho_g) / pho_g * (dm / cd))**0.5
        re = (0.0049 * pho_g * dm * vt) / ug
        cd_cal = 24 / re + 3 / re**0.5 + 0.34
        df1 = pd.DataFrame({'cd':[cd], 'Vt':[vt], 'Re':[re], 'Cd_cal':[cd_cal]})
        df = pd.concat([df, df1])
        cd = cd_cal
        row = np.array(df.iloc[-1, :])
        if isclose(row[0], row[-1], abs_tol=0.001) is True:
            break
    st.write(" Iterations Table:")
    st.dataframe(df)
    cd = df.iloc[-1, -1]
    # Minumum diameter to size the separator
    d_min = sqrt(5040 * (((T + 460) * z * qg) / P) *\
                 ((pho_g / (pho_l - pho_g)) * (cd / dm))**0.5)
    tr = [3, 2, 1]
    dia = [24, 30, 36, 42, 48]
    tabla = pd.DataFrame()
    # Looping to create results table
    for t in tr:
        for diam in dia:
            tabla1 = pd.DataFrame({'tr(min)': [t], 'd(in)': [diam]})
            tabla = pd.concat([tabla, tabla1])
    tabla['h(in)'] = (tabla['tr(min)'] * ql) / (tabla['d(in)']**2 * 0.12)
    tabla['Lss(ft)'] = np.where(tabla['d(in)'] <= 36, (tabla['h(in)'] + 76) / 12, \
                                (tabla['h(in)'] + tabla['d(in)'] + 40) / 12)
    tabla['12LSS/d'] = (12 * tabla['Lss(ft)']) / tabla['d(in)']
    st.write("Results Table:")
    st.dataframe(tabla)
    st.write("\nOptimal Results Table: \n Engineers must select a diameter greater than\
    the minimum diameter as well as a slenderness radius between 3 and 4")
    # Slice the results table, considering conditions to get the best dimension of the separator
    tabla_res = tabla.loc[(tabla['d(in)'] > d_min)\
                          & (tabla['12LSS/d'] > 3) & (tabla['12LSS/d'] < 4)]
    st.dataframe(tabla_res)
