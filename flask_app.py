
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, g
from openpyxl.compat import range
import pandas as pd
import sqlite3

import math



app = Flask(__name__)

DATABASE = 'ghi.db'
app.config.from_object(__name__)

from functools import wraps
from flask import request, Response


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'ghi' and password == 'ghi'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def connect_db():
    return sqlite3.connect('/home/roverdillon/mysite/ghi.db')

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

diseasedict = {'tb':'TB','hiv':'HIV','malaria':'Malaria','onchocerciasis':'Onchocerciasis','schistosomiasis':'Schistosomiasis','lf':'LF','hookworm':'Hookworm','roundworm':'Roundworm','whipworm':'Whipworm'}

@app.route('/')
def index():
    return render_template('index.html', showthediv=0)


@app.route('/about')
def about():
    return render_template('about.html', showthediv=0)

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/organization')
def organization():
    return render_template('organization.html',showindex=0)

@app.route('/resources')
def resources():
    return render_template('resources.html',showthediv=0,scrolling=2)

@app.route('/index/disease')
def diseaseinx():
    piedat = []
    clickdat = []
    g.db = connect_db()
    cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf from diseaseall2010 ')
    data = cur.fetchall()
    ddisease = 'All'
    dyear = '2010'
    for row in data:
        country = row[0]
        tb = row[1]
        malaria = row[2]
        hiv = row[3]
        roundworm = row[4]
        hookworm = row[5]
        whipworm = row[6]
        schistosomiasis = row[7]
        onchocerciasis = row[8]
        lf = row[9]
        total = tb+malaria+hiv+roundworm+hookworm+whipworm+schistosomiasis+onchocerciasis+lf
        xx = [country,total]
        xy = [country,tb,malaria,hiv,roundworm,hookworm,whipworm,schistosomiasis,onchocerciasis,lf]
        piedat.append(xx)
        clickdat.append(xy)
    seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
    index = [seq.index(v) for v in piedat]
    piedat.insert(0,['Country','DALY'])
    upp = ddisease.upper()
    speclocate = [dyear, ddisease,upp]
    return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index, disease=1, speclocate = speclocate, scrolling=1)

@app.route('/index/disease/<dyear>/<ddisease>')
def diseasepg(dyear,ddisease):
    if dyear == '2010':
        if ddisease == 'summary':
            piedata = []
            bar1data = []
            bar1 = []
            bar2 = []
            bar3 = []
            g.db = connect_db()
            cur = g.db.execute(' select disease, impact, color from disease2010 ')
            daly = g.db.execute(' select disease, daly, color from disease2010 ')
            barz = g.db.execute(' select disease, color, efficacy2010, coverage2010, need2010 from disbars ')
            barg = daly.fetchall()
            pied = cur.fetchall()
            bardata = barz.fetchall()
            c = 0
            barcolors = ['#FFB31C','#0083CA','#EF3E2E','#86AAB9','#003452','#CAEEFD','#546675','#8A5575','#305516']
            for row in bardata:
                diss = row[0]
                color = "color: " + barcolors[c]
                c+=1
                efficacy = row[2]
                coverage = row[3]
                need = row[4]
                x = [diss,efficacy,color]
                y = [diss,need,color]
                z = [diss,coverage,color]
                bar1.append(y)
                bar2.append(z)
                bar3.append(x)



            for row in pied:
                name = row[0]
                imp = row[1]
                color = "color: " + row[2]
                x = [name,imp]
                piedata.append(x)
            for row in barg:
                name = row[0]
                daly = row[1]
                color = "color: " + row[2]
                x = [name,daly,color]
                bar1data.append(x)
            g.db.close()
            upp = ddisease.upper()
            speclocate = [dyear, ddisease,upp]
            return render_template('disease.html', navsub=4, showindex=1, diseasepie = piedata, bar1data = bar1data, disease=0, bar1 = bar1, bar2 = bar2, bar3 = bar3, speclocate = speclocate, scrolling=1)
        elif ddisease == 'all':
            piedat = []
            clickdat = []
            g.db = connect_db()
            cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf from diseaseall2010 ')
            data = cur.fetchall()
            for row in data:
                country = row[0]
                tb = row[1]
                malaria = row[2]
                hiv = row[3]
                roundworm = row[4]
                hookworm = row[5]
                whipworm = row[6]
                schistosomiasis = row[7]
                onchocerciasis = row[8]
                lf = row[9]
                total = tb+malaria+hiv+roundworm+hookworm+whipworm+schistosomiasis+onchocerciasis+lf
                xx = [country,total]
                xy = [country,tb,malaria,hiv,roundworm,hookworm,whipworm,schistosomiasis,onchocerciasis,lf]
                piedat.append(xx)
                clickdat.append(xy)
            seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
            index = [seq.index(v) for v in piedat]
            piedat.insert(0,['Country','DALY'])
            upp = ddisease.upper()
            speclocate = [dyear, ddisease,upp]
            return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index, disease=1, speclocate = speclocate, scrolling=1)

    elif dyear == '2013':
        if ddisease == 'summary':
            piedata = []
            bar1data = []
            bar1 = []
            bar2 = []
            bar3 = []
            g.db = connect_db()
            cur = g.db.execute(' select disease, impact, color from disease2013 ')
            daly = g.db.execute(' select disease, daly, color from disease2013 ')
            barz = g.db.execute(' select disease, color, efficacy2013, coverage2013, need2013 from disbars ')
            barg = daly.fetchall()
            pied = cur.fetchall()
            bardata = barz.fetchall()
            c = 0
            barcolors = ['#FFB31C','#0083CA','#EF3E2E','#86AAB9','#003452','#CAEEFD','#546675','#8A5575','#305516']
            for row in bardata:
                diss = row[0]
                color = "color: " + barcolors[c]
                c+=1
                efficacy = row[2]
                coverage = row[3]
                need = row[4]
                x = [diss,efficacy,color]
                y = [diss,need,color]
                z = [diss,coverage,color]
                bar1.append(y)
                bar2.append(z)
                bar3.append(x)
            for row in pied:
                name = row[0]
                imp = row[1]
                color = "color: " + row[2]
                x = [name,imp]
                piedata.append(x)
            for row in barg:
                name = row[0]
                daly = row[1]
                color = "color: " + row[2]
                x = [name,daly,color]
                bar1data.append(x)
            g.db.close()
            upp = ddisease.upper()
            speclocate = [dyear, ddisease,upp]
            return render_template('disease.html', navsub=4, showindex=1, diseasepie = piedata, bar1data = bar1data, disease=0, bar1 = bar1, bar2 = bar2, bar3 = bar3, speclocate = speclocate)
        elif ddisease == 'all':
            piedat = []
            clickdat = []
            g.db = connect_db()
            cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf from diseaseall2013 ')
            data = cur.fetchall()
            for row in data:
                country = row[0]
                tb = row[1]
                malaria = row[2]
                hiv = row[3]
                roundworm = row[4]
                hookworm = row[5]
                whipworm = row[6]
                schistosomiasis = row[7]
                onchocerciasis = row[8]
                lf = row[9]
                total = tb+malaria+hiv+roundworm+hookworm+whipworm+schistosomiasis+onchocerciasis+lf
                xx = [country,total]
                xy = [country,tb,malaria,hiv,roundworm,hookworm,whipworm,schistosomiasis,onchocerciasis,lf]
                piedat.append(xx)
                clickdat.append(xy)
            seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
            index = [seq.index(v) for v in piedat]
            piedat.insert(0,['Country','DALY'])
            upp = ddisease.upper()
            speclocate = [dyear, ddisease,upp]
            return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index, disease=1, speclocate = speclocate, scrolling=1)


