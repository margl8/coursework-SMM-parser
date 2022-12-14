import os
import pandas as pd
import time

from flask import Flask, render_template, url_for, request
from src.vk_group import VkGroup
from datetime import datetime

app = Flask(__name__)


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/docs')
def docs():
    return render_template("docs.html")


@app.route('/tool')
@app.route('/tool/id', methods=['POST', 'GET'])
def id():
    if request.method == "POST":
        group_link = request.form.get("group_link")
        group_link = group_link.replace('https://vk.com/', '')
        return render_template("tool/id.html", group_id=VkGroup.get_id(group_link))
    else:
        return render_template("tool/id.html")


@app.route('/tool')
@app.route('/tool/members', methods=['POST', 'GET'])
def members():
    if request.method == "POST":
        group_link = request.form.get("group_link").strip(' ')
        screen_name = group_link.replace('https://vk.com/', '')
        id = VkGroup.get_id(screen_name)
        group = VkGroup()
        group(id)
        return render_template("tool/members.html", members=group.get_members())
    else:
        return render_template("tool/members.html")


@app.route('/tool')
@app.route('/tool/report', methods=['POST', 'GET'])
def report():
    today = datetime.now().strftime("%Y-%m-%d")
    min_date = datetime(datetime.now().year, datetime.now().month - 2, 1).strftime("%Y-%m-%d")
    if request.method == "POST":
        group_link = request.form.get("group_link").strip(' ')
        screen_name = group_link.replace('https://vk.com/', '')
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        id = VkGroup.get_id(screen_name)
        group = VkGroup()
        group(id)
        group.get_posts_by_date(start_date, end_date)
        output_file = group.get_report()
        return render_template("tool/report.html", today=today, min_date=min_date, output_file=output_file)
    else:
        return render_template("tool/report.html", today=today, min_date=min_date)


@app.route('/tool')
@app.route('/tool/monitor', methods=['POST', 'GET'])
def monitor():
    if request.method == "POST":
        group = VkGroup()
        file = request.form.get("file")
        df = pd.read_csv(file, header=0)
        groups_report = pd.DataFrame()
        lst = []
        rep = pd.DataFrame(group.__dict__)
        def proceed(id):
            # программа получает ID группы
            group(id)
            # собирает посты за ноябрь
            group.get_posts_by_date('01-11-2022', '30-11-2022')
            print(group)
            group.get_report()
        for index, row in df.iterrows():
            try:
                proceed(VkGroup.get_id(row['screen_name']))
            except TypeError:
                time.sleep(0.5)
                proceed(VkGroup.get_id(row['screen_name']))
            except KeyError:
                time.sleep(0.5)
                proceed(VkGroup.get_id(row['screen_name']))
            finally:
                rep.loc[len(rep)] = group.__dict__
        rep.drop(columns=['posts'], axis=1)
        rep.to_excel(f'./!ALL_GROUPS_REPORT.xlsx',
                     header=True, index=False)
        return render_template("tool/monitor.html")
    else:
        return render_template("tool/monitor.html")


if __name__ == "__main__":
    app.run('0.0.0.0', port=5001, debug=True)
