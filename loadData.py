import pandas as pd
import cv2
import numpy as np
from scipy.stats import kurtosis

import os

from skimage.feature import graycomatrix, graycoprops
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from scipy.stats import skew, kurtosis
from sklearn.preprocessing import MinMaxScaler
from joblib import dump, load

# 1. 재료구성 데이터 로드 함수
def load_excel_data(file_path, mode):

    try:
        print("엑셀 데이터 로드중......")
        df = pd.read_excel(file_path, skiprows=2, header=None) # 엑셀데이터 로드
        data = df.to_numpy()
        brick_num = len(data[:, 0])          # 벽돌 넘버
        comp_brick = data[:, 1:12]           # 재료 구성 데이터
        # 재료구성 데이터 비율 --> 무게[g]
        for i in range(brick_num):
            comp_brick[i, :10] = comp_brick[i, 10] * comp_brick[i, :10] / np.sum(comp_brick[i, :10])

        print("엑셀 데이터 로드 완료")
        if mode == "train":
            # 압축강도
            fc = data[:, 12]
            return brick_num, comp_brick, fc
        elif mode == "test":
            return brick_num, comp_brick
        

        
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
    


    
# 2. 이미지 데이터 로드 함수
def LoadProcessingImage(brick_num, folder_path):


    stat_features = {
        "numair": np.zeros((1, 4)),
        "mean": np.zeros((1, 4)),
        "variance": np.zeros((1, 4)),
        "std_dev": np.zeros((1, 4)),
        "skewness": np.zeros((1, 4)),
        "kurtosis": np.zeros((1, 4)),
        "entropy": np.zeros((1, 4)),
        "contrast": np.zeros((1, 4)),
        "energy": np.zeros((1, 4)),
        "homogeneity": np.zeros((1, 4)),
        "correlation": np.zeros((1, 4))
    }


    score_features = {
        "numair":       np.zeros((1, brick_num)),
        "mean":         np.zeros((1, brick_num)),
        "variance":     np.zeros((1, brick_num)),
        "std_dev":      np.zeros((1, brick_num)),
        "skewness":     np.zeros((1, brick_num)),
        "kurtosis":     np.zeros((1, brick_num)),
        "entropy":      np.zeros((1, brick_num)),
        "contrast":     np.zeros((1, brick_num)),
        "energy":       np.zeros((1, brick_num)),
        "homogeneity":  np.zeros((1, brick_num)),
        "correlation":  np.zeros((1, brick_num))
    }



    try:
        print("이미지 데이터 로드중......")
         # 이미지 특징 추출
        for i in range(brick_num):  # 벽돌개수
            for j in range(4):  # 면 (1~4)
                # 이미지 읽기
                image_name  = f"{i+1}-{j+1}.jpg"
                image_path  = os.path.join(folder_path, image_name)
                brick_im    = cv2.imread(image_path)
                if brick_im is None:
                    print(f"이미지를 불러올 수 없습니다: {image_path}")
                    continue

                # Grayscale 변환
                gBrick          = cv2.cvtColor(brick_im, cv2.COLOR_BGR2RGB)
                gBrick          = cv2.cvtColor(gBrick, cv2.COLOR_RGB2GRAY)
                col, row        = gBrick.shape
                image_double    = gBrick.astype(np.float64)

                # 이진화 처리
                threshold   = threshold_otsu(gBrick)  # Otsu threshold
                binary_img  = gBrick > threshold
                
                # 공극계산
                stat_features["numair"][0, j] = np.sum(binary_img == 0) / (col * row)
                

                img_normalized = (gBrick - gBrick.min()) / (gBrick.max() - gBrick.min()) * 7  # 픽셀 값을 0~7로 정규화
                img_normalized = img_normalized.astype(np.uint8) 

                glcm = graycomatrix(img_normalized, distances=[1], angles=[0], levels=8, symmetric=False, normed=False)
                

                # 통계 계산
                stat_features["mean"][0, j]         = np.mean(image_double)
                stat_features["variance"][0, j]     = np.var(image_double)
                stat_features["std_dev"][0, j]      = np.std(image_double)
                stat_features["skewness"][0, j]     = skew(image_double.flatten())
                stat_features["kurtosis"][0, j]     = kurtosis(image_double.flatten(), fisher=False)

                # entropy calculate
                img_array = np.array(gBrick)

                # 픽셀 값 히스토그램 계산 (256 레벨)
                hist, _ = np.histogram(img_array, bins=256, range=(0, 256))

                # 픽셀 확률 계산 (총 픽셀 수로 나눔)
                probabilities = hist / hist.sum()

                # 확률 값 중 0이 아닌 값만 사용
                probabilities = probabilities[probabilities > 0]
                stat_features["entropy"][0, j] = -np.sum(probabilities * np.log2(probabilities))

                # GLCM 특징
                props = ["contrast", "energy", "homogeneity", "correlation"]
                for prop in props:
                    stat_features[prop][0, j] = graycoprops(glcm, prop)[0, 0]

            # 샘플당 평균 점수 계산
            for key in stat_features.keys():
                score_features[key][0, i] = np.mean(stat_features[key])

        for key in stat_features.keys():
            score_features[key] = score_features[key].flatten()

        matrix      = np.column_stack([value for value in score_features.values()])
        print("이미지 데이터 로드 완료")

        return matrix
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
    except Exception as e:
        print(f"Error processing images: {e}")
        return None
    
# 3. 전체 학습 데이터 로드 함수
def data_load(excel_path, image_path, mode):

    try:
        if mode == "train":
            brick_num, comp_brick, fc = load_excel_data(excel_path, mode)
        elif mode == "test":
            brick_num, comp_brick = load_excel_data(excel_path, mode)

        image_data =  LoadProcessingImage(brick_num, image_path)
        comp_brick  = np.hstack([comp_brick, image_data])

        print("전체 데이터 로드 완료")
        
        if mode == "train":
            scaler      = MinMaxScaler()
            X_norm      = scaler.fit_transform(comp_brick)

            # 스케일러 저장
            dump(scaler, 'scaler.save')  # 'scaler.save' 파일에 저장

            return X_norm, fc
        
        elif mode == "test":
            scaler      = load('scaler.save')
            X_norm      = scaler.transform(comp_brick)
            return X_norm
        
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
