
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, g
from openpyxl.compat import range
import pandas as pd
import sqlite3
import json
import math

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
    return sqlite3.connect('/home/globalhealth/mysite/ghi.db')

@app.before_request
def before_request():
    # print("In before_request")
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
    maxTotal = 0
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
                diss = row[0]
                color = "color: " + barcolors[c]
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
                name = row[0]
                imp = row[1]
                color = "color: " + row[2]
                x = [name, imp]
                piedata.append(x)
            for row in barg:
                name = row[0]
                daly = row[1]
                color = "color: " + row[2]
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
            disease = row[0]
            tb = row[1]
            color = "color: " + barcolors[c]
            c += 1
            efficacy2010 = row[3]
            coverage2010 = row[4]
            xx = [disease, efficacy2010, color]
            xy = [disease, coverage2010, color]
            bar1.append(xx)
            bar2.append(xy)
            print('=======')
            print(efficacy2010)

        for row in data2:
            country = row[0]
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
                diss = row[0]
                color = "color: " + barcolors[c]
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
                name = row[0]
                imp = row[1]
                color = "color: " + row[2]
                x = [name, imp]
                piedata.append(x)
            for row in barg:
                name = row[0]
                daly = row[1]
                color = "color: " + row[2]
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
            disease = row[0]
            tb = row[1]
            color = "color: " + barcolors[c]
            c += 1
            efficacy2013 = row[3]
            coverage2013 = row[4]
            xx = [disease, efficacy2013, color]
            xy = [disease, coverage2013, color]
            bar1.append(xx)
            bar2.append(xy)
            print('=======')
            print(efficacy2013)

        for row in data2:
            country = row[0]
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
                diss = row[0]
                color = "color: " + barcolors[c]
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
                name = row[0]
                imp = row[1]
                color = "color: " + row[2]
                x = [name, imp]
                piedata.append(x)
            for row in barg:
                name = row[0]
                daly = row[1]
                color = "color: " + row[2]
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
            disease = row[0]
            tb = row[1]
            color = "color: " + barcolors[c]
            c += 1
            efficacy2013 = row[3]
            coverage2013 = row[4]
            xx = [disease, efficacy2013, color]
            xy = [disease, coverage2013, color]
            bar1.append(xx)
            bar2.append(xy)
            print('=======')
            print(efficacy2013)

        for row in data2:
            country = row[0]
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
            color = '#00cab1'
        row.append(color)
        c+=1
        if _row != 'Unmet Need':
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
    print(pielabb)
    print(piedata)
    print(impactpie)
    print(sortedpie2)
    return render_template('drug.html', data=piedata, drug='All', navsub=3, showindex=1, pielabb=pielabb, drugcolors=drugcolors, speclocate = speclocate, scrolling=1, impactpie=impactpie, sortedpie2 = sortedpie2)

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
                cur = g.db.execute(' select drug, hookworm from drugr2015 ')
            elif disease == 'schistosomiasis':
                cur = g.db.execute(' select drug, schistosomiasis from drugr2015 ')
            elif disease == 'onchocerciasis':
                cur = g.db.execute(' select drug, onchocerciasis from drugr2015 ')
            elif disease == 'lf':
                cur = g.db.execute(' select drug, lf from drugr2015 ')

    piee = cur.fetchall()
    impactpie = []
    for k in piee:
        drug = k[0]
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
            color = '#00cab1'
        row.append(color)
        c+=1
        if _row != 'Unmet Need':
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
    print(piedata)
    print(pielabb)
    print(impactpie)
    print(sortedpie2)
    return render_template('drug.html', data=piedata, drug=drugg, navsub=3, showindex=1, pielabb=pielabb, drugcolors=drugcolors, speclocate = speclocate, scrolling=1, impactpie=impactpie, sortedpie2 = sortedpie2)

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
        count = row[0]
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
        #print(row)
        count = row[0]
        if count is not None and count:
            #print("in here")
            combrow = [row,sortedval[i],[i]]
            # print(combrow)
            barlist.append(combrow)
            tmp = []
            #print(sortedval[i][0])
            if sortedval[i][0] is not None and sortedval[i][0]:
                for j in sortedval[i]:
                    tmp.append(j)
                # print(tmp)
                sort.append(tmp)
            i += 1

    print("********************")
    print("barlist")
    print(barlist)
    speclocate = [year,name,drugg]
    mapdata.insert(0,['Country','Score'])
    #sort.append(mapdata)
    print("printing sort")
    print(sort)
    g.db.close()
    return render_template('country.html', showindex=1, navsub=1, name=name, color=color, mapdata=mapdata, sortedlist=sortedlist, sortedval = sort, year=year, isall=isall, barlist = barlist, speclocate = speclocate)

@app.route('/index/country/<xyear>/<xdisease>')
def countrydata(xdisease,xyear):
    print("Inside countrydata ")
    print(xdisease)
    print(xyear)
    g.db = connect_db()
    print(g.db)
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
        print(xdisease)
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
        #vals = list(filter(lambda x: x[0] != None, vals))
        print(sortind)
        print(vals)
        sortvals = sorted(vals, key=lambda x: x[sortind], reverse=True)
        sort = []
        for row in sortvals:
            tmp = []
            for j in row:
                tmp.append(j)
            sort.append(tmp)
            print(sort)
    speclocate = [xyear,name,drugg]
    #sort = mapdata
    print(sort)
    mapdata.insert(0,['Country','Score'])
    #sort.append(mapdata)

    print("printing sort")
    print(sort)
    print("********************")
    print("barlist")
    print(barlist)
    g.db.close()
    return render_template('country.html', showindex=1, navsub=1, name=name, color=color, mapdata=mapdata, sortedlist=sortedlist, sortedval = sort, year=year, isall=isall, barlist = barlist, speclocate = speclocate,scrolling=1,disease = xdisease)



@app.route('/index/company')
def company():
    compcolors = ['#7A80A3','#B78988','#906F76','#8F918B','#548A9B','#BAE2DA','#C0E188','#f2c2b7',
                  '#d86375','#b1345d','#de9c2a','#f7c406','#f1dbc6','#5b75a7','#f15a22','#b83f98',
                  '#0083ca','#FFB31C','#0083CA','#EF3E2E','#003452','#86AAB9','#CAEEFD','#546675',
                  '#8A5575','#305516','#B78988','#BAE2DA','#B1345D','#5B75A7','#906F76','#C0E188',
                  '#B99BCF', '#DC2A5A', '#D3D472','#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5',
                  '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5', '#0ACD57', '#22419F','#D47C5B','#003452',
                  '#86AAB9', '#CAEEFD','#139A97', '#1CDDD8', '#FF033D', '#004444', '#C25C7D', '#B5A28F', '#C25C7D', '#90BA3E', '#DA8709', '#B0B0CE',
                  '#2D00DD', '#DD2D00', '#FAFDFD', '#F5FD2F', '#0DC4E0', '#FFD700', '#CC263C', '#F5F5DC', '#3D9C35', '#00CC00',
                  '#EAEAFF' ]
#------Jing 10/7----modify sql: add order by and use manudis as table to select data, apply color to piechart and bar chart------------------

    cur = g.db.execute(' select distinct company,disease, daly2010 from manudis order by daly2010 DESC')#====10.7
    cdd = g.db.execute(' select distinct company, disease, daly2010 from manudis order by daly2010 DESC ')
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
    company = 'AKelel'
    colcnt = 0

    for j in piee:
        precom=company
        company = j[0]
        disease = j[1]
        daly2010 = j[2]
        #color = j[2]
        color=compcolors[colcnt]

        if (company == 'Unalleviated Burden') and (disease != 'all'):
            continue
        if daly2010 > 0 and company is not precom :
            t = [company, daly2010, color]
            colcnt += 1
            piedata1.append(t)
            if company != 'Unalleviated Burden':
                piedata2.append(t)

    n = 0
    temprow = []
    for k in piedata1:
        print(k)
        if n < 4:
            comp = k[0]
            shortcomp = comp[0:10]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor=k[2]
            sscolor=scolor[1:7]
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
        if n < 4:
            comp = k[0]
            shortcomp = comp[0:10]
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

    for l in barr:
        precom = company
        company = l[0]
        if company == 'Unalleviated Burden':
            continue
        daly2010 = l[2]
        disease = l[1]
        color = compcolors[colcnt]
        colcnt += 1
        xyz = [company,daly2010,disease,color]
        barchart.append(xyz)
    print(len(barchart))
    if barchart and precom is not company:
        maxim = barchart[0]
        maxval = maxim[1]
        colcnt = 1
        for row in barchart:
            comp = row[0]
            daly = (row[1]/maxval) * 100
            disease = row[2]
            color = compcolors[colcnt]
            #color=row[3]
            colcnt += 1
            xyz = [comp,daly,disease,color]
            bardata.append(xyz)

    g.db.close()
    url = name.lower()
    speclocate = [year,name,url]
    return render_template('company.html', data1=piedata2, data2=piedata1,name=name, navsub=2, showindex=1, pielab1=pielab1, pielab2=pielab2, bardata=bardata, comptype = 0, speclocate = speclocate, scrolling=1)

