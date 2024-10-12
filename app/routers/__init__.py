from firebase_admin import credentials, initialize_app

cred = credentials.Certificate("service-firebase.json")
initialize_app(cred)
