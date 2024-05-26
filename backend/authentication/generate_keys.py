import pickle
from pathlib import Path

import streamlit as st

from streamlit_authenticator.utilities.hasher import Hasher

names = ["Berkay Dik", "Leonardo Rodriguez"]
usernames = ["berk", "leo"]
passwords = ["abc123","def456"]

hashed_passwords = Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"

with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)