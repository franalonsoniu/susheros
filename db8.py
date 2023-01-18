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

t1, t3, t4, t5  = st.columns((2,7,1,1))
# t3.title("Producción Susheros :bento:")
t5.image("foto.png")

hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''
st.markdown(hide_img_fs, unsafe_allow_html=True)

with t3:
    st.components.v1.html('''
    <p  style="text-align: center;
               color: #31333F;
               font-family: calibri;
               font-size: 300%;
               margin: 0;
               font-weight: bold;">
    Producción Susheros 🍱</p>
    ''', height=100)

######################################### RUT e Información Personal #######################################

st.subheader('Ingrese su rut: ')
con=psycopg2.connect(dbname= 'niu_db', host='niu-bi.cdx4hhfxpr2j.us-east-1.rds.amazonaws.com', port= '5432',
                     user= 'niufoods', password= 'J9SsTO8PHfQZtg6K')
cur = con.cursor()
cur.execute("""SELECT distinct filter_date
               FROM susheros_app
               WHERE filter_date  >=  CURRENT_DATE - INTERVAL '3 months'
               ;""")

meses3 = cur.fetchall()
meses3 = pd.DataFrame(meses3)
meses3.rename(columns = {0:'filter_date'}, inplace = True)
meses3['filter_date'] = pd.to_datetime(meses3['filter_date'])
meses3['filter'] = meses3['filter_date'].dt.month
conditions = [
                (meses3['filter'] == 1) ,
                (meses3['filter'] == 2) ,
                (meses3['filter'] == 3) ,
                (meses3['filter'] == 4) ,
                (meses3['filter'] == 5) ,
                (meses3['filter'] == 6) ,
                (meses3['filter'] == 7) ,
                (meses3['filter'] == 8) ,
                (meses3['filter'] == 9) ,
                (meses3['filter'] == 10) ,
                (meses3['filter'] == 11) ,
                (meses3['filter'] == 12) ]

values = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre',
          'Noviembre', 'Diciembre']
meses3['month'] = np.select(conditions, values)
meses3['filter_date'] = pd.to_datetime(meses3['filter_date'])
meses3 = meses3.sort_values(by=['filter_date'])

p1, p2 = st.columns((1,1))
input_rut = p1.text_input('(sin puntos ni guión, ej. 12345678k)')
dropdown_mes = p2.selectbox('Seleccione mes a consultar', meses3['month'])

##############################################################################################################

