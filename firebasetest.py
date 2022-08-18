from firebase_admin import credentials,initialize_app,storage
cred=credentials.Certificate('firebase_cred.json')
initialize_app(cred,{'storageBucket':'mystore-a35b6.appspot.com'})
def upload(link):
    bucket=storage.bucket()
    blob1=bucket.blob(link)
    blob1.upload_from_filename(link)
    return blob1.public_url
