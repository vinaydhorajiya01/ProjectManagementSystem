import firebase_admin
from firebase_admin import auth, credentials

# Initialize Firebase app
cred = credentials.Certificate('firebase_private_key.json')
firebase_admin.initialize_app()

# Get the user's UID
user = auth.get_user_by_email('sunny@gmail.com')
uid = user.uid

# Update the user's password
auth.update_user(
    uid,
    password='1234567'
)
