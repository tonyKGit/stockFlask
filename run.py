from flask import Flask, jsonify
import requests
import pandas as pd
import shioaji as sj
import threading
import time
from celery import Celery
from celery.schedules import crontab
# from flask_script import Manager, Server

app = Flask(__name__)
# manager = Manager(app)

# def custom_call():
#     print('custom call')
#     pass

# class CustomServer(Server):
#     def __call__(self, app, *args, **kwargs):
#         custom_call()
#         return Server.__call__(self, app, *args, **kwargs)

# manager.add_command('runserver', CustomServer())

# if __name__ == "__main__":
#     manager.run()

abc = ''

@app.before_first_request
def activate_job():
    global abc
    abc = '789'
    # def run_job():
    #     while True:
    #         res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    #         df = pd.read_html(res.text)[0]
    #         df.columns = df.iloc[0]
    #         number = df.loc[df['有價證券代號及名稱']=='上市認購(售)權證'].index[0]
    #         df = df.iloc[2:number]
    #         df = df['有價證券代號及名稱'].str.split('　').str.get(0).str.split(' ').str.get(0)
    #         response = df.to_json(orient='values')
    #         print("Run recurring task")

    # thread = threading.Thread(target=run_job)
    # thread.start()

@app.route('/')
def index():
    # global abc
    # abc = '456'
    res = requests.get("https://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
    df = pd.read_html(res.text)[0]
    df.columns = df.iloc[0]
    number = df.loc[df['有價證券代號及名稱']=='上市認購(售)權證'].index[0]
    df = df.iloc[2:number]
    df = df['有價證券代號及名稱'].str.split('　').str.get(0).str.split(' ').str.get(0)
    response = df.to_json(orient='values')
    return response

@app.route('/login')
def login():
    api = sj.Shioaji(simulation=True)
    api.login(
        person_id="PAPIUSER01",
        passwd="2222",
        contracts_cb=lambda security_type: print(f"{repr(security_type)} fetch done.")
    )
    return 'success'

@app.route('/test')
def test():
    global abc
    return abc;