@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/reports/<company>')
def reportcomp(company):
    reportdict = {
        'Abbot_Laboratories': 'Abbot Laboratories',
        'Bayer_Healthcare': 'Bayer Healthcare',
        'Boehringer_Ingelheim_Pharmaceuticals': 'Boehringer Ingelheim Pharmaceuticals',
        'Bristol-Myers_Squibb': 'Bristol-Myers Squibb',
        'Chonggin_Tonghe': 'Chonggin Tonghe',
        'Daichii_Sankyo': 'Daichii Sankyo',
        'Gilead_Science': 'Gilead Science',
        'GlaxoSmithKline': 'GlaxoSmithKline',
        'Hoffman-LaRoche': 'Hoffman-LaRoche',
        'Merck': 'Merck',
        'Novartis': 'Novartis',
        'Pfizer': 'Pfizer Inc.',
        'Sanofi': 'Sanofi',
        'Shire_Pharmaceuticals': 'Shire Pharmaceuticals',
        'ViiV': 'ViiV'
    }
    companyname = reportdict[company]
    return render_template('reports.html',company=companyname)
    g.db.close()

@app.route('/methodology')
def methadology():
    return render_template('methodology.html')

@app.route('/index/drug')
def druginx():
    drugcolors = ['#FFB31C', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD', '#546675', '#8A5575', '#305516',
                  '#B78988', '#BAE2DA', '#B1345D', '#5B75A7', '#906F76', '#C0E188', '#DE9C2A', '#F15A22', '#8F918B',
                  '#F2C2B7',
                  '#F7C406', '#B83F98', '#548A9B', '#D86375', '#F1DBC6', '#0083CA', '#7A80A3', '#CA8566', '#A3516E',
                  '#1DF533', '#510B95', '#DFF352', '#F2C883', '#E3744D', '#26B2BE', '#5006BA', '#B99BCF', '#DC2A5A',
                  '#D3D472', '#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5', '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5',
                  '#0ACD57', '#22419F', '#D47C5B']
    piedata = []
    drugg = []
    pielabb = []
    g.db = connect_db()
    cur = g.db.execute(' select drug, total from drugr2010 ')
    piee = cur.fetchall()
    impactpie = []
    for k in piee:
        drug = k[0]
        score = k[1]
        t = [drug,score]
        if score > 0:
            piedata.append(t)
    sortedpie2 = sorted(piedata, key=lambda xy: xy[1], reverse=True)
    maxrow = sortedpie2[0]
    if maxrow[0] == 'Unmet Need':
        maxrow = sortedpie2[1]

    maxval = maxrow[1]
    c = 0
    for row in sortedpie2:
        perc = (row[1] / maxval) * 100
        row.append(perc)
        color = drugcolors[c]
        row.append(color)
        c+=1
        if row[0] != 'Unmet Need':
            impactpie.append(row)
    lablist = []
    pielabb = []
    for k in impactpie:
        labit = []
        drug = k[0]
        score = k[1]
        color = k[3]
        shortdrug = drug[0:10]
        labit.append(drug)
        labit.append(shortdrug)
        labit.append(color)
        labit.append(score)
        lablist.append(labit)
    labrow = []
    xx = 0
    if len(lablist) < 4:
        pielabb.append(lablist)
    else:
        for item in lablist:
            labrow.append(item)
            xx += 1
            if xx % 4 == 0:
                pielabb.append(labrow)
                labrow = []
                xx = 0
    g.db.close()
    speclocate = ['2010','all','ALL']
    return render_template('drug.html', data=piedata, drug='All', navsub=3, showindex=1, pielabb=pielabb, drugcolors=drugcolors, speclocate = speclocate, scrolling=1, impactpie=impactpie, sortedpie2 = sortedpie2)

@app.route('/index/drug/<year>/<disease>')
def drug(year,disease):
    drugcolors = ['#FFB31C', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD', '#546675', '#8A5575', '#305516',
                  '#B78988', '#BAE2DA', '#B1345D', '#5B75A7', '#906F76', '#C0E188', '#DE9C2A', '#F15A22', '#8F918B',
                  '#F2C2B7',
                  '#F7C406', '#B83F98', '#548A9B', '#D86375', '#F1DBC6', '#0083CA', '#7A80A3', '#CA8566', '#A3516E',
                  '#1DF533', '#510B95', '#DFF352', '#F2C883', '#E3744D', '#26B2BE', '#5006BA', '#B99BCF', '#DC2A5A',
                  '#D3D472', '#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5', '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5',
                  '#0ACD57', '#22419F', '#D47C5B']
    piedata = []
    drugg = []
    pielabb = []
    g.db = connect_db()
    if disease == 'all':
        drugg = 'ALL'
        if year == '2010':
            cur = g.db.execute(' select drug, total from drugr2010 ')
        elif year == '2013':
            cur = g.db.execute(' select drug, total from drugr2013 ')
    else:
        drugg = diseasedict[disease]
        if year == '2010':
            if disease == 'malaria':
                cur = g.db.execute(' select drug, malaria from drugr2010 ')
            elif disease == 'hiv':
                cur = g.db.execute(' select drug, hiv from drugr2010 ')
            elif disease == 'tb':
                cur = g.db.execute(' select drug, tb from drugr2010 ')
            elif disease == 'roundworm':
                cur = g.db.execute(' select drug, roundworm from drugr2010 ')
            elif disease == 'hookworm':
                cur = g.db.execute(' select drug, hookworm from drugr2010 ')
            elif disease == 'whipworm':
                cur = g.db.execute(' select drug, hookworm from drugr2010 ')
            elif disease == 'schistosomiasis':
                cur = g.db.execute(' select drug, schistosomiasis from drugr2010 ')
            elif disease == 'onchocerciasis':
                cur = g.db.execute(' select drug, onchocerciasis from drugr2010 ')
            elif disease == 'lf':
                cur = g.db.execute(' select drug, lf from drugr2010 ')

        elif year == '2013':
            if disease == 'malaria':
                cur = g.db.execute(' select drug, malaria from drugr2013 ')
            elif disease == 'hiv':
                cur = g.db.execute(' select drug, hiv from drugr2013 ')
            elif disease == 'tb':
                cur = g.db.execute(' select drug, tb from drugr2013 ')
            elif disease == 'roundworm':
                cur = g.db.execute(' select drug, roundworm from drugr2013 ')
            elif disease == 'hookworm':
                cur = g.db.execute(' select drug, hookworm from drugr2013 ')
            elif disease == 'whipworm':
                cur = g.db.execute(' select drug, hookworm from drugr2013 ')
            elif disease == 'schistosomiasis':
                cur = g.db.execute(' select drug, schistosomiasis from drugr2013 ')
            elif disease == 'onchocerciasis':
                cur = g.db.execute(' select drug, onchocerciasis from drugr2013 ')
            elif disease == 'lf':
                cur = g.db.execute(' select drug, lf from drugr2013 ')

    piee = cur.fetchall()
    impactpie = []
    for k in piee:
        drug = k[0]
        score = k[1]
        t = [drug,score]
        if score > 0:
            piedata.append(t)
    sortedpie2 = sorted(piedata, key=lambda xy: xy[1], reverse=True)
    maxrow = sortedpie2[0]
    if maxrow[0] == 'Unmet Need':
        maxrow = sortedpie2[1]

    maxval = maxrow[1]
    c = 0
    for row in sortedpie2:
        perc = (row[1] / maxval) * 100
        row.append(perc)
        color = drugcolors[c]
        row.append(color)
        c+=1
        if row[0] != 'Unmet Need':
            impactpie.append(row)
    lablist = []
    pielabb = []
    for k in impactpie:
        labit = []
        drug = k[0]
        score = k[1]
        color = k[3]
        shortdrug = drug[0:10]
        labit.append(drug)
        labit.append(shortdrug)
        labit.append(color)
        labit.append(score)
        lablist.append(labit)
    labrow = []
    xx = 0
    if len(lablist) < 4:
        pielabb.append(lablist)
    else:
        for item in lablist:
            labrow.append(item)
            xx += 1
            if xx % 4 == 0:
                pielabb.append(labrow)
                labrow = []
                xx = 0
    g.db.close()
    speclocate = [year,drugg,disease]
    return render_template('drug.html', data=piedata, drug=drugg, navsub=3, showindex=1, pielabb=pielabb, drugcolors=drugcolors, speclocate = speclocate, scrolling=1, impactpie=impactpie, sortedpie2 = sortedpie2)

