# Project-Brick-Stress-Prediction-2024

## Process

### 1. download .zip file

### 2. download train image % test image
link(Test) ==> google drive link
link(train) ==> google drive link

### 3. unzip image file to folder
test ==> data/test/input/images
train ==> data/train/input/images


## folder composition
PYTHON
 - data
   - train
     - input
       - excel
         - brickData.xlsx (학습을 위한 파일)
           * 입력요소(12) : 재료구성(10) + 무게(1) + 압축강도(1)
       - images
         - 학습을 위한 이미지 데이터
           * 한 벽돌당 4개의 표면 이미지 **필요** / 이미지 네이밍: {벽돌 번호} + {벽돌 표면 번호} ex) 1-1.jpg
     - output
       - model
         - 학습된 모델
   - test
     - input
       - excel
         - brickData.xlsx (테스트를 위한 파일)
           * 입력요소(11) : 재료구성(10) + 무게(1)
       - images
         - 테스트를 위한 이미지 데이터
           * 한 벽돌당 4개의 표면 이미지 **필요** / 이미지 네이밍: {벽돌 번호} + {벽돌 표면 번호} ex) 1-1.jpg
     - output
       - excel
       - images

- main.py
 * 학습 및 테스트를 할 수 있는 코드

- testModel.py
 * test와 관련된 코드

- trainModel.py
 * train과 관련된 코드

- loadData.py
 * train과 test에 따라 데이터를 불러오는 코드

- config.py
 * folder path, model save path 등 configuration
