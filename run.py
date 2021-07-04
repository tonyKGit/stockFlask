from flask import Flask
import requests
import pandas as pd

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    df = pd.read_html(res.text)[0]
    df.columns = df.iloc[0]
    number = df.loc[df['有價證券代號及名稱']=='上市認購(售)權證'].index[0]
    number
    df = df.iloc[2:number]
    df = df['有價證券代號及名稱'].str.split('　').str.get(0).str.split(' ').str.get(0)
    response = df.to_json(orient='values')
    return response