@app.route('/index/country')
def country():
    g.db = connect_db()
    color = []
    year = 2010
    colors = {'tb': '#FFB31C', 'malaria': '#0083CA', 'hiv': '#EF3E2E', 'schistomasis': '#546675', 'lf': '#305516', 'hookworm': '#86AAB9', 'roundworm': '#003452', 'whipworm': '#CAEEFD', 'onchocerciasis': '#5CB85C'}
    isall = 1
    drugg = 'all'
    name = 'ALL'
    br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf from countryp2010 ')
    cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf from country2010 ')
    bars = br.fetchall()
    maps = cur.fetchall()
    mapdata = []

    for row in maps:
        count = row[0]
        score = row[1]
        hor = [count,score]
        mapdata.append(hor)
    sort = []
    sortedlist = sorted(bars, key=lambda xy: xy[1], reverse=True)
    sortedval = sorted(maps, key=lambda x: x[1], reverse=True)
    barlist = []
    i=0
    for row in sortedlist:
        combrow = [row,sortedval[i],[i]]
        barlist.append(combrow)
        tmp = []
        for j in sortedval[i]:
            tmp.append(j)
        i += 1
        sort.append(tmp)
    speclocate = [year,name,drugg]
    mapdata.insert(0,['Country','Score'])
    g.db.close()
    return render_template('country.html', showindex=1, navsub=1, name=name, color=color, mapdata=mapdata, sortedlist=sortedlist, sortedval = sort, year=year, isall=isall, barlist = barlist, speclocate = speclocate)

@app.route('/index/country/<xyear>/<xdisease>')
def countrydata(xdisease,xyear):
    g.db = connect_db()
    color = []
    year = xyear
    colors = {'tb': '#FFB31C', 'malaria': '#0083CA', 'hiv': '#EF3E2E', 'schistomasis': '#546675', 'lf': '#305516', 'hookworm': '#86AAB9', 'roundworm': '#003452', 'whipworm': '#CAEEFD', 'onchocerciasis': '#5CB85C'}
    if xdisease == 'all':
        isall = 1
        drugg = 'all'
        name = 'ALL'
        if xyear == '2010':
            br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf from countryp2010 ')
            cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf from country2010 ')
        elif xyear == '2013':
            cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf from country2013 ')
            br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf from countryp2013 ')
    else:
        isall = 0
        namedict = {'tb': 'TB', 'malaria': 'MALARIA', 'hiv': 'HIV', 'schistosomiasis': 'SCHISTOSOMIASIS', 'onchocerciasis':'ONCHOCERCIASIS', 'lf': 'LYMPHATIC FILARIASIS', 'hookworm': 'HOOKWORM', 'roundworm': 'ROUNDWORM', 'whipworm': 'WHIPWORM'}
        color = colors[xdisease]
        name = namedict[xdisease]
        drugg = xdisease
        if xyear == '2010':
            if xdisease == 'tb':
                cur = g.db.execute(' select country, tb from country2010 ')
                br = g.db.execute(' select country, tb from countryp2010 ')
                sortind = 1
            elif xdisease == 'malaria':
                cur = g.db.execute(' select country, malaria from country2010 ')
                br = g.db.execute(' select country, malaria from countryp2010 ')
                sortind = 2
            elif xdisease == 'hiv':
                cur = g.db.execute(' select country, hiv from country2010 ')
                br = g.db.execute(' select country, hiv from countryp2010 ')
                sortind = 3
            elif xdisease == 'roundworm':
                cur = g.db.execute(' select country, roundworm from country2010 ')
                br = g.db.execute(' select country, roundworm from countryp2010 ')
                sortind = 4
            elif xdisease == 'hookworm':
                cur = g.db.execute(' select country, hookworm from country2010 ')
                br = g.db.execute(' select country, hookworm from countryp2010 ')
                sortind = 5
            elif xdisease == 'whipworm':
                cur = g.db.execute(' select country, whipworm from country2010 ')
                br = g.db.execute(' select country, whipworm from countryp2010 ')
                sortind = 6
            elif xdisease == 'schistosomiasis':
                cur = g.db.execute(' select country, schistosomiasis from country2010 ')
                br = g.db.execute(' select country, schistosomiasis from countryp2010 ')
                sortind = 7
            elif xdisease == 'lf':
                cur = g.db.execute(' select country, lf from country2010 ')
                br = g.db.execute(' select country, lf from countryp2010 ')
                sortind = 8
        elif xyear == '2013':
            if xdisease == 'tb':
                cur = g.db.execute(' select country, tb from country2013 ')
                br = g.db.execute(' select country, tb from countryp2013 ')
                sortind = 1
            elif xdisease == 'malaria':
                cur = g.db.execute(' select country, malaria from country2013 ')
                br = g.db.execute(' select country, malaria from countryp2013 ')
                sortind = 2
            elif xdisease == 'hiv':
                cur = g.db.execute(' select country, hiv from country2013 ')
                br = g.db.execute(' select country, hiv from countryp2013 ')
                sortind = 3
            elif xdisease == 'roundworm':
                cur = g.db.execute(' select country, roundworm from country2013 ')
                br = g.db.execute(' select country, roundworm from countryp2013 ')
                sortind = 4
            elif xdisease == 'hookworm':
                cur = g.db.execute(' select country, hookworm from country2013 ')
                br = g.db.execute(' select country, hookworm from countryp2013 ')
                sortind = 5
            elif xdisease == 'whipworm':
                cur = g.db.execute(' select country, whipworm from country2013 ')
                br = g.db.execute(' select country, whipworm from countryp2013 ')
                sortind = 6
            elif xdisease == 'schistosomiasis':
                cur = g.db.execute(' select country, schistosomiasis from country2013 ')
                br = g.db.execute(' select country, schistosomiasis from countryp2013 ')
                sortind = 7
            elif xdisease == 'onchoceriasis':
                cur = g.db.execute(' select country, onchoceriasis from country2013 ')
                br = g.db.execute(' select country, onchoceriasis from countryp2013 ')
                sortind = 8
            elif xdisease == 'lf':
                cur = g.db.execute(' select country, lf from country2013 ')
                br = g.db.execute(' select country, lf from countryp2013 ')
                sortind = 9
    bars = br.fetchall()
    maps = cur.fetchall()
    mapdata = []

    for row in maps:
        count = row[0]
        score = row[1]
        hor = [count,score]
        mapdata.append(hor)
    sort = []
    sortedlist = sorted(bars, key=lambda xy: xy[1], reverse=True)
    sortedval = sorted(maps, key=lambda x: x[1], reverse=True)
    maxrow = sortedval[0]
    width = maxrow[1]
    if xdisease == 'all':
        barlist = []
        i=0
        for row in sortedlist:
            combrow = [row,sortedval[i],[i]]
            barlist.append(combrow)
            tmp = []
            for j in sortedval[i]:
                tmp.append(j)
            del(tmp[1])
            i += 1
            sort.append(tmp)
        print(sort)
    else:
        barlist = []
        for row in sortedval:
            perc = row[1] / width * 100
            temp = [row[0],row[1],perc]
            barlist.append(temp)
        if xyear == '2010':
            cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf from country2010 ')
        elif xyear == '2013':
            cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, onchoceriasis, lf from country2013 ')
        vals = cur.fetchall()
        sortvals = sorted(vals, key=lambda x: x[sortind], reverse=True)
        sort = []
        for row in sortvals:
            tmp = []
            for j in row:
                tmp.append(j)
            sort.append(tmp)
        print(sort)
    speclocate = [xyear,name,drugg]
    mapdata.insert(0,['Country','Score'])
    g.db.close()
    return render_template('country.html', showindex=1, navsub=1, name=name, color=color, mapdata=mapdata, sortedlist=sortedlist, sortedval = sort, year=year, isall=isall, barlist = barlist, speclocate = speclocate,scrolling=1)

