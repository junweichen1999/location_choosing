import os
import re

import geocoder
import geopandas as gpd
import gis.data_analysis as gis
import model.model_counting as usemodel
import requests
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from geopandas.tools import sjoin
from geopy.geocoders import Nominatim
from shapely.geometry import Point
from sqlalchemy import desc
from database.db import db_settings


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:{db_settings['port']}/{db_settings['db']}?charset={db_settings['charset']}"
)

# SQLAlchemy連接FLASK
db = SQLAlchemy(app)

# 資料庫新增table
class LocationData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    school_counts = db.Column(db.Integer)
    drink_counts = db.Column(db.Integer)
    train_counts = db.Column(db.Integer)
    bus_counts = db.Column(db.Integer)
    youbike_counts = db.Column(db.Integer)
    park_counts = db.Column(db.Integer)
    night_market_counts = db.Column(db.Integer)
    sports_facilities_counts = db.Column(db.Integer)
    mrt_counts = db.Column(db.Integer)
    movie_theater_counts = db.Column(db.Integer)
    hospital_counts = db.Column(db.Integer)


# 首頁顯示
@app.route("/")
def index():
    '''
    首頁 : 使用者輸入地址查詢
    '''

    return render_template("index.html")


# 在 Flask 新增頁面
@app.route("/page2.html")
def page2():
    '''
    儀錶板頁面
    '''

    # 歷史查詢 : 從資料庫中提取最後十筆資料，以最後更新時間排序
    data_from_db = LocationData.query.order_by(desc(LocationData.id)).limit(10).all()

    # 從資料中提取地址
    search_history = [record.address for record in data_from_db]
    return render_template("page2.html", search_history=search_history)


# 在你的 Flask 應用程式中新增這個路由
@app.route("/bi.html")
def bi():
    '''
    地區視覺化分析頁面
    '''

    return render_template("bi.html")


# 使用者輸入地址資料轉換
@app.route("/get_coordinates", methods=["GET", "POST"])
def get_coordinates():
    '''
    使用者地址 : 環域分析，合併地區資料
    '''

    data = request.json
    address = data["address"]
    # print(address)
    address_info = gis.buffer_analysis(address)
    # print(address_info)
    address_district_info = gis.user_district(address_info)

    user_full_data = gis.user_data(address_district_info)

    # Create a new LocationData instance and save it to the database
    location_data = LocationData(
        address = user_full_data['address'],
        latitude = user_full_data['latitude'],
        longitude = user_full_data['longitude'],
        school_counts = user_full_data['school_counts'],
        drink_counts = user_full_data['drink_counts'],
        train_counts = user_full_data['train_counts'],
        bus_counts = user_full_data['bus_counts'],
        youbike_counts = user_full_data['youbike_counts'],
        park_counts = user_full_data['park_counts'],
        night_market_counts = user_full_data['night_market_counts'],
        sports_facilities_counts = user_full_data['sports_facilities_counts'],
        mrt_counts = user_full_data['mrt_counts'],
        movie_theater_counts = user_full_data['movie_theater_counts'],
        hospital_counts = user_full_data['hospital_counts'],
    )
    db.session.add(location_data)
    db.session.commit()

    return jsonify(user_full_data)


# 接10大飲料店  (等csv)
@app.route("/top10_brand", methods=["POST"])
def top10_brand():
    '''
    前10大指標品牌 : 環域分析
    '''

    data = request.json
    address = data["address"]  
    top10_brand = gis.drink_top10_brand(address)

    return jsonify(top10_brand)


# 送到model接model資料
@app.route("/load_and_get_model", methods=["POST"])
def load_and_get_model():
    '''
    模型預測分數
    '''

    data = request.json
    address = data["address"]
    user_pred_point = usemodel.model_pred(address)
    return jsonify(user_pred_point)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
