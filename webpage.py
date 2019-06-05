from flask import Flask, render_template
import glob, re, json
import pandas as pd

year_re=r'[0-9]{4}'

app = Flask(__name__)

# An auxiliary function for creating a table

def country_year_table(code,year): 
    year_res_df = pd.read_csv('data/reports/score_awards_%s.csv' % year)
    to_report = year_res_df[year_res_df.code == code].reset_index().drop('index', axis=1)
    country=to_report['country'][0]
    to_report.drop(['country', 'sex', 'code'], axis=1, inplace=True)
    to_report.columns=["Rank", "Last Name", "First Name", "P1", "P2", "P3", "P4", "P5", "Total", "Award"]
    table=to_report.to_html(index=False, classes='table table-striped table-sm',border=0,justify='center')
    return table, country

def apmo_editions():
    editions_df = pd.read_csv('data/apmo_editions.csv', dtype={'year':object,
    'gold_cutoff':object, 'silver_cutoff':object, 'bronze_cutoff':object, 'num_countries':object,'num_contestants':object
    }).drop("chair", axis=1)
    editions_df.columns=['Year', 'Num. Countries', 'Num. Contestants', 'Gold cut', 'Silver cut', 'Bronze cut', 'SCC', 'ACC', 'MC']
    editions_df.sort_values('Year', ascending=False,inplace=True)
    editions_df['Results']='<a href=year_report/' + editions_df.Year.astype(str) +'> Go </a>'
    table=editions_df.to_html(index=False, classes='table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table

def participating_countries():
    countries_df = pd.read_csv('data/apmo_countries.csv')
    countries_df.columns=['Code', 'Country', 'Status', 'Current Representative']
    countries_df.sort_values('Country', inplace=True)
    countries_df['Results']='<a href=country_report/' + countries_df.Code.astype(str) +'/all> Go </a>'
    table=countries_df.to_html(index=False, classes='table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table

# The routing begins here

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
    table=apmo_editions()
    return render_template("timeline.html", table=table)

@app.route('/countries')
def countries():
    table=participating_countries()
    return render_template("countries.html", table=table)


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
    countries=[[x['code'],x['country']]  for _, x in pd.read_csv('data/apmo_countries.csv')[['code','country']].iterrows()]
    print(countries)
    return render_template("results.html",countries=countries)

@app.route('/year_report/<year>')
def year(year):
    with open('data/reports/by_country_ranked_%s.html' % year, 'r') as file:
        by_country=file.read()
    with open('data/reports/apmo_%s_info.json' % year) as json_file:
        competition_info = json.loads(json_file.read())
    return render_template("year_report.html",year=year, by_country=by_country, competition_info=competition_info)

@app.route('/country_report/<code>/<year>')
def country(code, year):
    if year=='all':
        return('Full country view')
    elif int(year)<=2015:
        return('Not enough info to display')
    elif int(year) in range(2016,2020): 
        table, country = country_year_table(code, year)
        return render_template('year_country_report.html', code=code, year=year, country=country, table=table)