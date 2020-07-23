from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
import numpy as np
from time import strftime,gmtime
 
dt_gmt = strftime("%d-%m-%Y %H:%M:%S", gmtime())
dt_gmt_2 = strftime("%d-%m-%Y %Hh %Mm %Ssec", gmtime())

def counter(counter):
    """
    ---What it does---
    Counter system to show progress of function
    """
    counter += 1
    sys.stdout.write("\r {0} %".format(counter))
    sys.stdout.flush()

def to_ML (df, label):
    """
    ---What it does---
    Creates a XGBClassifier model. Printing the overall accuracy and a classification report to asess performance.
    ---What it needs---
        + A df object with numerical columns (by default named 'time', 'duration', 'lenght' and 'lb_protocol').
        + The necessary libraries for XGBClassifier to work
            * confusion_matrix (sklearn)
            * MinMaxScaler (sklearn)
            * train_test_split (sklearn)
            * classification_report (sklearn)
            * XGBClassifier (xgboost)
        + The target to predict (label)
    ---What it returns---
    The XGBClassifier model with learning_rate = 0.5
    """
    
    # Splittig of data
    columns = ['time', 'duration', 'length', 'lb_protocol', 'lb_type_of_attack', 'lb_machine', 'lb_flag']
    if label in columns:
        columns.remove(label)

    X = df[columns]
    y = df[label]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    balance_ratio = dict(y.value_counts())
    print(f'Predicting {label} in data:')
    print(f'Classes in dataframe {balance_ratio}')
    
    for n in balance_ratio.keys():
        print(f"\t- Class {n} represents {round(balance_ratio[n]*100/sum(balance_ratio.values()) , 2)} % of the whole data")
    print('\n')

    # Scaling data
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Creation of the model
    xgb_model = XGBClassifier(learning_rate=0.5)
    xgb_model.fit(X_train, y_train)

    # Reporting on performance
    y_pred = xgb_model.predict(X_test)
    m = confusion_matrix(y_test, y_pred)

    shape = np.array(m.shape)[0]
    diag = 0
    diag_list = []
    while (diag < shape).all():
        diag_list.append(diag)
        diag = diag + 1
         
    diagonal_sum = 0
    for n in diag_list:
        diagonal_sum += m[n,n]

    precission = diagonal_sum / (m.sum())

    print("Classification Report")
    print(classification_report(y_test, y_pred))
    print(f"Overall accuracy: {round(precission*100, 2)}%")

    return xgb_model

def to_ML_attack (df, label):
    """
    ---What it does---
    Creates a XGBClassifier model. Printing the overall accuracy and a classification report to asess performance.
    ---What it needs---
        + A df object with numerical columns (by default named 'time', 'duration', 'lenght' and 'lb_protocol').
        + The necessary libraries for XGBClassifier to work
            * confusion_matrix (sklearn)
            * MinMaxScaler (sklearn)
            * train_test_split (sklearn)
            * classification_report (sklearn)
            * XGBClassifier (xgboost)
    ---What it returns---
    The XGBClassifier model with learning_rate = 0.5
    """
    
    # Splittig of data
    df = df.loc[df.attack ==1]
    columns = ['time', 'duration', 'length', 'lb_protocol', 'lb_type_of_attack', 'lb_machine', 'lb_flag']
    if label in columns:
        columns.remove(label)

    X = df[columns]
    y = df[label]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    balance_ratio = dict(y.value_counts())
    print(f'Predicting {label} in data:')
    print(f'Classes in dataframe {balance_ratio}')
    
    for n in balance_ratio.keys():
        print(f"\t- Class {n} represents {round(balance_ratio[n]*100/sum(balance_ratio.values()) , 2)} % of the whole data")
    
    print('\n')

    # Scaling data
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Creation of the model
    xgb_model = XGBClassifier(learning_rate=0.5)
    xgb_model.fit(X_train, y_train)

    # Reporting on performance
    y_pred = xgb_model.predict(X_test)
    m = confusion_matrix(y_test, y_pred)
    
    shape = np.array(m.shape)[0]
    diag = 0
    diag_list = []
    while (diag < shape).all():
        diag_list.append(diag)
        diag = diag + 1
         
    diagonal_sum = 0
    for n in diag_list:
        diagonal_sum += m[n,n]

    precission = diagonal_sum / (m.sum())

    print("Classification Report")
    print(classification_report(y_test, y_pred))
    print(f"Overall accuracy: {round(precission*100, 2)}%")

    return xgb_model

def predict_what (to_predict, label, model):
    """
    ---What it does---
    Predicts the label of the df using the model provided.

    ---What it needs---
        + A given row to predict
        + The label to predict
        + The model to use

    ---What it returns---
    The prediction (y_pred)
    """

    real_class = to_predict[label]
    columns = ['time', 'duration', 'length', 'lb_protocol', 'lb_type_of_attack', 'lb_machine', 'lb_flag']
    
    if label in columns:
        columns.remove(label)
    
    to_predict = to_predict[columns].astype('double')
    
    y_pred = model.predict(to_predict)

    return y_pred

def report_maker(machine, type_attack, info):
    """
                        ---What it does---
    Writes a simple attack report and saves it in the same directory of the program.

                        ---What it needs---
        + A choice made by input. It needs to be expressed thusly: y or Y
    """
    choice = input("Do you wish a report of the last attack to be saved? (Y/N)> ")

    if choice == 'y' or choice == 'Y':  
        f= open(f"Attack report {dt_gmt_2}.txt","w+")

        f.write(f"\t\t\t---Attack report {dt_gmt}---\n")
        f.write(f"Attack {type_attack} produced to a {machine} machine\n")
        f.write(f"Valuable info:\n\n{info}")
        f.close()