@app.route('/index/company/manufacturer/<year>/<disease>')
def companyindx(year,disease):
    compcolors =['#7A80A3','#B78988','#906F76','#8F918B','#548A9B','#BAE2DA','#C0E188','#f2c2b7',
                  '#d86375','#b1345d','#de9c2a','#f7c406','#f1dbc6','#5b75a7','#f15a22','#b83f98',
                  '#0083ca','#FFB31C','#0083CA','#EF3E2E','#003452','#86AAB9','#CAEEFD','#546675',
                  '#8A5575','#305516','#B78988','#BAE2DA','#B1345D','#5B75A7','#906F76','#C0E188',
                  '#B99BCF', '#DC2A5A', '#D3D472','#2A9DC4', '#C25C90', '#65A007', '#FE3289', '#C6DAB5',
                  '#DDF6AC', '#B7E038', '#1ADBBD', '#3BC6D5', '#0ACD57', '#22419F','#D47C5B','#003452',
                  '#86AAB9', '#CAEEFD','#139A97', '#1CDDD8', '#FF033D', '#004444', '#C25C7D', '#B5A28F', '#C25C7D', '#90BA3E', '#DA8709', '#B0B0CE',
                  '#2D00DD', '#DD2D00', '#FAFDFD', '#F5FD2F', '#0DC4E0', '#FFD700', '#CC263C', '#F5F5DC', '#3D9C35', '#00CC00',
                  '#EAEAFF' ]
   # colors = {'TB': '#FFB31C', 'Malaria': '#0083CA', 'HIV': '#EF3E2E', 'schistosomiasis': '#546675', 'lf': '#305516', 'hookworm': '#86AAB9', 'roundworm': '#003452', 'whipworm': '#CAEEFD', 'onchocerciasis': '#5CB85C'}
   # pielabb=[]
    piedata1 = []
    piedata2 = []
    g.db = connect_db()
    pielab1 = []
    pielab2 = []
    barchart = []
    bardata = []
    if year == '2010':
        if disease == 'all':
            cur = g.db.execute(' select company,disease, daly2010, color from manudis order by daly2010 DESC')
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis order by daly2010 DESC ')
            name = 'ALL'
            colcnt = 0
            piee = cur.fetchall()
            barr = cdd.fetchall()
            for j in piee:
                company = j[0]
                disease = j[1]
                daly2010 = j[2]
                # color = j[2]
                color = compcolors[colcnt]

                if (company == 'Unalleviated Burden') and (disease != 'all'):
                    continue
                if daly2010 > 0:
                    t = [company, daly2010, color]
                    colcnt += 1
                    piedata1.append(t)
                    if company != 'Unalleviated Burden':
                        piedata2.append(t)
            # piedata.sort(key=lambda x: x[1], reverse=True)
            n = 0
            temprow = []
            for k in piedata1:
                print(k)
                if n < 4:
                    comp = k[0]
                    shortcomp = comp[0:10]
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
                if n < 4:
                    comp = k[0]
                    shortcomp = comp[0:10]
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
            for l in barr:
                company = l[0]
                daly2010 = l[2]
                if company == 'Unalleviated Burden':
                    # colcnt += 1
                    continue
                disease = l[1]
                color = compcolors[colcnt]
                # color=l[3]
                colcnt += 1
                xyz = [company, daly2010, disease, color]
                barchart.append(xyz)
                print(barchart)
            # barchart.sort(key=lambda x: x[1], reverse=True)
            maxim = barchart[0]
            maxval = maxim[1]
            colcnt = 1
            for row in barchart:
                comp = row[0]
                print(row[1])
                if maxval > 0:
                    daly = (row[1] / maxval) * 100
                else:
                    daly = 0
                disease = row[2]
                color = compcolors[colcnt]
                # color = row[3]
                colcnt += 1
                xyz = [comp, daly, disease, color]
                bardata.append(xyz)
            # -----------------------------------------------------------------------------------------------------------------------------------------
            g.db.close()
            url = name.lower()
            speclocate = [year, name, url]
            print(bardata)
            print(pielab1)
            print(pielab2)
            return render_template('company.html', data1=piedata2, data2=piedata1, name=name, navsub=2, showindex=1,
                                   pielab1=pielab1, pielab2=pielab2, bardata=bardata, comptype=0, speclocate=speclocate,
                                   scrolling=1)
        elif disease == 'hiv':
            cur = g.db.execute(' select company,disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('HIV',))
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('HIV',))
            name = 'HIV/AIDS'
        elif disease == 'tb':
            cur = g.db.execute(' select company,disease, daly2010, color from manudis where disease = ? order by daly2010 DESC ', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2010, color from manudis  where disease = ? order by daly2010 DESC', ('TB',))
            name = 'TB'
     #Pooja Upadhyay - I do not know why this code was written for 2010A and 2010B so I commented it to make the broken website working
    #elif year == '2010B':
            #if disease == 'all':
            #cur = g.db.execute(' select company,disease, daly2010, color from company2015  order by daly2010 DESC')
            #cdd = g.db.execute(' select company, disease, daly2010, color from company2015 order by daly2010 DESC')
        #name = 'ALL'
            #elif disease == 'hiv':
            #cur = g.db.execute(' select company, disease,daly2010, color from company2015 where disease = ? order by daly2010 DESC', ('hiv',))
            #cdd = g.db.execute(' select company, disease, daly2010, color from company2015 where disease = ? order by daly2010 DESC', ('hiv',))
        #name = 'HIV/AIDS'
            #elif disease == 'tb':
            #cur = g.db.execute(' select company,disease, daly2010, color from company2015 where disease = ? order by daly2010 DESC', ('tb',))
            #cdd = g.db.execute(' select company, disease, daly2010, color from company2015 where disease = ? order by daly2010 DESC', ('tb',))
        #name = 'TB'
            #elif disease == 'malaria':
            #cur = g.db.execute(' select company,disease, daly2010, color from company2015 where disease = ? order by daly2010 DESC', ('malaria',))
            #cdd = g.db.execute(' select company, disease, daly2010, color from company2015 where disease = ? order by daly2010 DESC', ('malaria',))
    #name = 'MALARIA'
    elif year == '2013':
        if disease == 'all':
            cur = g.db.execute(' select company,disease, daly2013, color from manudis order by daly2013 DESC')
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis order by daly2013 DESC')
            name = 'ALL'
        elif disease == 'hiv':
            cur = g.db.execute(' select company, disease,daly2013, color from manudis where disease = ? order by daly2013 DESC', ('HIV',))
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis where disease = ? order by daly2013 DESC', ('HIV',))
            name = 'HIV/AIDS'
        elif disease == 'tb':
            cur = g.db.execute(' select company,disease, daly2013, color from manudis where disease = ? order by daly2013 DESC', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2013, color from manudis where disease = ? order by daly2013 DESC', ('TB',))
            name = 'TB'
    elif year == '2015':#=====add 2015 SQL=========
        if disease == 'all':
            cur = g.db.execute(' select company,disease, daly2015, color from manudis2015  order by daly2015 DESC')
            cdd = g.db.execute(' select company, disease, daly2015, color from manudis2015 order by daly2015 DESC')
            name = 'ALL'
        elif disease == 'hiv':
            cur = g.db.execute(' select company, disease,daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('HIV',))
            cdd = g.db.execute(' select company, disease,daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('HIV',))
            name = 'HIV/AIDS'
        elif disease == 'tb':
            cur = g.db.execute(' select company,disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('TB',))
            cdd = g.db.execute(' select company, disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('TB',))
            name = 'TB'
        elif disease == 'malaria':
            cur = g.db.execute(' select company,disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('Malaria',))
            cdd = g.db.execute(' select company, disease, daly2015, color from manudis2015 where disease = ? order by daly2015 DESC', ('Malaria',))
            name = 'MALARIA'
            #=====2015--end============
    piee = cur.fetchall()
    barr = cdd.fetchall()
    print(piee)
    print(barr)
    colocnt = 0
    for j in piee:
        company = j[0]
        print(company)
        dis = j[1]
        daly2010 = j[2]
        print(daly2010)
        if (company == 'Unalleviated Burden') and (disease != dis):
            #colcnt += 1
            continue
        #color = j[2]
        if daly2010 > 0:
            color = compcolors[colocnt]
            t = [company, daly2010, color]
            colocnt += 1
            print(t)
            piedata1.append(t)
            if company == 'Unalleviated Burden':
                continue
            piedata2.append(t)
    #piedata.sort(key=lambda x: x[1], reverse=True)
    n = 0
    temprow = []
    colocnt = 0

    for k in piedata1:
        print(k)
        if n < 4:
            comp = k[0]
            shortcomp = comp[0:10]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor=k[2]
            sscolor=scolor[1:7]
            temprow.append(sscolor)
            #colocnt += 1
            n += 1
        else:
            n = 0
            pielab1.append(temprow)
            temprow = []

    n = 0
    temprow = []
    colocnt = 0

    for k in piedata2:
        print(k)
        if n < 4:
            comp = k[0]
            shortcomp = comp[0:10]
            temprow.append(comp)
            temprow.append(shortcomp)
            scolor=k[2]
            sscolor=scolor[1:7]
            temprow.append(sscolor)
            #colocnt += 1
            n += 1
        else:
            n = 0
            pielab2.append(temprow)
            temprow = []

    colcnt = 0
    for l in barr:
        company = l[0]
        daly2010 = l[2]
        if company == 'Unalleviated Burden':
            #colcnt += 1
            continue
        disease = l[1]
        color = compcolors[colcnt]
        #color=l[3]
        colcnt += 1
        xyz = [company,daly2010,disease,color]
        barchart.append(xyz)
        print(barchart)
    #barchart.sort(key=lambda x: x[1], reverse=True)
    maxim = barchart[0]
    maxval = maxim[1]
    colcnt = 1
    for row in barchart:
        comp = row[0]
        print(row[1])
        if maxval > 0:
           daly = (row[1]/maxval) * 100
        else:
            daly = 0
        disease = row[2]
        color = compcolors[colcnt]
        #color = row[3]
        colcnt += 1
        xyz = [comp,daly,disease,color]
        bardata.append(xyz)
#-----------------------------------------------------------------------------------------------------------------------------------------
    g.db.close()
    url = name.lower()
    speclocate = [year,name,url]
    print(bardata)
    print(pielab1)
    print(pielab2)
    return render_template('company.html', data1=piedata2, data2=piedata1, name=name, navsub=2, showindex=1, pielab1=pielab1, pielab2=pielab2, bardata=bardata, comptype = 0, speclocate = speclocate, scrolling=1)


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
    patent1 = []
    patent2 = []
    for j in data:
        comp = j[0]
        score = j[1]
        color = j[2]
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
    conn = connect_db()
    print("inside update")
    try:
        conn.execute('''DELETE FROM manudis_bkp''')
        conn.execute('''DELETE FROM manutot_bkp''')
        conn.execute('''DELETE FROM patent2010_bkp''')
        conn.execute('''DELETE FROM patent2013_bkp''')
        conn.execute('''DELETE FROM manudis2015_bkp''')
        conn.execute('''DELETE FROM manutot2015_bkp''')
        conn.execute('''DELETE FROM patent2015_bkp''')
        conn.execute('''insert into manudis_bkp select * from manudis''')
        conn.execute('''insert into manutot_bkp select * from manutot''')
        conn.execute('''insert into patent2010_bkp select * from patent2010''')
        conn.execute('''insert into patent2013_bkp select * from patent2013''')
        conn.execute('''insert into manudis2015_bkp select * from manudis2015''')
        conn.execute('''insert into manutot2015_bkp select * from manutot2015''')
        conn.execute('''insert into patent2015_bkp select * from patent2015''')
        # conn.execute('''DELETE FROM manufacturer2010''')
        # conn.execute('''DELETE FROM manufacturer2013''')
        conn.execute('''DELETE FROM manudis''')
        conn.execute('''DELETE FROM manutot''')
        conn.execute('''DELETE FROM patent2010''')
        conn.execute('''DELETE FROM patent2013''')
        conn.execute('''DELETE FROM manudis2015''')
        conn.execute('''DELETE FROM manutot2015''')
        conn.execute('''DELETE FROM patent2015''')
        datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
        datasrc20102015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1560508440&single=true&output=csv'
        df = pd.read_csv(datasrc, skiprows=1)
        # datasrc20102015 = 'ORS_GlobalBurdenDisease_2010B_2015.csv'
        df = pd.read_csv(datasrc, skiprows=1)
        df2015 = pd.read_csv(datasrc20102015, skiprows=1)
        is_df2015_true = df2015.notnull()
        is_df_true = df.notnull()
        i = 0;
        colorlist = []
        colors = ['FFB31C', '0083CA', 'EF3E2E', '003452', '86AAB9', 'CAEEFD', '546675', '8A5575', '305516', 'B78988',
                  'BAE2DA', 'B1345D', '5B75A7', '906F76', 'C0E188', 'DE9C2A', 'F15A22', '8F918B', 'F2C2B7', 'F7C406',
                  'B83F98', '548A9B', 'D86375', 'F1DBC6', '0083CA', '7A80A3', 'CA8566', 'A3516E', '1DF533', '510B95',
                  'DFF352', 'F2C883', 'E3744D', '26B2BE', '5006BA', 'B99BCF', 'DC2A5A', 'D3D472', '2A9DC4', 'C25C90',
                  '65A007', 'FE3289', 'C6DAB5', 'DDF6AC', 'B7E038', '1ADBBD', '3BC6D5', '0ACD57', '22419F', 'D47C5B',
                  '139A97', '1CDDD8', 'FF033D', '004444', 'C25C7D', 'B5A28F', 'C25C7D', '90BA3E', 'DA8709', 'B0B0CE',
                  '2D00DD', 'DD2D00', 'FAFDFD', 'F5FD2F', '0DC4E0', 'FFD700', 'CC263C', 'F5F5DC', '3D9C35', '00CC00',
                  'EAEAFF']
        for x in colors:
            y = '#' + x
            colorlist.append(y)
        # print(colorlist)
        manudata = []
        manutotal = []
        manu2015total = []
        for k in range(25, 88):
            company = df.iloc[k, 2]
            if isinstance(company, float):
                if math.isnan(company):
                    break
            disease = 'TB'
            tbdaly2010 = float(df.iloc[k, 3].replace('-', '0').replace(',', ''))
            try:
             if float(df.iloc[k, 4].replace('-', '0').replace(',', '')) > 0:
                tbdaly2013 = float(df.iloc[k, 4].replace('-', '0').replace(',', ''))
             else:
                tbdaly2013 = 0
            except:
                tbdaly2013 = 0
            if tbdaly2010 > 0 or tbdaly2013 > 0:
                color = colors[i]
                row = [company, disease, tbdaly2010, tbdaly2013, color]
                manudata.append(row)
                i += 1
                conn.execute('insert into manudis values (?,?,?,?,?)', row)
        i = 0
        for k in range(25, 88):
            company = df.iloc[k, 5]
            if isinstance(company, float):
                if math.isnan(company):
                    break
            disease = 'HIV'
            try:
                hivdaly2010 = float(df.iloc[k, 6].replace('-', '0').replace(',', ''))
            except:
                hivdaly2010 = 0
            try:
                hivdaly2013 = float(df.iloc[k, 7].replace('-', '0').replace(',', ''))
            except:
                hivdaly2013 = 0
            if hivdaly2010 > 0 or hivdaly2013 > 0:
                color = colors[i]
                row = [company, disease, hivdaly2010, hivdaly2013, color]
                i += 1
                manudata.append(row)
                conn.execute('insert into manudis values (?,?,?,?,?)', row)
        i = 0
        for k in range(25, 88):
            company = df.iloc[k, 8]
            if isinstance(company, float):
                if math.isnan(company):
                    break
            disease = 'Malaria'
            try:
                hivdaly2010 = float(df.iloc[k, 9].replace('-', '0').replace(',', ''))
            except:
                hivdaly2010 = 0
            try:
                hivdaly2013 = float(df.iloc[k, 10].replace('-', '0').replace(',', ''))
            except:
                hivdaly2013 = 0
            if hivdaly2010 > 0 or hivdaly2013 > 0:
                color = colors[i]
                row = [company, disease, hivdaly2010, hivdaly2013, color]
                i += 1
                manudata.append(row)
                conn.execute('insert into manudis values (?,?,?,?,?)', row)
        i = 0
        for k in range(25, 98):
            company = df.iloc[k, 12]
            if isinstance(company, float):
                if math.isnan(company):
                    break
            try:
                daly2010 = float(df.iloc[k, 13].replace('-', '0').replace(',', ''))
            except:
                daly2010 = 0
            try:
                daly2013 = float(df.iloc[k, 14].replace('-', '0').replace(',', ''))
            except:
                daly2013 = 0
            if daly2010 > 0 or daly2013 > 0:
                color = colors[i]
                row = [company, daly2010, daly2013, color]
                i += 1
                manutotal.append(row)
                conn.execute('insert into manutot values (?,?,?,?)', row)
        i = 0
        for k in range(25, 62):
            company = df2015.iloc[k, 2]
            # print(company)
            if isinstance(company, float):
                if math.isnan(company):
                    break
            disease = 'TB'

            _k3 = df2015.iloc[k, 3]
            if is_df2015_true.iloc[k, 3] == False:
                temp1 = 0
            elif '-' in _k3:
                temp1 = _k3.replace('-', '0')
            elif ',' in _k3:
                temp1 = _k3.replace(',', '')
            else:
                temp1 = _k3
            try:
                tbdaly2010B = float(temp1)
            except:
                tbdaly2010B = 0

            _k4 = df2015.iloc[k, 4]
            if is_df2015_true.iloc[k, 4] == False:
                temp2 = 0
            elif '-' in _k4:
                temp2 = _k4.replace('-', '0')
            elif ',' in _k4:
                temp2 = _k4.replace(',', '')
            else:
                temp2 = _k4
            try:
                tbdaly2015 = float(temp2)
            except:
                tbdaly2015 = 0

            if tbdaly2010B > 0 or tbdaly2015 > 0:
                color = colors[i]
                row = [company, disease, tbdaly2010B, tbdaly2015, color]
                manudata.append(row)
                i += 1
                conn.execute('insert into manudis2015 values (?,?,?,?,?)', row)
        i = 0
        for k in range(25, 66):
            company = df2015.iloc[k, 5]
            if isinstance(company, float):
                if math.isnan(company):
                    break
            # print(company)
            disease = 'HIV'
            _k6 = df2015.iloc[k, 6]
            if is_df2015_true.iloc[k, 6] == False:
                temph = 0
            elif '-' in _k6:
                temph = _k6.replace('-', '0')
            elif ',' in _k6:
                temph = _k6.replace(',', '')
            else:
                temph = _k6

            hivdaly2010B = float(temph)

            k7 = df2015.iloc[k, 7]
            if is_df2015_true.iloc[k, 7] == False:
                temph1 = 0
            elif '-' in k7:
                temph1 = k7.replace('-', '0')
            elif ',' in k7:
                temph1 = k7.replace(',', '')
            else:
                temph1 = k7
            try:
                hivdaly2015 = float(temph1)
            except:
                hivdaly2015 = 0
            if hivdaly2010B > 0 or hivdaly2015 > 0:
                color = colors[i]
                row = [company, disease, hivdaly2010B, hivdaly2015, color]
                i += 1
                manudata.append(row)
                conn.execute('insert into manudis2015 values (?,?,?,?,?)', row)

        i = 0
        for k in range(25, 66):
            company = df2015.iloc[k, 8]
            if isinstance(company, float):
                if math.isnan(company):
                    break
            # print(company)
            disease = 'Malaria'
            _k9 = df2015.iloc[k, 9]
            if is_df2015_true.iloc[k, 9] == False:
                temph = 0
            elif '-' in _k9:
                temph = _k9.replace('-', '0')
            elif ',' in _k9:
                temph = _k9.replace(',', '')
            else:
                temph = _k9

            hivdaly2010B = float(temph)

            k10 = df2015.iloc[k, 10]
            if is_df2015_true.iloc[k, 10] == False:
                temph1 = 0
            elif '-' in k10:
                temph1 = k10.replace('-', '0')
            elif ',' in k10:
                temph1 = k10.replace(',', '')
            else:
                temph1 = k10

            hivdaly2015 = float(temph1)
            if hivdaly2010B > 0 or hivdaly2015 > 0:
                color = colors[i]
                row = [company, disease, hivdaly2010B, hivdaly2015, color]
                i += 1
                manudata.append(row)
                conn.execute('insert into manudis2015 values (?,?,?,?,?)', row)

        i = 0
        for k in range(25, 98):
            company = df2015.iloc[k, 12]
            if isinstance(company, float):
                if math.isnan(company):
                    break
            # print(company)
            k13 = df2015.iloc[k, 13]
            # print(k13)
            if is_df2015_true.iloc[k, 13] == False:
                temphd = 0
            elif '-' in k13:
                temphd = k13.replace('-', '0')
            elif ',' in k13:
                temphd = k13.replace(',', '')
            else:
                temphd = k13

            daly2010B = float(temphd)

            k14 = df2015.iloc[k, 14]
            # print(k14)
            if is_df2015_true.iloc[k, 14] == False:
                tempd1 = 0
            elif '-' in k14:
                tempd1 = k14.replace('-', '0')
            elif ',' in k14:
                tempd1 = k14.replace(',', '')
            else:
                tempd1 = k14

            daly2015 = float(tempd1)

            if daly2010B > 0 or daly2015 > 0:
                color = colors[i]
                row = [company, daly2010B, daly2015, color]
                i += 1
                manu2015total.append(row)
                # print(row)
                conn.execute('insert into manutot2015 values (?,?,?,?)', row)

        def cleanfloat(var):
            # print(var)
            if var == '#REF!' or var == '-' or var == 'nan':
                var = 0
            if type(var) != float:
                var = float(var.replace(',', ''))
            if var != var:
                var = 0
            return var

        oldrow = ['']
        pat2010 = []
        for i in range(1, 39):
            prow = []
            comp = df.iloc[1, i]
            # print(comp)
            prow.append(comp)
            for j in range(11, 21):
                if j == 11:
                    tb1 = cleanfloat(df.iloc[8, i])
                    tb2 = cleanfloat(df.iloc[9, i])
                    tb3 = cleanfloat(df.iloc[10, i])
                    tb = [tb1, tb2, tb3]
                    temp = (tb1 + tb2 + tb3)
                    prow.append(temp)
                elif j == 12:
                    mal1 = cleanfloat(df.iloc[11, i])
                    mal2 = cleanfloat(df.iloc[12, i])
                    mal = [mal1, mal2]
                    temp = (mal1 + mal2)
                    prow.append(temp)
                elif j == 20:
                    total = cleanfloat(df.iloc[j, i])
                    prow.append(total)
                else:
                    temp = df.iloc[j, i]
                    if isinstance(temp, float) == False and isinstance(temp, int) == False:
                        temp = float(temp.replace(',', ''))
                    if temp != temp:
                        temp = 0
                    prow.append(temp)
            if prow[0] == oldrow[0]:
                for ind in range(1, len(prow)):
                    prow[ind] += oldrow[ind]
            oldrow = prow
            if comp != df.iloc[1, i + 1]:
                pat2010.append(prow)
        unmet = ['Unmet Need']
        for j in range(11, 21):
            if j == 11:
                # print(df.iloc[7,46])
                tb1 = cleanfloat(df.iloc[8, 42])
                tb2 = cleanfloat(df.iloc[9, 42])
                tb3 = cleanfloat(df.iloc[10, 42])
                tb = [tb1, tb2, tb3]
                temp = (tb1 + tb2 + tb3)
                unmet.append(temp)
            elif j == 12:
                mal1 = cleanfloat(df.iloc[11, 42])
                mal2 = cleanfloat(df.iloc[12, 45])
                mal = [mal1, mal2]
                temp = (mal1 + mal2)
                unmet.append(temp)
            elif j == 20:
                total = cleanfloat(df.iloc[j, 42])
                unmet.append(total)
            else:
                temp = df.iloc[j, 42]
                if isinstance(temp, float) == False and isinstance(temp, int) == False:
                    temp = float(temp.replace(',', ''))
                if temp != temp:
                    temp = 0
                unmet.append(temp)
        pat2010.append(unmet)
        colind = 0
        for item in pat2010:
            item.append(colors[colind])
            colind += 1
            conn.execute(' insert into patent2010 values (?,?,?,?,?,?,?,?,?,?,?,?) ', item)
        # print(pat2010)

        oldrow = ['']
        pat2013 = []
        for i in range(45, 89):
            prow = []
            comp = df.iloc[1, i]
            prow.append(comp)
            # print(comp)
            for j in range(11, 21):
                if j == 11:
                    tb1 = cleanfloat(df.iloc[8, i])
                    tb2 = cleanfloat(df.iloc[9, i])
                    tb3 = cleanfloat(df.iloc[10, i])
                    tb = [tb1, tb2, tb3]
                    temp = (tb1 + tb2 + tb3)
                    prow.append(temp)
                elif j == 12:
                    mal1 = cleanfloat(df.iloc[11, i])
                    mal2 = cleanfloat(df.iloc[12, i])
                    mal = [mal1, mal2]
                    temp = (mal1 + mal2)
                    prow.append(temp)
                elif j == 20:
                    total = cleanfloat(df.iloc[j, i])
                    prow.append(total)
                else:
                    temp = df.iloc[j, i]
                    if isinstance(temp, float) == False and isinstance(temp, int) == False:
                        temp = float(temp.replace(',', ''))
                    if temp != temp:
                        temp = 0
                    prow.append(temp)
            if prow[0] == oldrow[0]:
                for ind in range(1, len(prow)):
                    prow[ind] += oldrow[ind]
            oldrow = prow
            if comp != df.iloc[1, i + 1]:
                pat2013.append(prow)
        unmet = ['Unmet Need']
        for j in range(11, 21):
            if j == 11:
                # print(df.iloc[8,93])
                tb1 = cleanfloat(df.iloc[8, 92])
                tb2 = cleanfloat(df.iloc[9, 92])
                tb3 = cleanfloat(df.iloc[10, 92])
                tb = [tb1, tb2, tb3]
                temp = (tb1 + tb2 + tb3)
                unmet.append(temp)
            elif j == 12:
                mal1 = cleanfloat(df.iloc[11, 92])
                mal2 = cleanfloat(df.iloc[12, 92])
                mal = [mal1, mal2]
                temp = (mal1 + mal2)
                unmet.append(temp)
            elif j == 20:
                total = cleanfloat(df.iloc[j, 92])
                unmet.append(total)
            else:
                temp = df.iloc[j, 92]
                if isinstance(temp, float) == False and isinstance(temp, int) == False:
                    temp = float(temp.replace(',', ''))
                if temp != temp:
                    temp = 0
                unmet.append(temp)
        pat2013.append(unmet)
        colind = 0
        for item in pat2013:
            item.append(colors[colind])
            colind += 1
            conn.execute(' insert into patent2013 values (?,?,?,?,?,?,?,?,?,?,?,?) ', item)
        # print(pat2013)

        oldrow = ['']
        pat2015 = []
        for i in range(45, 88):
            prow = []
            # print(i)
            # print(df2015)
            comp = df2015.iloc[0, i]
            if is_df2015_true.iloc[0, i] == True:
                temp_comp = comp
            else:
                comp = temp_comp
            prow.append(comp)
            # print(comp)
            for j in range(11, 21):
                if j == 11:
                    if is_df2015_true.iloc[7, i] == True:
                        tb1 = cleanfloat(df2015.iloc[7, i])
                    else:
                        tb1 = 0
                    if is_df2015_true.iloc[8, i] == True:
                        tb2 = cleanfloat(df2015.iloc[8, i])
                    else:
                        tb2 = 0
                    if is_df2015_true.iloc[9, i] == True:
                        tb3 = cleanfloat(df2015.iloc[9, i])
                    else:
                        tb3 = 0
                    tb = [tb1, tb2, tb3]
                    temp = (tb1 + tb2 + tb3)
                    prow.append(temp)
                elif j == 12:
                    if is_df2015_true.iloc[10, i] == True:
                        mal1 = cleanfloat(df2015.iloc[10, i])
                    else:
                        mal1 = 0
                    if is_df2015_true.iloc[11, i] == True:
                        mal2 = cleanfloat(df2015.iloc[11, i])
                    else:
                        mal2 = 0
                    mal = [mal1, mal2]
                    temp = (mal1 + mal2)
                    prow.append(temp)
                elif j == 20:
                    if is_df2015_true.iloc[j - 1, i] == True:
                        total = cleanfloat(df2015.iloc[j - 1, i])
                    else:
                        total = 0
                    prow.append(total)
                else:
                    temp = df2015.iloc[j - 1, i]
                    # print(temp)
                    if temp == '-' or temp == '#REF!':
                        temp = 0
                    if isinstance(temp, float) == False and isinstance(temp, int) == False:
                        temp = float(temp.replace(',', ''))
                    if temp != temp:
                        temp = 0
                    prow.append(temp)
            if prow[0] == oldrow[0]:
                for ind in range(1, len(prow)):
                    prow[ind] += oldrow[ind]
            oldrow = prow
            if is_df2015_true.iloc[0, i + 1] == True:
                if comp != is_df2015_true.iloc[0, i + 1]:
                    pat2015.append(prow)
            else:
                if comp != temp_comp:
                    pat2015.append(prow)
        unmet = ['Unmet Need']
        for j in range(11, 21):
            if j == 11:
                # print(df2015.iloc[8, 93])
                if is_df2015_true.iloc[7, 91] == True:
                    tb1 = cleanfloat(df2015.iloc[7, 91])
                else:
                    tb1 = 0
                if is_df2015_true.iloc[8, 91] == True:
                    tb2 = cleanfloat(df2015.iloc[8, 91])
                else:
                    tb2 = 0
                if is_df2015_true.iloc[9, 91] == True:
                    tb3 = cleanfloat(df2015.iloc[9, 91])
                else:
                    tb3 = 0
                tb = [tb1, tb2, tb3]
                temp = (tb1 + tb2 + tb3)
                unmet.append(temp)
            elif j == 12:
                if is_df2015_true.iloc[10, 91] == True:
                    mal1 = cleanfloat(df2015.iloc[10, 91])
                else:
                    mall = 0
                if is_df2015_true.iloc[11, 91] == True:
                    mal2 = cleanfloat(df2015.iloc[1, 91])
                else:
                    mal2 = 0
                mal = [mal1, mal2]
                temp = (mal1 + mal2)
                unmet.append(temp)
            elif j == 20:
                if is_df2015_true.iloc[j - 1, 91] == True:
                    total = cleanfloat(df2015.iloc[j - 1, 91])
                else:
                    total = 0
                unmet.append(total)
            else:
                temp = df2015.iloc[j - 1, 91]
                if temp == '-' or temp == '#REF!':
                    temp = 0
                if isinstance(temp, float) == False and isinstance(temp, int) == False:
                    temp = float(temp.replace(',', ''))
                if temp != temp:
                    temp = 0
                unmet.append(temp)
        pat2015.append(unmet)
        colind = 0
        for item in pat2015:
            item.append(colors[colind])
            colind += 1
            conn.execute(' insert into patent2015 values (?,?,?,?,?,?,?,?,?,?,?,?) ', item)
        #print("Man Done")
        conn.execute('''DELETE FROM countrybydis2010_bkp''')
        conn.execute('''DELETE FROM countrybydis2013_bkp''')
        conn.execute('''DELETE FROM diseaseall2010_bkp''')
        conn.execute('''DELETE FROM diseaseall2013_bkp''')
        conn.execute('''DELETE FROM diseaseall2015_bkp''')
        conn.execute('''INSERT INTO countrybydis2010_bkp SELECT * FROM countrybydis2010''')
        conn.execute('''INSERT INTO countrybydis2013_bkp SELECT * FROM countrybydis2013''')
        conn.execute('''INSERT INTO diseaseall2010_bkp SELECT * FROM diseaseall2010''')
        conn.execute('''INSERT INTO diseaseall2013_bkp SELECT * FROM diseaseall2013''')
        conn.execute('''INSERT INTO diseaseall2015_bkp SELECT * FROM diseaseall2015''')
        conn.execute('''DELETE FROM diseaseall2010''')
        conn.execute('''DELETE FROM diseaseall2013''')
        conn.execute('''DELETE FROM diseaseall2015''')
        conn.execute('''DELETE FROM countrybydis2010''')
        conn.execute('''DELETE FROM countrybydis2013''')
        datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1996016204&single=true&output=csv'
        df = pd.read_csv(datasrc, skiprows=1)
        datasrc3 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1996016204&single=true&output=csv'
        df_2010B_2015 = pd.read_csv(datasrc3, skiprows=1)
        for i in range(1, 218):
            temprow = []
            temp1 = df.iloc[i, 0]
            temprow.append(temp1)
            # print df.iloc[i, 0]
            for k in range(1, 10):
                temp = df.iloc[i, k]
                if isinstance(temp, float):
                    temprow.append(0.0)
                else:
                    temprow.append(float(temp.replace(',', '').replace('-', '0')))
            conn.execute(' insert into countrybydis2010 values (?,?,?,?,?,?,?,?,?,?)', temprow)
            conn.execute(' insert into diseaseall2010 values (?,?,?,?,?,?,?,?,?,?)', temprow)
        print("countrybydis2010 Done")
        for i in range(1, 218):
            temprow = []
            temprow.append(df.iloc[i, 11])
            for k in range(12, 21):
                temp = df.iloc[i, k]
                # if isinstance(temp, float):
                # temprow.append(0.0)
                if k in (15, 19):
                    try:
                        temprow.append(temp)
                    except:
                        temprow.append(0.0)
                else:
                    try:
                        temprow.append(float(temp.replace(',', '').replace('-', '0')))
                    except:
                        temprow.append(0.0)
            conn.execute(' insert into countrybydis2013 values (?,?,?,?,?,?,?,?,?,?)', temprow)
            conn.execute(' insert into diseaseall2013 values (?,?,?,?,?,?,?,?,?,?)', temprow)

        data2010B = []
        data2015 = []
        for i in range(1, 218):
            temprow = []
            temprow.append(df_2010B_2015.iloc[i, 11])
            for k in range(12, 21):
                temp = df_2010B_2015.iloc[i, k]
                # if isinstance(temp, float):
                # temprow.append(0.0)
                if k in (15, 19):
                    try:
                        temprow.append(temp)
                    except:
                        temprow.append(0.0)
                else:
                    try:
                        temprow.append(float(temp.replace(',', '').replace('-', '0')))
                    except:
                        temprow.append(0.0)
            # conn.execute(' insert into countrybydis2015 values (?,?,?,?,?,?,?,?,?,?)', temprow)
            conn.execute(' insert into diseaseall2015 values (?,?,?,?,?,?,?,?,?,?)', temprow)
        #print("Country Done")
        conn.execute(''' DELETE FROM country2010_bkp ''')
        conn.execute(''' DELETE FROM country2013_bkp ''')
        conn.execute(''' DELETE FROM country2015_bkp ''')
        conn.execute(''' DELETE FROM countryp2010_bkp ''')
        conn.execute(''' DELETE FROM countryp2013_bkp ''')
        conn.execute(''' DELETE FROM countryp2015_bkp ''')
        conn.execute(''' INSERT INTO country2010_bkp SELECT * FROM country2010''')
        conn.execute(''' INSERT INTO country2013_bkp SELECT * FROM country2013''')
        conn.execute(''' INSERT INTO country2015_bkp SELECT * FROM country2015''')
        conn.execute(''' INSERT INTO countryp2010_bkp SELECT * FROM countryp2010''')
        conn.execute(''' INSERT INTO countryp2013_bkp SELECT * FROM countryp2013''')
        conn.execute(''' INSERT INTO countryp2015_bkp SELECT * FROM countryp2015''')
        conn.execute(''' DELETE FROM country2010 ''')
        conn.execute(''' DELETE FROM country2013 ''')
        conn.execute(''' DELETE FROM country2015 ''')
        conn.execute(''' DELETE FROM countryp2010 ''')
        conn.execute(''' DELETE FROM countryp2013 ''')
        conn.execute(''' DELETE FROM countryp2015 ''')
        url = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=0&single=true&output=csv'
        df = pd.read_csv(url, skiprows=1)
        url2010B2015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=0&single=true&output=csv'
        df2015 = pd.read_csv(url2010B2015, skiprows=1)
        is_df2015_true = df2015.notnull()
        is_df_true = df.notnull()

        def clean(num):
            return float(num.replace(' ', '').replace(',', '').replace('-', '0'))

        countrydata = []
        mapp = []

        for i in range(3, 220):
            country = df.iloc[i, 0]
            tb = clean(df.iloc[i, 7])
            malaria = clean(df.iloc[i, 34])
            hiv = clean(df.iloc[i, 47])
            roundworm = clean(df.iloc[i, 56])
            hookworm = clean(df.iloc[i, 57])
            whipworm = clean(df.iloc[i, 58])
            schistosomiasis = clean(df.iloc[i, 61])
            lf = clean(df.iloc[i, 64])
            total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + lf
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf]
            countrydata.append(row)

        sortedlist = sorted(countrydata, key=lambda xy: xy[1], reverse=True)
        maxrow = sortedlist[0]
        maxval = maxrow[1]
        for j in sortedlist:
            country = j[0]
            total = (j[1] / maxval) * 100
            tb = (j[2] / maxval) * 100
            malaria = (j[3] / maxval) * 100
            hiv = (j[4] / maxval) * 100
            roundworm = (j[5] / maxval) * 100
            hookworm = (j[6] / maxval) * 100
            whipworm = (j[7] / maxval) * 100
            schistosomiasis = (j[8] / maxval) * 100
            lf = (j[9] / maxval) * 100
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf]
            mapp.append(row)
        for k in countrydata:
            conn.execute(''' INSERT INTO country2010 VALUES (?,?,?,?,?,?,?,?,?,?) ''', k)

        for l in mapp:
            conn.execute(''' INSERT INTO countryp2010 VALUES (?,?,?,?,?,?,?,?,?,?) ''', l)

        countrydata2 = []
        mapp2 = []
        for i in range(3, 220):
            country = df.iloc[i, 67]
            tb = clean(df.iloc[i, 74])
            malaria = clean(df.iloc[i, 104])
            hiv = clean(df.iloc[i, 115])
            roundworm = clean(df.iloc[i, 124])
            hookworm = clean(df.iloc[i, 125])
            whipworm = clean(df.iloc[i, 126])
            schistosomiasis = clean(df.iloc[i, 129])
            onchoceriasis = clean(df.iloc[i, 131])
            lf = clean(df.iloc[i, 134])
            total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + onchoceriasis + lf
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf]
            countrydata2.append(row)

        sortedlist2 = sorted(countrydata2, key=lambda xy: xy[1], reverse=True)
        maxrow = sortedlist2[0]
        maxval = maxrow[1]
        for j in sortedlist2:
            country = j[0]
            total = (j[1] / maxval) * 100
            tb = (j[2] / maxval) * 100
            malaria = (j[3] / maxval) * 100
            hiv = (j[4] / maxval) * 100
            roundworm = (j[5] / maxval) * 100
            hookworm = (j[6] / maxval) * 100
            whipworm = (j[7] / maxval) * 100
            schistosomiasis = (j[8] / maxval) * 100
            onchoceriasis = (j[9] / maxval) * 100
            lf = (j[10] / maxval) * 100
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf]
            mapp2.append(row)

        for k in countrydata2:
            conn.execute(''' INSERT INTO country2013 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', k)

        for l in mapp2:
            conn.execute(''' INSERT INTO countryp2013 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', l)

        countrydata3 = []
        mapp2 = []
        for i in range(3, 220):
            country = df2015.iloc[i, 67]
            if is_df2015_true.iloc[i, 74] == True:
                tb = clean(df2015.iloc[i, 74])
            else:
                tb = 0
            if is_df2015_true.iloc[i, 104] == True:
                malaria = clean(df2015.iloc[i, 104])
            else:
                malaria = 0
            if is_df2015_true.iloc[i, 115] == True:
                hiv = clean(df2015.iloc[i, 115])
            else:
                hiv = 0
            if is_df2015_true.iloc[i, 124] == True:
                roundworm = clean(df2015.iloc[i, 124])
            else:
                roundworm = 0
            if is_df2015_true.iloc[i, 125] == True:
                hookworm = clean(df2015.iloc[i, 125])
            else:
                hookworm = 0
            if is_df2015_true.iloc[i, 126] == True:
                whipworm = clean(df2015.iloc[i, 126])
            else:
                whipworm = 0
            if is_df2015_true.iloc[i, 129] == True:
                schistosomiasis = clean(df2015.iloc[i, 129])
            else:
                schistosomiasis = 0
            if is_df2015_true.iloc[i, 131] == True:
                onchoceriasis = clean(df2015.iloc[i, 131])
            else:
                onchoceriasis = 0
            if is_df2015_true.iloc[i, 134] == True:
                lf = clean(df2015.iloc[i, 134])
            else:
                lf = 0
            total = tb + malaria + hiv + roundworm + hookworm + whipworm + schistosomiasis + onchoceriasis + lf
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf]
            countrydata3.append(row)

        sortedlist2 = sorted(countrydata3, key=lambda xy: xy[1], reverse=True)
        maxrow = sortedlist2[0]
        maxval = maxrow[1]
        for j in sortedlist2:
            country = j[0]
            total = (j[1] / maxval) * 100
            tb = (j[2] / maxval) * 100
            malaria = (j[3] / maxval) * 100
            hiv = (j[4] / maxval) * 100
            roundworm = (j[5] / maxval) * 100
            hookworm = (j[6] / maxval) * 100
            whipworm = (j[7] / maxval) * 100
            schistosomiasis = (j[8] / maxval) * 100
            onchoceriasis = (j[9] / maxval) * 100
            lf = (j[10] / maxval) * 100
            row = [country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, onchoceriasis, lf]
            mapp2.append(row)
            # print(countrydata3)
        for k in countrydata3:
            # print(k)
            conn.execute(''' INSERT INTO country2015 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', k)

        for l in mapp2:
            # print(l)
            conn.execute(''' INSERT INTO countryp2015 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', l)
        #print("Country2 Done")
        conn.execute('''DELETE FROM disease2010_bkp''')
        conn.execute('''DELETE FROM disease2013_bkp''')
        conn.execute('''DELETE FROM disease2015_bkp''')
        conn.execute('''DELETE FROM disbars_bkp''')
        conn.execute('''DELETE FROM distypes_bkp''')
        conn.execute('''DELETE FROM disbars2010B2015_bkp''')
        conn.execute('''DELETE FROM distypes2010B2015_bkp''')

        conn.execute('''insert into disease2010_bkp select * from disease2010''')
        conn.execute('''insert into disease2013_bkp select * from disease2013''')
        conn.execute('''insert into disease2015_bkp select * from disease2015''')
        conn.execute('''insert into disbars_bkp select * from disbars''')
        conn.execute('''insert into distypes_bkp select * from distypes''')
        conn.execute('''insert into disbars2010B2015_bkp select * from disbars2010B2015''')
        conn.execute('''insert into distypes2010B2015_bkp select * from distypes2010B2015''')

        conn.execute('''DELETE FROM disease2010''')
        conn.execute('''DELETE FROM disease2013''')
        conn.execute('''DELETE FROM disease2015''')
        conn.execute('''DELETE FROM disbars''')
        conn.execute('''DELETE FROM distypes''')
        conn.execute('''DELETE FROM disbars2010B2015''')
        conn.execute('''DELETE FROM distypes2010B2015''')

        datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
        # datasrc = 'ORS_GlobalBurdenDisease_2010_2013.csv'
        df = pd.read_csv(datasrc, skiprows=1)
        # datasrc2 = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQI7j2NartMCCF_N-OCkFqAyD67N9Q32yybE21x-zaRPrETsszdZep91dVVVSCjeXXbPjPfZVdE-odE/pub?gid=1560508440&single=true&output=csv'
        datasrc2 = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
        datasrc3 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1560508440&single=true&output=csv'
        df2 = pd.read_csv(datasrc2, skiprows=1)
        df_2010B_2015 = pd.read_csv(datasrc3, skiprows=1)

        disease2010db = []
        disease2013db = []
        disease2015db = []
        i = 0
        for k in range(8, 20):
            distypes = ['TB', 'TB', 'TB', 'Malaria', 'Malaria', 'HIV', 'Roundworm', 'Hookworm', 'Whipworm',
                        'Schistosomiasis', 'Onchoceriasis', 'LF']
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            dis = ['Drug Susceptable TB', 'MDR-TB', 'XDR-TB', 'p. falc Malaria', 'p. vivax Malaria', 'HIV', 'Roundworm',
                   'Hookworm', 'Whipworm', 'Schistosomiasis', 'Onchoceriasis', 'LF']
            color = colors[i]
            disease = dis[i]
            distype = distypes[i]
            temp = df.iloc[k, 39]
            # print(temp)
            temp1 = df.iloc[k, 41]
            # print(temp1)
            temp2 = df.iloc[k, 42]
            # print(temp2)
            if type(temp) != float and type(temp1) != float and type(temp2) != float:
                impact = float(temp.replace(',', ''))
                daly = float(temp1.replace(',', ''))
                need = float(temp2.replace(',', ''))
                i += 1
                row = [disease, distype, impact, daly, need, color]
                disease2010db.append(row)
                conn.execute('insert into disease2010 values (?,?,?,?,?,?)', row)

        i = 0
        for k in range(8, 20):
            distypes = ['TB', 'TB', 'TB', 'Malaria', 'Malaria', 'HIV', 'Roundworm', 'Hookworm', 'Whipworm',
                        'Schistosomiasis', 'Onchoceriasis', 'LF']
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            dis = ['Drug Susceptable TB', 'MDR-TB', 'XDR-TB', 'p. falc Malaria', 'p. vivax Malaria', 'HIV', 'Roundworm',
                   'Hookworm', 'Whipworm', 'Schistosomiasis', 'Onchoceriasis', 'LF']
            color = colors[i]
            disease = dis[i]
            distype = distypes[i]
            temp = df.iloc[k, 89]
            temp1 = df.iloc[k, 91]
            temp2 = df.iloc[k, 92]
            # print(temp)
            # print(temp1)
            # print(temp2)
            # print(distype)
            # print(disease)
            if type(temp) != float and type(temp1) != float and type(temp2) != float:
                impact = float(temp.replace(',', ''))
                daly = float(temp1.replace(',', ''))
                need = float(temp2.replace(',', ''))
                i += 1
                row = [disease, distype, impact, daly, need, color]
                disease2013db.append(row)
                conn.execute('insert into disease2013 values (?,?,?,?,?,?)', row)
        i = 0
        for k in range(7, 19):
            distypes = ['TB', 'TB', 'TB', 'Malaria', 'Malaria', 'HIV', 'Roundworm', 'Hookworm', 'Whipworm',
                        'Schistosomiasis', 'Onchoceriasis', 'LF']
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            dis = ['Drug Susceptable TB', 'MDR-TB', 'XDR-TB', 'p. falc Malaria', 'p. vivax Malaria', 'HIV', 'Roundworm',
                   'Hookworm', 'Whipworm', 'Schistosomiasis', 'Onchoceriasis', 'LF']
            color = colors[i]
            disease = dis[i]
            distype = distypes[i]
            temp = df_2010B_2015.iloc[k, 88]
            temp1 = df_2010B_2015.iloc[k, 90]
            temp2 = df_2010B_2015.iloc[k, 91]
            # print(temp)
            # print(temp1)
            # print(temp2)
            # print(distype)
            # print(disease)
            if type(temp) != float and type(temp1) != float and type(temp2) != float:
                impact = float(temp.replace(',', ''))
                daly = float(temp1.replace(',', ''))
                need = float(temp2.replace(',', ''))
                i += 1
                row = [disease, distype, impact, daly, need, color]
                disease2013db.append(row)
                conn.execute('insert into disease2015 values (?,?,?,?,?,?)', row)

        def stripdata(x, y):
            try:
                tmp = df.iloc[x, y]
                if tmp == "#DIV/0!" or tmp == "nan" or tmp == "#REF!":
                    return (0)
                if isinstance(tmp, float) == False:
                    return (float(tmp.replace(',', '').replace(' ', '0').replace('%', '')))
                else:
                    return (0)
            except:
                return (0)

        def stripdata3(x, y):
            try:
                tmp = df_2010B_2015.iloc[x, y]
                if tmp == "#DIV/0!" or tmp == "nan" or tmp == "#REF!":
                    return (0)
                if isinstance(tmp, float) == False:
                    return (float(tmp.replace(',', '').replace(' ', '0').replace('%', '')))
                else:
                    return (0)
            except:
                return (0)

        def stripdata2(x, y):
            try:
                tmp = df2.iloc[x, y]
                if tmp == "#DIV/0!" or tmp == "nan" or tmp == "#REF!":
                    return (0)
                if isinstance(tmp, float) == False:
                    res = float(tmp.replace(',', '').replace(' ', '0').replace('%', ''))
                    if res > 10000:
                        res = res * 0.00001
                    # print(res)
                    return (0.01 * res)
                else:
                    return (0)
            except:
                return (0)

        disbars = []
        j = 0
        for k in range(104, 113):
            colors = ['#FFB31C', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            diseasename = df.iloc[k, 7]
            newdiseasename = df_2010B_2015.iloc[k, 7]
            # print(diseasename)
            color = colors[j]
            efficacy2010 = stripdata(k, 8)
            efficacy2013 = stripdata(k, 9)
            coverage2010 = stripdata(k, 10)
            coverage2013 = stripdata(k, 11)
            need2010 = stripdata(k, 12)
            need2013 = stripdata(k, 13)

            newefficacy2010 = stripdata3(k, 8)
            newefficacy2013 = stripdata3(k, 9)
            newcoverage2010 = stripdata3(k, 10)
            newcoverage2013 = stripdata3(k, 11)
            newneed2010 = stripdata3(k, 12)
            newneed2013 = stripdata3(k, 13)

            roww = [diseasename, color, efficacy2010, efficacy2013, coverage2010, coverage2013, need2010, need2013]
            newroww = [diseasename, color, newefficacy2010, newefficacy2013, newcoverage2010, newcoverage2013,
                       newneed2010,
                       newneed2013]
            # print(roww)
            disbars.append(roww)
            j += 1
            conn.execute('insert into disbars values (?,?,?,?,?,?,?,?)', roww)
            # print(newdiseasename)
            if (newdiseasename == 0):
                print("")
            else:
                conn.execute('insert into disbars2010B2015 values (?,?,?,?,?,?,?,?)', newroww)

        # =====================================Jing-3/3/2-18============================================
        i = 1
        j = 0
        mark = 0
        efficacy2010 = 0
        efficacy2013 = 0
        coverage2010 = 0
        coverage2013 = 0
        newefficacy2010 = 0
        newefficacy2013 = 0
        newcoverage2010 = 0
        newcoverage2013 = 0
        for k in [107, 109, 111, 112, 113, 115]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            dismap = [2, 3, 1]
            position = [2, 0, 1]
            disease = ['Normal-TB', 'MDR-TB', 'XDR-TB']
            disetype = 'TB'
            m = dismap[mark]
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacy2010 += stripdata(k, 1)
            efficacy2013 += stripdata(k, 2)
            coverage2010 += stripdata(k, 3)
            coverage2013 += stripdata(k, 5)

            newefficacy2010 += stripdata3(k, 1)
            newefficacy2013 += stripdata3(k, 2)
            newcoverage2010 += stripdata3(k, 3)
            newcoverage2013 += stripdata3(k, 5)
            # print('==========efficacy2010=====')

            if i == m:
                efficacy2010 /= m
                efficacy2013 /= m
                coverage2010 /= m
                coverage2013 /= m

                newefficacy2010 /= m
                newefficacy2013 /= m
                newcoverage2010 /= m
                newcoverage2013 /= m

                i = 0
                mark += 1
                roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
                distypes.append(roww)

                newroww = [diseasename, disetype, color, newefficacy2010, newefficacy2013, newcoverage2010,
                           newcoverage2013,
                           p]

                # print(roww)
                conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
                conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', newroww)
                efficacy2010 = 0
                efficacy2013 = 0
                coverage2010 = 0
                coverage2013 = 0

                newefficacy2010 = 0
                newefficacy2013 = 0
                newcoverage2010 = 0
                newcoverage2013 = 0

            j += 1
            i += 1
        cur = conn.execute(' select * from distypes where distype=? ', ('TB',))
        data = cur.fetchall()

        # print(data)
        # print(data)
        i = 1
        j = 0
        mark = 0
        efficacy2010 = 0
        efficacy2013 = 0
        coverage2010 = 0
        coverage2013 = 0
        for k in [124, 117, 118, 119, 120, 121, 122]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            dismap = [1, 6]
            position = [0, 1]
            disease = ['p. vivax Malaria', 'p. falc Malaria']
            disetype = 'Malaria'
            m = dismap[mark]
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacy2010 += stripdata(k, 1)
            efficacy2013 += stripdata(k, 2)
            coverage2010 += stripdata(k, 3)
            coverage2013 += stripdata(k, 5)

            newefficacy2010 += stripdata3(k, 1)
            newefficacy2013 += stripdata3(k, 2)
            newcoverage2010 += stripdata3(k, 3)
            newcoverage2013 += stripdata3(k, 5)
            # print('==========This is Malaria=====')

            if i == m:
                efficacy2010 /= m
                efficacy2013 /= m
                coverage2010 /= m
                coverage2013 /= m

                newefficacy2010 /= m
                newefficacy2013 /= m
                newcoverage2010 /= m
                newcoverage2013 /= m

                i = 0
                mark += 1
                roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
                distypes.append(roww)
                # print(roww)
                newroww = [diseasename, disetype, color, newefficacy2010, newefficacy2013, newcoverage2010,
                           newcoverage2013,
                           p]
                conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
                conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', newroww)
                efficacy2010 = 0
                efficacy2013 = 0
                coverage2010 = 0
                coverage2013 = 0
                newefficacy2010 = 0
                newefficacy2013 = 0
                newcoverage2010 = 0
                newcoverage2013 = 0

            j += 1
            i += 1
        cur = conn.execute(' select * from distypes where distype=? ', ('Malaria',))
        data = cur.fetchall()
        # print(data)

        i = 1
        j = 0
        mark = 0
        efficacy2010 = 0
        efficacy2013 = 0
        coverage2010 = 0
        coverage2013 = 0
        for k in [161, 162, 163, 164, 165, 166]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # dismap =[2,3,1]
            position = [5, 4, 3, 2, 1, 0]
            disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disetype = 'Hookworm'
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacy2010 += stripdata(k, 1)
            efficacy2013 += stripdata(k, 2)
            coverage2010 += stripdata(k, 3)
            coverage2013 += stripdata(k, 5)

            newefficacy2010 += stripdata3(k, 1)
            newefficacy2013 += stripdata3(k, 2)
            newcoverage2010 += stripdata3(k, 3)
            newcoverage2013 += stripdata3(k, 5)
            # print('==========This is Hookworm=====')
            i = 0
            roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            distypes.append(roww)
            # print(roww)
            newroww = [diseasename, disetype, color, newefficacy2010, newefficacy2013, newcoverage2010, newcoverage2013,
                       p]
            conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
            conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', roww)
            efficacy2010 = 0
            efficacy2013 = 0
            coverage2010 = 0
            coverage2013 = 0
            newefficacy2010 = 0
            newefficacy2013 = 0
            newcoverage2010 = 0
            newcoverage2013 = 0
            mark += 1
            j += 1
        cur = conn.execute(' select * from distypes where distype=? ', ('Hookworm',))
        data = cur.fetchall()
        # print(data)

        i = 1
        j = 0
        mark = 0
        for k in [168, 169, 170, 171, 172, 173]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # dismap =[2,3,1]
            position = [5, 4, 3, 2, 1, 0]
            disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disetype = 'Whipworm'
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacy2010 += stripdata(k, 1)
            efficacy2013 += stripdata(k, 2)
            coverage2010 += stripdata(k, 3)
            coverage2013 += stripdata(k, 5)
            # print('==========This is Whipworm=====')
            newefficacy2010 += stripdata3(k, 1)
            newefficacy2013 += stripdata3(k, 2)
            newcoverage2010 += stripdata3(k, 3)
            newcoverage2013 += stripdata3(k, 5)
            i = 0
            roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            distypes.append(roww)
            # print(roww)
            newroww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
            conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', newroww)
            efficacy2010 = 0
            efficacy2013 = 0
            coverage2010 = 0
            coverage2013 = 0
            newefficacy2010 = 0
            newefficacy2013 = 0
            newcoverage2010 = 0
            newcoverage2013 = 0
            mark += 1
            j += 1
        cur = conn.execute(' select * from distypes where distype=? ', ('Whipworm',))
        data = cur.fetchall()
        # print(data)

        i = 1
        j = 0
        mark = 0
        for k in [175, 176, 177, 178, 179, 180]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # dismap =[2,3,1]
            position = [5, 4, 3, 2, 1, 0]
            disease = ['Ivm + Alb', 'Dec + Alb', 'Pzq', 'Ivm', 'Dec', 'Alb']
            disetype = 'Schistosomiasis'
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacy2010 += stripdata(k, 1)
            efficacy2013 += stripdata(k, 2)
            coverage2010 += stripdata(k, 3)
            coverage2013 += stripdata(k, 5)
            # print('==========This is Schistosomiasis=====')
            newefficacy2010 += stripdata3(k, 1)
            newefficacy2013 += stripdata3(k, 2)
            newcoverage2010 += stripdata3(k, 3)
            newcoverage2013 += stripdata3(k, 5)
            i = 0
            roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            distypes.append(roww)
            # print(roww)
            newroww = [diseasename, disetype, color, newefficacy2010, newefficacy2013, newcoverage2010, newcoverage2013,
                       p]
            conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
            conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', newroww)
            efficacy2010 = 0
            efficacy2013 = 0
            coverage2010 = 0
            coverage2013 = 0
            newefficacy2010 = 0
            newefficacy2013 = 0
            newcoverage2010 = 0
            newcoverage2013 = 0
            mark += 1
            j += 1
        cur = conn.execute(' select * from distypes where distype=? ', ('Schistosomiasis',))
        data = cur.fetchall()
        # print(data)

        i = 1
        j = 0
        mark = 0
        for k in [182, 183, 184, 185]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # dismap =[2,3,1]
            position = [3, 2, 1, 0]
            disease = ['Nodulectomy', 'Suramin', 'Ivm', 'Dec']
            disetype = 'Onchoceriasis'
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacy2010 += stripdata(k, 1)
            efficacy2013 += stripdata(k, 2)
            coverage2010 += stripdata(k, 3)
            coverage2013 += stripdata(k, 5)

            newefficacy2010 += stripdata3(k, 1)
            newefficacy2013 += stripdata3(k, 2)
            newcoverage2010 += stripdata3(k, 3)
            newcoverage2013 += stripdata3(k, 5)
            # print('==========This is Onchoceriasis=====')
            i = 0
            roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            distypes.append(roww)
            # print(roww)
            newroww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
            conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', newroww)
            efficacy2010 = 0
            efficacy2013 = 0
            coverage2010 = 0
            coverage2013 = 0
            newefficacy2010 = 0
            newefficacy2013 = 0
            newcoverage2010 = 0
            newcoverage2013 = 0
            mark += 1
            j += 1
        cur = conn.execute(' select * from distypes where distype=? ', ('Onchoceriasis',))
        data = cur.fetchall()
        # print(data)

        i = 1
        j = 0
        mark = 0
        for k in [187, 188, 189]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # dismap =[2,3,1]
            position = [2, 1, 0]
            disease = ['Dec', 'Dec + Alb', 'Ivm + Alb']
            disetype = 'LF'
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacy2010 += stripdata(k, 1)
            efficacy2013 += stripdata(k, 2)
            coverage2010 += stripdata(k, 3)
            coverage2013 += stripdata(k, 5)
            # print('==========This is LF=====')
            newefficacy2010 += stripdata3(k, 1)
            newefficacy2013 += stripdata3(k, 2)
            newcoverage2010 += stripdata3(k, 3)
            newcoverage2013 += stripdata3(k, 5)
            i = 0
            roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            distypes.append(roww)
            # print(roww)
            newroww = [diseasename, disetype, color, newefficacy2010, newefficacy2013, newcoverage2010, newcoverage2013,
                       p]
            conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
            conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', newroww)
            efficacy2010 = 0
            efficacy2013 = 0
            coverage2010 = 0
            coverage2013 = 0
            newefficacy2010 = 0
            newefficacy2013 = 0
            newcoverage2010 = 0
            newcoverage2013 = 0
            mark += 1
            j += 1
        cur = conn.execute(' select * from distypes where distype=? ', ('LF',))
        data = cur.fetchall()

        conn.execute('''DELETE FROM drugr2010_bkp''')
        conn.execute('''DELETE FROM drugr2013_bkp''')
        conn.execute('''DELETE FROM drugr2015_bkp''')

        conn.execute('''INSERT INTO drugr2010_bkp SELECT * FROM drugr2010''')
        conn.execute('''INSERT INTO drugr2013_bkp SELECT * FROM drugr2013''')
        conn.execute('''INSERT INTO drugr2015_bkp SELECT * FROM drugr2015''')

        conn.execute('''DELETE FROM drugr2010''')
        conn.execute('''DELETE FROM drugr2013''')
        conn.execute('''DELETE FROM drugr2015''')
        datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1560508440&single=true&output=csv'
        # datasrc = 'ORS_GlobalBurdenDisease_2010_2013.csv'
        datasrc2010B2015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1560508440&single=true&output=csv';

        df = pd.read_csv(datasrc, skiprows=1)
        df2015 = pd.read_csv(datasrc2010B2015, skiprows=1)
        is_df2015_true = df2015.notnull()
        is_df_true = df.notnull()
        drugdata = []
        drugrdata = []
        drug2010 = []
        drug2013 = []
        drug2015 = []
        perc2010 = []

        def cleanfloat(var):
            if var == '#REF!':
                var = 0
            if type(var) != float and type(var) != int:
                var = float(var.replace(',', ''))
            if var != var:
                var = 0
            return var

        for i in range(1, 39):
            drugr = []
            name = df.iloc[5, i]
            # print(name)
            drugr.append(name)
            company = df.iloc[1, i]
            # print(company)
            drugr.append(company)
            for j in range(10, 20):
                if j == 10:
                    tb1 = cleanfloat(df.iloc[8, i])
                    tb2 = cleanfloat(df.iloc[9, i])
                    tb3 = cleanfloat(df.iloc[10, i])
                    tb = [tb1, tb2, tb3]
                    temp = (tb1 + tb2 + tb3)
                    drugr.append(temp)
                elif j == 11:
                    mal1 = cleanfloat(df.iloc[11, i])
                    mal2 = cleanfloat(df.iloc[12, i])
                    mal = [mal1, mal2]
                    temp = (mal1 + mal2)
                    drugr.append(temp)
                elif j == 19:
                    total = cleanfloat(df.iloc[j + 1, i])
                    zz = [name, total]
                    perc2010.append(zz)
                else:
                    temp = df.iloc[j + 1, i]
                    if isinstance(temp, float) == False and isinstance(temp, int) == False:
                        temp = float(temp.replace(',', ''))
                    if temp != temp:
                        temp = 0
                    drugr.append(temp)
                if int(temp) > 0:
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
                    company = df.iloc[1, i]
                    drugrow = [name, company, disease, temp, color]
                    drug2010.append(drugrow)

            if isinstance(df.iloc[20, i], float) == False:
                score = float(df.iloc[20, i].replace(',', ''))
            else:
                score = df.iloc[20, i]
            row = [name, score]
            drugdata.append(row)
            drugrdata.append(drugr)

        unmet = ['Unmet Need', 'Unmet Need']
        unmetsum = 0
        for xx in [[8, 9, 10], [11, 12], [13], [14], [15], [16], [17], [18], [19]]:
            val = 0
            for yy in xx:
                t = df.iloc[yy, 42]
                if isinstance(t, float) == False and isinstance(t, int) == False:
                    t = float(t.replace(',', ''))
                if t != t:
                    t = 0
                val += t
            unmet.append(val)
            unmetsum += val
        # print(unmet)
        # print(drugrdata[0])
        drugrdata.append(unmet)

        for row in drugrdata:
            tot = sum(row[2:])
            row.append(tot)
            conn.execute('insert into drugr2010 values (?,?,?,?,?,?,?,?,?,?,?,?)', row)

        drugdata = []
        drugrdata = []
        perc2013 = []

        for i in range(45, 89):
            drugr = []
            name = df.iloc[5, i]
            # print(name)
            drugr.append(name)
            company = df.iloc[1, i]
            drugr.append(company)
            # print(company)
            for j in range(10, 20):
                if j == 10:
                    tb1 = cleanfloat(df.iloc[8, i])
                    tb2 = cleanfloat(df.iloc[9, i])
                    tb3 = cleanfloat(df.iloc[10, i])
                    tb = [tb1, tb2, tb3]
                    temp = (tb1 + tb2 + tb3)
                    drugr.append(temp)
                elif j == 11:
                    mal1 = cleanfloat(df.iloc[11, i])
                    mal2 = cleanfloat(df.iloc[12, i])
                    mal = [mal1, mal2]
                    temp = (mal1 + mal2)
                    drugr.append(temp)
                elif j == 19:
                    total = cleanfloat(df.iloc[j + 1, i])
                    zz = [name, total]
                    perc2013.append(zz)
                else:
                    temp = df.iloc[j + 1, i]
                    if isinstance(temp, float) == False and isinstance(temp, int) == False:
                        temp = float(temp.replace(',', ''))
                    if temp != temp:
                        temp = 0
                    drugr.append(temp)
                if int(temp) > 0:
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
                    company = df.iloc[1, i]
                    drugrow = [name, company, disease, temp, color]
                    drug2013.append(drugrow)

            if isinstance(df.iloc[20, i], float) == False:
                score = float(df.iloc[20, i].replace(',', ''))
            else:
                score = df.iloc[20, i]
            row = [name, score]
            drugdata.append(row)
            drugrdata.append(drugr)

        unmet = ['Unmet Need', 'Unmet Need']
        unmetsum = 0
        for xx in [[8, 9, 10], [11, 12], [13], [14], [15], [16], [17], [18], [19]]:
            val = 0
            for yy in xx:
                t = df.iloc[yy, 92]
                if isinstance(t, float) == False and isinstance(t, int) == False:
                    t = float(t.replace(',', ''))
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

        drugrdata = []
        perc2015 = []
        for i in range(45, 88):
            drugr = []
            name = df2015.iloc[4, i]
            drugr.append(name)
            company = df2015.iloc[0, i]
            if is_df2015_true.iloc[0, i] == True:
                temp_comp = company
            else:
                company = temp_comp
            drugr.append(company)
            for j in range(11, 20):
                if j == 11:
                    tb1 = cleanfloat(df2015.iloc[7, i])
                    tb2 = cleanfloat(df2015.iloc[8, i])
                    tb3 = cleanfloat(df2015.iloc[9, i])
                    tb = [tb1, tb2, tb3]
                    temp = (tb1 + tb2 + tb3)
                    drugr.append(temp)
                elif j == 12:
                    mal1 = cleanfloat(df2015.iloc[10, i])
                    mal2 = cleanfloat(df2015.iloc[11, i])
                    mal = [mal1, mal2]
                    temp = (mal1 + mal2)
                    drugr.append(temp)
                elif j == 20:
                    total = cleanfloat(df2015.iloc[j, i])
                    zz = [name, total]
                    perc2015.append(zz)
                else:
                    temp = df2015.iloc[j - 1, i]
                    if isinstance(temp, float) == False and isinstance(temp, int) == False:
                        temp = float(temp.replace(',', ''))
                    if temp != temp:
                        temp = 0
                    drugr.append(temp)
                if int(temp) > 0:
                    if j == 11:
                        disease = 'TB'
                        color = 'FFB31C'
                    elif j == 12:
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
                    company = df2015.iloc[1, i]
                    drugrow = [name, company, disease, temp, color]
                    drug2015.append(drugrow)

            if isinstance(df2015.iloc[20, i], float) == False:
                score = float(df2015.iloc[20, i].replace(',', ''))
            else:
                score = df2015.iloc[20, i]
            row = [name, score]
            drugdata.append(row)
            drugrdata.append(drugr)

        unmet = ['Unmet Need', 'Unmet Need']
        unmetsum = 0
        for xx in [[7, 8, 9], [10, 11], [12], [13], [14], [15], [16], [17], [18]]:
            val = 0
            for yy in xx:
                t = df2015.iloc[yy, 91]
                if isinstance(t, float) == False and isinstance(t, int) == False:
                    t = float(t.replace(',', ''))
                if t != t:
                    t = 0
                val += t
            unmet.append(val)
            unmetsum += val
        drugrdata.append(unmet)
        sortedlist = sorted(drug2015, key=lambda xy: xy[3], reverse=True)

        for row in drugrdata:
            tot = sum(row[2:])
            row.append(tot)
            conn.execute('insert into drugr2015 values (?,?,?,?,?,?,?,?,?,?,?,?)', row)
        perc2015.sort(key=lambda x: x[1], reverse=True)
        conn.commit()
        print ("Completed Update")

    except Exception as e:
        error = str(e)
        conn.rollback()
        return render_template('accountF.html', error = error ,  showthediv=0)
    return render_template('accountS.html', showthediv=0)

if __name__ == '__main__':
    app.run(debug=False)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)

@app.errorhandler(500)
def internal_error_500(e):
    return render_template('error500.html',showindex=1, navsub=1), 500