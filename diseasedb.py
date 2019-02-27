import sqlite3
import pandas as pd

def CreateDiseae():
    #conn = sqlite3.connect('F:/global-health-impact-web/ghi.db')
    conn = sqlite3.connect('/home/globalhealth/mysite/ghi.db')
    conn.execute('''DROP TABLE IF EXISTS disease2010''')
    conn.execute('''DROP TABLE IF EXISTS disease2013''')
    conn.execute('''DROP TABLE IF EXISTS disease2015''')
    conn.execute('''DROP TABLE IF EXISTS disbars''')
    conn.execute('''DROP TABLE IF EXISTS distypes''')
    conn.execute('''DROP TABLE IF EXISTS disbars2010B2015''')
    conn.execute('''DROP TABLE IF EXISTS distypes2010B2015''')

    conn.execute('''CREATE TABLE disease2013
                (disease text, distype text, impact real, daly real, need text, color text)''')

    conn.execute('''CREATE TABLE disease2010
                (disease text, distype text, impact real, daly real, need text, color text)''')

    conn.execute('''CREATE TABLE disease2015
                (disease text, distype text, impact real, daly real, need text, color text)''')

    conn.execute('''CREATE TABLE disbars
               (disease text, color text, efficacy2010 real, efficacy2013 real, coverage2010 real, coverage2013 real, need2010 real, need2013 real)''')

    conn.execute('''CREATE TABLE distypes
               (disease text,distype text, color text, efficacy2010 real, efficacy2013 real, coverage2010 real, coverage2013 real,position real)''')

    conn.execute('''CREATE TABLE disbars2010B2015
               (disease text, color text, efficacy2010 real, efficacy2013 real, coverage2010 real, coverage2013 real, need2010 real, need2013 real)''')

    conn.execute('''CREATE TABLE distypes2010B2015
               (disease text,distype text, color text, efficacy2010 real, efficacy2013 real, coverage2010 real, coverage2013 real,position real)''')
    conn.commit()
    conn.close()

