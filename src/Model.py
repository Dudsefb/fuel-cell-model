from abc import ABC, abstractmethod

class State:
    '''
    A class to facilitate the storage and transfer of model state information
    All properties can be accessed externally
    '''

    def __init__(self,state=None):
        #All properties are initialized as None
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

    #The absolute temperature, in K
    @property
    def T(self):
        return self._T

    @T.setter
    def T(self,value):
        if value<0: raise ValueError("State.T: Expected value >=0, got {0}".format(value))
        self._T = value

    @T.deleter
    def T(self):
        del self._T

    #The absolute pressure, in Pa
    @property
    def P(self):
        return self._P

    @P.setter
    def P(self,value):
        if value<0: raise ValueError("State.P: Expected value>=0, got {0}".format(value))
        self._P = value

    @P.deleter
    def P(self):
        del self._P

    #Anode hydrogen partial pressure, in Pa
    @property
    def pH2(self):
        return self._pH2

    @pH2.setter
    def pH2(self,value):
        if value<0: raise ValueError("State.pH2: Expected value >=0, got {0}".format(value))
        self._pH2 = value

    @pH2.deleter
    def pH2(self):
        del self._pH2

    #Cathode oxygen partial pressure, in Pa
    @property
    def pO2(self):
        return self._pO2

    @pO2.setter
    def pO2(self,value):
        if value<0: raise ValueError("State.pO2: Expected value >=0, got {0}".format(value))
        self._pO2 = value

    @pO2.deleter
    def pO2(self):
        del self._pO2

    #Anode water partial pressure, in Pa
    @property
    def pH2O(self):
        return self._pH2O

    @pH2O.setter
    def pH2O(self,value):
        if value<0: raise ValueError("State.pH2O: Expected value >=0, got {0}".format(value))
        self._pH2O = value

    @pH2O.deleter
    def pH2O(self):
        del self._pH2O

class SOFC_Model(ABC):
    '''
    An abstract class describing the general interface of a SOFC lumped model
    The implementation of the model itself is left for the child classes
    The class is setup assuming isothermal and isobaric operation
    '''
    
    #Constants
    #WARNING: Overwrite their values in the child class if using different units
    R = 8.31446261815324 #J/mol.K
    F = 96485.3321 #C    
    
    #The state under which the calculations are performed
    @property
    def state(self):
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
        pass

    #A method to calculate the output voltage
    @abstractmethod
    def E(self,*args,**kwargs):
        pass
