"""@package src
This module contains classes to handle experimental data.

It contains classes for data input and output, as well as some classes to facilitate data handling.
"""

from Model import State
import csv

class DataPoint:
    """A simple class to store data points.

    Its main purpose is to store experimental data, which is assumed to be:
        j Current density
        E Voltage
        state A State object containing the thermodynamic state under which the voltage and current density have been measured.
    """

    def __init__(self,arr=[]):
        """The constructor expects an array (optional) where:
            @param arr An input array where.
                [0] Current density [A/m^2]        
                [1] Voltage [V]                    
                [2] Temperature [K]                
                [3] Pressure [Pa]                  
                [4] Hydrogen partial pressure [Pa] 
                [5] Oxygen partial pressure [Pa]
                [6] H2O partial pressure [Pa]      
        """
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

    @property
    def j(self):
        """The current density."""
        return self._j

    @j.setter
    def j(self,value):
        if value<0: raise ValueError("DataPoint.j: Expected >=0, got {0}".format(value))
        self._j = value

    @j.deleter
    def j(self):
        del self._j

    @property
    def E(self):
        """The cells voltage."""
        return self._E

    @E.setter
    def E(self,value):
        if value<0: raise ValueError("DataPoint.E: Expected >=0, got {0}".format(value))
        self._E = value

    @E.deleter
    def E(self):
        del self._E

    @property
    def state(self):
        """The thermodynamic state under which the data point has been aquired."""
        return self._state

    @state.setter
    def state(self,value):
        if not isinstance(value,State): raise ValueError("DataPoint.state: Expected a State object, got {0}".format(value))
        self._state = State(value)

    @state.deleter
    def state(self):
        del self._state

class DataManager:
    """The DataManager is responsible for handling experimental data and carrying out batch operations.
    """

    def __init__(self):
        """The constructor initializes a DataManager object with an empty list of points."""
        self._points = []

    @property
    def points(self):
        """The list of DataPoint objects."""
        return self._points

    def addPoint(self,point):
        """Adds a DataPoint object to the list.

            @param point A DataPoint object.
        """
        if not isinstance(point,DataPoint): raise TypeError("DataManager.addPoint: Expected a DataPoint object, got {0}".format(type(point)))
        self._points.append(point)

    @points.deleter
    def points(self):
        del self._points

    def getNumberOfPoints(self):
        return len(self._points)
    
    def fill_j(self,value):
        """Sets the point's j value if it has None."""
        for point in self.points:
            if point.j == None: point.j = value

    def fill_E(self,value):
        """Sets the point's E value if it has None."""
        for point in self.points:
            if point.E == None: point.E = value

    def fill_T(self,value):
        """Sets the point's T value if it has None."""
        for point in self.points:
            if point.state.T == None: point.state.T = value

    def fill_P(self,value):
        """Sets the point's P value if it has None."""
        for point in self.points:
            if point.state.P == None: point.state.P = value

    def fill_pH2(self,value):
        """Sets the point's pH2 value if it has None."""
        for point in self.points:
            if point.state.pH2 == None: point.state.pH2 = value

    def fill_pO2(self,value):
        """Sets the point's pO2 value if it has None."""
        for point in self.points:
            if point.state.pO2 == None: point.state.pO2 = value

    def fill_pH2O(self,value):
        """Sets the point's pH2O value if it has None."""
        for point in self.points:
            if point.state.pH2O == None: point.state.pH2O = value
    
    def overwrite_j(self,value):
        """Overwrites the point's j value."""
        for point in self.points:
            point.j = value

    def overwrite_E(self,value):
        """Overwrites the point's E value."""
        for point in self.points:
            point.E = value

    def overwrite_T(self,value):
        """Overwrites the point's T value."""
        for point in self.points:
            point.state.T = value

    def overwrite_P(self,value):
        """Overwrites the point's P value."""
        for point in self.points:
            point.state.P = value

    def overwrite_pH2(self,value):
        """Overwrites the point's pH2 value."""
        for point in self.points:
            point.state.pH2 = value

    def overwrite_pO2(self,value):
        """Overwrites the point's pO2 value."""
        for point in self.points:
            point.state.pO2 = value

    def overwrite_pH2O(self,value):
        """Overwrites the point's pH2O value."""
        for point in self.points:
            point.state.pH2O = value

    def rescale_j(self,value):
        """Multiplies the point's j value by a factor."""
        for point in self.points:
            point.j *= value

    def rescale_E(self,value):
        """Multiplies the point's E value by a factor."""
        for point in self.points:
            point.E *= value

    def rescale_T(self,value):
        """Multiplies the point's T value by a factor."""
        for point in self.points:
            point.state.T *= value

    def rescale_P(self,value):
        """Multiplies the point's P value by a factor."""
        for point in self.points:
            point.state.P *= value

    def rescale_pH2(self,value):
        """Multiplies the point's pH2 value by a factor."""
        for point in self.points:
            point.state.pH2 *= value

    def rescale_pO2(self,value):
        """Multiplies the point's pO2 value by a factor."""
        for point in self.points:
            point.state.pO2 *= value

    def rescale_pH2O(self,value):
        """Multiplies the point's pH2O value by a factor."""
        for point in self.points:
            point.state.pH2O *= value

    def offset_j(self,value):
        """Offsets the point's j by the specified value."""
        for point in self.points:
            point.j += value

    def offset_E(self,value):
        """Offsets the point's E by the specified value."""
        for point in self.points:
            point.E += value

    def offset_T(self,value):
        """Offsets the point's T by the specified value."""
        for point in self.points:
            point.state.T += value

    def offset_P(self,value):
        """Offsets the point's P by the specified value."""
        for point in self.points:
            point.state.P += value

    def offset_pH2(self,value):
        """Offsets the point's pH2 by the specified value."""
        for point in self.points:
            point.state.pH2 += value

    def offset_pO2(self,value):
        """Offsets the point's pO2 by the specified value."""
        for point in self.points:
            point.state.pO2 += value

    def offset_pH2O(self,value):
        """Offsets the point's pH2O by the specified value."""
        for point in self.points:
            point.state.pH2O += value

    def save_txt(self,path):
        """Saves the contents of the DataManager to a text file."""
        with open(path,'w') as file:
            for point in self.points:
                file.write("{0} {1} {2} {3} {4} {5} {6}\n".format(point.j,point.E,
                    point.state.T,point.state.P,point.state.pH2,point.state.pO2,point.state.pH2O))
            file.close()

class Reader:
    """The reader class has tools to handle the import of pre-formatted data.
    
    It currently accepts csv and txt files.
    """

    def __init__(self):
        """The constructor."""
        pass

    def __trim(self,arr):
        """Removes any empty entries from a list.

            @param arr The array from which empty entries will be removed.
        """
        while('' in arr):
            arr.pop(arr.index(''))
        while(' ' in arr):
            arr.pop(arr.index(' '))
        while([] in arr):
            arr.pop(arr.index([]))
        return arr

    def read_txt(self,path):
        """Reads pre-formatted data from a txt file and returns it as a DataManager object.
            
            @param path The path where the pre-formatted txt file is stored.
            
            @return A DataManager object containing the file data.
        """
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
        """Reads pre-formatted data from a csv file.

            @param path The path where the pre-formatted csv file is stored.

            @return A dictionary containing the data.
        """
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
