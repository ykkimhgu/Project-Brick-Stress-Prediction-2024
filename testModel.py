import pandas as pd
from config import *



# 1. 데이터 선택 함수
def FeatureSelection_test(x):

    try:       
        data = x[:, [0, 3, 8, 15]]
        return data
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

# 2. 결과 출력
def modelResult_test(model, x_test, comp_brick):

    try:
        data    = FeatureSelection_test(x_test)
        y_pred  = model.predict(data)

        # 데이터 저장
        length  = len(y_pred)
        columns = list(range(1, length + 1))  # 1부터 9까지
        
        comp_brick[:, 11] = [f"{value:.2f}" for value in comp_brick[:, 11]]
        y_pred = [f"{value:.2f}" for value in y_pred]
        
        out = {
            '항목': ['벽돌번호', '공극률[%]', '압축강도[MPa]'],
            **{f'열_{i+1}': [str(columns[i]), str(comp_brick[i, 11]), str(y_pred[i])] for i in range(length)}
        }

        df = pd.DataFrame(out)

        # 엑셀 파일로 저장
        output_file = test_output_path
        df.to_excel(output_file, index=False, header=True, sheet_name='Data')
        
        print(f"데이터가 '{output_file}' 파일로 저장되었습니다.")

        return  None

    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None
