import numpy as np
import sys
import pandas as pd
import csv
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression , LogisticRegression
from sklearn.model_selection import train_test_split


def main():

    model_type = LinearRegression

    evidence , labels = load_data_from_dataset()
    x_train , x_test , y_train , y_test = train_test_split(evidence , labels , test_size=0.4)
    model = RandomForestRegressor(random_state=1)
    model.fit(x_train , y_train)
    predictions = model.predict(x_test) 

    

    error = []
    for label, prediction in zip(y_test, predictions):
       
        err = (label - prediction)**2
        error.append(err)

    
    
    print(predictions)
    

    plt.plot( error)
    plt.show()
     
    


def load_data_from_dataset():

    evidence=[]
    labels=[]
    with open("dataset.csv") as file:
        reader=csv.reader(file)
        next(reader)
        for row in reader:
            #0 for yes and 1 for no
            evidence.append([
                            int(row[0]),
                            int(row[1]),
                            int(row[2]),
                            int(row[3]),
                            float(row[4]),
                            float(row[5]),
                            float(row[6]),
                            int(row[7]),
                            ])
            labels.append(int(row[8]))
    
    return (evidence , labels)



    

if __name__ == "__main__":
    main()