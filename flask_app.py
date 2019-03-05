
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, g
from openpyxl.compat import range
import pandas as pd
import sqlite3
import json
import math
import companydb as objDbComp
import countrybydisdb as objDbCountryDis
import countrydb as objDBCountry
import dbupdate as objDBDrug
import diseasedb as objDBDisease

app = Flask(__name__)

DATABASE = 'ghi.db'
app.config.from_object(__name__)

from functools import wraps
from flask import request, Response
diseaseColorMap = {'tb':'#FFB31C','hiv':'#0083CA','malaria':'#EF3E2E','onchocerciasis':'#86AAB9','schistosomiasis':'#003452','lf':'#CAEEFD','hookworm':'#546675','roundworm':'#8A5575','whipworm':'#305516'}

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
        if not authorization or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def connect_db():
    return sqlite3.connect('/Users/shankydoodle/Technovanza/Projects/GHI PROJECT/global-health-impact-web-/ghi.db')
    # return sqlite3.connect('/home/globalhealth/mysite/ghi.db')

@app.before_request
def before_request():
    # print("In before_request")
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

diseasedict = {'tb':'TB','hiv':'HIV','malaria':'Malaria','onchocerciasis':'Onchocerciasis','schistosomiasis':'Schistosomiasis','lf':'LF','hookworm':'Hookworm','roundworm':'Roundworm','whipworm':'Whipworm'}

def getTreatmentEffectivenessByDrug(disease, year):
    g.db = connect_db()

    drugData = g.db.execute(
        " select drug, " + disease + ", 'color: darkblue' from drugr" + year +
        " where " + disease + " > 0 "
    ).fetchall()
    g.db.close()

    formattedData = []

    for row in drugData:
        drug = str(row[0])
        tb = row[1]
        color = row[2]
        formattedData.append([drug, tb, color])
    return formattedData

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
    maxTotal = 0
    g.db = connect_db()
    cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf from diseaseall2010 ')
    data = cur.fetchall()
    ddisease = 'All'
    dyear = '2010'
    print(data)
    for row in data:
        country = str(row[0].encode('ascii','ignore'))
        print(country)
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
    return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index, disease=1, speclocate = speclocate, scrolling=1, maxTotal = total)

