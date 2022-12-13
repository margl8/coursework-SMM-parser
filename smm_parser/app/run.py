from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/docs')
def docs():
    return render_template("docs.html")


@app.route('/tool')
@app.route('/tool/id')
def id():
    return render_template("tool/id.html")


@app.route('/tool')
@app.route('/tool/members')
def members():
    return render_template("tool/members.html")


@app.route('/tool')
@app.route('/tool/monitor')
def monitor():
    return render_template("tool/monitor.html")


@app.route('/tool')
@app.route('/tool/report')
def report():
    return render_template("tool/report.html")


if __name__ == "__main__":
    app.run('0.0.0.0', port=5001, debug=True)
