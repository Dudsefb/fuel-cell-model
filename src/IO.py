from Model import State

import csv

class DataPoint:
    '''
    A simple class to store experimental data points
    It stores the current density and voltage, as well as the State under
    which the experiment has been performed
    '''
    def __init__(self,arr=[]):
        '''
        The initialization expects an array (optional) where:
        [0] - Current density [A/m^2]        - optional
        [1] - Voltage [V]                    - optional
        [2] - Temperature [K]                - optional
        [3] - Pressure [Pa]                  - optional
        [4] - Hydrogen partial pressure [Pa] - optional
        [5] - Oxygen partial pressure [Pa]   - optional
        [6] - H2O partial pressure [Pa]      - optional
        '''
        self._j = None
        self._E = None
        self.state = State()
        if len(arr)>0: self.j = arr[0]
        if len(arr)>1: self.E = arr[1]
        if len(arr)>2: self.state.T = arr[2]
        if len(arr)>3: self.state.P = arr[3]
        if len(arr)>4: self.state.pH2 = arr[4]
        if len(arr)>5: self.state.pO2 = arr[5]
        if len(arr)>6: self.state.pH2O = arr[6]

    #The current density [A/m^2]
    @property
    def j(self):
        return self._j

    @j.setter
    def j(self,value):
        if value<0: raise ValueError("DataPoint.j: Expected >=0, got {0}".format(value))
        self._j = value

    @j.deleter
    def j(self):
        del self._j

    #The voltage [V]
    @property
    def E(self):
        return self._E

    @E.setter
    def E(self,value):
        if value<0: raise ValueError("DataPoint.E: Expected >=0, got {0}".format(value))
        self._E = value

    @E.deleter
    def E(self):
        del self._E

    #The state
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self,value):
        if not isinstance(value,State): raise ValueError("DataPoint.state: Expected a State object, got {0}".format(value))
        self._state = State(value)

    @state.deleter
    def state(self):
        del self._state

class DataManager:
    '''
    The DataManager is responsible for handling experimental data and
    carrying out batch operations
    '''

    def __init__(self):
        #The object initializes with an empty list of DataPoint objects
        self._points = []

    #The list of DataPoint objects
    @property
    def points(self):
        return self._points

    def addPoint(self,point):
        if not isinstance(point,DataPoint): raise TypeError("DataManager.addPoint: Expected a DataPoint object, got {0}".format(type(point)))
        self._points.append(point)

    @points.deleter
    def points(self):
        del self._points

    def getNumberOfPoints(self):
        return len(self._points)
    
    #Operations to set the variable to a value if doesn't have a value
    def fill_j(self,value):
        for point in self.points:
            if point.j == None: point.j = value

    def fill_E(self,value):
        for point in self.points:
            if point.E == None: point.E = value

    def fill_T(self,value):
        for point in self.points:
            if point.state.T == None: point.state.T = value

    def fill_P(self,value):
        for point in self.points:
            if point.state.P == None: point.state.P = value

    def fill_pH2(self,value):
        for point in self.points:
            if point.state.pH2 == None: point.state.pH2 = value

    def fill_pO2(self,value):
        for point in self.points:
            if point.state.pO2 == None: point.state.pO2 = value

    def fill_pH2O(self,value):
        for point in self.points:
            if point.state.pH2O == None: point.state.pH2O = value
    
    #Operations to overwrite the variable with a value
    def overwrite_j(self,value):
        for point in self.points:
            point.j = value

    def overwrite_E(self,value):
        for point in self.points:
            point.E = value

    def overwrite_T(self,value):
        for point in self.points:
            point.state.T = value

    def overwrite_P(self,value):
        for point in self.points:
            point.state.P = value

    def overwrite_pH2(self,value):
        for point in self.points:
            point.state.pH2 = value

    def overwrite_pO2(self,value):
        for point in self.points:
            point.state.pO2 = value

    def overwrite_pH2O(self,value):
        for point in self.points:
            point.state.pH2O = value

    #Operations to rescale the variable by a certain factor
    def rescale_j(self,value):
        for point in self.points:
            point.j *= value

    def rescale_E(self,value):
        for point in self.points:
            point.E *= value

    def rescale_T(self,value):
        for point in self.points:
            point.state.T *= value

    def rescale_P(self,value):
        for point in self.points:
            point.state.P *= value

    def rescale_pH2(self,value):
        for point in self.points:
            point.state.pH2 *= value

    def rescale_pO2(self,value):
        for point in self.points:
            point.state.pO2 *= value

    def rescale_pH2O(self,value):
        for point in self.points:
            point.state.pH2O *= value

    #Operations to offset the variable by a certain value
    def offset_j(self,value):
        for point in self.points:
            point.j += value

    def offset_E(self,value):
        for point in self.points:
            point.E += value

    def offset_T(self,value):
        for point in self.points:
            point.state.T += value

    def offset_P(self,value):
        for point in self.points:
            point.state.P += value

    def offset_pH2(self,value):
        for point in self.points:
            point.state.pH2 += value

    def offset_pO2(self,value):
        for point in self.points:
            point.state.pO2 += value

    def offset_pH2O(self,value):
        for point in self.points:
            point.state.pH2O += value

    #Exports the data contained in the object to a txt file
    def save_txt(self,path):
        with open(path,'w') as file:
            for point in self.points:
                file.write("{0} {1} {2} {3} {4} {5} {6}\n".format(point.j,point.E,
                    point.state.T,point.state.P,point.state.pH2,point.state.pO2,point.state.pH2O))
            file.close()

class Reader:
    '''
    The reader class has some tools to handle the import of pre-formatted data
    It currently works with csv and txt files
    '''

    def __init__(self):
        pass

    def __trim(self,arr):
        #This fucntion removes any empty entries from a list
        while('' in arr):
            arr.pop(arr.index(''))
        while(' ' in arr):
            arr.pop(arr.index(' '))
        while([] in arr):
            arr.pop(arr.index([]))
        return arr

    def read_txt(self,path):
        #This function returns a DataManager object with the data from a txt file
        with open(path,'r') as file:
            buffer = file.read().split('\n')
            buffer = self.__trim(buffer)
            ans = DataManager()
            for i in range(0,len(buffer)):
                buffer[i] = self.__trim(buffer[i].split(' '))
                for j in range(0,len(buffer[i])):
                    buffer[i][j] = float(buffer[i][j])
                ans.addPoint(DataPoint(buffer[i]))
            file.close()
        return ans

    def read_csv(self,path):
        #This function returns a dictionary with the data from a csv file
        with open(path,newline='\n') as file:
            csv_reader = csv.reader(file,delimiter=',',quotechar='\"')
            buffer = []
            for row in csv_reader:
                buffer.append(row)
            headers = self.__trim(buffer[0])
            ans = {}
            for header in headers:
                ans[header] = []
            for i in range(2,len(buffer)):
                for j in range(0,len(buffer[i]),2):
                    try:
                        ans[headers[int(j/2)]].append([float(buffer[i][j]),float(buffer[i][j+1])])
                    except:
                        continue
            file.close()
        return ans
