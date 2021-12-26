import pandas as pd
import numpy as np
import math
from random import random
import random


class FCM2():
    
    
    def __init__(self, *args, **kwargs):
        self.dict_cluster = {}
        self.c = 0
        return
   
    def read_data(self, path):
        self.data = pd.read_csv(path , header = None)
        self.data_table = np.array(self.data)
    def preprocess_data(self, col):
        
        self.value = self.data.loc[:,self.data.columns != col]
        self.value = self.value.select_dtypes(include=["float64", "int64"])
        self.label = self.data.loc[:, self.data.columns ==col]
        
        self.label_list = pd.unique(self.label[self.label.columns[0]])
        self.label_list = self.label_list.tolist()
        self.num_class = len(self.label_list)
        self.label_data =self.label[self.label.columns[0]].values.tolist()
        self.label_count = np.array(self.label[self.label.columns[0]].value_counts())
        self.X = np.array(self.value)
        self.n = self.X.shape[0]
        self.p = self.X.shape[1]

    def setC(self, i):
        self.c = i
    def generate_M(self,m,m1,k,c):
        self.M = np.zeros((self.n,self.c))
        self.index_x_giamsat = random.sample(range(self.n),k)
        index_x_giamsat = np.sort(self.index_x_giamsat)
        for i in range(self.n):
            if i in index_x_giamsat:
                if len(self.dict_cluster) == 0 :
                    c1= random.randint(0,self.c-1)
                else:
                    c1= self.dict_cluster[self.label_data[i]]
                    #Chọn vị trí cụm giám sát
                self.M[i] = m
                self.M[i][c1] = m1
            else:
                self.M[i] = m
    def generate_V(self,c):
        self.V=np.random.rand(self.c,self.p)
        self.V_truoc=self.V
    def generate_U(self,c):
        self.U=np.zeros((self.n,self.c))
    def update_D(self,n,c):
        self.D=np.zeros((self.n,self.c))
        for i in range(self.n):
            for k in range(self.c):
                self.D[i][k]=math.sqrt(sum(pow(self.X[i]-self.V[k],2)))
    def solve_mu(self,sum_mu_i,d_ik,m,m1,epsilon):
        mu = 0
        vp = pow(1/(m1*d_ik*d_ik),1/(m1-1))
        vt = -1
        left = 0.0
        right = 2.0
        while (abs(vt-vp) > epsilon):
            mu = (right + left)/2
            vt = mu/pow(mu + sum_mu_i, (m1-m)/(m1-1))  
            if vt<vp:
                left = mu
            else:
                right =mu
        return mu
    def update_U(self,m,m1,c,epsilon):
        self.update_D(self.n,c)
        for i in range(self.n):
            if i not in self.index_x_giamsat:
                for k in range(c):
                    mau_so = sum(pow( self.D[i][k] / self.D[i], 2/(m-1)))
                    self.U[i][k] = 1/mau_so
            elif i in self.index_x_giamsat:
                d_min = np.amin(self.D[i])
                d_i = self.D[i]/d_min
                mu_i = np.zeros(self.c)
                for j in range(self.c):
                    if (self.M[i][j]==m):
                        mu_i[j]=1/pow( m *d_i[j]*d_i[j] , 1/(m-1) )
                sum_mu_i=sum(mu_i)
                for j in range(self.c):
                    if (self.M[i][j]==m1):
                        mu_i[j] = self.solve_mu(sum_mu_i, d_i[j], m, m1 , epsilon)
                        # mu_i[j] = sum_mu_i
                        
                self.U[i] = mu_i/sum(mu_i)
    def update_V(self,c):
        V_temp=np.zeros((self.c,self.p))
        for k in range(self.c):
            temp=pow((self.U.T)[k],(self.M.T)[k])
            tu_so=np.zeros(self.p)
            for i in range(self.n):
                tu_so+=temp[i]*self.X[i]
            V_temp[k]=tu_so/sum(temp)
        return V_temp
    def count_class(self, num_class, num_cluster):
        self.count_class_cluster = np.zeros((num_class,num_cluster), dtype="int64")
        for k in range(self.n):
            k_class = self.label_list.index(self.label_data[k])
            index_max = np.argmax(self.U[k])
            self.count_class_cluster[k_class][index_max] +=1 
    def external_validity(self,num_class, c):
        
        a1 = b1 = c1 = d1= 0
        for i in range(num_class):
            a1+= sum ( (self.count_class_cluster[i]-1)*self.count_class_cluster[i]/2 )
            b1+= (pow(sum(self.count_class_cluster[i]),2) - sum(pow(self.count_class_cluster[i],2)) )/2
        for i in range(num_class-1):
            for j in range(i+1, num_class):
                for k in range(c):
                    c1+=self.count_class_cluster[i][k] * self.count_class_cluster[j][k]
                    for h in range(c):
                        if h!=k :
                            d1+=self.count_class_cluster[i][k] * self.count_class_cluster[j][h] 
        # Rand int
        w1 =  (a1 + d1)/ (a1 +b1 + c1 +d1)
        # Adjusted Rand Index
        M= a1 + b1 +c1 +d1
        w2 = (a1 - (a1+c1)*(a1+b1)/M) /( (2*a1+b1+c1)/2 - (a1+c1)*(a1+b1)/M )
        #Jaccard Coefficient
        w3 = a1 / (a1+b1+c1)
        self.w1=w1
        self.w2=w2
        self.w3=w3
        
        
    def set_dict_cluster(self):
        for i in range(self.num_class):
            temp = np.argmax(self.count_class_cluster[i])
            self.dict_cluster[self.label_list[i]] = temp
        return

    def rs_dict_cluster(self):
        self.dict_cluster = {}
        return   
    
    def thuat_toan_1_pha(self,m,m1,c,k,epsilon):
        self.setC(c)
        self.generate_V(c)
        self.generate_U(c)
        Epsilon = np.zeros((self.c,self.p)) + epsilon
        self.rs_dict_cluster()
        self.generate_M(m,m1,k,c)
        while True:
            self.update_U(m,m1,c,epsilon)
            self.V_truoc=self.V
            self.V=self.update_V(c)
            delta_V=abs(self.V-self.V_truoc)
            ktra = np.less_equal(delta_V, Epsilon)
            if (np.all(ktra)):
                break
        self.count_class(self.num_class, self.c)
        self.external_validity(self.num_class, self.c)       
            
            
    def thuat_toan_2_pha(self,m,m1,c,k,epsilon):
        #Pha 1
        self.thuat_toan_1_pha(m,m1,c,0,epsilon)
        self.set_dict_cluster()     
            #Pha 2 
        Epsilon = np.zeros((self.c,self.p)) + epsilon
        self.generate_M(m,m1,k,c)
        while True:
            self.update_U(m,m1,c,epsilon)
            self.V_truoc=self.V
            self.V=self.update_V(c)
            delta_V=abs(self.V-self.V_truoc)
            ktra = np.less_equal(delta_V, Epsilon)
            if (np.all(ktra)):
                break
        self.count_class(self.num_class, self.c)
        self.external_validity(self.num_class, self.c)     
        return



fcm2 = FCM2()
fcm2.read_data("E:\BackKhoaBatDiet\Project1\sSFCM\Resources\iris.data")
fcm2.preprocess_data(4)
fcm2.thuat_toan_2_pha(2, 6, 3 , 150,1e-6)
print(fcm2.w1)
print(fcm2.w2)
print(fcm2.w3)

