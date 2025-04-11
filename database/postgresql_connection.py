import psycopg2
import streamlit as st

def init_postgres_connection_local():
    """
    Initializes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",  # Replace with your PostgreSQL host
            database="Bays_Mountain",  # Replace with your PostgreSQL database name
            user="bays_owner",  # Replace with your PostgreSQL username
            password="B@V5"  # Replace with your PostgreSQL password
        )
        return conn
    except Exception as e:
        print("Error connecting to the PostgreSQL database:", e)
        raise


def init_postgres_connection():
    """
    Initializes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host=st.secrets["host"],  # Replace with your PostgreSQL host
            port=st.secrets["port"],
            database=st.secrets["database"],  # Replace with your PostgreSQL database name
            user=st.secrets["user"],  # Replace with your PostgreSQL username
            password= st.secrets["auth_key"]
        )
        return conn
    except Exception as e:
        print("Error connecting to the PostgreSQL database:", e)
        raise
