import pandas as pd
import time
from flask import Flask, render_template, request, url_for, redirect, current_app
from app.vk import Group
from app.main import bp
from datetime import datetime

@bp.route('/')
@bp.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@bp.route('/docs')
def docs():
    return render_template("docs.html")

@bp.route('/tool')
@bp.route('/tool/id', methods=['POST', 'GET'])
def id():
    if request.method == "POST":
        group_link = request.form.get("group_link")
        screen_name = Group.clear_link(group_link)
        return render_template("tool/id.html", group_id=Group.get_id(screen_name))
    else:
        return render_template("tool/id.html")


@bp.route('/tool')
@bp.route('/tool/members', methods=['POST', 'GET'])
def members():
    if request.method == "POST":
        group_link = request.form.get("group_link")
        screen_name = Group.clear_link(group_link)
        id = Group.get_id(screen_name)
        return render_template("tool/members.html",
                               members=Group.get_members(id))
    else:
        return render_template("tool/members.html")


@bp.route('/tool')
@bp.route('/tool/report', methods=['POST', 'GET'])
def report():
    today = datetime.now().strftime("%Y-%m-%d")
    min_date = datetime(datetime.now().year, datetime.now().month - 2, 1).strftime("%Y-%m-%d")
    if request.method == "POST":
        group_link = request.form.get("group_link")
        screen_name = Group.clear_link(group_link)
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        id = Group.get_id(screen_name)
        group = Group(id)
        group.get_posts_by_date(start_date, end_date)
        output_file = group.get_report()
        return render_template("tool/report.html", today=today, min_date=min_date, output_file=output_file)
    else:
        return render_template("tool/report.html", today=today, min_date=min_date)


@bp.route('/tool')
@bp.route('/tool/monitor', methods=['POST', 'GET'])
def monitor():
    if request.method == "POST":
        group = Group()
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
                proceed(Group.get_id(row['screen_name']))
            except TypeError:
                time.sleep(0.5)
                proceed(Group.get_id(row['screen_name']))
            except KeyError:
                time.sleep(0.5)
                proceed(Group.get_id(row['screen_name']))
            finally:
                rep.loc[len(rep)] = group.__dict__
        rep.drop(columns=['posts'], axis=1)
        rep.to_excel(f'./!ALL_GROUPS_REPORT.xlsx',
                     header=True, index=False)
        return render_template("tool/monitor.html")
    else:
        return render_template("tool/monitor.html")
