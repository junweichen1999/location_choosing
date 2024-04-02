import os
import re

import geocoder
import geopandas as gpd
import pandas as pd
from geopandas.tools import sjoin
from geopy.geocoders import Nominatim
from shapely.geometry import Point


# 環域分析
def buffer_analysis(address):
    '''
    使用者地址方圓1公里設施數量

    Attributes:
        address: string
            使用者地址

    return: -> dictionary
        "address": string,
        "latitude": string,
        "longitude": string,
        "school_counts": int,
        "drink_counts": int,
        "train_counts": int,
        "bus_counts": int,
        "youbike_counts": int,
        "park_counts": int,
        "night_market_counts": int,
        "sports_facilities_counts": int,
        "mrt_counts": int,
        "movie_theater_counts": int,
        "hospital_counts": int
    
    '''

    # 輸入地址轉經緯度
    coordinates = geocoder.arcgis(address).latlng
    if coordinates:
        # 給定經度、緯度
        longitude = coordinates[1]  # 經度
        latitude = coordinates[0]  # 緯度

        # 創建中心點
        center_point = Point(longitude, latitude)
        # 建立中心點gdf
        center_gdf = gpd.GeoDataFrame(geometry=[center_point], crs="epsg:4326")
        # 設置原始數據的 CRS 為 WGS 84

        # 載入資料集
        # 指定存放CSV文件的資料夾路徑

        base_folder = os.path.abspath(os.path.dirname(__file__))

        # 雙北飲料店
        drink_df = gpd.read_file(f"{base_folder}\\Dataset\\drink.csv")
        drink_gdf = gpd.GeoDataFrame(
            drink_df,
            geometry=[Point(xy) for xy in zip(drink_df.longitude, drink_df.latitude)],
            crs="epsg:4326",
        )

        # 雙北火車
        train_df = gpd.read_file(f"{base_folder}\\Dataset\\train.csv")
        train_gdf = gpd.GeoDataFrame(
            train_df,
            geometry=[Point(xy) for xy in zip(train_df.longitude, train_df.latitude)],
            crs="epsg:4326",
        )

        # 雙北公車站
        bus_df = gpd.read_file(f"{base_folder}\\Dataset\\bus.csv")
        bus_gdf = gpd.GeoDataFrame(
            bus_df,
            geometry=[Point(xy) for xy in zip(bus_df.longitude, bus_df.latitude)],
            crs="epsg:4326",
        )

        # 雙北youbike站
        youbike_df = gpd.read_file(f"{base_folder}\\Dataset\\youbike.csv")
        youbike_gdf = gpd.GeoDataFrame(
            youbike_df,
            geometry=[
                Point(xy) for xy in zip(youbike_df.longitude, youbike_df.latitude)
            ],
            crs="epsg:4326",
        )

        # 雙北公園
        park_df = gpd.read_file(f"{base_folder}\\Dataset\\park.csv")
        park_gdf = gpd.GeoDataFrame(
            park_df,
            geometry=[Point(xy) for xy in zip(park_df.longitude, park_df.latitude)],
            crs="epsg:4326",
        )

        # 雙北夜市
        night_market_df = gpd.read_file(f"{base_folder}\\Dataset\\night_market.csv")
        night_market_gdf = gpd.GeoDataFrame(
            night_market_df,
            geometry=[
                Point(xy)
                for xy in zip(night_market_df.longitude, night_market_df.latitude)
            ],
            crs="epsg:4326",
        )

        # 雙北捷運
        mrt_df = gpd.read_file(f"{base_folder}\\Dataset\\mrt.csv")
        mrt_gdf = gpd.GeoDataFrame(
            mrt_df,
            geometry=[Point(xy) for xy in zip(mrt_df.longitude, mrt_df.latitude)],
            crs="epsg:4326",
        )

        # 雙北學校
        sports_facilities_df = gpd.read_file(
            f"{base_folder}\\Dataset\\sports_facilities.csv"
        )
        sports_facilities_gdf = gpd.GeoDataFrame(
            sports_facilities_df,
            geometry=[
                Point(xy)
                for xy in zip(
                    sports_facilities_df.longitude, sports_facilities_df.latitude
                )
            ],
            crs="epsg:4326",
        )

        # 雙北電影院
        movie_theater_df = gpd.read_file(f"{base_folder}\\Dataset\\movie_theater.csv")
        movie_theater_gdf = gpd.GeoDataFrame(
            movie_theater_df,
            geometry=[
                Point(xy)
                for xy in zip(movie_theater_df.longitude, movie_theater_df.latitude)
            ],
            crs="epsg:4326",
        )

        # 雙北學校
        school_df = gpd.read_file(f"{base_folder}\\Dataset\\school.csv")
        school_gdf = gpd.GeoDataFrame(
            school_df,
            geometry=[Point(xy) for xy in zip(school_df.longitude, school_df.latitude)],
            crs="epsg:4326",
        )

        # 雙北醫院
        hospital_df = gpd.read_file(f"{base_folder}\\Dataset\\hospital.csv")
        hospital_gdf = gpd.GeoDataFrame(
            hospital_df,
            geometry=[
                Point(xy) for xy in zip(hospital_df.longitude, hospital_df.latitude)
            ],
            crs="epsg:4326",
        )

        # 轉換坐標系統到 Web Mercator (epsg:3826(TWD97 121分帶)) 以計算以公尺為單位距離
        center_gdf = center_gdf.to_crs(epsg=3826)
        school_gdf = school_gdf.to_crs(epsg=3826)
        drink_gdf = drink_gdf.to_crs(epsg=3826)
        train_gdf = train_gdf.to_crs(epsg=3826)
        bus_gdf = bus_gdf.to_crs(epsg=3826)
        youbike_gdf = youbike_gdf.to_crs(epsg=3826)
        park_gdf = park_gdf.to_crs(epsg=3826)
        night_market_gdf = night_market_gdf.to_crs(epsg=3826)
        sports_facilities_gdf = sports_facilities_gdf.to_crs(epsg=3826)
        mrt_gdf = mrt_gdf.to_crs(epsg=3826)
        movie_theater_gdf = movie_theater_gdf.to_crs(epsg=3826)
        hospital_gdf = hospital_gdf.to_crs(epsg=3826)

        # 建立中心點的id(唯一值)
        center_gdf["shop_id"] = range(len(center_gdf))

        # 建立緩衝區(輪廓) GeoDataFrame
        buffer_gdf = gpd.GeoDataFrame(center_gdf[["shop_id", "geometry"]].copy())
        buffer_gdf["geometry"] = buffer_gdf.geometry.buffer(
            1000, resolution=99
        )  # 建立1公里緩衝區(輪廓)

        # 空間連接(join)
        school_joined_gdf = sjoin(
            buffer_gdf, school_gdf, how="inner", predicate="contains"
        )
        drink_joined_gdf = sjoin(
            buffer_gdf, drink_gdf, how="inner", predicate="contains"
        )
        train_joined_gdf = sjoin(
            buffer_gdf, train_gdf, how="inner", predicate="contains"
        )
        bus_joined_gdf = sjoin(buffer_gdf, bus_gdf, how="inner", predicate="contains")
        youbike_joined_gdf = sjoin(
            buffer_gdf, youbike_gdf, how="inner", predicate="contains"
        )
        park_joined_gdf = sjoin(buffer_gdf, park_gdf, how="inner", predicate="contains")
        night_market_joined_gdf = sjoin(
            buffer_gdf, night_market_gdf, how="inner", predicate="contains"
        )
        sports_facilities_joined_gdf = sjoin(
            buffer_gdf, sports_facilities_gdf, how="inner", predicate="contains"
        )
        mrt_joined_gdf = sjoin(buffer_gdf, mrt_gdf, how="inner", predicate="contains")
        movie_theater_joined_gdf = sjoin(
            buffer_gdf, movie_theater_gdf, how="inner", predicate="contains"
        )
        hospital_joined_gdf = sjoin(
            buffer_gdf, hospital_gdf, how="inner", predicate="contains"
        )

        # 執行統計每個緩沖區內的設施數量
        school_counts = school_joined_gdf.groupby("shop_id").size()
        drink_counts = drink_joined_gdf.groupby("shop_id").size()
        train_counts = train_joined_gdf.groupby("shop_id").size()
        bus_counts = bus_joined_gdf.groupby("shop_id").size()
        youbike_counts = youbike_joined_gdf.groupby("shop_id").size()
        park_counts = park_joined_gdf.groupby("shop_id").size()
        night_market_counts = night_market_joined_gdf.groupby("shop_id").size()
        sports_facilities_counts = sports_facilities_joined_gdf.groupby(
            "shop_id"
        ).size()
        mrt_counts = mrt_joined_gdf.groupby("shop_id").size()
        movie_theater_counts = movie_theater_joined_gdf.groupby("shop_id").size()
        hospital_counts = hospital_joined_gdf.groupby("shop_id").size()

        # 需要將計數結果與原始的多邊形 GeoDataFrame 進行合併
        # 為了確保即使是數值為 0 的多邊形也能被統計
        buffer_gdf["school_counts"] = buffer_gdf.index.map(school_counts).fillna(0)
        buffer_gdf["drink_counts"] = buffer_gdf.index.map(drink_counts).fillna(0)
        buffer_gdf["train_counts"] = buffer_gdf.index.map(train_counts).fillna(0)
        buffer_gdf["bus_counts"] = buffer_gdf.index.map(bus_counts).fillna(0)
        buffer_gdf["youbike_counts"] = buffer_gdf.index.map(youbike_counts).fillna(0)
        buffer_gdf["park_counts"] = buffer_gdf.index.map(park_counts).fillna(0)
        buffer_gdf["night_market_counts"] = buffer_gdf.index.map(
            night_market_counts
        ).fillna(0)
        buffer_gdf["sports_facilities_counts"] = buffer_gdf.index.map(
            sports_facilities_counts
        ).fillna(0)
        buffer_gdf["mrt_counts"] = buffer_gdf.index.map(mrt_counts).fillna(0)
        buffer_gdf["movie_theater_counts"] = buffer_gdf.index.map(
            movie_theater_counts
        ).fillna(0)
        buffer_gdf["hospital_counts"] = buffer_gdf.index.map(hospital_counts).fillna(0)

        # 設施數量
        school_counts = int(buffer_gdf["school_counts"].values[0])
        drink_counts = int(buffer_gdf["drink_counts"].values[0])
        train_counts = int(buffer_gdf["train_counts"].values[0])
        bus_counts = int(buffer_gdf["bus_counts"].values[0])
        youbike_counts = int(buffer_gdf["youbike_counts"].values[0])
        park_counts = int(buffer_gdf["park_counts"].values[0])
        night_market_counts = int(buffer_gdf["night_market_counts"].values[0])
        sports_facilities_counts = int(buffer_gdf["sports_facilities_counts"].values[0])
        mrt_counts = int(buffer_gdf["mrt_counts"].values[0])
        movie_theater_counts = int(buffer_gdf["movie_theater_counts"].values[0])
        hospital_counts = int(buffer_gdf["hospital_counts"].values[0])
        return {
            "address": address,
            "latitude": latitude,
            "longitude": longitude,
            "school_counts": school_counts,
            "drink_counts": drink_counts,
            "train_counts": train_counts,
            "bus_counts": bus_counts,
            "youbike_counts": youbike_counts,
            "park_counts": park_counts,
            "night_market_counts": night_market_counts,
            "sports_facilities_counts": sports_facilities_counts,
            "mrt_counts": mrt_counts,
            "movie_theater_counts": movie_theater_counts,
            "hospital_counts": hospital_counts,
        }

    else:
        return {"error": "Invalid address"}


