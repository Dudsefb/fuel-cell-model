from Model import SOFC_Model
from IO import DataManager

import numpy as np
from scipy.optimize import minimize
tp = np.float32

from abc import ABC, abstractmethod

class Analyzer(ABC):
"""An abstract class to define the common attributes of model analyzers."""

    def __init__(self,*args,**kwargs):
        """The constructor, which accepts both positional and non-positional arguments. If both are given, non-positional arguments take precedence.
        
            @param data A DataManager object containing the experimental data.
            @param model A Model object.
        """
        if len(args)>0: self.data = args[0]
        if len(args)>1: self.model = args[1]
        if "data" in kwargs: self.data = kwargs["data"]
        if "model" in kwargs: self.model = kwargs["model"]

    @property
    def data(self):
        """A DataManager object containing the experimental data."""
        return self._data

    @data.setter
    def data(self,value):
        if not isinstance(value,DataManager): raise TypeError("Analyzer.data: Expected a DataManager object, got {0}".format(type(value)))
        self._data = value

    @data.deleter
    def data(self,value):
        del self._data

    @property
    def model(self):
        """A Model object."""
        return self._model

    @model.setter
    def model(self,value):
        if not isinstance(value,SOFC_Model): raise TypeError("Analyzer.model: Expected a SOFC_Model object, got {0}".format(type(value)))
        self._model = value

    @model.deleter
    def model(self):
        del self._model

class Optimizer(Analyzer):
"""A simple class that makes use of scipy's minimize() function to optimize the model's constants."""

    def __init__(self,*args,**kwargs):
        """The constructor, which passes the arguments to the Analyzer parent class."""
        super().__init__(*args,**kwargs)    

    def maxError(self):
        """Calculates the maximum error between the experimental data and the model.
            
            @return The modulus of the maximum relative error \f$max\left(\left|\frac{E_{Model}-E_{Experimental}\right|}{E_{Experimental}}\right)\f$
        """
        n = len(self.data.points)
        error = np.zeros(n,dtype=tp)
        maxError = 0
        for i in range(0,n):
            self.model.state = self.data.points[i].state
            error[i] = abs(self.model.E(self.data.points[i].j)-self.data.points[i].E)/self.data.points[i].E
            if error[i]>maxError: maxError = error[i]
        return maxError

    def meanError(self):
        """Calculates the mean error between the experimental data and the model.

            @return The modulus of the mean relative error \f$\frac{1}{n}\sum_{i=0}^{n}\left(\left|\frac{E_{Model,i}-E_{Experimental,i}\right|}{E_{Experimental,i}}\right)\f$
        """
        n = len(self.data.points)
        acc = 0
        for i in range(0,n):
            self.model.state = self.data.points[i].state
            acc += abs(self.model.E(self.data.points[i].j)-self.data.points[i].E)/self.data.points[i].E
        return acc/n

    def __objective(self,X):
        """The objective function that will be optimized.
            
            @param X A numpy array containing the model constants, as specified in the model's implementation.

            @return The mean error between the experimental data and the model.
        """
        self.model.constants = X
        return self.meanError()

    def findOptimum(self,X0,method,options,bounds=None):
        """Optimizes the model's constants.
        
            @param X0 The set of initial values for the constants.
            @param method A string defining the optimization method that will be used (see scipy.optimize.minimize() for more info).
            @param options A dictionary containing the options for the optimization algorithm.
            @param bounds The bounds of the values, in case a bounded algorithm is selected.

            @return An array with the optimized constants.
        """
        if(bounds==None):
            ans = minimize(self.__objective,X0,method=method,options=options)
        else:
            ans = minimize(self.__objective,X0,method=method,options=options,bounds=bounds)
        return ans.x