@app.route('/index/disease/<dyear>/<ddisease>')
def diseasepg(dyear, ddisease):
    piedata = []
    bar1data = []
    bar1 = []
    bar2 = []
    bar3 = []
    piedat = []
    clickdat = []
    maxTotal = 0

    print(ddisease)

    if dyear == '2010':
        if ddisease == 'summary':
            g.db = connect_db()
            cur = g.db.execute(' select disease, impact, color from disease2010 ')
            daly = g.db.execute(' select disease, daly, color from disease2010 ')
            barz = g.db.execute(' select disease, color, efficacy2010, coverage2010, need2010 from disbars ')
            barg = daly.fetchall()
            pied = cur.fetchall()
            bardata = barz.fetchall()
            c = 0
            barcolors = ['#FFB31C', '#0083CA', '#EF3E2E', '#86AAB9', '#003452', '#CAEEFD', '#546675', '#8A5575',
                         '#305516']
            for row in bardata:
                diss = str(row[0])
                color = "color: " +  str(row[1])
                c += 1
                efficacy = row[2]
                coverage = row[3]
                need = row[4]
                x = [diss, efficacy, color]
                y = [diss, need, color]
                z = [diss, coverage, color]
                bar1.append(y)
                bar2.append(z)
                bar3.append(x)

            for row in pied:
                name = str(row[0])
                imp = row[1]
                color = "color: " + str(row[2])
                x = [name, imp]
                piedata.append(x)
            for row in barg:
                name = str(row[0])
                daly = row[1]
                color = "color: " + str(row[2])
                x = [name, daly, color]
                bar1data.append(x)
            g.db.close()
            upp = ddisease.upper()
            speclocate = [dyear, ddisease, upp]
            return render_template('disease.html', navsub=4, showindex=1, diseasepie=piedata, bar1data=bar1data,
                                   disease=0, bar1=bar1, bar2=bar2, bar3=bar3, speclocate=speclocate, scrolling=1, maxTotal = maxTotal)

        elif ddisease == 'malaria':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, malaria from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010 ,position from distypes where distype=? order by position ASC ',
                ('Malaria',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'tb':
            g.db = connect_db()
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010 ,position from distypes where distype=? order by position ASC ',
                ('TB',))
            cur2 = g.db.execute(' select country, tb from diseaseall2010 ')
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'hiv':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, hiv from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010 ,position from distypes where distype=? order by position ASC ',
                ('HIV',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'onchocerciasis':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, onchocerciasis from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010 ,position from distypes where distype=? order by position ASC ',
                ('Onchoceriasis',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'schistosomiasis':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, schistosomiasis from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010 ,position from distypes where distype=? order by position ASC ',
                ('Schistosomiasis',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'lf':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, lf from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010 ,position from distypes where distype=? order by position ASC ',
                ('LF',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'hookworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, hookworm from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010,position from distypes where distype=? order by position ASC ',
                ('Hookworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'roundworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, roundworm from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010,position from distypes where distype=? order by position ASC ',
                ('Roundworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'whipworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, whipworm from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2010,coverage2010,position from distypes where distype=? order by position ASC ',
                ('Whipworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'all':
            g.db = connect_db()
            cur = g.db.execute(
                ' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf from diseaseall2010 ')
            data = cur.fetchall()
            for row in data:
                country = str(row[0].encode('ascii','ignore'))
                tb = row[1]
                malaria = row[2]
                hiv = row[3]
                roundworm = row[4]
                hookworm = row[5]
                whipworm = row[6]
                schistosomiasis = row[7]
                onchocerciasis = row[8]
                lf = row[9]
                total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + onchocerciasis + lf
                xx = [country, total]
                xy = [country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf]
                piedat.append(xx)
                clickdat.append(xy)
                seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
                index = [seq.index(v) for v in piedat]
                piedat.insert(0, ['Country', 'DALY'])
                g.db.close()
                upp = ddisease.upper()
                speclocate = [dyear, ddisease, upp]
                return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index,
                           disease=1, speclocate=speclocate, scrolling=1, maxTotal = total)
        barcolors = ['#FFD480', '#CCCC00', '#CCA300', '#86AAB9', '#003452', '#CAEEFD', '#546675', '#8A5575', '#305516']
        c = 0
        print(data)
        for row in data:
            disease = str( row[0])
            tb = row[1]
            color = "color: " + str(row[2])
            c += 1
            efficacy2010 = row[3]
            coverage2010 = row[4]
            xx = [disease, efficacy2010, color]
            xy = [disease, coverage2010, color]
            bar1.append(xx)
            bar2.append(xy)
            print('=======')
            print(efficacy2010)

        bar2 = getTreatmentEffectivenessByDrug(ddisease, dyear)
        for row in data2:
            country = str(row[0].encode('ascii','ignore'))
            tb = row[1]
            # xx = [country,tb]
            xy = [country, tb]
            if tb > maxTotal:
                maxTotal = tb
            piedat.append(xy)
            clickdat.append(xy)
        print('==========efficacy2010=====')
        print(bar1)
        print(bar2)
        seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
        index = [seq.index(v) for v in piedat]
        piedat.insert(0, ['Country', 'DALY'])
        print(piedat)
        upp = ddisease.upper()
        speclocate = [dyear, ddisease, upp]
        return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index,
                               bar1=bar1, bar2=bar2, disease=2, speclocate=speclocate, scrolling=1, maxTotal = maxTotal)

    elif dyear == '2013':
        if ddisease == 'summary':
            g.db = connect_db()
            cur = g.db.execute(' select disease, impact, color from disease2013 ')
            daly = g.db.execute(' select disease, daly, color from disease2013 ')
            barz = g.db.execute(' select disease, color, efficacy2013, coverage2013, need2013 from disbars ')
            barg = daly.fetchall()
            pied = cur.fetchall()
            bardata = barz.fetchall()
            c = 0
            barcolors = ['#FFB31C', '#0083CA', '#EF3E2E', '#86AAB9', '#003452', '#CAEEFD', '#546675', '#8A5575',
                         '#305516']
            for row in bardata:
                diss = str(row[0])
                color = "color: "  + str(row[1])
                c += 1
                efficacy = row[2]
                coverage = row[3]
                need = row[4]
                x = [diss, efficacy, color]
                y = [diss, need, color]
                z = [diss, coverage, color]
                bar1.append(y)
                bar2.append(z)
                bar3.append(x)
            for row in pied:
                name = str(row[0])
                imp = row[1]
                color = "color: "  + str(row[2])
                x = [name, imp]
                piedata.append(x)
            for row in barg:
                name = str( row[0])
                daly = row[1]
                color = "color: " + str(row[2])
                x = [name, daly, color]
                bar1data.append(x)
            g.db.close()
            upp = ddisease.upper()
            speclocate = [dyear, ddisease, upp]
            return render_template('disease.html', navsub=4, showindex=1, diseasepie=piedata, bar1data=bar1data,
                                   disease=0, bar1=bar1, bar2=bar2, bar3=bar3, speclocate=speclocate, maxTotal = maxTotal)


        elif ddisease == 'malaria':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, malaria from diseaseall2010 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('Malaria',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'tb':
            g.db = connect_db()
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('TB',))
            cur2 = g.db.execute(' select country, tb from diseaseall2013 ')
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'hiv':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, hiv from diseaseall2013 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('HIV',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'onchocerciasis':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, onchocerciasis from diseaseall2013 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('Onchoceriasis',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'schistosomiasis':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, schistosomiasis from diseaseall2013 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('Schistosomiasis',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'lf':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, lf from diseaseall2013 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('LF',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'hookworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, hookworm from diseaseall2013 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('Hookworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'roundworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, roundworm from diseaseall2013 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('Roundworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'whipworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, whipworm from diseaseall2013 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes where distype=? order by position ASC ',
                ('Whipworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()



        elif ddisease == 'all':
            g.db = connect_db()
            cur = g.db.execute(
                ' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf from diseaseall2013 ')
            data = cur.fetchall()
            for row in data:
                country = str(row[0])
                tb = row[1]
                malaria = row[2]
                hiv = row[3]
                roundworm = row[4]
                hookworm = row[5]
                whipworm = row[6]
                schistosomiasis = row[7]
                onchocerciasis = row[8]
                lf = row[9]
                total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + onchocerciasis + lf
                xx = [country, total]
                xy = [country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf]
                piedat.append(xx)
                clickdat.append(xy)
            seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
            index = [seq.index(v) for v in piedat]
            piedat.insert(0, ['Country', 'DALY'])
            g.db.close()
            upp = ddisease.upper()
            speclocate = [dyear, ddisease, upp]
            return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index,
                                   disease=1, speclocate=speclocate, scrolling=1, maxTotal = maxTotal)

        barcolors = ['#FFD480', '#CCCC00', '#CCA300', '#86AAB9', '#003452', '#CAEEFD', '#546675', '#8A5575', '#305516']
        c = 0
        print(data)
        for row in data:
            disease = str( row[0])
            tb = row[1]
            color = "color: " + str(row[2])
            c += 1
            efficacy2013 = row[3]
            coverage2013 = row[4]
            xx = [disease, efficacy2013, color]
            xy = [disease, coverage2013, color]
            bar1.append(xx)
            # bar2.append(xy)
            print('=======')
            print(efficacy2013)
        bar2 = getTreatmentEffectivenessByDrug(ddisease, dyear)
        for row in data2:
            country = str(row[0])
            tb = row[1]
            # xx = [country,tb]
            xy = [country, tb]
            if tb > maxTotal:
                maxTotal = tb
            piedat.append(xy)
            clickdat.append(xy)
        print('==========efficacy2010=====')
        print(bar1)

        seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
        index = [seq.index(v) for v in piedat]
        piedat.insert(0, ['Country', 'DALY'])
        upp = ddisease.upper()
        speclocate = [dyear, ddisease, upp]
        return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index,
                               bar1=bar1, bar2=bar2, disease=2, speclocate=speclocate, scrolling=1, maxTotal = maxTotal)
    elif dyear == '2015':
        if ddisease == 'summary':
            g.db = connect_db()
            cur = g.db.execute(' select disease, impact, color from disease2015 ')
            daly = g.db.execute(' select disease, daly, color from disease2015 ')
            barz = g.db.execute(' select disease, color, efficacy2013, coverage2013, need2013 from disbars2010B2015 ')
            barg = daly.fetchall()
            pied = cur.fetchall()
            bardata = barz.fetchall()
            c = 0
            barcolors = ['#FFB31C', '#0083CA', '#EF3E2E', '#86AAB9', '#003452', '#CAEEFD', '#546675', '#8A5575',
                         '#305516']
            for row in bardata:
                # diss = str( row[0])
                # color = "color: "  + str(row[1])
                print(row)
                diss = str(row[0])
                color = "color: " + str(row[1])
                c += 1
                efficacy = row[2]
                coverage = row[3]
                need = row[4]
                x = [diss, efficacy, color]
                y = [diss, need, color]
                z = [diss, coverage, color]
                bar1.append(y)
                bar2.append(z)
                bar3.append(x)
            for row in pied:
                name = str(row[0])
                imp = row[1]
                color = "color: " + str(row[2])
                x = [name, imp]
                piedata.append(x)
            for row in barg:
                name = row[0]
                daly = row[1]
                color = "color: " + str(row[2])
                x = [name, daly, color]
                bar1data.append(x)
            g.db.close()
            upp = ddisease.upper()
            speclocate = [dyear, ddisease, upp]
            return render_template('disease.html', navsub=4, showindex=1, diseasepie=piedata, bar1data=bar1data,
                                   disease=0, bar1=bar1, bar2=bar2, bar3=bar3, speclocate=speclocate, maxTotal = maxTotal)


        elif ddisease == 'malaria':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, malaria from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('Malaria',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'tb':
            g.db = connect_db()
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('TB',))
            cur2 = g.db.execute(' select country, tb from diseaseall2013 ')
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'hiv':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, hiv from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('HIV',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'onchocerciasis':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, onchocerciasis from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('Onchoceriasis',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'schistosomiasis':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, schistosomiasis from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('Schistosomiasis',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'lf':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, lf from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('LF',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'hookworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, hookworm from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('Hookworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'roundworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, roundworm from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('Roundworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()

        elif ddisease == 'whipworm':
            g.db = connect_db()
            cur2 = g.db.execute(' select country, whipworm from diseaseall2015 ')
            cur = g.db.execute(
                ' select disease,distype,color,efficacy2013,coverage2013 ,position from distypes2010B2015 where distype=? order by position ASC ',
                ('Whipworm',))
            data = cur.fetchall()
            data2 = cur2.fetchall()
            g.db.close()



        elif ddisease == 'all':
            g.db = connect_db()
            cur = g.db.execute(
                ' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf from diseaseall2015 ')
            data = cur.fetchall()
            print(data)
            for row in data:
                country = str(row[0])
                tb = row[1]
                malaria = row[2]
                hiv = row[3]
                roundworm = row[4]
                hookworm = row[5]
                whipworm = row[6]
                schistosomiasis = row[7]
                onchocerciasis = row[8]
                lf = row[9]
                total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + onchocerciasis + lf
                xx = [country, total]
                xy = [country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchocerciasis, lf]
                piedat.append(xx)
                clickdat.append(xy)
            seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
            index = [seq.index(v) for v in piedat]
            piedat.insert(0, ['Country', 'DALY'])
            g.db.close()
            upp = ddisease.upper()
            speclocate = [dyear, ddisease, upp]
            return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index,
                                   disease=1, speclocate=speclocate, scrolling=1, maxTotal = maxTotal)

        barcolors = ['#FFD480', '#CCCC00', '#CCA300', '#86AAB9', '#003452', '#CAEEFD', '#546675', '#8A5575', '#305516']
        c = 0
        print(data)
        for row in data:
            disease = str(row[0])
            tb = row[1]
            color = "color: "  + str(row[2])
            c += 1
            efficacy2013 = row[3]
            coverage2013 = row[4]
            xx = [disease, efficacy2013, color]
            xy = [disease, coverage2013, color]
            bar1.append(xx)
            # bar2.append(xy)
            print('=======')
            print(efficacy2013)
        bar2 = getTreatmentEffectivenessByDrug(ddisease, dyear)
        for row in data2:
            country = str(row[0])
            tb = row[1]
            # xx = [country,tb]
            xy = [country, tb]
            if tb > maxTotal:
                maxTotal = tb
            piedat.append(xy)
            clickdat.append(xy)
        print('==========efficacy2010=====')
        print(bar1)

        seq = sorted(piedat, key=lambda sc: sc[1], reverse=True)
        index = [seq.index(v) for v in piedat]
        piedat.insert(0, ['Country', 'DALY'])
        upp = ddisease.upper()
        speclocate = [dyear, ddisease, upp]
        return render_template('disease.html', navsub=4, showindex=1, piedat=piedat, clickdat=clickdat, index=index,
                               bar1=bar1, bar2=bar2, disease=2, speclocate=speclocate, scrolling=1, maxTotal = maxTotal)


@app.route('/reports')
def reports():
    repdata = g.db.execute('select * from reports2010')
    repbar = g.db.execute('select * from reportsdetail2010')

    reports2010 = repdata.fetchall()
    reportsbar2010 = repbar.fetchall()
    reportdict = []
    reportbar2010 = []
    print(reports2010)
    print(reportsbar2010)

    for i in reports2010:
        id = i[0]
        year = i[1]
        cname = str(i[2])
        timpactscre = i[3]
        rank = i[4]
        numOfDis = i[5]
        row = [id, year, cname, timpactscre, rank, numOfDis]
        reportdict.append(row)
    print(reportdict)


    for i in reportsbar2010:
        _id = i[0]
        year = i[1]
        cname = str(i[2])
        drug = str(i[3])
        disease = str(i[4])
        impact = i[5]
        rowbar = [_id, year, cname, drug, disease, impact]
        reportbar2010.append(rowbar)
    print(reportbar2010)


    return render_template('reports.html',report2010=reportdict, reportdetail2010 = reportbar2010)

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
    drugcolors = ['#7A80A3','#B78988','#906F76','#8F918B','#548A9B','#BAE2DA','#C0E188','#f2c2b7',
                  '#d86375','#b1345d','#de9c2a','#f7c406','#f1dbc6','#5b75a7','#f15a22','#b83f98',
                  '#0083ca','#FFB31C','#0083CA','#EF3E2E','#003452','#86AAB9','#CAEEFD','#546675',
                  '#8A5575','#305516','#B78988','#BAE2DA','#B1345D','#5B75A7','#906F76','#C0E188',
                  '#B99BCF', '#DC2A5A', '#D3D472','#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5',
                  '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5', '#0ACD57', '#22419F','#D47C5B','#003452',
                  '#86AAB9', '#CAEEFD' ]
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
        _row = str(row[0])
        if _row != 'Unmet Need':
            color = drugcolors[c]
        else:
            color = '#a6a6a6'
        row.append(color)
        c+=1
        if _row != 'Unmet Need':
            impactpie.append(row)
    pielabb = []
    n=0
    temprow=[]
    for k in impactpie:
        print(k)
        if n < 2:
            drug = k[0]
            tempcomp = drug
            tempval = len(drug)
            print(tempval)
            if tempval > 25:
                if len(drug) == 48:
                    shortdrug = tempcomp.rsplit(' ', 4)[0]
                else:
                    shortdrug = tempcomp.rsplit(' ', 2)[0]
            else:
                shortdrug = drug[0:25]
            score = k[1]
            color = k[3]
            col =  color[1:7]
            temprow.append(drug)
            temprow.append(shortdrug)
            temprow.append(col)
            temprow.append(score)
            n+=1
        else:
            n=0
            pielabb.append(temprow)
            temprow=[]

    speclocate = ['2010','all','ALL']
    pielabb2=[]
    n = 0
    temprow = []
    for k in sortedpie2:
        print(k)
        if n < 2:
            drug = str( k[0])
            tempcomp = drug
            tempval = len(drug)
            if tempval > 25:
                if len(drug) == 48:
                    shortdrug = tempcomp.rsplit(' ', 4)[0]
                else:
                    shortdrug = tempcomp.rsplit(' ', 2)[0]
            else:
                shortdrug = drug[0:25]
            score = k[1]
            color = k[3]
            col =  color[1:7]
            temprow.append(drug)
            temprow.append(shortdrug)
            temprow.append(col)
            temprow.append(score)
            n+=1
        else:
            n = 0
            pielabb2.append(temprow)
            temprow = []
    print(pielabb)
    print(pielabb2)
    g.db.close()
    return render_template('drug.html', data=piedata, drug='All', navsub=3, showindex=1, pielab1=pielabb2,pielab2=pielabb, drugcolors=drugcolors, speclocate = speclocate, scrolling=1, impactpie=impactpie, sortedpie2 = sortedpie2)

@app.route('/index/drug/<year>/<disease>')
def drug(year,disease):
    drugcolors = ['#7A80A3','#B78988','#906F76','#8F918B','#548A9B','#BAE2DA','#C0E188','#f2c2b7',
                  '#d86375','#b1345d','#de9c2a','#f7c406','#f1dbc6','#5b75a7','#f15a22','#b83f98',
                  '#0083ca','#FFB31C','#0083CA','#EF3E2E','#003452','#86AAB9','#CAEEFD','#546675',
                  '#8A5575','#305516','#B78988','#BAE2DA','#B1345D','#5B75A7','#906F76','#C0E188',
                  '#B99BCF', '#DC2A5A', '#D3D472','#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5',
                  '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5', '#0ACD57', '#22419F','#D47C5B','#003452',
                  '#86AAB9', '#CAEEFD' ]
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
        elif year == '2015':
            cur = g.db.execute(' select drug, total from drugr2015 ')
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
                cur = g.db.execute(' select drug, whipworm from drugr2010 ')
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
                cur = g.db.execute(' select drug, whipworm from drugr2013 ')
            elif disease == 'schistosomiasis':
                cur = g.db.execute(' select drug, schistosomiasis from drugr2013 ')
            elif disease == 'onchocerciasis':
                cur = g.db.execute(' select drug, onchocerciasis from drugr2013 ')
            elif disease == 'lf':
                cur = g.db.execute(' select drug, lf from drugr2013 ')

        elif year == '2015':
            if disease == 'malaria':
                cur = g.db.execute(' select drug, malaria from drugr2015 ')
            elif disease == 'hiv':
                cur = g.db.execute(' select drug, hiv from drugr2015 ')
            elif disease == 'tb':
                cur = g.db.execute(' select drug, tb from drugr2015 ')
            elif disease == 'roundworm':
                cur = g.db.execute(' select drug, roundworm from drugr2015 ')
            elif disease == 'hookworm':
                cur = g.db.execute(' select drug, hookworm from drugr2015 ')
            elif disease == 'whipworm':
                cur = g.db.execute(' select drug, whipworm from drugr2015 ')
            elif disease == 'schistosomiasis':
                cur = g.db.execute(' select drug, schistosomiasis from drugr2015 ')
            elif disease == 'onchocerciasis':
                cur = g.db.execute(' select drug, onchocerciasis from drugr2015 ')
            elif disease == 'lf':
                cur = g.db.execute(' select drug, lf from drugr2015 ')

    piee = cur.fetchall()
    impactpie = []
    for k in piee:
        drug = k[0].replace('\n','')
        score = k[1]
        t = [drug,score]
        if score > 0:
            piedata.append(t)
    print(piedata)
    sortedpie2 = sorted(piedata, key=lambda xy: xy[1], reverse=True)
    if (len(sortedpie2) > 0):
     maxrow = sortedpie2[0]
     if maxrow[0] == 'Unmet Need':
        maxrow = sortedpie2[1]
        print(maxrow)
        maxval = maxrow[1]
     else:
      maxval = maxrow[1]
    c = 0
    for row in sortedpie2:
        print(sortedpie2)
        print(maxval)
        perc = (row[1] / maxval) * 100
        row.append(perc)
        _row = str(row[0])
        if _row != 'Unmet Need':
            color = drugcolors[c]
        else:
            color = '#a6a6a6'
        row.append(color)
        c+=1
        if _row != 'Unmet Need':
            impactpie.append(row)
    g.db.close()
    pielabb = []
    n = 0
    temprow = []
    len(impactpie)
    for k in impactpie:
        print(k)
        if n < 2:
            drug = k[0].replace('\n','')
            tempcomp = drug
            tempval = len(drug)
            print(tempval)
            if tempval > 25:
                if len(drug) == 48:
                    shortdrug = tempcomp.rsplit(' ', 4)[0]
                else:
                    shortdrug = tempcomp.rsplit(' ', 2)[0]
            else:
                shortdrug = drug[0:25]
            score = k[1]
            color = k[3]
            col = color[1:7]
            temprow.append(drug)
            temprow.append(shortdrug)
            temprow.append(col)
            temprow.append(score)
            n += 1
        else:
            n = 0
            pielabb.append(temprow)
            temprow = []

    pielabb2 = []
    n = 0
    temprow = []
    for k in sortedpie2:
        print(k)
        if n < 2:
            drug = str(k[0]).replace('\n','')
            tempcomp = drug
            tempval = len(drug)
            if tempval > 25:
                if len(drug) == 48:
                    shortdrug = tempcomp.rsplit(' ', 4)[0]
                else:
                    shortdrug = tempcomp.rsplit(' ', 2)[0]
            else:
                shortdrug = drug[0:25]
            score = k[1]
            color = k[3]
            col = color[1:7]
            temprow.append(drug)
            temprow.append(shortdrug)
            temprow.append(col)
            temprow.append(score)
            n += 1
        else:
            n = 0
            pielabb2.append(temprow)
            temprow = []
    speclocate = [year,drugg,disease]
    return render_template('drug.html', data=piedata, drug=drugg, navsub=3, showindex=1, pielab1=pielabb2, pielab2=pielabb, drugcolors=drugcolors, speclocate = speclocate, scrolling=1, impactpie=impactpie, sortedpie2 = sortedpie2)

@app.route('/index/country')
def country():
    print("inside country")
    g.db = connect_db()
    color = []
    year = 2010
    colors = {'tb': '#FFB31C', 'malaria': '#0083CA', 'hiv': '#EF3E2E', 'schistosomiasis': '#546675', 'lf': '#305516', 'hookworm': '#86AAB9', 'roundworm': '#003452', 'whipworm': '#CAEEFD', 'onchocerciasis': '#5CB85C'}
    isall = 1
    drugg = 'all'
    name = 'ALL'
    br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from countryp2010 ')
    cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from country2010 ')
    bars = br.fetchall() # has percentile
    maps = cur.fetchall() # has actual val
    # print(bars)
    # print(maps)
    bars = list(filter(lambda x: x[0] != None, bars))
    maps = list(filter(lambda x: x[0] != None, maps))
    mapdata = []
    for row in maps:
        count = str(row[0].encode('utf8'))
        score = row[1]
        hor = [count,score]
        mapdata.append(hor)
    # print("printing mapdata")
    #print(mapdata)
    sort = []
    sortedlist = sorted(bars, key=lambda xy: xy[1], reverse=True)
    sortedval = sorted(maps, key=lambda x: x[1], reverse=True)
    barlist = []
    i=0
    print("sortedlist")
    for row in sortedlist:
        count = str(row[0].encode('utf8'))
        if count is not None and count:
            #print("in here")
            combrow = [row,sortedval[i],[i]]
            barlist.append(combrow)
            tmp = []
            #print(sortedval[i][0])
            if sortedval[i][0] is not None and sortedval[i][0]:
                for j in sortedval[i]:
                    tmp.append(j)
                # print(tmp)
                sort.append(tmp)
            i += 1

    speclocate = [year,name,drugg]
    mapdata.insert(0,['Country','Score'])
    #sort.append(mapdata)
    g.db.close()
    return render_template('country.html', showindex=1, navsub=1, name=name, color=color, mapdata=mapdata, sortedlist=sortedlist, sortedval = sort, year=year, isall=isall, barlist = barlist, speclocate = speclocate)

@app.route('/index/country/<xyear>/<xdisease>')
def countrydata(xdisease,xyear):
    g.db = connect_db()
    color = []
    year = xyear
    colors = {'tb': '#FFB31C', 'malaria': '#0083CA', 'hiv': '#EF3E2E', 'schistosomiasis': '#546675', 'lf': '#305516', 'hookworm': '#86AAB9', 'roundworm': '#003452', 'whipworm': '#CAEEFD', 'onchocerciasis': '#5CB85C'}
    if xdisease == 'all':
        isall = 1
        drugg = 'all'
        name = 'ALL'
        if xyear == '2010A':
            br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from countryp2010 ')
            cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from country2010 ')
        elif xyear == '2010B':
            br = g.db.execute(
                ' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from countryp2010 ')
            cur = g.db.execute(
                ' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from country2010 ')
        elif xyear == '2010':
            br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from countryp2010 ')
            cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from countryp2010 ')
        elif xyear == '2013':
            cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from country2013 ')
            br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from countryp2013 ')
        elif xyear == '2015':
            cur = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from country2015 ')
            br = g.db.execute(' select country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from countryp2015 ')
    else:
        isall = 0
        namedict = {'tb': 'TB', 'malaria': 'MALARIA', 'hiv': 'HIV/AIDS', 'schistosomiasis': 'SCHISTOSOMIASIS', 'onchocerciasis':'ONCHOCERCIASIS', 'lf': 'LYMPHATIC FILARIASIS', 'hookworm': 'HOOKWORM', 'roundworm': 'ROUNDWORM', 'whipworm': 'WHIPWORM'}
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
            elif xdisease == 'onchocerciasis':
                cur = g.db.execute(' select country, onchocerciasis from country2010 ')
                br = g.db.execute(' select country, onchocerciasis from countryp2010 ')
                sortind = 8
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
            elif xdisease == 'onchocerciasis':
                cur = g.db.execute(' select country, onchoceriasis from country2013 ')
                br = g.db.execute(' select country, onchoceriasis from countryp2013 ')
                sortind = 8
            elif xdisease == 'lf':
                cur = g.db.execute(' select country, lf from country2013 ')
                br = g.db.execute(' select country, lf from countryp2013 ')
                sortind = 9
        elif xyear == '2015':
            if xdisease == 'tb':
                cur = g.db.execute(' select country, tb from country2015 ')
                br = g.db.execute(' select country, tb from countryp2015 ')
                sortind = 1
            elif xdisease == 'malaria':
                cur = g.db.execute(' select country, malaria from country2015 ')
                br = g.db.execute(' select country, malaria from countryp2015 ')
                sortind = 2
            elif xdisease == 'hiv':
                cur = g.db.execute(' select country, hiv from country2015 ')
                br = g.db.execute(' select country, hiv from countryp2015 ')
                sortind = 3
            elif xdisease == 'roundworm':
                cur = g.db.execute(' select country, roundworm from country2015 ')
                br = g.db.execute(' select country, roundworm from countryp2015 ')
                sortind = 4
            elif xdisease == 'hookworm':
                cur = g.db.execute(' select country, hookworm from country2015 ')
                br = g.db.execute(' select country, hookworm from countryp2015 ')
                sortind = 5
            elif xdisease == 'whipworm':
                cur = g.db.execute(' select country, whipworm from country2015 ')
                br = g.db.execute(' select country, whipworm from countryp2015 ')
                sortind = 6
            elif xdisease == 'schistosomiasis':
                cur = g.db.execute(' select country, schistosomiasis from country2015 ')
                br = g.db.execute(' select country, schistosomiasis from countryp2015 ')
                sortind = 7
            elif xdisease == 'onchocerciasis':
                cur = g.db.execute(' select country, onchoceriasis from country2015 ')
                br = g.db.execute(' select country, onchoceriasis from countryp2015 ')
                sortind = 8
            elif xdisease == 'lf':
                cur = g.db.execute(' select country, lf from country2015 ')
                br = g.db.execute(' select country, lf from countryp2015 ')
                sortind = 9
    bars = br.fetchall()
    maps = cur.fetchall()
    mapdata = []
    bars = list(filter(lambda x: x[0] != None, bars))
    maps = list(filter(lambda x: x[0] != None, maps))
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
            # del tmp[1]
            i += 1
            sort.append(tmp)
        print(sort)
    else:
        barlist = []
        for row in sortedval:
            if row[1] != 0.0:
                perc = row[1] / width * 100
                temp = [row[0],row[1],perc]
                barlist.append(temp)
        if xyear == '2010':
            cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf from country2010 ')
        elif xyear == '2013':
            cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf from country2013 ')
        elif xyear == '2015':
            cur = g.db.execute(' select country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf from country2015 ')
        vals = cur.fetchall()
        sortvals = sorted(vals, key=lambda x: x[sortind], reverse=True)
        sort = []
        for row in sortvals:
            tmp = []
            for j in row:
                tmp.append(j)
            sort.append(tmp)
    speclocate = [xyear,name,drugg]
    #sort = mapdata
    mapdata.insert(0,['Country','Score'])
    #sort.append(mapdata)
    g.db.close()
    return render_template('country.html', showindex=1, navsub=1, name=name, color=color, mapdata=mapdata, sortedlist=sortedlist, sortedval = sort, year=year, isall=isall, barlist = barlist, speclocate = speclocate,scrolling=1,disease = xdisease)



@app.route('/index/company')
def company():
    cur = g.db.execute(' select distinct company,disease, daly2010,color from manudis order by daly2010 DESC')
    cdd = g.db.execute(' select distinct company, disease, daly2010,color from manudis order by daly2010 DESC ')
    unmetneedOnly = g.db.execute(' select distinct company, disease, daly2010,color from manudis  where company = ? ', ('Unmet Need',))
    piedata1 = []
    piedata2 = []
    g.db = connect_db()
    pielab1 = []
    pielab2 = []
    barchart = []
    bardata = []
    name = 'ALL'
    disease = 'All'
    year = '2010'
    piee = cur.fetchall()
    barr = cdd.fetchall()
    unmetned= unmetneedOnly.fetchall()
    cnt=0
    sum=0
    colr=''
    for j in unmetned:
        sum+=j[2]
        colr="#"+ str(j[3])
    t = ['Unmet Need', sum, colr]
    piedata1.append(t)
    print(piedata1)
    colcnt = 0
    unmetsum=0
    for j in piee:
        company = str(j[0])
        disease = j[1]
        daly2010 = j[2]
        color = "#"+ str(j[3])
        if (company == 'Unmet Need'):
            continue
        if daly2010 > 0:
            t = [company, daly2010, color]
            colcnt += 1
            piedata1.append(t)
            print(piedata1)
    piedata1.sort(key=lambda x: x[1], reverse=True)
    maxrow = piedata1[0]
    if maxrow[0] == 'Unmet Need':
        maxrow = piedata1[0]
    maxval = maxrow[1]
    for row in piedata1:
        percent = row[1] / maxval * 100
        row.append(percent)
        if row[0] != 'Unmet Need':
            piedata2.append(row)
    print(piedata2)
    n = 0
    temprow = []
    for k in piedata1:
        print(k)
        if n < 2:
            comp = k[0]
            tempcomp = comp
            tempval = len(comp)
            if tempval > 25:
                if len(comp) == 77:
                    shortcomp = tempcomp.rsplit(' ', 7)[0]
                else:
                    shortcomp = tempcomp.rsplit(' ', 2)[0]
            else:
                shortcomp = comp[0:25]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor=k[2]
            sscolor=scolor[1:7]
            temprow.append(sscolor)
            print(pielab1)
            n += 1
        else:
            n = 0
            pielab1.append(temprow)
            print(pielab1)
            temprow = []

    n = 0
    temprow = []
    for k in piedata2:
        print(k)
        if n < 2:
            comp = k[0]
            tempcomp = comp
            tempval = len(comp)
            if tempval > 25:
                if len(comp) == 77:
                    shortcomp = tempcomp.rsplit(' ', 7)[0]
                else:
                    shortcomp = tempcomp.rsplit(' ', 2)[0]
            else:
                shortcomp = comp[0:25]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor=k[2]
            sscolor=scolor[1:7]
            temprow.append(sscolor)
            n += 1
        else:
            n = 0
            pielab2.append(temprow)
            temprow = []

    colcnt = 0
    print(pielab1)
    print('pir lab 2')
    print(pielab2)
    for l in barr:
        company = str(l[0])
        if company == 'Unmet Need':
            continue
        daly2010 = l[2]
        disease = str(l[1])
        color = '#'+ str(l[3])
        colcnt += 1
        xyz = [company,daly2010,disease,color]
        barchart.append(xyz)
    print(len(barchart))
    if len(barchart) >0:
        maxim = barchart[0]
        maxval = maxim[1]
        colcnt = 1
        for row in barchart:
            comp = row[0]
            daly = (row[1]/maxval) * 100
            disease = row[2]
            color = row[3]
            #color=row[3]
            colcnt += 1
            actualNumDaly=row[1]
            xyz = [comp,daly,disease,color, actualNumDaly]
            bardata.append(xyz)

    g.db.close()
    url = name.lower()
    speclocate = [year,name,url]

    print(pielab1)
    print(pielab2)
    return render_template('company.html', data1=piedata2, data2=piedata1,name=name, navsub=2, showindex=1, pielab1=pielab1, pielab2=pielab2, bardata=bardata, comptype = 0, speclocate = speclocate, scrolling=1)

@app.route('/index/company/manufacturer/<year>/<disease>')
def companyindx(year,disease):
    piedata1 = []
    piedata2 = []
    g.db = connect_db()
    pielab1 = []
    pielab2 = []
    barchart = []
    bardata = []
    if year == '2010':
        if disease == 'all':
            cur = g.db.execute(' select distinct company,disease, daly2010, color from manudis order by daly2010 DESC')
            cdd = g.db.execute(' select distinct company, disease, daly2010, color from manudis order by daly2010 DESC ')
            unmetneedOnly = g.db.execute(' select distinct company, disease, daly2010,color from manudis  where company = ? ', ('Unmet Need',))
            name = 'ALL'
        elif disease == 'hiv':
            cur = g.db.execute(' select company,disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('HIV',))
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('HIV',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2010,color from manudis  where company = ? and disease=? ',
                ('Unmet Need', 'HIV'))
            name = 'HIV/AIDS'
        elif disease == 'tb':
            cur = g.db.execute(' select company,disease, daly2010, color from manudis where disease = ? order by daly2010 DESC ', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('TB',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2010,color from manudis  where company = ? and disease=? ',
                ('Unmet Need', 'TB'))
            name = 'TB'
        elif disease == 'malaria':
            cur = g.db.execute(' select company,disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('Malaria',))
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('Malaria',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2010,color from manudis  where company = ? and disease=? ',
                ('Unmet Need', 'Malaria'))
            name = 'MALARIA'
    elif year == '2013':
        if disease == 'all':
            cur = g.db.execute(' select distinct company,disease, daly2013, color from manudis order by daly2013 DESC')
            cdd = g.db.execute(' select distinct company, disease, daly2013, color from manudis order by daly2013 DESC ')
            unmetneedOnly = g.db.execute(' select distinct company, disease, daly2013,color from manudis  where company = ? ', ('Unmet Need',))
            name = 'ALL'
        elif disease == 'hiv':
            cur = g.db.execute(' select company, disease,daly2013, color from manudis where disease = ? order by daly2013 DESC', ('HIV',))
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis where disease = ? order by daly2013 DESC', ('HIV',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2013,color from manudis  where company = ? and disease=? ',
                ('Unmet Need', 'HIV'))
            name = 'HIV/AIDS'
        elif disease == 'tb':
            cur = g.db.execute(' select company,disease, daly2013, color from manudis where disease = ? order by daly2013 DESC', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis where disease = ? order by daly2013 DESC', ('TB',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2013,color from manudis  where company = ? and disease=? ',
                ('Unmet Need', 'TB'))
            name = 'TB'
        elif disease == 'malaria':
            cur = g.db.execute(' select company,disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('Malaria',))
            cdd = g.db.execute(' select company, disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('Malaria',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2013,color from manudis  where company = ? and disease=? ',
                ('Unmet Need', 'Malaria'))
            name = 'MALARIA'
    elif year == '2015':#=====add 2015 SQL=========
        if disease == 'all':
            cur = g.db.execute(' select distinct company,disease, daly2015, color from manudis2015 order by daly2015 DESC')#====10.7
            cdd = g.db.execute(' select distinct company, disease, daly2015, color from manudis2015 order by daly2015 DESC ')
            unmetneedOnly = g.db.execute(' select distinct company, disease, daly2015,color from manudis2015  where company = ? ', ('Unmet Need',))
            name = 'ALL'
        elif disease == 'hiv':
            cur = g.db.execute(' select company, disease,daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('HIV',))
            cdd = g.db.execute(' select company, disease,daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('HIV',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2015,color from manudis2015  where company = ? and disease=? ',
                ('Unmet Need', 'HIV'))
            name = 'HIV/AIDS'
        elif disease == 'tb':
            cur = g.db.execute(' select company,disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('TB',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2015,color from manudis2015  where company = ? and disease=? ',
                ('Unmet Need', 'TB'))
            name = 'TB'
        elif disease == 'malaria':
            cur = g.db.execute(' select company,disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('Malaria',))
            cdd = g.db.execute(' select company, disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('Malaria',))
            unmetneedOnly = g.db.execute(
                ' select distinct company, disease, daly2015,color from manudis2015  where company = ? and disease=? ',
                ('Unmet Need', 'Malaria'))
            name = 'MALARIA'
    piee = cur.fetchall()
    barr = cdd.fetchall()
    cnt = 0
    unmetned = unmetneedOnly.fetchall()
    sum = 0
    colr = ''
    for j in unmetned:
        sum += j[2]
        colr = "#" + str(j[3])
    t = ['Unmet Need', sum, colr]
    piedata1.append(t)
    print(piedata1)

    colcnt = 0
    unmetsum = 0
    print(piee)
    for j in piee:
        company = str(j[0])
        disease = j[1]
        daly2010 = j[2]
        color = "#" + str(j[3])
        if (company == 'Unmet Need'):
            continue
        if daly2010 > 0:
            t = [company, daly2010, color]
            colcnt += 1
            piedata1.append(t)
            print(piedata1)
    piedata1.sort(key=lambda x: x[1], reverse=True)
    maxrow = piedata1[0]
    if maxrow[0] == 'Unmet Need':
        maxrow = piedata1[0]
    maxval = maxrow[1]
    for row in piedata1:
        percent = row[1] / maxval * 100
        row.append(percent)
        if row[0] != 'Unmet Need':
            piedata2.append(row)
    print(piedata2)
    n = 0
    temprow = []
    for k in piedata1:
        print(k)
        if n < 2:
            comp = k[0]
            tempcomp = comp
            tempval = len(comp)
            if tempval > 25:
                if len(comp) == 77:
                    shortcomp = tempcomp.rsplit(' ', 7)[0]
                else:
                    shortcomp = tempcomp.rsplit(' ', 2)[0]
            else:
                shortcomp = comp[0:25]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor = k[2]
            sscolor = scolor[1:7]
            temprow.append(sscolor)
            n += 1
        else:
            n = 0
            pielab1.append(temprow)
            temprow = []

    n = 0
    temprow = []
    for k in piedata2:
        print(k)
        if n < 2:
            comp = k[0]
            tempcomp = comp
            tempval = len(comp)
            if tempval > 25:
                if len(comp) == 77:
                    shortcomp = tempcomp.rsplit(' ', 7)[0]
                else:
                    shortcomp = tempcomp.rsplit(' ', 2)[0]
            else:
                shortcomp = comp[0:25]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor = k[2]
            sscolor = scolor[1:7]
            temprow.append(sscolor)
            n += 1
        else:
            n = 0
            pielab2.append(temprow)
            temprow = []

    colcnt = 0
    print(pielab1)
    print('pir lab 2')
    print(pielab2)
    for l in barr:
        company = str(l[0])
        if company == 'Unmet Need':
            continue
        daly2010 = l[2]
        disease = str(l[1])
        color = '#' + str(l[3])
        colcnt += 1
        xyz = [company, daly2010, disease, color]
        barchart.append(xyz)
    print(len(barchart))
    if len(barchart) > 0:
        maxim = barchart[0]
        maxval = maxim[1]
        colcnt = 1
        for row in barchart:
            comp = row[0]
            daly = (row[1] / maxval) * 100
            disease = row[2]
            color =  row[3]
            # color=row[3]
            colcnt += 1
            actualNumDaly = row[1]
            xyz = [comp, daly, disease, color, actualNumDaly]
            bardata.append(xyz)

    g.db.close()
    url = name.lower()
    speclocate = [year, name, url]
    return render_template('company.html', data1=piedata2, data2=piedata1, name=name, navsub=2, showindex=1,
                           pielab1=pielab1, pielab2=pielab2, bardata=bardata, comptype=0, speclocate=speclocate,
                           scrolling=1)

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
    elif year == '2015':
        if disease == 'all':
            dat = g.db.execute(' select company, total, color from patent2015 ')
        elif disease == 'tb':
            dat = g.db.execute(' select company, tb, color from patent2015 ')
        elif disease == 'malaria':
            dat = g.db.execute(' select company, malaria, color from patent2015 ')
        elif disease == 'hiv':
            dat = g.db.execute(' select company, hiv, color from patent2015 ')
        elif disease == 'roundworm':
            dat = g.db.execute(' select company, roundworm, color from patent2015 ')
        elif disease == 'hookworm':
            dat = g.db.execute(' select company, hookworm, color from patent2015 ')
        elif disease == 'whipworm':
            dat = g.db.execute(' select company, whipworm, color from patent2015 ')
        elif disease == 'schistosomiasis':
            dat = g.db.execute(' select company, schistosomiasis, color from patent2015 ')
        elif disease == 'onchocerciasis':
            dat = g.db.execute(' select company, onchocerciasis, color from patent2015 ')
        elif disease == 'lf':
            dat = g.db.execute(' select company, lf, color from patent2015 ')
    data = dat.fetchall()
    print(data)
    patent1 = []
    patent2 = []
    for j in data:
        comp = str(j[0]).replace('\n','')
        score = j[1]
        color =  str(j[2])
        if score > 0:
            patent1.append([comp,score,color])
    patent1.sort(key=lambda x: x[1], reverse=True)
    print(patent1)
    maxrow = patent1[0]
    if maxrow[0] == 'Unmet Need':
        maxrow = patent1[0]
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
    n = 0
    p = 0
    temprow = []
    for k in patent1:
        #print(len(patent1))
        # if len(patent1) <= 2:
        #     comp = str(k[0])
        #     tempcomp = comp
        #     tempval = len(comp)
        #     if tempval > 25:
        #         if len(comp) == 77:
        #             shortcomp = tempcomp.rsplit(' ', 7)[0]
        #         else:
        #             shortcomp = tempcomp.rsplit(' ', 2)[0]
        #     else:
        #         shortcomp = comp[0:25]
        #     temprow.append(comp)
        #     temprow.append(shortcomp)
        #     scolor = str(k[2])
        #     temprow.append(scolor)
        #     p=p+1
        #     if p == 2:
        #         pielabb1.append(temprow)
        #         temprow = []
        #         p = 0
        # else:
        if n < 2:
            n += 1
            comp = str(k[0])
            tempcomp = comp
            tempval = len(comp)
            if tempval > 25:
                if len(comp) == 77:
                    shortcomp = tempcomp.rsplit(' ', 7)[0]
                else:
                    shortcomp = tempcomp.rsplit(' ', 2)[0]
            else:
                shortcomp = comp[0:25]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor = str(k[2])
            temprow.append(scolor)
            if n == 2 or patent1.index(k)-(len(patent1)-1)==0:
                n = 0
                pielabb1.append(temprow)
                temprow = []
    print(patent2)
    print(patent1)
    n = 0
    temprow = []
    pielabb2=[]
    for k in patent2:
        # print(len(patent2))
        # if len(patent2) == 1:
        #     comp = str(k[0])
        #     tempcomp = comp
        #     print(len(comp))
        #     tempval = len(comp)
        #     if tempval > 25:
        #         if len(comp) == 77:
        #             shortcomp = tempcomp.rsplit(' ', 7)[0]
        #         else:
        #             shortcomp = tempcomp.rsplit(' ', 2)[0]
        #     else:
        #         shortcomp = comp[0:25]
        #     temprow.append(comp)
        #     temprow.append(shortcomp)
        #     scolor = str(k[2])
        #     temprow.append(scolor)
        #     pielabb2.append(temprow)
        # else:
        if n < 2:
            n+=1
            comp = str(k[0])
            tempcomp = comp
            print(len(comp))
            tempval = len(comp)
            if tempval > 25:
                if len(comp) == 77:
                    shortcomp = tempcomp.rsplit(' ', 7)[0]
                else:
                    shortcomp = tempcomp.rsplit(' ', 2)[0]
            else:
                shortcomp = comp[0:25]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor = str(k[2])
            temprow.append(scolor)
            if n == 2 or patent2.index(k)-(len(patent2)-1)==0:
                n = 0
                pielabb1.append(temprow)
                temprow = []
    print(pielabb1)
    print(pielabb2)
    return render_template('company.html', navsub=2, showindex=1, comptype = 1, speclocate = speclocate, scrolling=1, patent1 = patent1, patent2 = patent2, pielab1 = pielabb1, pielab2 = pielabb2)

@app.route('/account')
def account():
    return render_template('account.html', showthediv=0)

@app.route('/revert')
def revert():
    print("in revert")
    conn = connect_db();
    conn.execute('''delete from manudis''')
    conn.execute('''insert into manudis select * from manudis_bkp''')
    conn.execute('''delete from manudis2015''')
    conn.execute('''insert into manudis2015 select * from manudis2015_bkp''')
    conn.execute('''delete from manutot''')
    conn.execute('''insert into manutot select * from manutot_bkp''')
    conn.execute('''delete from manutot2015''')
    conn.execute('''insert into manutot2015 select * from manutot2015_bkp''')
    conn.execute('''delete from countrybydis2010''')
    conn.execute('''insert into countrybydis2010 select * from countrybydis2010_bkp''')
    conn.execute('''delete from countrybydis2013''')
    conn.execute('''insert into countrybydis2013 select * from countrybydis2013_bkp''')
    conn.execute('''delete from country2010''')
    conn.execute('''insert into country2010 select * from country2010_bkp''')
    conn.execute('''delete from country2013''')
    conn.execute('''insert into country2013 select * from country2013_bkp''')
    conn.execute('''delete from country2015''')
    conn.execute('''insert into country2015 select * from country2015_bkp''')
    conn.execute('''delete from countryp2010''')
    conn.execute('''insert into countryp2010 select * from countryp2010_bkp''')
    conn.execute('''delete from countryp2013''')
    conn.execute('''insert into countryp2013 select * from countryp2013_bkp''')
    conn.execute('''delete from countryp2015''')
    conn.execute('''insert into countryp2015 select * from countryp2015_bkp''')
    conn.execute('''delete from diseaseall2010''')
    conn.execute('''insert into diseaseall2010 select * from diseaseall2010_bkp''')
    conn.execute('''delete from diseaseall2013''')
    conn.execute('''insert into diseaseall2013 select * from diseaseall2013_bkp''')
    conn.execute('''delete from diseaseall2015''')
    conn.execute('''insert into diseaseall2015 select * from diseaseall2015_bkp''')
    conn.execute('''delete from disease2010''')
    conn.execute('''insert into disease2010 select * from disease2010_bkp''')
    conn.execute('''delete from disease2013''')
    conn.execute('''insert into disease2013 select * from disease2013_bkp''')
    conn.execute('''delete from disease2015''')
    conn.execute('''insert into disease2015 select * from disease2015_bkp''')
    conn.execute('''delete from disbars''')
    conn.execute('''insert into disbars select * from disbars_bkp''')
    conn.execute('''delete from distypes''')
    conn.execute('''insert into distypes select * from distypes_bkp''')
    conn.execute('''delete from disbars2010B2015''')
    conn.execute('''insert into disbars2010B2015 select * from disbars2010B2015_bkp''')
    conn.execute('''delete from distypes2010B2015''')
    conn.execute('''insert into distypes2010B2015 select * from distypes2010B2015_bkp''')
    conn.execute('''delete from drugr2010''')
    conn.execute('''insert into drugr2010 select * from drugr2010_bkp''')
    conn.execute('''delete from drugr2013''')
    conn.execute('''insert into drugr2013 select * from drugr2013_bkp''')
    conn.execute('''delete from drugr2015''')
    conn.execute('''insert into drugr2015 select * from drugr2015_bkp''')
    conn.execute('''delete from patent2010''')
    conn.execute('''insert into patent2010 select * from patent2010_bkp''')
    conn.execute('''delete from patent2013''')
    conn.execute('''insert into patent2013 select * from patent2013_bkp''')
    conn.execute('''delete from patent2015''')
    conn.execute('''insert into patent2015 select * from patent2015_bkp''')
    conn.commit()
    print("Database Backup Restored")
    return render_template('revert.html', showthediv=0)



@app.route('/accountS')
def ManageAccount():
    #conn = connect_db()
    print("inside update")
    result = objDbComp.companydbUpdate()
    if result != 'success':
        return render_template('accountF.html', error=result, showthediv=0)
    print ("Company Completed Update")
    result = objDbCountryDis.countryDisdbUpdate()
    if result != 'success':
        return render_template('accountF.html', error=result, showthediv=0)
    print ("Completed Update")
    result = objDBCountry.countrydbUpdate()
    print (result)
    if result != 'success':
        return render_template('accountF.html', error=result, showthediv=0)
    result = objDBDrug.DrugDbUpdate()
    print (result)
    if result != 'success':
        return render_template('accountF.html', error=result, showthediv=0)
    result = objDBDisease.DiseaseDbUpdate()
    print (result)
    if result == 'success':
        return render_template('accountS.html', showthediv=0)
    else:
        return render_template('accountF.html', error=result, showthediv=0)

if __name__ == '__main__':
    app.run(debug=False)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

@app.errorhandler(500)
def internal_error_500(e):
    return render_template('error500.html',showindex=1, navsub=1), 500