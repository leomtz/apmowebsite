from flask import Flask, render_template
import glob, re, json
import pandas as pd

year_re=r'[0-9]{4}'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("landing.html")

@app.route('/regulations')
def regulations():
    reg_list=glob.glob("static/regulations/*.pdf")
    year=[x.split('-')[2].split('.')[0] for x in reg_list]
    reg_pairs=list(zip(year,reg_list))
    reg_pairs.sort(reverse=True)
    return render_template("regulations.html", reg_pairs=reg_pairs)

@app.route('/timeline')
def timeline():
    return render_template("timeline.html")

@app.route('/countries')
def countries():
    return render_template("countries.html")


@app.route('/problems')
def problems():
    prob_list=glob.glob("static/problems/*.pdf")
    year=[re.search(year_re,x).group(0) for x in prob_list]
    prob_pairs=list(zip(year,prob_list))
    prob_pairs.sort(reverse=True)

    sol_list=glob.glob("static/solutions/*.pdf")
    year=[re.search(year_re,x).group(0) for x in sol_list]
    sol_pairs=list(zip(year,sol_list))
    sol_pairs.sort(reverse=True)
    return render_template("problems.html", prob_pairs=prob_pairs, sol_pairs=sol_pairs)

@app.route('/results')
def results():
    return render_template("results.html")

@app.route('/year_report/<year>')
def year(year):
    with open('static/data/by_country_ranked_%s.html' % year, 'r') as file:
        by_country=file.read()
    with open('static/data/apmo_%s_info.json' % year) as json_file:
        competition_info = json.loads(json_file.read())
    return render_template("year_report.html",year=year, by_country=by_country, competition_info=competition_info)

@app.route('/country_report/<country>/<year>')
def country(country, year):
    if year=='all':
        pass
    if int(year)>=2016:
        pass
    with open('static/data/by_country_ranked_%s.html' % year, 'r') as file:
        by_country=file.read()
    with open('static/data/apmo_%s_info.json' % year) as json_file:
        competition_info = json.loads(json_file.read())

    return render_template("year_report.html",year=year, by_country=by_country, competition_info=competition_info)