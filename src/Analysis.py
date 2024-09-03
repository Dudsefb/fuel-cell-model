from Model import SOFC_Model
from IO import DataManager

import numpy as np
from scipy.optimize import minimize
tp = np.float32

from abc import ABC, abstractmethod

class Analyzer(ABC):

    def __init__(self,*args,**kwargs):
        if len(args)>0: self.data = args[0]
        if len(args)>1: self.model = args[1]
        if "data" in kwargs: self.data = kwargs["data"]
        if "model" in kwargs: self.model = kwargs["model"]

    @property
    def data(self):
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
        return self._model

    @model.setter
    def model(self,value):
        if not isinstance(value,SOFC_Model): raise TypeError("Analyzer.model: Expected a SOFC_Model object, got {0}".format(type(value)))
        self._model = value

    @model.deleter
    def model(self):
        del self._model

class Optimizer(Analyzer):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)    

    def maxError(self):
        n = len(self.data.points)
        error = np.zeros(n,dtype=tp)
        maxError = 0
        for i in range(0,n):
            self.model.state = self.data.points[i].state
            error[i] = abs(self.model.E(self.data.points[i].j)-self.data.points[i].E)/self.data.points[i].E
            if error[i]>maxError: maxError = error[i]
        return maxError

    def meanError(self):
        n = len(self.data.points)
        acc = 0
        for i in range(0,n):
            self.model.state = self.data.points[i].state
            acc += abs(self.model.E(self.data.points[i].j)-self.data.points[i].E)/self.data.points[i].E
        return acc/n

    def __objective(self,X):
        self.model.constants = X
        return self.meanError()

    def findOptimum(self,X0,method,options,bounds=None):
        if(bounds==None):
            ans = minimize(self.__objective,X0,method=method,options=options)
        else:
            ans = minimize(self.__objective,X0,method=method,options=options,bounds=bounds)
        return ans.x
