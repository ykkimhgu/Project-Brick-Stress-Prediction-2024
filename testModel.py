import pandas as pd

import numpy as np
from scipy.stats import kurtosis

from config import *

from skimage.filters import threshold_otsu

from sklearn.feature_selection import RFECV
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

# 1. 데이터 선택 함수
def FeatureSelection_test(x):

    try:
        
        data = x[:, [0, 3, 8, 15]]
        
        return data
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

    
# 2. 결과 출력
def modelResult_test(model, x_test):

    try:
        data = FeatureSelection_test(x_test)
        y_pred  = model.predict(data)

        print("-----------------------------------------[공극률]---------------------------------------")
        print(x_test[:, 11])
        print("----------------------------------------------------------------------------------------\n")
        print("------------------------------------[Predict_value]----------------------------------")
        print(y_pred)
        print("----------------------------------------------------------------------------------------\n")

        return  None

    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
