from flask import Flask, send_file
from google.cloud import storage
import io

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Download files from GCS - go to /dl'

@app.route('/dl1')
def dl_file1():
    filename = '50MB.zip'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('buck-dl-ap')
    blob = bucket.blob(filename)
    return send_file(io.BytesIO(blob.download_as_string()), mimetype="application/octet-stream", as_attachment=True, attachment_filename=filename)

@app.route('/dl2')
def dl_file2():
    filename = '50MB.zip'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('buck-dl-ap')
    blob = bucket.blob(filename)
    return send_file(blob.download_to_filename(filename), mimetype='application/octet-stream', as_attachment=True, attachment_filename=filename)

@app.route('/dl3')
def download_blob():
    storage_client = storage.Client()
    bucket_name = 'buck-dl-ap'
    source_blob_name = '50MB.zip'
    destination_file_name = 'download_ok'

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