if input_rut:
    xs = (meses3[(meses3.month == dropdown_mes)]).iloc[0,0]
    cur.execute(f"""SELECT *
                   FROM susheros_app sa
                   WHERE user_legal_id = '{input_rut}' AND filter_date = '{xs}'
                   ORDER BY order_date, commnad_number; """)

    tb = cur.fetchall()
    cur.close()
    tb = pd.DataFrame(tb)
    tb.rename(columns = {0:'id',
                         1:'id_db',
                         2:'command_number',
                         3:'command_code',
                         4:'fiscal_number',
                         5:'filter_date',
                         6:'service_period_shifts',
                         7:'command_scaned_at',
                         8:'order_date',
                         9:'restaurant_name',
                         10:'user_legal_id',
                         11:'user_name',
                         12:'user_email',
                         13:'product_id',
                         14:'product_code',
                         15:'product_name',
                         16:'product_category_name',
                         17:'category',
                         18:'alert',
                         19:'quantity',
                         20:'roll_price',
                         21:'total_quantity',
                         22:'total_to_pay',
                        },
                inplace = True)


    tb['dia_semana'] = pd.to_datetime(tb['order_date']).dt.day_of_week

    cond = [
                    (tb['dia_semana'] == 1) ,
                    (tb['dia_semana'] == 2) ,
                    (tb['dia_semana'] == 3) ,
                    (tb['dia_semana'] == 4) ,
                    (tb['dia_semana'] == 5) ,
                    (tb['dia_semana'] == 6) ,
                    (tb['dia_semana'] == 0) ]

    val = ['Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab', 'Dom']
    tb['date'] = np.select(cond, val)

    tb['order_date'] = pd.to_datetime(tb['order_date'])
    tb['year'] = tb['order_date'].dt.year
    tb['mes'] = tb['order_date'].dt.month
    tb['day'] = tb['order_date'].dt.day

    tb['command_scaned_at'] = pd.to_datetime(tb['command_scaned_at'])
    tb['year2'] = tb['command_scaned_at'].dt.year
    tb['mes2'] = tb['command_scaned_at'].dt.month
    tb['day2'] = tb['command_scaned_at'].dt.day

    tb['filter_date'] = pd.to_datetime(tb['filter_date'])
    tb['mes_correspondiente'] = tb['filter_date'].dt.month

    tb["Fecha Orden"] = tb['day'].astype(str) +"/"+ tb['mes'].astype(str) +"/"+ tb['year'].astype(str)
    tb["Fecha Escaneo Comanda"] = tb['day2'].astype(str) +"/"+ tb['mes2'].astype(str) +"/"+ tb['year2'].astype(str)

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

    for i in input_rut:
        if len(input_rut) == 9:
            new_rut = (f"{input_rut[0]}{input_rut[1]}.{input_rut[2]}{input_rut[3]}{input_rut[4]}.{input_rut[5]}{input_rut[6]}{input_rut[7]}-{input_rut[8]}")
            break
        elif len(input_rut) == 8:
            new_rut = (f"{input_rut[0]}.{input_rut[1]}{input_rut[2]}{input_rut[3]}.{input_rut[4]}{input_rut[5]}{input_rut[6]}-{input_rut[7]}")
            break

    nombre = (pd.DataFrame(tb['user_name'].unique())).iloc[0,0]
    mes = dropdown_mes
    comandas = (tb["command_number"].unique()).shape[0]
    rolls = np.sum((tb["total_quantity"]))
    pago = "${:,}".format(round(tb['total_to_pay'].sum()))

    st.write('')
    st.write('')
    st.write('')
    st.write('')

    co1, co2, co3, co4 = st.columns(4)

    with co1:
        st.components.v1.html('''
        <style>
        div {
          width: 90%;
          padding: 20px;
          background-color: #181818;
          border: 5px #181818;
          margin: 0 auto;
        }
        </style>
        <body>
        <div style="text-align:center;
                   color: white;
                   font-family: calibri;
                   font-size: 150%;
                   font-weight: bold;" >Rut</div>
        </body>
        ''', height=80)
        st.components.v1.html(f'''
        <p  style="text-align: center;
                   color: black;
                   font-family: calibri;
                   font-size: 200%;
                   margin: 0;">
        {new_rut}</p>
        ''', height=50)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

    with co2:
        st.components.v1.html('''
        <style>
        div {
          width: 90%;
          padding: 20px;
          background-color: #181818;
          border: 5px #181818;
          margin: 0 auto;
        }
        </style>
        <body>
        <div style="text-align:center;
                   color: white;
                   font-family: calibri;
                   font-size: 150%;
                   font-weight: bold;" >Nombre</div>
        </body>
        ''', height=80)
        st.components.v1.html(f'''
        <p  style="text-align: center;
                   color: black;
                   font-family: calibri;
                   font-size: 200%;
                   margin: 0;">
        {nombre.title()}</p>
        ''', height=50)

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

    with co3:
        st.components.v1.html('''
        <style>
        div {
          width: 90%;
          padding: 20px;
          background-color: #181818;
          border: 5px #181818;
          margin: 0 auto;
        }
        </style>
        <body>
        <div style="text-align:center;
                   color: white;
                   font-family: calibri;
                   font-size: 150%;
                   font-weight: bold;" >Mes de Consultar</div>
        </body>
        ''', height=80)
        st.components.v1.html(f'''
        <p  style="text-align: center;
                   color: black;
                   font-family: calibri;
                   font-size: 200%;
                   margin: 0;">
        {mes}</p>
        ''', height=50)

