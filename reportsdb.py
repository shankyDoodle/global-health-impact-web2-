import sqlite3
import pandas as pd
import math
conn = sqlite3.connect('ghi.db')

conn.execute('''DROP TABLE IF EXISTS reports2010''')
conn.execute('''DROP TABLE IF EXISTS reportsdetail2010''')
conn.execute('''DROP TABLE IF EXISTS reports2013''')
conn.execute('''DROP TABLE IF EXISTS reportsdata2013''')

conn.execute(
    ''' CREATE TABLE reports2010 (id, year, company name, total impact score, rank overall, number of diseases) ''')

conn.execute(
    ''' CREATE TABLE reportsdetail2010 (id, year, company name, drug, disease target, individual impact) ''')


conn.execute(
    ''' CREATE TABLE reports2013 (company name, total impact score, rank overall, number of diseases,drug) ''')

datasrc = 'ORS_Reports.csv'
df = pd.read_csv(datasrc)
is_df_true = df.notnull()
#print(df)

def cleanfloat(var):
    #print(var)
    if var == '#REF!':
        var = 0
    if var == '#DIV/0!' or var == 'No data':
        var = 0
    if type(var) != float and type(var) != int:
        var = float(var.replace(',', '').replace('%', ''))
    if var != var:
        var = 0
    return var

reports2010 = []
reportsdetail2010 = []
reports2013 = []
reportsdata2013 = []

id = 0;
for k in range(0, 44):
    if is_df_true.iloc[k, 1] == True:
        companyname = df.iloc[k, 1]
        print(companyname)
    if is_df_true.iloc[k, 2] == True:
        totalimpactscore = cleanfloat(df.iloc[k, 2])
        print(totalimpactscore)
    if is_df_true.iloc[k, 3] == True:
        companyrank = cleanfloat(df.iloc[k, 3])
        print(companyrank)
    if is_df_true.iloc[k, 4] == True:
        numOfDisease = cleanfloat(df.iloc[k, 4])
        print(numOfDisease)
    if is_df_true.iloc[k, 1] == True and is_df_true.iloc[k, 2] == True and  is_df_true.iloc[k, 3] == True and  is_df_true.iloc[k, 4] == True:
        id = id+1
        row = [id, 2010, companyname, totalimpactscore, companyrank, numOfDisease]
        reports2010.append(row)

for item in reports2010:
    print(item)
    conn.execute(' insert into reports2010 values (?,?,?,?,?,?) ', item)

_id = 0;
tempcompanyname = ""
for k in range(0, 44):
    companyname = df.iloc[k,1]
    if is_df_true.iloc[k, 1] == False:
        companyname = tempcompanyname
    else:
        _id = _id + 1;
        tempcompanyname = companyname
    print(tempcompanyname)
    print(companyname)
    drug = df.iloc[k, 5]
    print(drug)
    diseaseTargeted = df.iloc[k, 6]
    print(diseaseTargeted)
    individualImpactScore = cleanfloat(df.iloc[k, 7])
    print(individualImpactScore)
    rowdata = [_id, 2010, companyname, drug, diseaseTargeted, individualImpactScore]
    reportsdetail2010.append(rowdata)

for item in reportsdetail2010:
    print(item)
    conn.execute(' insert into reportsdetail2010 values (?,?,?,?,?,?) ', item)




conn.commit()
print("Database operation complete")