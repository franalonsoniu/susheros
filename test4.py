import psycopg2
import streamlit as st


import psycopg2
import streamlit as st

if "logs" not in st.session_state:
    st.session_state.logs = []

# Function to validate psycopg2 connection
def validate_connection(conn):
    try:
        # Check if connection is valid
        # by executing a simple query
        with conn.cursor() as curs:
            curs.execute("SELECT 1")
            curs.fetchone()
    except:
        st.session_state.logs.append("Connection lost. Reconnecting...")
        # Connection is invalid, invalidate cache
        return False
    return True # Connection is valid, don't invalidate cache

# Get connection parameters
dbname= 'niu_db'
host='niu-bi.cdx4hhfxpr2j.us-east-1.rds.amazonaws.com'
port= '5432'
user= 'niufoods'
password= 'J9SsTO8PHfQZtg6K'

# Initialize connection
# Connection will be reinitialized if validation function returns False.
@st.experimental_singleton(validate=validate_connection)
def init_connection():
    # Connect to the database
    conn = psycopg2.connect(
        host=host,
        dbname=dbname,
        port=port,
        user=user,
        password=password,
    )
    return conn

conn = init_connection()

# Create a cursor object
cursor = conn.cursor()

# Execute query
cursor.execute("SELECT * FROM susheros_app where filter_date  >=  CURRENT_DATE - INTERVAL '3 months'")

# Fetch data
data = cursor.fetchall()

# Append to logs
st.session_state.logs.append("Data fetched successfully.")

# Create a Dataframe
st.dataframe(data)

# Display logs
st.write(st.session_state.logs)

# Checkbox to close connection
if st.checkbox("Close connection"):
    cursor.close()
    conn.close()
    st.session_state.logs.append("Connection closed.")

st.button("Rerun")
