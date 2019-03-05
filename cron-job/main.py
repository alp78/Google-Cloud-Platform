from flask import Flask, request
from google.cloud import datastore
from google.cloud import bigquery
import random
import pymysql
import os
import string
from random import randint
import urllib.request

app = Flask(__name__)

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

bq_client = bigquery.Client()
datastore_client = datastore.Client()

TABLE="pairs.pairs"
randword = ''
randnum = ''

@app.route('/cron')
def cron_minute():
    randword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(3))
    randnum = randint(1, 9)
    cronurl = 'https://wave18-peringer.appspot.com/pairs?word={}&times={}'.format(randword, randnum)
    response = urllib.request.urlopen(cronurl)
    result = response.read()
    return result


@app.route('/pairs')
def pairs():	    
	    
    if 'word' in request.args and 'times' in request.args:
        word = request.args.get('word')
        times = request.args.get('times')
        result = word * int(times)
        
        # Create, populate and persist an entity with keyID=1234
        key = datastore_client.key('Pair', word+times)
        entity = datastore.Entity(key=key)
        entity.update({
            'Word': word,
            'Times': times,
            'Result': result,
        })
        datastore_client.put(entity)
        
        stream_to_bq(TABLE, word, times)
        save_to_cloud_sql(word, times)

        return(result)
    return ""

@app.route('/bigquery')
def query_bigquery():
    QUERY = (
    'SELECT * FROM `wave18-peringer.largecsv.Sales`'
    'WHERE Country = "Chad"'
    'LIMIT 100')
    query_job = bq_client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    res = []
    for row in rows:
        res.append(row)
    return str(res)

def stream_to_bq(table, word, times):
    rows = [
            {"word":word, "times":times}
            ]
    bq_client.insert_rows_json(table, rows)

def save_to_cloud_sql(word, times):
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('INSERT INTO pair (word, times, id) VALUES ("{}", "{}", "{}");'.format(word, times, word+str(times)))
        cnx.commit()
    cnx.close()
    return "OK"

@app.route('/selectall')
def selectall():
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

    with cnx.cursor() as cursor:
        cursor.execute('USE {};'.format(db_name))
        cursor.execute('SELECT * FROM pair;')
        result = cursor.fetchall()
    cnx.close()
    
    return str(result)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