@app.route('/index/company')
def company():
    compcolors = ['#FFB31C', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD', '#546675', '#8A5575', '#305516', '#B78988', '#BAE2DA', '#B1345D', '#5B75A7', '#906F76', '#C0E188', '#DE9C2A', '#F15A22', '#8F918B', '#F2C2B7',
 '#F7C406', '#B83F98', '#548A9B', '#D86375', '#F1DBC6', '#0083CA', '#7A80A3', '#CA8566', '#A3516E', '#1DF533', '#510B95', '#DFF352', '#F2C883', '#E3744D', '#26B2BE', '#5006BA', '#B99BCF', '#DC2A5A', '#D3D472',
 '#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5', '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5', '#0ACD57', '#22419F', '#D47C5B']
    cur = g.db.execute(' select company, daly2010, color from manutot ')
    cdd = g.db.execute(' select company, disease, daly2010, color from manudis ')
    piedata = []
    g.db = connect_db()
    pielab = []
    barchart = []
    bardata = []
    name = 'ALL'
    disease = 'All'
    year = '2010'
    piee = cur.fetchall()
    barr = cdd.fetchall()

    for j in piee:
        company = j[0]
        daly2010 = j[1]
        color = j[2]
        if daly2010 > 0:
            t = [company, daly2010, color]
            print(t)
            piedata.append(t)
    piedata.sort(key=lambda x: x[1], reverse=True)
    n = 0
    temprow = []
    for k in piedata:
        print(k)
        if n < 4:
            comp = k[0]
            shortcomp = comp[0:10]
            temprow.append(comp)
            temprow.append(shortcomp)
            temprow.append(k[2])
            n += 1
        else:
            n = 0
            pielab.append(temprow)
            temprow = []
    colcnt = 0
    for l in barr:
        company = l[0]
        daly2010 = l[2]
        disease = l[1]
        color = compcolors[colcnt]
        colcnt += 1
        xyz = [company,daly2010,disease,color]
        barchart.append(xyz)
    barchart.sort(key=lambda x: x[1], reverse=True)
    maxim = barchart[0]
    maxval = maxim[1]
    colcnt = 0
    for row in barchart:
        comp = row[0]
        daly = (row[1]/maxval) * 100
        disease = row[2]
        color = compcolors[colcnt]
        colcnt += 1
        xyz = [comp,daly,disease,color]
        bardata.append(xyz)

    g.db.close()
    url = name.lower()
    speclocate = [year,name,url]
    return render_template('company.html', data=piedata, navsub=2, showindex=1, pielab=pielab, bardata=bardata, comptype = 0, speclocate = speclocate, scrolling=1)

