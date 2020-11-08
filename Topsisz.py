import sys
import pandas as pd
import numpy as np
import scipy.stats as ss
import os

class myexception(Exception):
      pass

def data_mat(filename,weights,impact):

    dataset = pd.read_csv(filename)
    attributes = dataset.iloc[:,1:].values

    # if (dataset.shape[1]<3):
    #     raise myexception("Input file must contain three or more columns")

    if (len(weights)!=len(impact)!=len(attributes[0][:])):
        raise myexception("Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same")

    # is_int = dataset.apply(lambda s: pd.to_numeric(s, errors='coerce').notnull().all())
    # for i in range(1,len(is_int)):
    #     if is_int[i]!=True:
    #         raise myexception("For the Given Dataset from column2 all values must be numeric")


    sum_columns = np.zeros(len(attributes[0]),dtype=float)

    for i in range (len(attributes)):
        for j in range (len(attributes[i])):
            sum_columns[j] += np.square(attributes[i][j])

    for i in range(len(sum_columns)):
        sum_columns[i]=np.sqrt(sum_columns[i]) 

    for i in range(len(attributes)):
        for j in range(len(attributes[i])):
            attributes[i][j]=attributes[i][j]/sum_columns[j]

    return (attributes)


def weight_assign(attributes,weights):
    weights=weights.split(',')
    sum_weights = 0

    sum_weights = sum(map(float,weights))
    for i in range(len(weights)):
        weights[i]=float(weights[i])/sum_weights

    weighted_attributes=[]
    for i in range(len(attributes)):
        temp=[]
        for j in range(len(attributes[i])):
            temp.append(attributes[i][j]*weights[j])
        weighted_attributes.append(temp)

    return(weighted_attributes)    


def impact_matrix(weighted_attributes,impacts):
    q =weighted_attributes
    q = np.array(q)
    q[:,0]

    Vjpositive=[0]*(len(weighted_attributes[0]))
    Vjnegative=[0]*(len(weighted_attributes[0]))

    for i in range(len(weighted_attributes[0])):
            if impacts[i]=='+':
                Vjpositive[i]=max(q[:,i])
                Vjnegative[i]=min(q[:,i])
            elif impacts[i]=='-':
                Vjpositive[i]=min(q[:,i])
                Vjnegative[i]=max(q[:,i])

    Sjpositive=[0]*len(weighted_attributes)
    Sjnegative=[0]*len(weighted_attributes)

    for i in range(len(weighted_attributes)):
        for j in range(len(weighted_attributes[i])):
            Sjpositive[i]+=np.square(weighted_attributes[i][j]-Vjpositive[j])
            Sjnegative[i]+=np.square(weighted_attributes[i][j]-Vjnegative[j])
    for i in range(len(Sjpositive)):
        Sjpositive[i]=np.sqrt(Sjpositive[i])
        Sjnegative[i]=np.sqrt(Sjnegative[i])
    Performance_score=[0]*len(weighted_attributes)
    for i in range(len(weighted_attributes)):
        Performance_score[i]=Sjnegative[i]/(Sjnegative[i]+Sjpositive[i])
    
    return(Performance_score)

def adding_data(score,filename):
    df = pd.read_csv(filename)
    df = df.assign(Topsis=score)
    df = df.assign(Rank=ss.rankdata(score))
    return (df)

def main():
    # if len(sys.argv)!=5:
    #     raise myexception("You have missed an input file..,Use : python topsis.py inputfile.csv “1,1,1,2” “+,+,-,+” result.csv")

    path=os.getcwd()
    # input_folder_name = 'Input files for Assignment06'
    # path_folder=os.path.join(path,input_folder_name)
    filename = os.path.join(path,sys.argv[1])

    if not os.path.exists(filename):
        raise myexception("file does not exists")

    
    weights = sys.argv[2]
    impacts = sys.argv[3]
    result = sys.argv[4]

    impacts=impacts.split(',')

    # for i in range(0,len(impacts)):
    #     if impacts[i]=='-':
    #         continue
    #     elif impacts[i]=='+':
    #         continue
    #     else:
    #         raise myexception("Impacts must be either +ve or -ve.")

    a = data_mat(filename,weights,impacts)
    c = weight_assign(a,weights)
    d = impact_matrix(c,impacts)
    new_dataset = adding_data(d,filename)
    new_dataset.to_csv(result) 

if __name__=='__main__':
    main()