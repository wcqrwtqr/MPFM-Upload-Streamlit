#!/usr/bin/env python3
import numpy as np
import streamlit as st

def PressureDrop(pipelengtheqv,viscosity,flowrate,head,pipeid,rr,density):
    '''
    Calculate the drop in pressure inside a pipe
    params:
    pipelengtheqv in meter
    viscosity in cp
    flow rate l/hour
    head in m
    pipid in m
    rr
    density

    resutls:
    drop pressure due friction
    drop pressure in head
    drop total
    '''
    velocity = flowrate/(np.pi*(pipeid/2)**2)
    reynum = (pipeid * velocity) / viscosity
    if reynum < 2300:
        fricfac = 64/reynum
    else:
        fricfac = 1
        f = 0.000001
        for x in range(0, 1000):
            #Colebrook equation as a function of friction factor
            fx = 1/np.sqrt(f)+2*np.log10((rr/(3.7*pipeid*1000))+(2.51/(reynum*np.sqrt(f))))
            #First derivative of colebrook equation
            fxprime = -0.5*(f**(-3/2))*(1+((2*2.51)/(np.log10((rr/(3.7*pipeid*1000))+2.51/(reynum*np.sqrt(f)))*reynum)))
            if fx >= -0.0001 and fx <= 0.0001:
                fricfac = f
                break
            #Newton Raphson iterative solution formula
            f = f - (fx/fxprime)
            if x > 999:
                st.write("Solution invalid equation did not converge")
    Dpfric = fricfac * (pipelengtheqv/pipeid)*((density*velocity**2)/2)*1*10**-5
    Dphead = density*9.81*head*1*10**-5
    Dptotal = Dpfric+Dphead
    return Dptotal, velocity, reynum
