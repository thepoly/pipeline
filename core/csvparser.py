import csv
import sys

import numpy as np
import plotly.graph_objs as go
import plotly.offline as ply

#import plotly
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

def csv_parse(file_name):
    with open('temp.csv', 'r') as importedTable:
        csv_reader = csv.reader(importedTable, delimiter=',')
        myList = list(csv_reader)
    
    headers = myList[0]
    myList.remove(myList[0])
    return headers, myList

if __name__ == "__main__":
    with open('temp.csv', 'r') as importedTable:
        csv_reader = csv.reader(importedTable, delimiter=',')
        myList = list(csv_reader)
    
    headers = myList[0]
    myList.remove(myList[0])
    
    
    
    # print(myList)
    x = []
    y = []
    for i in range(len(myList)):
        x[i] = myList[i][0]
        y[i] = mylist[i][1]
        
    np_x = np.array(x)
    np_y = np.array(y)
    
    
    
    iplot([{x_header : x_values, y_header : y_values}])
    
        
    
        