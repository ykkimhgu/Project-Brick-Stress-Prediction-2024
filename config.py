from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
# -----------------------------------Time config-------------------------------------#
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 예: 20240427_153045

# -----------------------------------Folder Path-------------------------------------#


# train path
train_inputExcel_path   = "data/train/input/excel/trainData.xlsx"
train_inputImage_path   = "data/train/input/image/" 
train_output_path       = f"data/train/output/model/model_{current_time}.joblib"


# test path
test_inputExcel_path   = "data/test/input/excel/testData.xlsx"
test_inputImage_path   = "data/test/input/image/"
test_model_path        = f"data/train/output/model/model_20241212_165536.joblib"
test_output_path   = "data/test/output/"


# -------------------------------------mode select----------------------------------#
MIM_VALUE = 0
MAX_VALUE = 0


# 데이터 컬럼 이름 정의
column_names = [
    "Cement", "Sand", "Crushed Gravel", "Water", "Foaming Agent", "Water-Reducing Agent", 
    "Fly Ash", "Silica Fume", "Ground Granulated Blast-Furnace Slag (GGBFS)", "Fiber", 
    "Weight", "Void Pixel Ratio", "Mean", "Variance", "Standard Deviation", 
    "Skewness", "Kurtosis", "Entropy", "Contrast", "Energy", "Uniformity", "Correlation"
]


# Material Types
material_types = ["WR", "BFS", "Orin", "W", "F", "deF", "SF", "gSF", "FA"]