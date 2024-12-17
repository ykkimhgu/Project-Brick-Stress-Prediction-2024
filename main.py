#---------------------------------------------------------------------------------------#
# Department of Mechanical & Control Engineering in Handong Global University
# Affiliation   : Industrial Intelligence LAB
# Data          : 2024-11-21 (wed)
# Author        : Yang Ji-Woo
#---------------------------------------------------------------------------------------#from dataLoad import *
from config import *
from loadData import *
from trainModel import *
from testModel import *

from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump, load

# Mode select - train or test
mode = "test"

def main():

    if mode == "train":
        print("-----------------[TRAIN] 모드입니다.--------------")
        # 1. data load
        input_data, fc = data_load(train_inputExcel_path, train_inputImage_path, mode)

        # 2. Train model
        # 2-1. select input feature
        x_train, x_test, y_train, y_test = FeatureSelection(input_data, fc)

        # 2-2 train model
        model = trainOptimization(x_train, y_train)
        
        # 2-3 Save the model
        dump(model, train_output_path)

        # 3. print out - RMSE/R^2
        modelResult(model, x_test, y_test)

    elif mode == "test":
        print("-----------------[TEST] 모드입니다.--------------")
        # 1. Test input load
        data = data_load(test_inputExcel_path, test_inputImage_path, mode)
        
        # 2. Test
        model = load(test_model_path)

        # 3. print out - y_pred, 공극률
        modelResult_test(model, data)
    else:
        print("알 수 없는 모드입니다. 'train' 또는 'test'로 설정하세요.")




if __name__ == "__main__":
    main()