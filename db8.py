import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import numpy as np
import datetime
import streamlit.components.v1 as components
import calendar
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Producción Susheros", page_icon=":sushi:",layout="wide")
image = Image.open("foto.png")
t1, t3, t4, t5  = st.columns((3,4,2,1))
t5.image("foto.png")

with t3:
    st.components.v1.html('''
    <p  style="text-align: center;
               color: #31333F;
               font-family: calibri;
               font-size: 300%;
               margin: 0;
               font-weight: bold;">
    Producción Susheros 🍱</p>
    ''')


@st.experimental_singleton()
def init_connection():
    # Connect to the database
    conn = psycopg2.connect(
        host='niu-bi.cdx4hhfxpr2j.us-east-1.rds.amazonaws.com',
        dbname='niu_db',
        port='5432',
        user='niufoods',
        password='J9SsTO8PHfQZtg6K',
    )
    return conn

conn = init_connection()
cursor = conn.cursor()
cursor.execute("""SELECT *
               FROM susheros_app
               WHERE filter_date  >=  CURRENT_DATE - INTERVAL '3 months'
               ORDER BY order_date, commnad_number;""")
data = cursor.fetchall()
tb = cursor.fetchall()
tb = pd.DataFrame(tb)
cursor.close()
tb

tb['mes_correspondiente'] = tb['filter_date'].dt.month
conditions = [
                (tb['mes_correspondiente'] == 1) ,
                (tb['mes_correspondiente'] == 2) ,
                (tb['mes_correspondiente'] == 3) ,
                (tb['mes_correspondiente'] == 4) ,
                (tb['mes_correspondiente'] == 5) ,
                (tb['mes_correspondiente'] == 6) ,
                (tb['mes_correspondiente'] == 7) ,
                (tb['mes_correspondiente'] == 8) ,
                (tb['mes_correspondiente'] == 9) ,
                (tb['mes_correspondiente'] == 10) ,
                (tb['mes_correspondiente'] == 11) ,
                (tb['mes_correspondiente'] == 12) ]

values = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
          'Noviembre', 'Diciembre']
tb['month'] = np.select(conditions, values)

###############################################################################################
meses3 = pd.DataFrame(tb["month"].unique())

st.subheader('Ingrese su rut: ')

p1, p2 = st.columns((1,1))
input_rut = p1.text_input('(sin puntos ni guión, ej. 12345678k)')
dropdown_mes = p2.selectbox('Seleccione mes a consultar', meses3)

