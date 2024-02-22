import pandas as pd
import streamlit as st
from pymongo import MongoClient
import certifi


st.title("Prueba de conexion a Mongo DB")


def conection():
    return MongoClient("mongodb+srv://"+st.secrets["DB_USERNAME"]+":"+st.secrets["DB_PASSWORD"]+"@prediccion2024.uiek7iw.mongodb.net/",tlsCAFile=certifi.where())

conexion = conection()


def getData():
    db = conexion.get_database("Oprediccion")
    collection = db.get_collection("ejemplo2")
    items = collection.find({}, {'_id': 0})  # Exclude _id field
    return list(items)


def add_data(Year, Emissions):
    db = conexion.get_database("Oprediccion")
    collection = db.get_collection("ejemplo2")
    collection.insert_one({"year": Year, "emissions": Emissions})

datos = getData()
st.subheader("Emisiones de carbono por año")
st.dataframe(pd.DataFrame(datos))

dfGlobalCO2Emissions = pd.read_csv("venv/datos/GlobalCO2Emissions.csv")
st.dataframe(dfGlobalCO2Emissions)

st.subheader("Registrar un nuevo año")
with st.form(key='my_form'):
    year = st.number_input("Año")
    emissions = st.number_input("Emisiones")
    submit_button = st.form_submit_button(label='Agregar')

# Procesar los datos del formulario
if submit_button:
    add_data(year, emissions)
    st.write("¡Datos agregados con éxito!")