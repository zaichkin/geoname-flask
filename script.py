# -*- coding: utf-8 -*-

import sqlite3
from flask import request
from flask import Flask
from flask import jsonify
import pytz
from datetime import datetime

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

alphabet = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о",
            "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]


@app.route('/getbyid/<int:id>', methods=['GET'])
def geoname(id):
    conn = sqlite3.connect('RU.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM geoname WHERE geonameid = {id}")
    return jsonify(cur.fetchall())

@app.route('/getpage/<int:page>/<int:number>', methods=['GET'])
def getgeoname(page, number):
    conn = sqlite3.connect('RU.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM geoname LIMIT {(page - 1) * number}, {number}")
    return jsonify(cur.fetchall())

@app.route(u'/compare/<string:city1>/<string:city2>', methods=['GET'])
def compare(city1, city2):
    conn = sqlite3.connect('RU.db')
    cur = conn.cursor()
    fin = []

    cur.execute(f"SELECT * FROM geoname  WHERE alternatenames LIKE '{city1}' ORDER BY population DESC LIMIT 1")
    ct1 = cur.fetchall()[0]
    cur.execute(f"SELECT * FROM geoname  WHERE alternatenames LIKE '{city2}' ORDER BY population DESC LIMIT 1")
    ct2 = cur.fetchall()[0]

    if ct1[4] > ct2[4]:
        nrt = ct1[1]
    else:
        nrt = ct2[1]

    fin.append(ct1)
    fin.append(ct2)

    tz1 = datetime.now(pytz.timezone(ct1[17]))
    tz2 = datetime.now(pytz.timezone(ct2[17]))

    fin.append((f"Город {nrt} находится севернее", f"Временная разница UTC + {abs(int(str(tz1)[27:29])-int(str(tz2)[27:29]))}"))

    return  jsonify(fin)

@app.route('/find/<string:city1>', methods=['GET'])
def helper(city1):
    conn = sqlite3.connect('RU.db')
    cur = conn.cursor()
    cur.execute(f"SELECT alternatenames FROM geoname WHERE alternatenames LIKE '%{city1}%'")
    lst = cur.fetchall()
    hv = []
    for tp in lst:
        for line in tp:
            p = line.split(',')
            for t in p:
                g = 0
                for s in t:
                    if bool(set(alphabet).intersection(set(s.lower()))) or s ==' ':
                        g+=1
                    if (len(t) == g) and (t.find(city1) != -1):
                        hv.append(t)

    return jsonify(hv)


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8000)
