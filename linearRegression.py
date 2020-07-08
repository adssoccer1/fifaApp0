import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

def initLinearRegModelOverall(dataSet, instance):

    df = pd.DataFrame.from_records(dataSet)
    print(df)
    overall = df[48].copy()
    potential = df[49].copy()
    print(overall.head(10))
    print(potential.head(10))
    df = df.drop(df.columns[[46, 47, 48, 49, 50, 51, 52, 53]], axis=1) 
    print(df.head(10))

    X_train, X_test, y_train, y_test = train_test_split(df, overall, test_size=0.2, random_state=42)
    lin_regOverall = LinearRegression()
    lin_regOverall.fit(X_train, y_train)

    X_train, X_test, y_train, y_test = train_test_split(df, potential, test_size=0.2, random_state=42)
    lin_regPotential = LinearRegression()
    lin_regPotential.fit(X_train, y_train)

    predOverall = lin_regOverall.predict([df.iloc[instance]])
    predPotential = lin_regPotential.predict([df.iloc[instance]])
    print (predOverall[0], " LLOOOK HERE")
    return predOverall[0], predPotential[0] 
    
    """
    print(y_pred)
    lin_mse = mean_squared_error(y_test, y_pred)
    print("LINEAR REGRESSION")
    print("mean squared error: " , lin_mse)
    lin_rmse = np.sqrt(lin_mse)
    print("root mean squared error: " , lin_rmse)
    lin_mae = mean_absolute_error(y_test, y_pred)
    print("mean absolute error: " , lin_mae, "\n")
    #cross validation on the linear regression model
    from sklearn.model_selection import cross_val_score
    lin_scores = cross_val_score(lin_reg, X_train, y_train, scoring="neg_mean_squared_error", cv=10)
    lin_rmse_scores = np.sqrt(-lin_scores)
    """

