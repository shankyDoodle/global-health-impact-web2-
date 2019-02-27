import sqlite3
import pandas as pd
import math
conn = sqlite3.connect('ghi.db')


conn.execute('''DROP TABLE IF EXISTS country2010_bkp''')
conn.execute('''DROP TABLE IF EXISTS country2013_bkp''')
conn.execute('''DROP TABLE IF EXISTS country2015_bkp''')
conn.execute('''DROP TABLE IF EXISTS countrybydis2010_bkp''')
conn.execute('''DROP TABLE IF EXISTS countrybydis2013_bkp''')
conn.execute('''DROP TABLE IF EXISTS countryp2010_bkp''')
conn.execute('''DROP TABLE IF EXISTS countryp2013_bkp''')
conn.execute('''DROP TABLE IF EXISTS countryp2015_bkp''')


conn.execute('''DROP TABLE IF EXISTS disbars_bkp''')
conn.execute('''DROP TABLE IF EXISTS disbars2010B2015_bkp''')
conn.execute('''DROP TABLE IF EXISTS disease2010_bkp''')
conn.execute('''DROP TABLE IF EXISTS disease2013_bkp''')
conn.execute('''DROP TABLE IF EXISTS disease2015_bkp''')
conn.execute('''DROP TABLE IF EXISTS diseaseall2010_bkp''')
conn.execute('''DROP TABLE IF EXISTS diseaseall2013_bkp''')
conn.execute('''DROP TABLE IF EXISTS diseaseall2015_bkp''')
conn.execute('''DROP TABLE IF EXISTS distypes_bkp''')
conn.execute('''DROP TABLE IF EXISTS distypes2010B2015_bkp''')

conn.execute('''DROP TABLE IF EXISTS drugr2010_bkp''')
conn.execute('''DROP TABLE IF EXISTS drugr2013_bkp''')
conn.execute('''DROP TABLE IF EXISTS drugr2015_bkp''')

conn.execute('''DROP TABLE IF EXISTS manudis_bkp''')
conn.execute('''DROP TABLE IF EXISTS manudis2015_bkp''')
conn.execute('''DROP TABLE IF EXISTS manutot_bkp''')
conn.execute('''DROP TABLE IF EXISTS manutot2015_bkp''')


conn.execute('''DROP TABLE IF EXISTS patent2010_bkp''')
conn.execute('''DROP TABLE IF EXISTS patent2013_bkp''')
conn.execute('''DROP TABLE IF EXISTS patent2015_bkp''')

conn.execute('''CREATE TABLE country2010_bkp
             (country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf)''')
conn.execute('''CREATE TABLE country2013_bkp
             (country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchoceriasis, lf)''')
conn.execute('''CREATE TABLE country2015_bkp
             (country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchoceriasis, lf)''')
conn.execute('''CREATE TABLE countrybydis2010_bkp
             (country, tb, malaria, hiv, roundworm, hookworm, whipworm, schis, onch, lf)''')
conn.execute('''CREATE TABLE countrybydis2013_bkp
             (country, tb, malaria, hiv, roundworm, hookworm, whipworm, schis, onch, lf)''')
conn.execute('''CREATE TABLE countryp2010_bkp
             (country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis, lf)''')
conn.execute('''CREATE TABLE countryp2013_bkp
             (country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchoceriasis, lf)''')
conn.execute('''CREATE TABLE countryp2015_bkp
             (country, total, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchoceriasis, lf)''')



conn.execute('''CREATE TABLE disbars_bkp
             (disease, color, efficacy2010, efficacy2013, coverage2010, coverage2013, need2010, need2013)''')
conn.execute('''CREATE TABLE disbars2010B2015_bkp
             (disease, color, efficacy2010, efficacy2015, coverage2010, coverage2015, need2010, need2015)''')
conn.execute('''CREATE TABLE disease2010_bkp
             (disease, distype, impact, daly, need, color)''')
conn.execute('''CREATE TABLE disease2013_bkp
             (disease, distype, impact, daly, need, color)''')
conn.execute('''CREATE TABLE disease2015_bkp
             (disease, distype, impact, daly, need, color)''')
conn.execute('''CREATE TABLE diseaseall2010_bkp
             (country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf)''')
conn.execute('''CREATE TABLE diseaseall2013_bkp
             (country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf)''')
conn.execute('''CREATE TABLE diseaseall2015_bkp
             (country, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf)''')
conn.execute('''CREATE TABLE distypes_bkp
             (disease, distype, color, efficacy2010,efficacy2013,coverage2010,coverage2013,position)''')
conn.execute('''CREATE TABLE distypes2010B2015_bkp
             (disease, distype, color, efficacy2010,efficacy2015,coverage2010,coverage2015,position)''')



conn.execute('''CREATE TABLE drugr2010_bkp
             (drug, company, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf, total)''')
conn.execute('''CREATE TABLE drugr2013_bkp
             (drug, company, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf, total)''')
conn.execute('''CREATE TABLE drugr2015_bkp
             (drug, company, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf, total)''')



conn.execute('''CREATE TABLE manudis_bkp
             (company, disease,daly2010,daly2013,color)''')
conn.execute('''CREATE TABLE manudis2015_bkp
             (company, disease,daly2010B,daly2015,color)''')
conn.execute('''CREATE TABLE manutot2015_bkp
             (company, daly2010B,daly2015,color)''')
conn.execute('''CREATE TABLE manutot_bkp
             (company,daly2010,daly2013,color)''')


conn.execute('''CREATE TABLE patent2010_bkp
             ( company, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf, total, color)''')
conn.execute('''CREATE TABLE patent2013_bkp
             ( company, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf, total, color)''')
conn.execute('''CREATE TABLE patent2015_bkp
             ( company, tb, malaria, hiv, roundworm, hookworm, whipworm, schistosomiasis,onchocerciasis, lf, total, color)''')

conn.commit()
print("Database operation complete")