# 取得行政區、鄰里
def user_district(address_info):

    latitude = address_info["latitude"]
    longitude = address_info["longitude"]

    # 經緯度座標轉地址
    def get_address_from_coordinates(latitude, longitude):
        geolocator = Nominatim(
            user_agent="your_app_name"
        )  # 設定你的應用程式名稱作為 user_agent
        location = geolocator.reverse(
            (latitude, longitude), language="zh-tw"
        )  # 設定查詢語言為繁體中文
        address = location.address if location else "找不到地址"
        return address

    address = get_address_from_coordinates(latitude, longitude)
    re_addess = r"(.{2}里),.(.{2}區),"
    address_search = re.search(re_addess, address)

    district = address_search[2]
    neighborhood = address_search[1]

    add_district = {"district": district, "neighborhood": neighborhood}

    address_info.update(add_district)

    return address_info


def user_data(address_district_info):
    '''
    使用者環域分析資料合併地區數值資料

    Attributes:
        address_district_info: dictionary
            使用者環域分析資料

    return: -> dictionary
        "address": string,
        "latitude": string,
        "longitude": string,
        "school_counts": int,
        "drink_counts": int,
        "train_counts": int,
        "bus_counts": int,
        "youbike_counts": int,
        "park_counts": int,
        "night_market_counts": int,
        "sports_facilities_counts": int,
        "mrt_counts": int,
        "movie_theater_counts": int,
        "hospital_counts": int
        
        add:
            "salary_income_median": int,
            "age": int,
            "people_flow_mean": int,
            "road_area_ratio": int,
            "knock_down_price_mean": int,
            "star_mean": int
    
    '''

    base_folder = os.path.abspath(os.path.dirname(__file__))

    # 地區薪資中位數
    salary_df = pd.read_csv(f"{base_folder}\\Dataset\\area\\salary.csv")
    salary_district_mask = salary_df[
        salary_df["district"] == address_district_info["district"]
    ]
    salary_neighborhood_mask = salary_district_mask[
        salary_district_mask["neighborhood"] == address_district_info["neighborhood"]
    ]
    salary_income_median = salary_neighborhood_mask["median"].iloc[0]

    # 地區平均年齡
    age_df = pd.read_csv(f"{base_folder}\\Dataset\\area\\age.csv")
    age_area_mask = age_df["district"] == address_district_info["district"]
    age = age_df.loc[age_area_mask, "age"].iloc[0]

    # 地區人流
    people_flow_mean_df = pd.read_csv(
        f"{base_folder}\\Dataset\\area\\people_flow_mean.csv"
    )
    people_flow_mean_area_mask = (
        people_flow_mean_df["district"] == address_district_info["district"]
    )
    people_flow_mean = people_flow_mean_df.loc[
        people_flow_mean_area_mask, "people_flow_mean"
    ].iloc[0]

    # 道路面積比例
    road_area_df = pd.read_csv(f"{base_folder}\\Dataset\\area\\Road_area_ratio.csv")
    road_area_mask = road_area_df["district"] == address_district_info["district"]
    road_area_ratio = road_area_df.loc[road_area_mask, "Road_area_ratio"].iloc[0]

    # 地區單坪成交租金
    knock_down_price_df = pd.read_csv(
        f"{base_folder}\\Dataset\\area\\knock_down_price_mean.csv"
    )
    knock_down_price_mask = (
        knock_down_price_df["district"] == address_district_info["district"]
    )
    knock_down_price_mean = knock_down_price_df.loc[
        knock_down_price_mask, "knock_down_price_mean"
    ].iloc[0]

    # 地區平均星數
    star_mean_df = pd.read_csv(
        f"{base_folder}\\Dataset\\area\\star_mean.csv"
    )
    star_mean_mask = (
        star_mean_df["district"] == address_district_info["district"]
    )
    star_mean = star_mean_df.loc[
        star_mean_mask, "star"
    ].iloc[0]

    add_scalar_data = {
        "salary_income_median": int(salary_income_median),
        "age": age,
        "people_flow_mean": int(people_flow_mean),
        "road_area_ratio": int(road_area_ratio),
        "knock_down_price_mean": int(knock_down_price_mean),
        "star_mean": int(star_mean)
    }

    address_district_info.update(add_scalar_data)

    return address_district_info


