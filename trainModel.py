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
def FeatureSelection(x, y):

    try:
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        X_train = X_train[:, [0, 3, 8, 15]]
        X_test = X_test[:, [0, 3, 8, 15]]
        
        return X_train, X_test, y_train, y_test
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

# 2. 최적화
def trainOptimization(X_train_rfecv, y_train):

    try:
        param_grid = {
            'max_depth': [3, 5, 10, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        # GridSearchCV 설정
        grid_search = GridSearchCV(
            estimator = DecisionTreeRegressor(random_state=42),
            param_grid=param_grid,
            scoring='neg_mean_squared_error',   # MSE 기반 평가
            cv = 5,                              # 5-폴드 교차 검증
            n_jobs = 1                           # 병렬 처리
        )

                # 최적의 하이퍼파라미터 탐색
        grid_search.fit(X_train_rfecv, y_train)

        # 최적의 파라미터와 성능 출력
        best_model = grid_search.best_estimator_

        
        return  best_model

    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
    
# 3. 최적화
def modelResult(model, x_test, y_test):

    try:
        y_pred  = model.predict(x_test)

        # 7. 모델 성능 및 결과 출력
        # 성능 평가
        mse     = mean_squared_error(y_test, y_pred)
        rmse    = np.sqrt(mse)
        r2      = r2_score(y_test, y_pred)
        
        print("----------------------------------[Performance of Model]--------------------------------")
        print(f"Root Mean Squared Error: {rmse:.2f}[MPa]")      # 모델 성능평가 1. Root Mean Squared Error
        print(f"R2 Score: {r2:.2f}")                            # 모델 성능평가 2  R squared
        print("----------------------------------------------------------------------------------------\n")

        
        return  None

    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
