import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import datetime

# Fetch the service account key JSON file contents
cred = credentials.Certificate("firebase_private_key.json")

# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'projectmanagement-3e8a8.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)
blobs = bucket.list_blobs(prefix="DESKTOP-3S7MM6C")
img_url = []
for blob in blobs:
    img_url.append(blob.generate_signed_url(datetime.timedelta(seconds=100000), method='GET'))
# blob2 = bucket.blob('')
print(img_url)
# print(blob.generate_signed_url(datetime.timedelta(seconds=1000), method='GET'))
# print(blob)
