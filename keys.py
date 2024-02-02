import pickle
from pathlib import Path
import streamlit_authenticator as stauth

names = ["Vijay Kumar","Suresh Fatehpuria"]
usernames = ["vkumar","sfatehpuria"]
passwords = ["vijay@123","suresh@123"]
user_type = [[1,3],[1,2]]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)