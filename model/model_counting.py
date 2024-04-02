import os
import numpy as np
from joblib import load
import gis.data_analysis as gis


def model_pred(address):
    '''
    使用者地址 -> 預測該地址分數

    Attributes:
        address: string
            使用者地址

    return: -> dictionary
        reccomanding_grade = {"pred_point": pred_point}
            exmple: reccomanding_grade[key] = "推薦"
    '''

    base_folder = os.path.abspath(os.path.dirname(__file__))

    # 載入模型
    model = load(f"{base_folder}\\XGBoost model_best.joblib")
    
    # 環域分析
    address_info = gis.buffer_analysis(address)
    address_district_info = gis.user_district(address_info)
    user_full_data = gis.user_data(address_district_info)

    # 模型特徵準備
    user_info = np.array(
        [
            [
                3,
                user_full_data["school_counts"],
                user_full_data["drink_counts"],
                user_full_data["train_counts"],
                user_full_data["youbike_counts"],
                user_full_data["bus_counts"],
                user_full_data["park_counts"],
                user_full_data["night_market_counts"],
                user_full_data["sports_facilities_counts"],
                user_full_data["mrt_counts"],
                user_full_data["movie_theater_counts"],
                user_full_data["hospital_counts"],
                user_full_data["salary_income_median"],
                user_full_data["people_flow_mean"],
                user_full_data["knock_down_price_mean"],
                2,
                user_full_data["road_area_ratio"],
                user_full_data["age"],
                50,
            ]
        ]
    )
    # 注意：這裡的數據應該與模型訓練時的格式相匹配

    # 模型預測
    pred_point = model.predict(user_info)

    reccomanding_grade = {"pred_point": pred_point[0]}
    # print(reccomanding_grade)

    # 分數轉換成文字顯示
    for key, value in reccomanding_grade.items():
        reccomanding_grade[key] = int(value)

    if reccomanding_grade[key] == 0:
        reccomanding_grade[key] = "極度不推薦"
        return reccomanding_grade
    
    elif reccomanding_grade[key] == 1:
        reccomanding_grade[key] = "不推薦"
        return reccomanding_grade
    
    elif reccomanding_grade[key] == 2:
        reccomanding_grade[key] = "普通"
        return reccomanding_grade
    
    elif reccomanding_grade[key] == 3:
        reccomanding_grade[key] = "推薦"
        return reccomanding_grade
    
    else:
        reccomanding_grade[key] = "極度推薦"
        return reccomanding_grade

