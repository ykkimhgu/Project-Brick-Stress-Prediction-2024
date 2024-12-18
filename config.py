from datetime import datetime
# -----------------------------------Time config-------------------------------------#
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 예: 20240427_153045

# -----------------------------------Folder Path-------------------------------------#
# Mode select : train or test
mode = "test"

# -----------------------------------Folder Path-------------------------------------#


# train path
train_inputExcel_path   = "data/train/input/excel/trainData.xlsx"
train_inputImage_path   = "data/train/input/image/" 
train_output_path       = f"data/train/output/model/model_{current_time}.joblib"


# test path
test_inputExcel_path   = "data/test/input/excel/testData.xlsx"
test_inputImage_path   = "data/test/input/image/"
test_model_path        = f"data/train/output/model/model_20241217_164408.joblib"
test_output_path       = f"data/test/output/{current_time}_predictResult.xlsx"
