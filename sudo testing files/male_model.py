from cv2 import SparseMat_MAGIC_VAL
import numpy as np
import sys
import pandas as pd
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def main():

    evidence , labels = load_data_from_dataset()
    
    glucose,bp,skinthickness,insulin,bmi,dpf,age  = survey()
    d = {
            'Glucose' : glucose,
            'Bp' : bp,
            'Skin Thickness' : skinthickness,
            'Insulin' : insulin,
            'BMI' : bmi,
            'DPF' : dpf,
            'AGE' : age,
        }
    df = pd.DataFrame([d])
    df.to_csv("user_data.csv")

    testing_data = pd.read_csv("user_data.csv",index_col=False)
    testing_features = ["Glucose","Bp","Skin Thickness","Insulin","BMI","DPF","AGE"]
    test = testing_data[testing_features]

    model = RandomForestRegressor(random_state=1)
    model.fit(evidence , labels)
    print(model.predict(test    ))
    
    
    


def load_data_from_dataset():

    evidence=[]
    labels=[]
    with open("dataset.csv") as file:
        reader=csv.reader(file)
        next(reader)
        for row in reader:
            #0 for yes and 1 for no
            evidence.append([
                            
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

def survey():
    
    #pregnancy = int(input("If female, how many pregnancies have you experienced : \n "))
    glucose = int(input("Whats your blood glucode level :\n "))
    bp = int(input("Whats your current bp :\n "))
    skinthickness = int(input("skin thickness :\n"))
    insulin = int(input("Insulin level :\n "))
    bmi = float(input("Bmi:\n "))
    dpf = float(input("Diabetes Pedigree Function: \n"))
    age = int(input("Age :\n "))

    return (glucose,bp,skinthickness,insulin,bmi,dpf,age)
def test_model():
    evidence , labels = load_data_from_dataset()
    x_train , x_test , y_train , y_test = train_test_split(evidence , labels , test_size=0.4)
    model = RandomForestRegressor(random_state=1)
    model.fit(x_train , y_train)
    return model.predict(x_test)


if __name__ == "__main__":
    main()