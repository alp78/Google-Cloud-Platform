from flask import Flask
from google.cloud import bigquery

app = Flask(__name__)

@app.route('/')
def hello_bq():
    return 'app running go to /cronbq'

@app.route('/cronbq')
def cron_job():
    client = bigquery.Client()

    bucket_name = 'cron-bq-dump'
    project = 'cron-bq-to-ds'
    dataset_id = 'words'
    table_id = 'definition'

    destination_uri = 'gs://{}/{}'.format(bucket_name, 'bq-dump-1-ap.csv')
    dataset_ref = client.dataset(dataset_id, project=project)
    table_ref = dataset_ref.table(table_id)
    extract_job = client.extract_table(
        table_ref,
        destination_uri,
        location='US')
    extract_job.result()
    
    completion_msg = 'Exported {}:{}.{} to {}'.format(project, dataset_id, table_id, destination_uri)
    
    return completion_msg

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)





