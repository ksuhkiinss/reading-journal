import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import altair as alt

st.set_page_config(page_title="Мої читалочки", page_icon="📚")

# --- Підключення до бази ---
conn = sqlite3.connect('reading_journal.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS books
             (id INTEGER PRIMARY KEY, title TEXT, status TEXT, date_added DATE)''')
c.execute('''CREATE TABLE IF NOT EXISTS logs
             (id INTEGER PRIMARY KEY, book_title TEXT, pages INTEGER, minutes INTEGER, date_logged DATE)''')
conn.commit()
conn.close()

st.title("📚 Мої книги")
st.write("Це твій Streamlit-щоденник книг!")
