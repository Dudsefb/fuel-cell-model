"""@package src
The Model module contains a description of a model's thermodynamic state, as well as the abstract class from which the model will be derived.

@mainpage Fuel Cell Model

@section description_main Description
A simple python program containing a set of tools to analyze fuel cell lumped models.

@section notes_main Notes
 - The Fuel Cell model implementation is left to the user.
"""

from abc import ABC, abstractmethod

class State:
    """A class to facilitate the storage and transfer of model thermodynamic state information.
    
    The thermodynamic state is understood to be the:
        @param T Temperature
        @param P Pressure
        @param pH2 Hydrogen partial pressure
        @param pO2 Oxygen partial pressure
        @param pH2O Water partial pressure
    """

    def __init__(self,state=None):
        """A State object can be instantiated with no arguments, in which case the variables are initialized with None. If another State object is passed, the new instance will copy the values of the old one."""
        self._T = None
        self._P = None
        self._pH2 = None
        self._pO2 = None
        self._pH2O = None
        if(isinstance(state,State)):
            self._T = state.T
            self._P = state.P
            self._pH2 = state.pH2
            self._pO2 = state.pO2
            self._pH2O = state.pH2O
        elif(state!=None):
            raise TypeError("State: Expected a State object, got {0}".format(type(state)))

    @property
    def T(self):
        """The fuel cell's temperature."""
        return self._T

    @T.setter
    def T(self,value):
        if value<0: raise ValueError("State.T: Expected value >=0, got {0}".format(value))
        self._T = value

    @T.deleter
    def T(self):
        del self._T

    @property
    def P(self):
        """The fuel cell's pressure."""
        return self._P

    @P.setter
    def P(self,value):
        if value<0: raise ValueError("State.P: Expected value>=0, got {0}".format(value))
        self._P = value

    @P.deleter
    def P(self):
        del self._P

    @property
    def pH2(self):
        """The fuel cell's hydrogen partial pressure."""
        return self._pH2

    @pH2.setter
    def pH2(self,value):
        if value<0: raise ValueError("State.pH2: Expected value >=0, got {0}".format(value))
        self._pH2 = value

    @pH2.deleter
    def pH2(self):
        del self._pH2

    @property
    def pO2(self):
        """The fuel cell's oxygen partial pressure."""
        return self._pO2

    @pO2.setter
    def pO2(self,value):
        if value<0: raise ValueError("State.pO2: Expected value >=0, got {0}".format(value))
        self._pO2 = value

    @pO2.deleter
    def pO2(self):
        del self._pO2

    @property
    def pH2O(self):
        """The fuel cell's water partial pressure."""
        return self._pH2O

    @pH2O.setter
    def pH2O(self,value):
        if value<0: raise ValueError("State.pH2O: Expected value >=0, got {0}".format(value))
        self._pH2O = value

    @pH2O.deleter
    def pH2O(self):
        del self._pH2O

class Model(ABC):
    """An abstract class describing the general interface of a fuel cell lumped model.

    The implementation of the mathematical model itself is left for the child classes.
    The class is setup with isothermal and isobaric operation in mind.
    """
    
    #Constants
    #WARNING: Overwrite their values in the child class if using different units
    R = 8.31446261815324 #J/mol.K
    F = 96485.3321 #C    
    
    @property
    def state(self):
        """The thermodynamic state in which the calculations will be performed."""
        return self._state

    @state.setter
    def state(self,value):
        if not isinstance(value,State): raise TypeError("SOFC_Model.state: Expected a State object, got {0}".format(type(value)))
        self._state = State(value)

    @state.deleter
    def state(self):
        del self._state

    @property
    @abstractmethod
    def constants(self):
        """This method shall return the constants used in the implemented model.

        This method's implementation is required for the Optimization class to function.
        """
        pass

    @abstractmethod
    def E(self,*args,**kwargs):
        """This method shall return the fuel cell voltage predicted by the model."""
        pass
