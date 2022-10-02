import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from nodalanalysis import *
import streamlit as st

def IPR_curve(q_test, pwf_test, pr, pwf:list, pb):
    # Creating Dataframe
    df = pd.DataFrame()
    df['Pwf(psia)'] = pwf
    df['Qo(bpd)'] = df['Pwf(psia)'].apply(lambda x: qo_ipr_compuesto(q_test, pwf_test, pr, x, pb))
    fig, ax = plt.subplots(figsize=(10, 10))
    x = df['Qo(bpd)']
    y = df['Pwf(psia)']
    # The following steps are used to smooth the curve
    X_Y_Spline = make_interp_spline(x, y)
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = X_Y_Spline(X_)
    #Build the curve
    ax.plot(X_, Y_, c='g')
    ax.set_xlabel('Qo(bpd)', fontsize=14)
    ax.set_ylabel('Pwf(psia)', fontsize=14)
    ax.set_title('IPR', fontsize=18)
    ax.set(xlim=(0, df['Qo(bpd)'].max() + 10), ylim=(0, df['Pwf(psia)'][0] + 100))
    # Arrow and Annotations
    plt.annotate(
        'Bubble Point', xy=(Qb(q_test, pwf_test, pr, pb), pb),xytext=(Qb(q_test, pwf_test, pr, pb) + 100, pb + 100) ,
        arrowprops=dict(arrowstyle='->',lw=1)
    )
    # Horizontal and Vertical lines at bubble point
    plt.axhline(y=pb, color='r', linestyle='--')
    plt.axvline(x=Qb(q_test, pwf_test, pr, pb), color='r', linestyle='--')
    ax.grid()
    st.pyplot(fig)
    # plt.show()

   # IPR Curve
def IPR_curve_methods(q_test, pwf_test, pr, pwf:list, pb, method, ef=1, ef2=None):
    # Creating Dataframe
    fig, ax = plt.subplots(figsize=(20, 10))
    df = pd.DataFrame()
    df['Pwf(psia)'] = pwf
    if method == 'Darcy':
        df['Qo(bpd)'] = df['Pwf(psia)'].apply(lambda x: qo_darcy(q_test, pwf_test, pr, x, pb))
    elif method == 'Vogel':
        df['Qo(bpd)'] = df['Pwf(psia)'].apply(lambda x: qo_vogel(q_test, pwf_test, pr, x, pb))
    elif method == 'IPR_compuesto':
        df['Qo(bpd)'] = df['Pwf(psia)'].apply(lambda x: qo_ipr_compuesto(q_test, pwf_test, pr, x, pb))
        # Stand the axis of the IPR plot
    x = df['Qo(bpd)']
    y = df['Pwf(psia)']
    # st.dataframe(df)
    # The following steps are used to smooth the curve
    X_Y_Spline = make_interp_spline(x, y)
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = X_Y_Spline(X_)
    #Build the curve
    ax.plot(X_, Y_, c='g')
    ax.set_xlabel('Qo(bpd)')
    ax.set_ylabel('Pwf(psia)')
    ax.set_title('IPR')
    ax.set(xlim=(0, df['Qo(bpd)'].max() + 10), ylim=(0, df['Pwf(psia)'].max() + 100))
    # Arrow and Annotations
    plt.annotate(
        'Bubble Point', xy=(Qb(q_test, pwf_test, pr, pb), pb),xytext=(Qb(q_test, pwf_test, pr, pb) + 100, pb + 100) ,
        arrowprops=dict(arrowstyle='->',lw=1)
    )
    # Horizontal and Vertical lines at bubble point
    plt.axhline(y=pb, color='r', linestyle='--')
    plt.axvline(x=Qb(q_test, pwf_test, pr, pb), color='r', linestyle='--')
    ax.grid()
    return fig
# plt.show()
# st.pyplot(fig)



def vlp_curve(THP, API, wc, sg_h2o, md, tvd, ID, C ):
    # Creating Dataframe
    df = pd.DataFrame()
    df['Q'] = np.array([0, 1000, 2000, 3000, 4000, 5000, 6000])
    df['THP (psi)'] = THP
    df['Pgravity (psia)'] = gradient_avg(API, wc, sg_h2o) * tvd
    df['f'] = df['Q'].apply(lambda x: f_darcy(x, ID, C))
    df['F (ft)'] = df['f'] * md
    df['Pf (psia)'] = df['F (ft)'] * gradient_avg(API, wc, sg_h2o)
    df['Po (psia)'] = df['THP (psi)'] + df['Pgravity (psia)'] + df['Pf (psia)']
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df['Q'], df['Po (psia)'], c='g')
    ax.set_xlabel('Q (BPD)', fontsize=14)
    ax.set_ylabel('Po (psia)')
    ax.set(xlim=(df['Q'].min(), df['Q'].max()))
    ax.set_title('Po vs Q (VLP)', fontsize=16)
    ax.grid()
    return fig



def IPR_vlp_curve(THP, API, wc, sg_h2o, md, tvd, ID, C, q_test, pwf_test,  pr, pb, method ):
    columns = ['Q(bpd)', 'Pwf(psia)', 'THP(psia)', 'Pgravity(psia)', 'f', 'F(ft)', 'Pf(psia)', 'Po(psia)', 'Psys(psia)']
    df = pd.DataFrame(columns=columns)
    df[columns[0]] = np.array([750, 1400, 2250, 3000, 3750, 4500, 5250, 6000, 6750, 7500])
    if method == 'Darcy':
        df[columns[1]] = df['Q(bpd)'].apply(lambda x: pwf_darcy(q_test, pwf_test, x, pr, pb))
    elif method == 'Vogel':
        df[columns[1]] = df['Q(bpd)'].apply(lambda x: pwf_vogel(q_test, pwf_test, x, pr, pb))
    df[columns[2]] = THP
    df[columns[3]] = gradient_avg(API, wc, sg_h2o) * tvd
    df[columns[4]] = df['Q(bpd)'].apply(lambda x: f_darcy(x, ID, C))
    df[columns[5]] = df['f'] * md
    df[columns[6]] = gradient_avg(API, wc, sg_h2o) * df['F(ft)']
    df[columns[7]] = df['THP(psia)'] + df['Pgravity(psia)'] + df['Pf(psia)']
    df[columns[8]] = df['Po(psia)'] - df['Pwf(psia)']
    # st.dataframe(df)
    # Graphing the results
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(df['Q(bpd)'], df['Pwf(psia)'], c='red', label='IPR')
    ax.plot(df['Q(bpd)'], df['Po(psia)'], c='green', label='VLP')
    ax.plot(df['Q(bpd)'], df['Psys(psia)'], c='b', label='System Curve')
    ax.set_xlabel('Q(bpd)')
    ax.set_ylabel('Pwf(psia)')
    ax.set_xlim(df['Q(bpd)'].min(), df['Q(bpd)'].max())
    ax.set_title('Nodal Analysis')
    ax.grid()
    plt.legend()
    return fig
