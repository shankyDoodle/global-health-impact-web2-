import sqlite3
import pandas as pd

def createTablesCountryDist():

    conn = sqlite3.connect('/home/globalhealth/mysite/ghi.db')

    conn.execute('''DROP TABLE IF EXISTS countrybydis2010''')
    conn.execute('''DROP TABLE IF EXISTS countrybydis2013''')

    conn.execute('''CREATE TABLE countrybydis2010
                 (country text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schis real, onch real, lf real)''')

    conn.execute('''CREATE TABLE countrybydis2013
                 (country text, tb real, malaria real, hiv real, roundworm real, hookworm real, whipworm real, schis real, onch real, lf real)''')
    conn.close()

#datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1996016204&single=true&output=csv'

def countryDisdbUpdate():
    try:
        
        conn = sqlite3.connect('/home/globalhealth/mysite/ghi.db')
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
        conn.execute('''DELETE FROM countrybydis2010''')
        conn.execute('''DELETE FROM countrybydis2013''')
        conn.execute('''DELETE FROM diseaseall2010''')
        conn.execute('''DELETE FROM diseaseall2013''')
        conn.execute('''DELETE FROM diseaseall2015''')
        datasrc = 'https://docs.google.com/spreadsheets/d/1IBfN_3f-dG65YbLWQbkXojUxs2PlQyo7l04Ubz9kLkU/pub?gid=1996016204&single=true&output=csv'
        df = pd.read_csv(datasrc, skiprows=1)
        datasrc3 = 'https://docs.google.com/spreadsheets/d/1vwMReqs8G2jK-Cx2_MWKn85MlNjnQK-UR3Q8vZ_pPNk/pub?gid=1996016204&single=true&output=csv'
        df_2010B_2015 = pd.read_csv(datasrc3, skiprows=1)
        is_df2015_true = df_2010B_2015.notnull()
        is_df_true = df.notnull()
        for i in range(1, 218):
            print(i)
            temprow = []
            temprow.append(df.iloc[i, 0])
            for k in range(1, 10):
                temp = df.iloc[i, k]
                if isinstance(temp, float):
                    temprow.append(0.0)
                else:
                    temprow.append(float(temp.replace(',', '').replace('-', '0')))
            print(temprow)
            conn.execute(' insert into countrybydis2010 values (?,?,?,?,?,?,?,?,?,?)', temprow)
            conn.execute(' insert into diseaseall2010 values (?,?,?,?,?,?,?,?,?,?)', temprow)

        for i in range(1, 218):
            temprow = []
            temprow.append(df.iloc[i, 11])
            for k in range(12, 21):
                temp = df.iloc[i, k]
                if isinstance(temp, float):
                    temprow.append(0.0)
                else:
                    temprow.append(float(temp.replace(',', '').replace('-', '0')))
            print(temprow)
            conn.execute(' insert into countrybydis2013 values (?,?,?,?,?,?,?,?,?,?)', temprow)
            conn.execute(' insert into diseaseall2013 values (?,?,?,?,?,?,?,?,?,?)', temprow)

        data2010B = []
        data2015 = []
        for i in range(1, 218):
            temprow = []
            temprow.append(df_2010B_2015.iloc[i, 11])
            print(temprow)
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

        conn.commit()
        conn.close()
        print("Database operation complete")
        return 'success'

    except Exception as e:
        error = "Country Dist page not updated"
        conn.rollback()
        conn.close()
        return error
