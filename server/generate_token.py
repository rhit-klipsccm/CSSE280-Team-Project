import os

from google_auth import generate_new_token

if os.path.exists('./token.pickle'):
    os.remove('./token.pickle')

generate_new_token()

print("Generated fresh token.pickle")