@app.route('/index/company/manufacturer/<year>/<disease>')
def companyindx(year,disease):
    compcolors = ['#FFB31C', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD', '#546675', '#8A5575', '#305516', '#B78988', '#BAE2DA', '#B1345D', '#5B75A7', '#906F76', '#C0E188', '#DE9C2A', '#F15A22', '#8F918B', '#F2C2B7',
 '#F7C406', '#B83F98', '#548A9B', '#D86375', '#F1DBC6', '#0083CA', '#7A80A3', '#CA8566', '#A3516E', '#1DF533', '#510B95', '#DFF352', '#F2C883', '#E3744D', '#26B2BE', '#5006BA', '#B99BCF', '#DC2A5A', '#D3D472',
 '#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5', '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5', '#0ACD57', '#22419F', '#D47C5B']
    colors = {'TB': '#FFB31C', 'Malaria': '#0083CA', 'HIV': '#EF3E2E', 'schistomasis': '#546675', 'lf': '#305516', 'hookworm': '#86AAB9', 'roundworm': '#003452', 'whipworm': '#CAEEFD', 'onchocerciasis': '#5CB85C'}
    piedata = []
    g.db = connect_db()
    pielabb=[]
    pielab = []
    barchart = []
    bardata = []
    if year == '2010':
        if disease == 'all':
            cur = g.db.execute(' select company, daly2010, color from manutot ')
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis ')
            name = 'ALL'
        elif disease == 'hiv':
            cur = g.db.execute(' select company, daly2010, color from manudis where disease = ? ', ('HIV',))
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis where disease = ? ', ('HIV',))
            name = 'HIV'
        elif disease == 'tb':
            cur = g.db.execute(' select company, daly2010, color from manudis where disease = ? ', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis where disease = ? ', ('TB',))
            name = 'TB'
    elif year == '2013':
        if disease == 'all':
            cur = g.db.execute(' select company, daly2013, color from manudis ')
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis ')
            name = 'ALL'
        elif disease == 'hiv':
            cur = g.db.execute(' select company, daly2013, color from manudis where disease = ? ', ('HIV',))
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis where disease = ? ', ('HIV',))
            name = 'HIV'
        elif disease == 'tb':
            cur = g.db.execute(' select company, daly2013, color from manudis where disease = ? ', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis where disease = ? ', ('TB',))
            name = 'TB'
    piee = cur.fetchall()
    barr = cdd.fetchall()

    for j in piee:
        company = j[0]
        daly2010 = j[1]
        color = j[2]
        if daly2010 > 0:
            t = [company, daly2010, color]
            print(t)
            piedata.append(t)
    piedata.sort(key=lambda x: x[1], reverse=True)
    n = 0
    temprow = []
    for k in piedata:
        print(k)
        if n < 4:
            comp = k[0]
            shortcomp = comp[0:10]
            temprow.append(comp)
            temprow.append(shortcomp)
            temprow.append(k[2])
            n += 1
        else:
            n = 0
            pielab.append(temprow)
            temprow = []
    colcnt = 0
    for l in barr:
        company = l[0]
        daly2010 = l[2]
        disease = l[1]
        color = compcolors[colcnt]
        colcnt += 1
        xyz = [company,daly2010,disease,color]
        barchart.append(xyz)
    barchart.sort(key=lambda x: x[1], reverse=True)
    maxim = barchart[0]
    maxval = maxim[1]
    colcnt = 0
    for row in barchart:
        comp = row[0]
        daly = (row[1]/maxval) * 100
        disease = row[2]
        color = compcolors[colcnt]
        colcnt += 1
        xyz = [comp,daly,disease,color]
        bardata.append(xyz)

    g.db.close()
    url = name.lower()
    speclocate = [year,name,url]
    return render_template('company.html', data=piedata, navsub=2, showindex=1, pielab=pielab, bardata=bardata, comptype = 0, speclocate = speclocate, scrolling=1)

@app.route('/index/company/patent/<year>/<disease>')
def patent(year,disease):
    if year == '2010':
        if disease == 'all':
            dat = g.db.execute(' select company, total, color from patent2010 ')
        elif disease == 'tb':
            dat = g.db.execute(' select company, tb, color from patent2010 ')
        elif disease == 'malaria':
            dat = g.db.execute(' select company, malaria, color from patent2010 ')
        elif disease == 'hiv':
            dat = g.db.execute(' select company, hiv, color from patent2010 ')
        elif disease == 'roundworm':
            dat = g.db.execute(' select company, roundworm, color from patent2010 ')
        elif disease == 'hookworm':
            dat = g.db.execute(' select company, hookworm, color from patent2010 ')
        elif disease == 'whipworm':
            dat = g.db.execute(' select company, whipworm, color from patent2010 ')
        elif disease == 'schistosomiasis':
            dat = g.db.execute(' select company, schistosomiasis, color from patent2010 ')
        elif disease == 'onchocerciasis':
            dat = g.db.execute(' select company, onchocerciasis, color from patent2010 ')
        elif disease == 'lf':
            dat = g.db.execute(' select company, lf, color from patent2010 ')
    elif year == '2013':
        if disease == 'all':
            dat = g.db.execute(' select company, total, color from patent2013 ')
        elif disease == 'tb':
            dat = g.db.execute(' select company, tb, color from patent2013 ')
        elif disease == 'malaria':
            dat = g.db.execute(' select company, malaria, color from patent2013 ')
        elif disease == 'hiv':
            dat = g.db.execute(' select company, hiv, color from patent2013 ')
        elif disease == 'roundworm':
            dat = g.db.execute(' select company, roundworm, color from patent2013 ')
        elif disease == 'hookworm':
            dat = g.db.execute(' select company, hookworm, color from patent2013 ')
        elif disease == 'whipworm':
            dat = g.db.execute(' select company, whipworm, color from patent2013 ')
        elif disease == 'schistosomiasis':
            dat = g.db.execute(' select company, schistosomiasis, color from patent2013 ')
        elif disease == 'onchocerciasis':
            dat = g.db.execute(' select company, onchocerciasis, color from patent2013 ')
        elif disease == 'lf':
            dat = g.db.execute(' select company, lf, color from patent2013 ')
    data = dat.fetchall()
    patent1 = []
    patent2 = []
    for j in data:
        comp = j[0]
        score = j[1]
        color = j[2]
        if score > 0:
            patent1.append([comp,score,color])
    patent1.sort(key=lambda x: x[1], reverse=True)
    maxrow = patent1[0]
    if maxrow[0] == 'Unmet Need':
        maxrow = patent1[1]
    maxval = maxrow[1]
    for row in patent1:
        percent = row[1] / maxval * 100
        row.append(percent)
        if row[0] != 'Unmet Need':
            patent2.append(row)
    specname = disease
    specname[0].upper()
    speclocate = [year,specname,disease]
    pielabb1 = []
    lablist1 = []
    for k in patent1:
        labit = []
        comp = k[0]
        score = k[1]
        color = "#"+k[2]
        shortcomp = comp[0:10]
        labit.append(comp)
        labit.append(shortcomp)
        labit.append(color)
        labit.append(score)
        lablist1.append(labit)
    labrow = []
    xx = 0
    if len(lablist1) < 4:
        pielabb1.append(lablist1)
    else:
        for item in lablist1:
            labrow.append(item)
            xx += 1
            if xx % 4 == 0:
                pielabb1.append(labrow)
                labrow = []
                xx = 0
    pielabb2 = []
    lablist2 = []
    for k in patent2:
        labit = []
        comp = k[0]
        score = k[1]
        color = "#"+k[2]
        shortcomp = comp[0:10]
        labit.append(comp)
        labit.append(shortcomp)
        labit.append(color)
        labit.append(score)
        lablist2.append(labit)
    labrow = []
    xx = 0
    if len(lablist2) < 4:
        pielabb2.append(lablist2)
    else:
        for item in lablist2:
            labrow.append(item)
            xx += 1
            if xx % 4 == 0:
                pielabb2.append(labrow)
                labrow = []
                xx = 0
    return render_template('company.html', navsub=2, showindex=1, comptype = 1, speclocate = speclocate, scrolling=1, patent1 = patent1, patent2 = patent2, pielabb1 = pielabb1, pielabb2 = pielabb2)


@app.route('/dbupdate')
def dbupdate():
    return render_template('updatedb.html', scrolling=2)


def cleanfloat(var):
        if var == '#REF!':
            var = 0
        if var == '#DIV/0!':
            var = 0
        if type(var) != float and type(var) != int:
            var = float(var.replace(',','').replace('%',''))
        if var != var:
            var = 0
        return var

@app.route('/db/drug/refresh')
@requires_auth
def drugdbref():
    conn = sqlite3.connect('ghi.db')
    conn.execute('''DROP TABLE IF EXISTS drugr2010''')
    conn.execute('''DROP TABLE IF EXISTS drugr2013''')
    conn.execute('''CREATE TABLE drugr2010
                (drug text, company text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchocerciasis real, lf real, total real)''')
    conn.execute('''CREATE TABLE drugr2013
                (drug text, company text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchocerciasis real, lf real, total real)''')

    datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
    df = pd.read_csv(datasrc, skiprows=1)
    drugdata = []
    drugrdata = []
    drug2010 = []
    drug2013 = []
    perc2010 = []

    for i in range(1,43):
        drugr = []
        name = df.iloc[4,i]
        drugr.append(name)
        company = df.iloc[1,i]
        drugr.append(company)
        for j in range(10,20):
            if j == 10:
                tb1 = cleanfloat(df.iloc[7,i])
                tb2 = cleanfloat(df.iloc[8,i])
                tb3 = cleanfloat(df.iloc[9,i])
                tb=[tb1,tb2,tb3]
                temp = (tb1+tb2+tb3)
                drugr.append(temp)
            elif j == 11:
                mal1 = cleanfloat(df.iloc[10,i])
                mal2 = cleanfloat(df.iloc[11,i])
                mal=[mal1,mal2]
                temp = (mal1+mal2)
                drugr.append(temp)
            elif j == 19:
                total = cleanfloat(df.iloc[j,i])
                zz = [name,total]
                perc2010.append(zz)
            else:
                temp = df.iloc[j,i]
                if isinstance(temp,float) == False and isinstance(temp,int) == False:
                    temp = float(temp.replace(',',''))
                if temp != temp:
                    temp = 0
                drugr.append(temp)
            if temp > 0:
                if j == 10:
                    disease = 'TB'
                    color = 'FFB31C'
                elif j == 11 or j == 12:
                    disease = 'Malaria'
                    color = '0083CA'
                elif j == 13:
                    disease = 'HIV'
                    color = 'EF3E2E'
                elif j == 14:
                    disease = 'Roundworm'
                    color = '003452'
                elif j == 15:
                    disease = 'Hookworm'
                    color = '86AAB9'
                elif j == 16:
                    disease = 'Whipworm'
                    color = 'CAEEFD'
                elif j == 17:
                    disease = 'Schistosomiasis'
                    color = '546675'
                elif j == 18:
                    disease = 'Onchocerasis'
                    color = '8A5575'
                elif j == 19:
                    disease = 'LF'
                    color = '305516'
                company = df.iloc[1,i]
                drugrow = [name, company, disease, temp, color]
                drug2010.append(drugrow)



        if isinstance(df.iloc[20,i],float) == False:
            score = float(df.iloc[20,i].replace(',',''))
        else:
            score = df.iloc[20,i]
        row = [name,score]
        drugdata.append(row)
        drugrdata.append(drugr)

    unmet = ['Unmet Need','Unmet Need']
    unmetsum = 0
    for xx in [[7,8,9],[10,11],[12],[13],[14],[15],[16],[17],[18]]:
        val = 0
        for yy in xx:
            t = df.iloc[yy,45]
            if isinstance(t,float) == False and isinstance(t,int) == False:
                t = float(t.replace(',',''))
            if t != t:
                t = 0
            val += t
        unmet.append(val)
        unmetsum += val
    print(unmet)
    print(drugrdata[0])
    drugrdata.append(unmet)

    for row in drugrdata:
        tot = sum(row[2:])
        row.append(tot)
        conn.execute('insert into drugr2010 values (?,?,?,?,?,?,?,?,?,?,?,?)', row)

    drugdata = []
    drugrdata = []
    perc2013 = []
    for i in range(50,91):
        drugr = []
        name = df.iloc[4,i]
        drugr.append(name)
        company = df.iloc[1,i]
        drugr.append(company)
        for j in range(10,20):
            if j == 10:
                tb1 = cleanfloat(df.iloc[7,i])
                tb2 = cleanfloat(df.iloc[8,i])
                tb3 = cleanfloat(df.iloc[9,i])
                tb=[tb1,tb2,tb3]
                temp = (tb1+tb2+tb3)
                drugr.append(temp)
            elif j == 11:
                mal1 = cleanfloat(df.iloc[10,i])
                mal2 = cleanfloat(df.iloc[11,i])
                mal=[mal1,mal2]
                temp = (mal1+mal2)
                drugr.append(temp)
            elif j == 19:
                total = cleanfloat(df.iloc[j,i])
                zz = [name,total]
                perc2013.append(zz)
            else:
                temp = df.iloc[j,i]
                if isinstance(temp,float) == False and isinstance(temp,int) == False:
                    temp = float(temp.replace(',',''))
                if temp != temp:
                    temp = 0
                drugr.append(temp)
            if temp > 0:
                if j == 10:
                    disease = 'TB'
                    color = 'FFB31C'
                elif j == 11 or j == 12:
                    disease = 'Malaria'
                    color = '0083CA'
                elif j == 13:
                    disease = 'HIV'
                    color = 'EF3E2E'
                elif j == 14:
                    disease = 'Roundworm'
                    color = '003452'
                elif j == 15:
                    disease = 'Hookworm'
                    color = '86AAB9'
                elif j == 16:
                    disease = 'Whipworm'
                    color = 'CAEEFD'
                elif j == 17:
                    disease = 'Schistosomiasis'
                    color = '546675'
                elif j == 18:
                    disease = 'Onchocerasis'
                    color = '8A5575'
                elif j == 19:
                    disease = 'LF'
                    color = '305516'
                company = df.iloc[1,i]
                drugrow = [name, company, disease, temp, color]
                drug2013.append(drugrow)
        if isinstance(df.iloc[20,i],float) == False:
            score = float(df.iloc[20,i].replace(',',''))
        else:
            score = df.iloc[20,i]
        row = [name,score]
        drugdata.append(row)
        drugrdata.append(drugr)

    unmet = ['Unmet Need','Unmet Need']
    unmetsum = 0
    for xx in [[7,8,9],[10,11],[12],[13],[14],[15],[16],[17],[18]]:
        val = 0
        for yy in xx:
            t = df.iloc[yy,93]
            if isinstance(t,float) == False and isinstance(t,int) == False:
                t = float(t.replace(',',''))
            if t != t:
                t = 0
            val += t
        unmet.append(val)
        unmetsum += val
    drugrdata.append(unmet)
    sortedlist = sorted(drug2013, key=lambda xy: xy[3], reverse=True)

    for row in drugrdata:
        tot = sum(row[2:])
        row.append(tot)
        conn.execute('insert into drugr2013 values (?,?,?,?,?,?,?,?,?,?,?,?)', row)
    perc2013.sort(key=lambda x: x[1], reverse=True)
    conn.commit()
    xx = conn.execute(' select * from drugr2010 ')
    yy = conn.execute(' select * from drugr2013 ')
    drug2010 = xx.fetchall()
    drug2013 = yy.fetchall()
    sheetdata = [[drug2010,list(map(lambda x: x[0], xx.description)),'Table: drug2010'],[drug2013,list(map(lambda x: x[0], yy.description)),'Table: drug2013']]
    dbheader = ['Drug Tables','drug']
    return render_template('dbviewer.html', sheetdata=sheetdata, scrolling=2, dbheader=dbheader)

@app.route('/db/disease/refresh')
@requires_auth
def disdbref():
    conn = sqlite3.connect('ghi.db')
    conn.execute('''DROP TABLE IF EXISTS disease2010''')
    conn.execute('''DROP TABLE IF EXISTS disease2013''')
    conn.execute('''DROP TABLE IF EXISTS disbars''')
    conn.execute('''CREATE TABLE disease2013
                 (disease text, distype text, impact real, daly real, need text, color text)''')

    conn.execute('''CREATE TABLE disease2010
                 (disease text, distype text, impact real, daly real, need text, color text)''')

    conn.execute('''CREATE TABLE disbars
                (disease text, color text, efficacy2010 real, efficacy2013 real, coverage2010 real, coverage2013 real, need2010 real, need2013 real)''')

    datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
    df = pd.read_csv(datasrc, skiprows=1)

    disease2010db = []
    disease2013db = []

    i = 0
    for k in range(7,19):
        distypes = ['TB','TB','TB','Malaria','Malaria','HIV','Roundworm','Hookworm','Whipworm','Schistosomiasis','Onchoceriasis','LF']
        colors = ['#FFB31C','#FFB31C','#FFB31C','#0083CA','#0083CA','#EF3E2E','#003452','#86AAB9','#CAEEFD','#546675','#8A5575','#305516']
        dis = ['Drug Susceptable TB','MDR-TB','XDR-TB','p. falc Malaria','p. vivax Malaria','HIV','Roundworm','Hookworm','Whipworm','Schistosomiasis','Onchoceriasis','LF']
        color = colors[i]
        disease = dis[i]
        distype = distypes[i]
        impact = cleanfloat(df.iloc[k,43])
        daly = cleanfloat(df.iloc[k,45])
        need = cleanfloat(df.iloc[k,46])
        i += 1
        row = [disease,distype,impact,daly,need,color]
        disease2010db.append(row)
        conn.execute('insert into disease2010 values (?,?,?,?,?,?)', row)

    i = 0
    for k in range(7,19):
        distypes = ['TB','TB','TB','Malaria','Malaria','HIV','Roundworm','Hookworm','Whipworm','Schistosomiasis','Onchoceriasis','LF']
        colors = ['#FFB31C','#FFB31C','#FFB31C','#0083CA','#0083CA','#EF3E2E','#003452','#86AAB9','#CAEEFD','#546675','#8A5575','#305516']
        dis = ['Drug Susceptable TB','MDR-TB','XDR-TB','p. falc Malaria','p. vivax Malaria','HIV','Roundworm','Hookworm','Whipworm','Schistosomiasis','Onchoceriasis','LF']
        color = colors[i]
        disease = dis[i]
        distype = distypes[i]
        impact = cleanfloat(df.iloc[k,92])
        daly = cleanfloat(df.iloc[k,94])
        need = cleanfloat(df.iloc[k,95])
        i += 1
        row = [disease,distype,impact,daly,need,color]
        disease2013db.append(row)
        conn.execute('insert into disease2013 values (?,?,?,?,?,?)', row)


    def stripdata(x,y):
        tmp = df.iloc[x,y]
        return cleanfloat(tmp)

    disbars = []
    j=0
    for k in range(90, 99):
        colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                  '#546675', '#8A5575', '#305516']
        diseasename = df.iloc[k,7]
        color = colors[j]
        efficacy2010 = cleanfloat(df.iloc[k,8])
        efficacy2013 = cleanfloat(df.iloc[k,9])
        coverage2010 = cleanfloat(df.iloc[k,10])
        coverage2011 = cleanfloat(df.iloc[k,11])
        need2010 = cleanfloat(df.iloc[k,12])
        need2013 = cleanfloat(df.iloc[k,13])
        roww = [diseasename,color,efficacy2010,efficacy2013,coverage2010,coverage2011,need2010,need2013]
        print(roww)
        disbars.append(roww)
        j+=1
        conn.execute('insert into disbars values (?,?,?,?,?,?,?,?)', roww)

    conn.commit()
    xx = conn.execute(' select * from disease2010 ')
    yy = conn.execute(' select * from disease2013 ')
    zz = conn.execute(' select * from disbars ')
    disease2010 = xx.fetchall()
    disease2013 = yy.fetchall()
    disbars = zz.fetchall()
    sheetdata = [[disease2010,list(map(lambda x: x[0], xx.description)),'Table: disease2010'],[disease2013,list(map(lambda x: x[0], yy.description)),'Table: disease2013'],[disbars,list(map(lambda x: x[0], zz.description)),'Table: disbars']]
    dbheader = ['Drug Tables','drug']
    return render_template('dbviewer.html', sheetdata=sheetdata, scrolling=2, dbheader=dbheader)


@app.route('/dbupdate/<db>')
def updateit(db):
    conn = connect_db()
    if db == 'company':
        conn.execute('''DROP TABLE IF EXISTS manufacturer2010''')
        conn.execute('''DROP TABLE IF EXISTS manufacturer2013''')
        conn.execute('''DROP TABLE IF EXISTS manudis''')
        conn.execute('''DROP TABLE IF EXISTS manutot''')
        conn.execute('''CREATE TABLE manudis
                     (company text, disease text, daly2010 real, daly2013 real, color text)''')
        conn.execute('''CREATE TABLE manutot
                     (company text, daly2010 real, daly2013 real, color text)''')
        datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
        df = pd.read_csv(datasrc, skiprows=1)
        i = 0;
        colorlist = []
        colors = ['FFB31C','0083CA','EF3E2E','003452','86AAB9','CAEEFD','546675','8A5575','305516','B78988','BAE2DA','B1345D','5B75A7','906F76','C0E188','DE9C2A','F15A22','8F918B','F2C2B7','F7C406','B83F98','548A9B','D86375','F1DBC6','0083CA','7A80A3','CA8566','A3516E','1DF533','510B95','DFF352','F2C883','E3744D','26B2BE','5006BA','B99BCF','DC2A5A','D3D472','2A9DC4','C25C90','65A007','FE3289','C6DAB5','DDF6AC','B7E038','1ADBBD','3BC6D5','0ACD57','22419F','D47C5B']
        for x in colors:
            y = '#'+x
            colorlist.append(y)
        print(colorlist)
        manudata = []
        manutotal = []
        for k in range(24,88):
            company = df.iloc[k,2]
            if isinstance(company,float):
                if math.isnan(company):
                    break
            disease = 'TB'
            tbdaly2010 = float(df.iloc[k,3].replace('-','0').replace(',',''))
            tbdaly2013 = float(df.iloc[k,4].replace('-','0').replace(',',''))
            if tbdaly2010 > 0 or tbdaly2013 > 0:
                color = colors[i]
                row=[company,disease,tbdaly2010,tbdaly2013,color]
                manudata.append(row)
                i += 1
                conn.execute('insert into manudis values (?,?,?,?,?)', row)
        i=0
        for k in range(24,88):
            company = df.iloc[k,6]
            if isinstance(company,float):
                if math.isnan(company):
                    break
            disease = 'HIV'
            hivdaly2010 = float(df.iloc[k,10].replace('-','0').replace(',',''))
            hivdaly2013 = float(df.iloc[k,11].replace('-','0').replace(',',''))
            if hivdaly2010 > 0 or hivdaly2013 > 0:
                color = colors[i]
                row=[company,disease,hivdaly2010,hivdaly2013,color]
                i += 1
                manudata.append(row)
                conn.execute('insert into manudis values (?,?,?,?,?)', row)
        i=0
        for k in range(24,88):
            company = df.iloc[k,12]
            if isinstance(company,float):
                if math.isnan(company):
                    break
            daly2010 = float(df.iloc[k,13].replace('-','0').replace(',',''))
            daly2013 = float(df.iloc[k,14].replace('-','0').replace(',',''))
            if daly2010 > 0 or daly2013 > 0:
                color = colors[i]
                row=[company,daly2010,daly2013,color]
                i += 1
                manutotal.append(row)
                conn.execute('insert into manutot values (?,?,?,?)', row)
        conn.commit()
    elif db == 'country':
        conn.execute('''DROP TABLE IF EXISTS countrybydis2010''')
        conn.execute('''DROP TABLE IF EXISTS countrybydis2013''')
        conn.execute('''CREATE TABLE countrybydis2010
                     (country text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schis real, onch real, lf real)''')
        conn.execute('''CREATE TABLE countrybydis2013
                     (country text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schis real, onch real, lf real)''')
        datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1996016204&single=true&output=csv'
        df = pd.read_csv(datasrc, skiprows=1)
        for i in range (1,216):
            temprow = []
            temprow.append(df.iloc[i,0])
            for k in range(1,10):
                temp = df.iloc[i,k]
                if isinstance(temp,float):
                    temprow.append(0.0)
                else:
                    temprow.append(float(temp.replace(',','').replace('-','0')))
            conn.execute(' insert into countrybydis2010 values (?,?,?,?,?,?,?,?,?,?)', temprow)
        for i in range (1,216):
            temprow = []
            temprow.append(df.iloc[i,11])
            for k in range(12,21):
                temp = df.iloc[i,k]
                if isinstance(temp,float):
                    temprow.append(0.0)
                else:
                    temprow.append(float(temp.replace(',','').replace('-','0')))
            conn.execute(' insert into countrybydis2013 values (?,?,?,?,?,?,?,?,?,?)', temprow)
        conn.execute(''' DROP TABLE IF EXISTS country2010 ''')
        conn.execute(''' DROP TABLE IF EXISTS country2013 ''')
        conn.execute(''' DROP TABLE IF EXISTS countryp2010 ''')
        conn.execute(''' DROP TABLE IF EXISTS countryp2013 ''')

        conn.execute(''' CREATE TABLE country2010 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistomasis real, lf real) ''')
        conn.execute(''' CREATE TABLE country2013 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistomasis real, onchoceriasis real, lf real) ''')

        conn.execute(''' CREATE TABLE countryp2010 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistomasis real, lf real) ''')
        conn.execute(''' CREATE TABLE countryp2013 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistomasis real, onchoceriasis real, lf real) ''')


        url = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=0&single=true&output=csv'
        df = pd.read_csv(url, skiprows=1)

        def clean(num):
            return float(num.replace(' ','').replace(',','').replace('-','0'))

        countrydata = []
        mapp = []

        for i in range(3, 218):
            country = df.iloc[i,0]
            tb = clean(df.iloc[i,7])
            malaria = clean(df.iloc[i,34])
            hiv = clean(df.iloc[i,47])
            roundworm = clean(df.iloc[i,66])
            hookworm = clean(df.iloc[i,67])
            whipworm = clean(df.iloc[i,68])
            schistomasis = clean(df.iloc[i,76])
            lf = clean(df.iloc[i,80])
            total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistomasis + lf
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf]
            countrydata.append(row)

        sortedlist = sorted(countrydata, key=lambda xy: xy[1], reverse=True)
        maxrow = sortedlist[0]
        maxval = maxrow[1]
        for j in sortedlist:
            country = j[0]
            total = (j[1]/maxval) *  100
            tb = (j[2]/maxval) *  100
            malaria = (j[3]/maxval) *  100
            hiv = (j[4]/maxval) *  100
            roundworm = (j[5]/maxval) *  100
            hookworm = (j[6]/maxval) *  100
            whipworm = (j[7]/maxval) *  100
            schistomasis = (j[8]/maxval) *  100
            lf = (j[9]/maxval) *  100
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, lf]
            mapp.append(row)
        for k in countrydata:
            conn.execute(''' INSERT INTO country2010 VALUES (?,?,?,?,?,?,?,?,?,?) ''', k)

        for l in mapp:
            conn.execute(''' INSERT INTO countryp2010 VALUES (?,?,?,?,?,?,?,?,?,?) ''', l)

        countrydata2 = []
        mapp2 = []
        for i in range(3, 218):
            country = df.iloc[i,83]
            tb = clean(df.iloc[i,90])
            malaria = clean(df.iloc[i,120])
            hiv = clean(df.iloc[i,131])
            roundworm = clean(df.iloc[i,150])
            hookworm = clean(df.iloc[i,151])
            whipworm = clean(df.iloc[i,152])
            schistomasis = clean(df.iloc[i,160])
            onchoceriasis = clean(df.iloc[i,165])
            lf = clean(df.iloc[i,169])
            total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistomasis + onchoceriasis + lf
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, onchoceriasis, lf]
            countrydata2.append(row)

        sortedlist2 = sorted(countrydata2, key=lambda xy: xy[1], reverse=True)
        maxrow = sortedlist2[0]
        maxval = maxrow[1]
        for j in sortedlist2:
            country = j[0]
            total = (j[1]/maxval) *  100
            tb = (j[2]/maxval) *  100
            malaria = (j[3]/maxval) *  100
            hiv = (j[4]/maxval) *  100
            roundworm = (j[5]/maxval) *  100
            hookworm = (j[6]/maxval) *  100
            whipworm = (j[7]/maxval) *  100
            schistomasis = (j[8]/maxval) *  100
            onchoceriasis = (j[9]/maxval) * 100
            lf = (j[10]/maxval) *  100
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistomasis, onchoceriasis, lf]
            mapp2.append(row)

        for k in countrydata2:
            conn.execute(''' INSERT INTO country2013 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', k)

        for l in mapp2:
            conn.execute(''' INSERT INTO countryp2013 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', l)
        conn.commit()
    conn.close()
    return render_template('updatedb.html')

@app.route('/viewdb/<table>')
def dbviewer(table):
    sheetdata = []
    if table == 'company':
        conn = connect_db()
        xx = conn.execute(' select * from manutot ')
        yy = conn.execute(' select * from manudis ')
        manutot = xx.fetchall()
        manudis = yy.fetchall()
        sheetdata = [[manutot,list(map(lambda x: x[0], xx.description)),'Table: manutot'],[manudis,list(map(lambda x: x[0], yy.description)),'Table: manudis']]
        dbheader = ['Company Tables','company']
    elif table == 'country':
        conn = connect_db()
        cd2010 = conn.execute(' select * from countrybydis2010 ')
        cd2013 = conn.execute(' select * from countrybydis2013 ')
        cnt2010 = conn.execute(' select * from country2010 ')
        cnt2013 = conn.execute(' select * from country2013 ')
        cntp2010 = conn.execute(' select * from countryp2010 ')
        cntp2013 = conn.execute(' select * from countryp2013 ')
        countrybydis2010 = cd2010.fetchall()
        countrybydis2013 = cd2013.fetchall()
        country2010 = cnt2010.fetchall()
        country2013 = cnt2013.fetchall()
        countryp2010 = cntp2010.fetchall()
        countryp2013 = cntp2013.fetchall()
        sheetdata = [[countrybydis2010,list(map(lambda x: x[0], cd2010.description)),'Table: countrybydis2010'],[countrybydis2013,list(map(lambda x: x[0], cd2013.description)),'Table: countrybydis2013'],[country2010,list(map(lambda x: x[0], cnt2010.description)),'Table: country2010'],[country2013,list(map(lambda x: x[0], cnt2013.description)),'Table: country2013'],[countryp2010,list(map(lambda x: x[0], cntp2010.description)),'Table: countryp2010'],[countryp2013,list(map(lambda x: x[0], cntp2013.description)),'Table: countryp2013']]
        dbheader = ['Country Tables','country']
    return render_template('dbviewer.html', sheetdata=sheetdata, scrolling=2, dbheader=dbheader)



if __name__ == '__main__':
    app.run(debug=False)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

