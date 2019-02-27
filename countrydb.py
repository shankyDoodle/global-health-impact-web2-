import sqlite3
import pandas as pd
import unicodedata

def createTablesCountry():
    conn = sqlite3.connect('/home/globalhealth/mysite/ghi.db')

    conn.execute(''' DROP TABLE IF EXISTS country2010 ''')
    conn.execute(''' DROP TABLE IF EXISTS country2013 ''')
    conn.execute(''' DROP TABLE IF EXISTS country2015 ''')
    conn.execute(''' DROP TABLE IF EXISTS countryp2010 ''')
    conn.execute(''' DROP TABLE IF EXISTS countryp2013 ''')
    conn.execute(''' DROP TABLE IF EXISTS countryp2015 ''')
    conn.execute(
        ''' CREATE TABLE country2010 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, lf real) ''')
    conn.execute(
        ''' CREATE TABLE country2013 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchoceriasis real, lf real) ''')
    conn.execute(
        ''' CREATE TABLE country2015 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchoceriasis real, lf real) ''')

    conn.execute(
        ''' CREATE TABLE countryp2010 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, lf real) ''')
    conn.execute(
        ''' CREATE TABLE countryp2013 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchoceriasis real, lf real) ''')
    conn.execute(
        ''' CREATE TABLE countryp2015 (country text, total real, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schistosomiasis real, onchoceriasis real, lf real) ''')
    conn.close()


# url = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=0&single=true&output=csv'

# createTablesCountry()

def countrydbUpdate():
    try:

        conn = sqlite3.connect('/home/globalhealth/mysite/ghi.db')
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
        # url = 'ORS_Impact_Score_2010_2013.csv'
        # url2010B2015 = 'ORS_Impact_Score_2010B_2015.csv'
        url = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=0&single=true&output=csv'
        df = pd.read_csv(url, skiprows=1)
        url2010B2015 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=0&single=true&output=csv'
        df2015 = pd.read_csv(url2010B2015, skiprows=1)
        is_df2015_true = df2015.notnull()
        is_df_true = df.notnull()

        def clean(value):
            try:
                strVal = str(value)
                if '-' in strVal:
                    resVal = strVal.replace('-', '0')
                elif ',' in strVal:
                    resVal = strVal.replace(',', '')
                else:
                    resVal = strVal
                resVal = float(resVal)
                return resVal
            except:
                return 0

        countrydata = []
        mapp = []

        for i in range(3, 220):
            country = df.iloc[i, 0]
            #country = unicodedata.normalize('NFKD', country).encode('ascii', 'ignore')
            if is_df_true.iloc[i, 7] == True:
                tb = clean(df.iloc[i, 7])
            else:
                tb = 0
            if is_df_true.iloc[i, 31] == True:
                malaria = clean(df.iloc[i, 31])
            else:
                malaria = 0
            if is_df_true.iloc[i, 44] == True:
                hiv = clean(df.iloc[i, 44])
            else:
                hiv = 0
            if is_df_true.iloc[i, 53] == True:
                roundworm = clean(df.iloc[i, 53])
            else:
                roundworm = 0
            if is_df_true.iloc[i, 55] == True:
                hookworm = clean(df.iloc[i, 55])
            else:
                hookworm = 0
            if is_df_true.iloc[i, 56] == True:
                whipworm = clean(df.iloc[i, 56])
            else:
                whipworm = 0
            if is_df_true.iloc[i, 58] == True:
                schistosomiasis = clean(df.iloc[i, 58])
            else:
                schistosomiasis = 0
            if is_df_true.iloc[i, 61] == True:
                lf = clean(df.iloc[i, 61])
            else:
                lf = 0
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
        for i in range(3, 218):
            country = df.iloc[i, 64]
            if is_df_true.iloc[i, 71] == True:
                tb = clean(df.iloc[i, 71])
            else:
                tb = 0
            if is_df_true.iloc[i, 101] == True:
                malaria = clean(df.iloc[i, 101])
            else:
                malaria = 0
            if is_df_true.iloc[i, 113] == True:
                hiv = clean(df.iloc[i, 113])
            else:
                hiv = 0
            if is_df_true.iloc[i, 122] == True:
                roundworm = clean(df.iloc[i, 122])
            else:
                roundworm = 0
            if is_df_true.iloc[i, 123] == True:
                hookworm = clean(df.iloc[i, 123])
            else:
                hookworm = 0
            if is_df_true.iloc[i, 124] == True:
                whipworm = clean(df.iloc[i, 124])
            else:
                whipworm = 0
            if is_df_true.iloc[i, 127] == True:
                schistosomiasis = clean(df.iloc[i, 127])
            else:
                schistosomiasis = 0
            if is_df_true.iloc[i, 129] == True:
                onchoceriasis = clean(df.iloc[i, 129])
            else:
                onchoceriasis = 0
            if is_df_true.iloc[i, 132] == True:
                lf = clean(df.iloc[i, 132])
            else:
                lf = 0
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
        for i in range(3, 218):
            country = df2015.iloc[i, 64]
            if is_df2015_true.iloc[i, 71] == True:
                tb = clean(df2015.iloc[i, 71])
            else:
                tb = 0
            if is_df2015_true.iloc[i, 98] == True:
                malaria = clean(df2015.iloc[i, 98])
            else:
                malaria = 0
            if is_df2015_true.iloc[i, 109] == True:
                hiv = clean(df2015.iloc[i, 109])
            else:
                hiv = 0
            if is_df2015_true.iloc[i, 118] == True:
                roundworm = clean(df2015.iloc[i, 118])
            else:
                roundworm = 0
            if is_df2015_true.iloc[i, 119] == True:
                hookworm = clean(df2015.iloc[i, 119])
            else:
                hookworm = 0
            if is_df2015_true.iloc[i, 120] == True:
                whipworm = clean(df2015.iloc[i, 120])
            else:
                whipworm = 0
            if is_df2015_true.iloc[i, 123] == True:
                schistosomiasis = clean(df2015.iloc[i, 123])
            else:
                schistosomiasis = 0
            if is_df2015_true.iloc[i, 125] == True:
                onchoceriasis = clean(df2015.iloc[i, 125])
            else:
                onchoceriasis = 0
            if is_df2015_true.iloc[i, 128] == True:
                lf = clean(df2015.iloc[i, 128])
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
            print(country)
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
        for k in countrydata3:
            conn.execute(''' INSERT INTO country2015 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', k)

        for l in mapp2:
            conn.execute(''' INSERT INTO countryp2015 VALUES (?,?,?,?,?,?,?,?,?,?,?) ''', l)

        conn.commit()
        conn.close()
        print("Database operation compelete")
        return 'success'

    except Exception as e:
        error = e
        conn.rollback()
        conn.close()
        return error
