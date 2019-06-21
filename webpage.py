from flask import Flask, render_template
import glob, re, json
import pandas as pd
import os

THIS_FILE = os.path.abspath(__file__)
THIS_DIR = os.path.dirname(THIS_FILE)
os.chdir(THIS_DIR)

pd.set_option('max_colwidth', 70)

year_re=r'[0-9]{4}'

app = Flask(__name__)

files_ranked_all=glob.glob('data/reports/by_country_ranked_*.csv')
ranked_all_dfs=[]
for filename in files_ranked_all:
    year=filename[-8:-4]
    temp_df=pd.read_csv(filename)
    temp_df['Year']=year
    ranked_all_dfs.append(temp_df)
ranked_all_df=pd.concat(ranked_all_dfs, axis=0)

# Auxiliary table creating functions

def apmo_editions():
    editions_df = pd.read_csv('data/apmo_editions.csv', dtype={'year':object,
    'gold_cutoff':object, 'silver_cutoff':object, 'bronze_cutoff':object, 'num_countries':object,'num_contestants':object
    }).drop("chair", axis=1)
    editions_df.columns=['Year', 'Num. Countries', 'Num. Contestants', 'Gold cut', 'Silver cut', 'Bronze cut', 'SCC *', 'ACC *', 'MC *']
    editions_df.sort_values('Year', ascending=False,inplace=True)
    editions_df['Results']='<a href=/year_report/' + editions_df.Year.astype(str) +'> Go </a>'
    table=editions_df.to_html(index=False, classes='d-none d-lg-table table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table

def apmo_editions_short():
    editions_df = pd.read_csv('data/apmo_editions.csv', dtype={'year':object,
    'gold_cutoff':object, 'silver_cutoff':object, 'bronze_cutoff':object, 'num_countries':object,'num_contestants':object
    }).drop(['senior', 'assistant', 'moderating', 'chair'], axis=1)
    editions_df.columns=['Year', 'Cou.*', 'Con.*', 'Gold', 'Silver', 'Bronze']
    editions_df.sort_values('Year', ascending=False,inplace=True)
    editions_df['More']='<a href=/year_report/' + editions_df.Year.astype(str) +'> Go </a>'
    table=editions_df.to_html(index=False, classes='d-table d-lg-none table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table

def country_year_table(code,year): 
    year_res_df = pd.read_csv('data/reports/score_awards_%s.csv' % year)
    to_report = year_res_df[year_res_df.code == code].reset_index().drop('index', axis=1)
    country=to_report['country'][0]
    to_report.drop(['country', 'sex', 'code'], axis=1, inplace=True)
    to_report.columns=["Rank", "Last Name", "First Name", "P1", "P2", "P3", "P4", "P5", "Total", "Award"]
    table=to_report.to_html(index=False, classes='d-none d-lg-table table table-striped table-sm',border=0,justify='center', escape=False)
    return table, country

def country_year_table_short(code,year): 
    year_res_df = pd.read_csv('data/reports/score_awards_%s.csv' % year)
    to_report = year_res_df[year_res_df.code == code].reset_index().drop('index', axis=1)
    country=to_report['country'][0]
    to_report.award = to_report.award.map({'Gold':'G', 'Silver':'S', 'Bronze': 'B', 'Hon. Men.': 'HM', '':''})
    to_report.drop(['country', 'sex', 'code'], axis=1, inplace=True)
    to_report['scores']=to_report.p1.astype(str)+', ' + to_report.p2.astype(str) + ', ' + to_report.p3.astype(str) + ', ' + to_report.p4.astype(str) + ', ' + to_report.p5.astype(str) + ', <b>' + to_report.total.astype(str) + '</b>'
    to_report.drop(['p1','p2','p3','p4','p5','total'], axis=1, inplace=True)
    list_columns=to_report.columns.tolist()
    new_columns=list_columns[:-2]+list_columns[-1:-3:-1]
    to_report=to_report[new_columns]
    to_report.columns=["Rank", "Last Name", "First Name", "Scores", "Award"]
    table=to_report.to_html(index=False, classes='d-table d-lg-none table table-striped table-sm',border=0,justify='center', escape=False)
    return table, country

def country_all_table(code):
    country_all_df=ranked_all_df[ranked_all_df['Code']==code].reset_index().drop('index', axis=1).sort_values('Year', ascending=False)
    country_all_df['Year']='<a href=/country_report/' + code + '/' + country_all_df.Year.astype(str) + '> ' + country_all_df.Year.astype(str) + ' </a>'
    country=country_all_df['Country'][0]
    country_all_df.drop(['Code', 'Country'], axis=1, inplace=True)
    list_columns=country_all_df.columns.tolist()
    new_columns=[list_columns[-1]]+list_columns[:-1]
    country_all_df=country_all_df[new_columns]
    table=country_all_df.to_html(index=False, classes='d-none d-lg-table table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table, country

def country_all_table_short(code):
    country_all_df=ranked_all_df[ranked_all_df['Code']==code].reset_index().drop('index', axis=1).sort_values('Year', ascending=False)
    country_all_df['Year']='<a href=/country_report/' + code + '/' + country_all_df.Year.astype(str) + '> ' + country_all_df.Year.astype(str) + ' </a>'
    country=country_all_df['Country'][0]
    country_all_df['Awards (G,S,B,HM)']=country_all_df['Gold Awards'].astype(str) + ', ' + country_all_df['Silver Awards'].astype(str) + ', ' + country_all_df['Bronze Awards'].astype(str) + ', ' + country_all_df['Honorable Mentions'].astype(str)
    country_all_df.drop(['Code', 'Country','Gold Awards', 'Silver Awards', 'Bronze Awards', 'Honorable Mentions'], axis=1, inplace=True)
    list_columns=country_all_df.columns.tolist()
    new_columns=[list_columns[-2]]+list_columns[:-2]+[list_columns[-1]] 
    country_all_df=country_all_df[new_columns]
    country_all_df.columns=['Year', 'Rank', 'Contestants', 'Score', 'Awards (G,S,B,HM)']
    table=country_all_df.to_html(index=False, classes='d-table d-lg-none table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table, country

def participating_countries():
    countries_df = pd.read_csv('data/apmo_countries.csv')
    countries_df.columns=['Code', 'Country', 'Status', 'Contact']
    countries_df.sort_values('Country', inplace=True)
    countries_df['Results']='<a href="/country_report/' + countries_df.Code.astype(str) +'/all"> Go </a>'
    table=countries_df.to_html(index=False, classes='table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table

def ranked_table(year):
    ranked_df = pd.read_csv('data/reports/by_country_ranked_%s.csv' % year)
    ranked_df['Country']='<a href="/country_report/' + ranked_df.Code.astype(str) + ('/%s">' % year) + ranked_df.Country + '</a>'
    ranked_df.drop(['Code'], axis=1, inplace=True)
    table=ranked_df.to_html(index=False, classes='d-none d-lg-table table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table

def ranked_table_short(year):
    ranked_df = pd.read_csv('data/reports/by_country_ranked_%s.csv' % year)
    ranked_df['Country']='<a href="/country_report/' + ranked_df.Code.astype(str) + ('/%s">' % year) + ranked_df.Country + '</a>'
    ranked_df['Awards (G,S,B,HM)']=ranked_df['Gold Awards'].astype(str) + ', ' + ranked_df['Silver Awards'].astype(str) + ', ' + ranked_df['Bronze Awards'].astype(str) + ', ' + ranked_df['Honorable Mentions'].astype(str)
    ranked_df.drop(['Code','Gold Awards', 'Silver Awards', 'Bronze Awards', 'Honorable Mentions'], axis=1, inplace=True)
    ranked_df.columns=['Rank','Country', 'Con.*', 'Score', 'Awards (G,S,B,HM)']
    table=ranked_df.to_html(index=False, classes='d-table d-lg-none table table-striped table-sm', border=0, justify='center',na_rep='', escape=False)
    return table

def load_info(year):
    try:
        with open('data/reports/apmo_%s_info.json' % year) as json_file:
            return json.loads(json_file.read())
    except:
        with open('data/reports/apmo_dummy_info.json') as json_file:
            return json.loads(json_file.read())

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
    table_short=apmo_editions_short()
    return render_template("timeline.html", table=table, table_short=table_short)

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
    return render_template("results.html",countries=countries)

@app.route('/year_report/<year>')
def year_report(year):
    try:
        year=int(year)
    except:
        return render_template('not_enough_info.html')
    if year in range(2010,2020):
        problem_stats=False
        if year in range(2016,2020):
            problem_stats=True
        competition_info=load_info(year)
        table=ranked_table(year)
        table_short = ranked_table_short(year)
        return render_template("year_report.html",year=year, table=table, table_short=table_short, competition_info=competition_info,problem_stats=problem_stats)
    elif int(year) in range(2005,2016):
        return results()
    else:
        return render_template('not_enough_info.html')

@app.route('/country_report/<code>/<year>')
def country(code, year):
    if year=='all':
        try:
            table, country = country_all_table(code)
            table_short, country = country_all_table_short(code)
            return render_template('country.html', country=country, table=table,  table_short=table_short)
        except:
            return render_template('not_enough_info.html')
    try:
        year=int(year)
        if year in range(2016,2020):
            table, country = country_year_table(code, year)
            table_short, country= country_year_table_short(code, year)
            return render_template('year_country_report.html', code=code, year=year, country=country, table=table, table_short=table_short)
        else:
            return render_template('not_enough_info.html')
    except:
        return render_template('not_enough_info.html')
       