def DiseaseDbUpdate():
    try:
        #conn = sqlite3.connect('F:/global-health-impact-web/ghi.db')
        conn = sqlite3.connect('/home/globalhealth/mysite/ghi.db')
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
            temp = df.iloc[k, 44]
            print(temp)
            temp1 = df.iloc[k, 46]
            print(temp1)
            temp2 = df.iloc[k, 47]
            print(temp2)
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
            temp = df.iloc[k, 95]
            temp1 = df.iloc[k, 97]
            temp2 = df.iloc[k, 98]
            print(temp)
            print(temp1)
            print(temp2)
            print(distype)
            print(disease)
            if type(temp) != float and type(temp1) != float and type(temp2) != float:
                impact = float(temp.replace(',', ''))
                daly = float(temp1.replace(',', ''))
                need = float(temp2.replace(',', ''))
                i += 1
                row = [disease, distype, impact, daly, need, color]
                disease2013db.append(row)
                conn.execute('insert into disease2013 values (?,?,?,?,?,?)', row)
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
            temp = df_2010B_2015.iloc[k, 95]
            temp1 = df_2010B_2015.iloc[k, 97]
            temp2 = df_2010B_2015.iloc[k, 98]
            print(temp)
            print(temp1)
            print(temp2)
            print(distype)
            print(disease)
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
                if tmp == "#DIV/0!" or tmp == "nan":
                    return (0)
                if tmp == 'No Data':
                    return (0)
                if isinstance(tmp, float) == False:
                    return (float(tmp.replace(',', '').replace(' ', '0').replace('%', '')))
                else:
                    return (0)
            except:
                return 0


        def stripdata3(x, y):
            try:
                tmp = df_2010B_2015.iloc[x, y]
                if tmp == "#DIV/0!" or tmp == "nan" or tmp == "#REF!":
                    return (0)
                if tmp == 'No Data':
                    return (0)
                if isinstance(tmp, float) == False:
                    return (float(tmp.replace(',', '').replace(' ', '0').replace('%', '')))
                else:
                    return (0)
            except:
                return 0


        def stripdata2(x, y):
            tmp = df2.iloc[x, y]
            if tmp == "#DIV/0!" or tmp == "nan" or tmp == "#REF!":
                return (0)
            if tmp == 'No Data':
                return (0)
            if isinstance(tmp, float) == False:
                res = float(tmp.replace(',', '').replace(' ', '0').replace('%', ''))
                if res > 10000:
                    res = res * 0.00001
                # print(res)
                return (0.01 * res)
            else:
                return (0)

        disbars = []
        j = 0
        for k in range(104, 113):
            colors = ['#FFB31C', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            diseasename = df.iloc[k, 7]
            color = colors[j]
            efficacy2010 = stripdata(k, 8)
            efficacy2013 = stripdata(k, 9)
            coverage2010 = stripdata(k, 10)
            coverage2013 = stripdata(k, 11)
            need2010 = stripdata(k, 12)
            need2013 = stripdata(k, 13)
            roww = [diseasename, color, efficacy2010, efficacy2013, coverage2010, coverage2013, need2010, need2013]
            disbars.append(roww)
            j += 1
            conn.execute('insert into disbars values (?,?,?,?,?,?,?,?)', roww)

        disbars = []
        j = 0
        for k in range(104, 113):
            colors = ['#FFB31C', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            newdiseasename = df_2010B_2015.iloc[k, 7]
            color = colors[j]
            newefficacy2010 = stripdata3(k, 8)
            newefficacy2013 = stripdata3(k, 9)
            newcoverage2010 = stripdata3(k, 10)
            newcoverage2013 = stripdata3(k, 11)
            newneed2010 = stripdata3(k, 12)
            newneed2013 = stripdata3(k, 13)
            newroww = [newdiseasename, color, newefficacy2010, newefficacy2013, newcoverage2010, newcoverage2013,
                       newneed2010, newneed2013]
            j += 1
            disbars.append(newroww)
            conn.execute('insert into disbars2010B2015 values (?,?,?,?,?,?,?,?)', newroww)

        def doStuff(k, i, m, mark, diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013,
                    p, year):
            if disetype == 'TB' or disetype == 'Malaria':
                efficacy2010 /= m
                efficacy2013 /= m
                coverage2010 /= m
                coverage2013 /= m
            roww = [diseasename, disetype, color, efficacy2010, efficacy2013, coverage2010, coverage2013, p]
            print(roww)
            if year == 2010:
                conn.execute('insert into distypes values (?,?,?,?,?,?,?,?)', roww)
            elif year == 2015:
                conn.execute('insert into distypes2010B2015 values (?,?,?,?,?,?,?,?)', roww)

        efficacyone = 0
        efficacytwo = 0
        coverageone = 0
        coveragetwo = 0
        i = 1
        j = 0
        mark = 0
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
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            if i == m:
                doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo,
                        p,
                        year)
                i = 0
                mark += 1
                efficacyone = 0
                efficacytwo = 0
                coverageone = 0
                coveragetwo = 0
            i += 1
            j += 1

        i = 1
        j = 0
        mark = 0
        for k in [107, 109,111, 112, 113, 115]:
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
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            if i == m:
                doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo,
                        p,
                        year)
                i = 0
                mark += 1
                efficacyone = 0
                efficacytwo = 0
                coverageone = 0
                coveragetwo = 0
            i += 1
            j += 1

        i = 1
        j = 0
        mark = 0
        for k in [117, 118, 119, 120, 121, 122, 124]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            dismap = [6, 1]
            position = [0, 1]
            disease = ['p. falc Malaria', 'p. vivax Malaria']
            disetype = 'Malaria'
            m = dismap[mark]
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            if i == m:
                doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo,
                        p,
                        year)
                i = 0
                mark += 1
                efficacyone = 0
                efficacytwo = 0
                coverageone = 0
                coveragetwo = 0
            i += 1
            j += 1

        i = 1
        mark = 0
        for k in [117, 118, 119, 120, 121, 122, 124]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            dismap = [6, 1]
            position = [0, 1]
            disease = ['p. falc Malaria', 'p. vivax Malaria']
            disetype = 'Malaria'
            m = dismap[mark]
            p = position[mark]
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            if i == m:
                doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo,
                        p,
                        year)
                i = 0
                mark += 1
                efficacyone = 0
                efficacytwo = 0
                coverageone = 0
                coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [160]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disease = ['Roundworm']
            disetype = 'Roundworm'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [160]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disease = ['Roundworm']
            disetype = 'Roundworm'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [164]:

            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disease = ['Hookworm']
            disetype = 'Hookworm'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [158]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disease = ['Hookworm']
            disetype = 'Hookworm'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [167]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disease = ['Whipworm']
            disetype = 'Whipworm'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [161]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Alb', 'Mbd', 'Ivm + Alb', 'Dec + Alb', 'Pzq + Alb', 'Pzq + Mbd']
            disease = ['Whipworm']
            disetype = 'Whipworm'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [171]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Ivm + Alb', 'Dec + Alb', 'Pzq', 'Ivm', 'Dec', 'Alb']
            disease = ['Schistosomiasis', 'Dec + Alb',
+                       'Pzq', 'Ivm', 'Dec', 'Alb']
            disetype = 'Schistosomiasis'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [165]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Ivm + Alb', 'Dec + Alb', 'Pzq', 'Ivm', 'Dec', 'Alb']
            disease = ['Schistosomiasis', 'Dec + Alb','Pzq', 'Ivm', 'Dec', 'Alb']
            disetype = 'Schistosomiasis'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [173]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Nodulectomy', 'Suramin', 'Ivm', 'Dec']
            disetype = 'Onchoceriasis'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [167]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Nodulectomy', 'Suramin', 'Ivm', 'Dec']
            disetype = 'Onchoceriasis'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [175]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            # disease = ['Dec', 'Dec + Alb', 'Ivm + Alb']
            disease = ['LF']
            disetype = 'LF'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata(k, 1)
            efficacytwo += stripdata(k, 2)
            coverageone += stripdata(k, 3)
            coveragetwo += stripdata(k, 5)
            year = 2010
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1

        i = 1
        mark = 0
        for k in [169]:
            colors = ['#FFB31C', '#FFB31C', '#FFB31C', '#0083CA', '#0083CA', '#EF3E2E', '#003452', '#86AAB9', '#CAEEFD',
                      '#546675', '#8A5575', '#305516']
            disease = ['LF']
            disetype = 'LF'
            m = 0
            p = 0
            color = colors[j % 12]
            diseasename = disease[mark]
            efficacyone += stripdata3(k, 1)
            efficacytwo += stripdata3(k, 2)
            coverageone += stripdata3(k, 3)
            coveragetwo += stripdata3(k, 5)
            year = 2015
            doStuff(k, i, m, mark, diseasename, disetype, color, efficacyone, efficacytwo, coverageone, coveragetwo, p,
                    year)
            i = 0
            mark += 1
            efficacyone = 0
            efficacytwo = 0
            coverageone = 0
            coveragetwo = 0
            i += 1
        conn.commit()
        conn.close()
        return 'success'
    except Exception as e:
        error = "Disease page not updated"
        conn.rollback()
        conn.close()
        return error