#################################################################################################################################

    col1, col2 = st.columns((1,3))

    with col1:
        st.components.v1.html('''
        <style>
        div {
          width: 90%;
          padding: 20px;
          background-color: #181818;
          border: 5px #181818;
          margin: 0 auto;
        }
        </style>
        <body>
        <div style="text-align:center;
                   color: white;
                   font-family: calibri;
                   font-size: 150%;
                   font-weight: bold;" >Cantidad Total de Rolls</div>
        </body>
        ''', height=80)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        st.components.v1.html(f'''
        <p  style="text-align: center;
                   color: black;
                   font-family: calibri;
                   font-size: 200%;
                   margin: 0;">
        {rolls}</p>
        ''', height=50)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        st.components.v1.html('''
        <style>
        div {
          width: 90%;
          padding: 20px;
          background-color: #181818;
          border: 5px #181818;
          margin: 0 auto;
        }
        </style>
        <body>
        <div style="text-align:center;
                   color: white;
                   font-family: calibri;
                   font-size: 150%;
                   font-weight: bold;" >Cantidad Total de Comandas</div>
        </body>
        ''',height=82)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        st.components.v1.html(f'''
        <p  style="text-align:center;
                   color: black;
                   font-family: calibri;
                   font-size: 200%;
                   margin: 0;">
        {comandas}</p>
        ''',  height=50)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        st.components.v1.html('''
        <style>
        div {
          width: 90%;
          padding: 20px;
          background-color: #181818;
          border: 5px #181818;
          margin: 0 auto;
        }
        </style>
        <body>
        <div style="text-align:center;
                   color: white;
                   font-family: calibri;
                   font-size: 150%;
                   font-weight: bold;" >Monto Total a Pagar</div>
        </body>
        ''',height=82)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
        st.components.v1.html(f'''
        <p  style="text-align:center;
                   color: black;
                   font-family: calibri;
                   font-size: 200%;
                   margin: 0;">
        {pago}</p>
        ''',  height=50)
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

    with col2:
        st.components.v1.html('''
        <style>
        div {
          width: 99%;
          padding: 20px;
          background-color: #181818;
          border: 5px #181818;
          margin: 0 auto;
        }
        </style>
        <body>
        <div style="text-align:center;
                    color: white;
                    font-family: calibri;
                    font-size: 150%;
                    font-weight: bold;" >Desglose Diario</div>
        </body>
        ''', height=80)

        des = pd.pivot_table(tb, index=['year','mes','day','date'], columns='user_legal_id', values='total_to_pay',
                            aggfunc="sum",fill_value=0,sort=False)
        des.reset_index(inplace=True)
        des = des.sort_values(by=['year','mes', 'day'])
        des["Period"] = des['date'].astype(str) +" "+ des['day'].astype(str) +"/"+ des['mes'].astype(str)
        des[input_rut] = round(des[input_rut].astype(float))
        des.rename(columns = {'Period':'Fecha', input_rut:'Monto'}, inplace = True)

        fig = px.bar(des, x = 'Fecha', y = 'Monto', title="", text_auto='',
                    labels={'Period': 'Fecha', 'pattern': 'Monto'}, width=1000)
        fig.update_traces(marker_color='#E74C3C', marker_line_color='#000000', marker_line_width=1, textposition='outside')
        config = {'staticPlot': True, 'displayModeBar': False}
        fig.update_layout(yaxis_tickprefix = '$', yaxis_tickformat = ',.')
        st.plotly_chart(fig, config=config)

    st.write('')

    def highlight_greaterthan(x):
        if x['Monto a Pagar']!= '$0':
            return ['background-color: ']*len(x)
        else:
            return ['background-color: #E74C3C']*len(x)

    pivot = pd.pivot_table(tb, index=["command_code","Fecha Orden", 'Fecha Escaneo Comanda'], values="total_to_pay",
                           aggfunc="sum",fill_value="",sort=False)
    pivot.reset_index(inplace=True)
    pivot = pivot.loc[:,['Fecha Orden','Fecha Escaneo Comanda','command_code','total_to_pay']]
    pivot = pivot.rename(columns = {'command_code':'Código Comanda','total_to_pay': 'Monto a Pagar'})

    tb = tb.drop(['id','id_db','fiscal_number','filter_date','command_scaned_at','order_date',
    'user_legal_id','user_name','user_email','product_id','product_code','product_category_name',
    'category','alert','roll_price','total_quantity','dia_semana','date','year2',
    'mes2','day2','mes_correspondiente'], axis=1)

    tb = tb.loc[:,['Fecha Orden','restaurant_name','service_period_shifts','command_number',
    'command_code','product_name','Fecha Escaneo Comanda','quantity','total_to_pay']]

    tb.rename(columns = {'restaurant_name':'Local  ',
                         'command_number':'Número Cuenta',
                         'command_code':'Código Comanda',
                         'product_name':'Producto',
                         'quantity':'Cantidad de Rolls',
                         'total_to_pay':'Monto a Pagar',
                         'service_period_shifts':'Turno'}, inplace = True)

    tb.loc[:, "Monto a Pagar"] ='$'+ tb["Monto a Pagar"].map('{:,.0f}'.format)

    p1,p7 = st.columns((6,1))
    p1.write("#### Detalle Producción :sushi:")

    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csv = convert_df(pivot)
    p7.download_button(
        label="Descarga archivo CSV",
        data=csv,
        file_name='susheros.csv')

#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    # st.table(tb1.style.apply(highlight_greaterthan, axis=1))
#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I#I

    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    st.dataframe(tb.style.apply(highlight_greaterthan, axis=1), use_container_width=True)

hide_menu = """
<style>
#MainMenu {
    visibility:hidden;
}

</style>
"""

st.markdown(hide_menu, unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------------------

hide_streamlit_style = """
            <style>
            MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
