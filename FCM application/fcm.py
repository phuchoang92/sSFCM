import pandas as pd
import numpy as np
from random import random




# Load data from .....
def loadData(s):
    global data
    data = pd.read_csv( s , header = None)
    #Remove NaN (not a number ) data
    data = data.select_dtypes(include=["float64", "int64"])
    
    global X,n,p
    #Matrix X 
    X = np.array(data)
    n = X.shape[0]
    p = X.shape[1]
    
def generate_V(x):
    global c, V
    c = x
    V = np.random.rand(c,p)

#-- Generate U_ngang 

# With condition
def generate_U_ngang(k1):
    global U_ngang
    U_ngang = np.zeros((n,c))
    f
        
#Random
def generate_U_ngang(k1):
    global U_ngang
    U_ngang = np.random.rand(n,c)
    sum_i = np.zeros(n) 
    # Doan nay lam tong u_ki <= 1 , i = 1,c 
    for i in range(n):
        U_ngang[i] = U_ngang[i]/sum(U_ngang[i])*random()
        sum_i[i] = sum(U_ngang[i])
