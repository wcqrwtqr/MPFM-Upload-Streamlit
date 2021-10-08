import random
import simpy
import streamlit as st


class Loadingtruck(object):
    """A lading has a limited number of loading stations (``NUM_LOADING``) to
    fill truck in parallel.

    Trucks have to request one of the loading stations. When they got one, they
    can start the loading processes and wait for it to finish (which
    takes ``loading time`` minutes).
    """
    def __init__(self, env, num_loading_station, loadingtime):
        self.env = env
        self.loadingstation = simpy.Resource(env, num_loading_station)
        self.loadingtime = loadingtime

    # def filltruck(self, truck): ########
    def filltruck(self, truck, loadingtime):
        """The loading processes. It takes a ``Truck`` processes and starts
        to fill it oil."""
        yield self.env.timeout(random.randint(loadingtime-10, loadingtime+10)) #####

    def drivetrucktostation(self, truck):
        """The moving process to enter the truck to loading processes. It takes a ``truck`` processes and tries."""
        yield self.env.timeout(random.randint(5, 15))

def truck(env, name, cw, loadingtime):
    """The truck process (each truck has a ``name``) arrives at the loading stations
    (``cw``) and requests a cleaning loading station.

    It then starts the loading process, waits for it to finish and
    leaves to never come back ...
    """
    with cw.loadingstation.request() as request:
        yield request

        st.write(f'🚚....{name} drives to loading station at {round(env.now/60,0)} hours.')
        yield env.process(cw.drivetrucktostation(name))

        st.write('%s Start loading process at %.1f hours. 🕓 ' % (name, env.now/60))
        yield env.process(cw.filltruck(name, loadingtime))

        yield env.process(cw.drivetrucktostation(name))
        st.write('🏁.... %s left the loading station at %.1f hours.' % (name, env.now/60))


def setup(env, num_loading_station, loadingtime, t_inter, no_trucks):
    """Create a loading truck, a number of initial trucks and keep creating trucks
    approx. Every ``t_inter`` minutes."""
    # Create the loading truck
    loadingtruck = Loadingtruck(env, num_loading_station, loadingtime)

    # Create x initial trucks
    for i in range(no_trucks):
        env.process(truck(env, 'Truck %d' % i, loadingtruck, loadingtime))

    # Create more trucks while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 5, t_inter + 5))
        i += 1
        # i += num_loading_station
        env.process(truck(env, 'Truck %d' % i, loadingtruck, loadingtime))