def drink_top10_brand(address):
    '''
    使用者地址方圓1公里前10大飲料品牌數量

    Attributes:
        address: string
            使用者地址

    return: -> dictionary
        "五十嵐": int,
        "大苑子": int,
        "珍煮丹": int,
        "先喝道": int,
        "CoCo都可": int,
        "麻古茶坊": int,
        "一沐日": int,
        "五桐號": int,
        "春水堂": int,
        "清心福全": int
    
    '''

    coordinates = geocoder.arcgis(address).latlng
    if coordinates:
        # 給定經度、緯度
        longitude = coordinates[1]  # 經度
        latitude = coordinates[0]  # 緯度

        # 創建中心點
        center_point = Point(longitude, latitude)
        # 建立中心點gdf
        center_gdf = gpd.GeoDataFrame(geometry=[center_point], crs="epsg:4326")
        # 設置原始數據的 CRS 為 WGS 84

        # 載入資料集
        # 指定存放CSV文件的資料夾路徑

        base_folder = os.path.abspath(os.path.dirname(__file__))

        # 載入各品牌地點資料
        COCO_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\COCO.csv")
        COCO_gdf = gpd.GeoDataFrame(
            COCO_df,
            geometry=[Point(xy) for xy in zip(COCO_df.longitude, COCO_df.latitude)],
            crs="epsg:4326",
        )

        五桐號_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\五桐號.csv")
        五桐號_gdf = gpd.GeoDataFrame(
            五桐號_df,
            geometry=[Point(xy) for xy in zip(五桐號_df.longitude, 五桐號_df.latitude)],
            crs="epsg:4326",
        )

        五十嵐_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\五十嵐.csv")
        五十嵐_gdf = gpd.GeoDataFrame(
            五十嵐_df,
            geometry=[Point(xy) for xy in zip(五十嵐_df.longitude, 五十嵐_df.latitude)],
            crs="epsg:4326",
        )

        大苑子_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\大苑子.csv")
        大苑子_gdf = gpd.GeoDataFrame(
            大苑子_df,
            geometry=[Point(xy) for xy in zip(大苑子_df.longitude, 大苑子_df.latitude)],
            crs="epsg:4326",
        )

        先喝道_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\先喝道.csv")
        先喝道_gdf = gpd.GeoDataFrame(
            先喝道_df,
            geometry=[Point(xy) for xy in zip(先喝道_df.longitude, 先喝道_df.latitude)],
            crs="epsg:4326",
        )

        麻古茶坊_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\麻古茶坊.csv")
        麻古茶坊_gdf = gpd.GeoDataFrame(
            麻古茶坊_df,
            geometry=[Point(xy) for xy in zip(麻古茶坊_df.longitude, 麻古茶坊_df.latitude)],
            crs="epsg:4326",
        )

        一沐日_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\一沐日.csv")
        一沐日_gdf = gpd.GeoDataFrame(
            一沐日_df,
            geometry=[Point(xy) for xy in zip(一沐日_df.longitude, 一沐日_df.latitude)],
            crs="epsg:4326",
        )

        春水堂_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\春水堂.csv")
        春水堂_gdf = gpd.GeoDataFrame(
            春水堂_df,
            geometry=[Point(xy) for xy in zip(春水堂_df.longitude, 春水堂_df.latitude)],
            crs="epsg:4326",
        )

        清心福全_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\清心福全.csv")
        清心福全_gdf = gpd.GeoDataFrame(
            清心福全_df,
            geometry=[Point(xy) for xy in zip(清心福全_df.longitude, 清心福全_df.latitude)],
            crs="epsg:4326",
        )

        珍煮丹_df = gpd.read_file(f"{base_folder}\\Dataset\\top10\\珍煮丹.csv")
        珍煮丹_gdf = gpd.GeoDataFrame(
            珍煮丹_df,
            geometry=[Point(xy) for xy in zip(珍煮丹_df.longitude, 珍煮丹_df.latitude)],
            crs="epsg:4326",
        )

        # 轉換坐標系統到 Web Mercator (epsg:3826(TWD97 121分帶)) 以計算以公尺為單位距離
        center_gdf = center_gdf.to_crs(epsg=3826)
        COCO_gdf = COCO_gdf.to_crs(epsg=3826)
        五桐號_gdf = 五桐號_gdf.to_crs(epsg=3826)
        五十嵐_gdf = 五十嵐_gdf.to_crs(epsg=3826)
        大苑子_gdf = 大苑子_gdf.to_crs(epsg=3826)
        先喝道_gdf = 先喝道_gdf.to_crs(epsg=3826)
        麻古茶坊_gdf = 麻古茶坊_gdf.to_crs(epsg=3826)
        一沐日_gdf = 一沐日_gdf.to_crs(epsg=3826)
        春水堂_gdf = 春水堂_gdf.to_crs(epsg=3826)
        清心福全_gdf = 清心福全_gdf.to_crs(epsg=3826)
        珍煮丹_gdf = 珍煮丹_gdf.to_crs(epsg=3826)

        # 建立中心點的id(唯一值)
        center_gdf["shop_id"] = range(len(center_gdf))

        # 建立緩衝區(輪廓) GeoDataFrame
        buffer_gdf = gpd.GeoDataFrame(center_gdf[["shop_id", "geometry"]].copy())
        # 建立1公里緩衝區(輪廓)
        buffer_gdf["geometry"] = buffer_gdf.geometry.buffer(
            1000, resolution=99
        )  

        # 空間連接(join)
        COCO_gdf_joined_gdf = sjoin(
            buffer_gdf, COCO_gdf, how="inner", predicate="contains"
        )  
    
        五十嵐_gdf_joined_gdf = sjoin(
            buffer_gdf, 五十嵐_gdf, how="inner", predicate="contains"
        )  

        大苑子_gdf_joined_gdf = sjoin(
            buffer_gdf, 大苑子_gdf, how="inner", predicate="contains"
        )  

        先喝道_gdf_joined_gdf = sjoin(
            buffer_gdf, 先喝道_gdf, how="inner", predicate="contains"
        )  

        麻古茶坊_gdf_joined_gdf = sjoin(
            buffer_gdf, 麻古茶坊_gdf, how="inner", predicate="contains"
        )  

        一沐日_gdf_joined_gdf = sjoin(
            buffer_gdf, 一沐日_gdf, how="inner", predicate="contains"
        )  

        春水堂_gdf_joined_gdf = sjoin(
            buffer_gdf, 春水堂_gdf, how="inner", predicate="contains"
        ) 

        五桐號_gdf_joined_gdf = sjoin(
            buffer_gdf, 五桐號_gdf, how="inner", predicate="contains"
        )  

        清心福全_gdf_joined_gdf = sjoin(
            buffer_gdf, 清心福全_gdf, how="inner", predicate="contains"
        )  

        珍煮丹_gdf_joined_gdf = sjoin(
            buffer_gdf, 珍煮丹_gdf, how="inner", predicate="contains"
        )

        # 執行統計每個緩沖區內的設施數量
        coco_counts = COCO_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        五十嵐_counts = 五十嵐_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        大苑子_counts = 大苑子_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        先喝道_counts = 先喝道_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        麻古茶坊_counts = 麻古茶坊_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        一沐日_counts = 一沐日_gdf_joined_gdf.groupby(
            "shop_id"
        ).size() 
        春水堂_counts = 春水堂_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        清心福全_counts = 清心福全_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        珍煮丹_counts = 珍煮丹_gdf_joined_gdf.groupby(
            "shop_id"
        ).size()  
        五桐號_counts = 五桐號_gdf_joined_gdf.groupby("shop_id").size()

        # 需要將計數結果與原始的多邊形 GeoDataFrame 進行合併
        # 為了確保即使是數值為 0 的多邊形也能被統計
        buffer_gdf["coco_counts"] = buffer_gdf.index.map(coco_counts).fillna(0)
        buffer_gdf["五十嵐_counts"] = buffer_gdf.index.map(五十嵐_counts).fillna(0)
        buffer_gdf["大苑子_counts"] = buffer_gdf.index.map(大苑子_counts).fillna(0)
        buffer_gdf["先喝道_counts"] = buffer_gdf.index.map(先喝道_counts).fillna(0)
        buffer_gdf["麻古茶坊_counts"] = buffer_gdf.index.map(麻古茶坊_counts).fillna(0)
        buffer_gdf["一沐日_counts"] = buffer_gdf.index.map(一沐日_counts).fillna(0)
        buffer_gdf["春水堂_counts"] = buffer_gdf.index.map(春水堂_counts).fillna(0)
        buffer_gdf["清心福全_counts"] = buffer_gdf.index.map(清心福全_counts).fillna(0)
        buffer_gdf["珍煮丹_counts"] = buffer_gdf.index.map(珍煮丹_counts).fillna(0)
        buffer_gdf["五桐號_counts"] = buffer_gdf.index.map(五桐號_counts).fillna(0)

        # 設施數量
        coco_counts = int(buffer_gdf["coco_counts"].values[0])
        五十嵐_counts = int(buffer_gdf["五十嵐_counts"].values[0])
        大苑子_counts = int(buffer_gdf["大苑子_counts"].values[0])
        先喝道_counts = int(buffer_gdf["先喝道_counts"].values[0])
        麻古茶坊_counts = int(buffer_gdf["麻古茶坊_counts"].values[0])
        一沐日_counts = int(buffer_gdf["一沐日_counts"].values[0])
        春水堂_counts = int(buffer_gdf["春水堂_counts"].values[0])
        清心福全_counts = int(buffer_gdf["清心福全_counts"].values[0])
        珍煮丹_counts = int(buffer_gdf["珍煮丹_counts"].values[0])
        五桐號_counts = int(buffer_gdf["五桐號_counts"].values[0])

        # print(
        #     {
        #         "50嵐": 五十嵐_counts,
        #         "大苑子": 大苑子_counts,
        #         "珍煮丹": 珍煮丹_counts,
        #         "先喝道": 先喝道_counts,
        #         "CoCo都可": coco_counts,
        #         "麻古茶坊": 麻古茶坊_counts,
        #         "一沐日": 一沐日_counts,
        #         "五桐號": 五桐號_counts,
        #         "春水堂": 春水堂_counts,
        #         "清心福全": 清心福全_counts,
        #     }
        # )

        return {
                "五十嵐": 五十嵐_counts,
                "大苑子": 大苑子_counts,
                "珍煮丹": 珍煮丹_counts,
                "先喝道": 先喝道_counts,
                "CoCo都可": coco_counts,
                "麻古茶坊": 麻古茶坊_counts,
                "一沐日": 一沐日_counts,
                "五桐號": 五桐號_counts,
                "春水堂": 春水堂_counts,
                "清心福全": 清心福全_counts,
                }
    else:
        return {"error": "Invalid address"}

