import streamlit as st
import json
import os
from datetime import datetime


class GestorJugadores:
    def __init__(self, archivo_json="jugadores.json", archivo_historial="historial.json"):
        self.archivo_json = archivo_json
        self.archivo_historial = archivo_historial
        self.jugadores = {}
        self.cargar_jugadores()

    def agregar_jugador(self, nombre):
        """Agrega un jugador al diccionario de jugadores."""
        if nombre in self.jugadores:
            st.warning(f"{nombre} ya existe.")
        else:
            self.jugadores[nombre] = 0
            self.guardar_jugadores()
            st.success(f"Jugador {nombre} agregado.")

    def guardar_jugadores(self):
        """Guarda los jugadores en el archivo JSON."""
        with open(self.archivo_json, "w") as archivo:
            json.dump(self.jugadores, archivo, indent=4)

    def cargar_jugadores(self):
        """Carga los jugadores desde el archivo JSON."""
        if os.path.exists(self.archivo_json):
            with open(self.archivo_json, "r") as archivo:
                self.jugadores = json.load(archivo)
        else:
            self.jugadores = {}

    def mostrar_jugadores(self):
        """Muestra los jugadores y sus puntos en la interfaz de Streamlit."""
        if self.jugadores:
            st.subheader("Jugadores y puntos:")
            for nombre, puntos in self.jugadores.items():
                st.write(f"{nombre}: {puntos} puntos")
        else:
            st.write("No hay jugadores registrados.")

    def modificar_nombre_jugador(self, nombre_actual, nuevo_nombre):
        """Modifica el nombre de un jugador existente."""
        if nombre_actual not in self.jugadores:
            st.warning(f"{nombre_actual} no se encuentra en el diccionario de jugadores.")
            return

        if nuevo_nombre in self.jugadores:
            st.warning(f"Ya existe un jugador con el nombre {nuevo_nombre}.")
            return

        self.jugadores[nuevo_nombre] = self.jugadores.pop(nombre_actual)
        st.success(f"El nombre del jugador ha sido modificado de {nombre_actual} a {nuevo_nombre}.")
        self.guardar_jugadores()

    def obtener_jugadores_historial(self):
        """Obtiene todos los jugadores registrados en el archivo historial.json."""
        jugadores = set()  # Usamos un set para evitar duplicados

        try:
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)
                
                # Iterar sobre las partidas para obtener los jugadores
                for juego, datos in historial.items():
                    partidas = datos.get("partidas", {})
                    
                    # Iterar sobre los jugadores registrados en cada juego
                    for jugador in partidas:
                        jugadores.add(jugador)
            
            return list(jugadores)  # Convertir el set a lista para devolverlo
        except FileNotFoundError:
            print("El archivo historial.json no se encuentra.")
            return []
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
            return []

    def guardar_historial(self, juego, modalidad, ganador):
        """
        Guarda el historial de partidas ganadas por un jugador, 
        organizadas por juego, modalidad y fecha/hora.
        """
        # Cargar historial existente si el archivo ya existe
        if os.path.exists(self.archivo_historial):
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)
        else:
            historial = {}

        # Asegurarse de que el juego exista en el historial
        if juego not in historial:
            historial[juego] = {}

        # Asegurarse de que la modalidad exista dentro del juego
        if modalidad not in historial[juego]:
            historial[juego][modalidad] = {}

        # Añadir la nueva entrada al historial con fecha y hora
        fecha_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if ganador not in historial[juego][modalidad]:
            historial[juego][modalidad][ganador] = []
        historial[juego][modalidad][ganador].append(fecha_hora)

        # Guardar el historial actualizado en el archivo
        with open(self.archivo_historial, "w") as archivo:
            json.dump(historial, archivo, indent=4)

    def obtener_total_victorias(self, juego, modalidad, jugador):
        """
        Devuelve el total de victorias de un jugador en un juego y modalidad específica.
        """
        if os.path.exists(self.archivo_historial):
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)
            if juego in historial and modalidad in historial[juego] and jugador in historial[juego][modalidad]:
                return len(historial[juego][modalidad][jugador])
        return 0


    def menu_gestion_jugadores(self):
        """Menú para gestionar jugadores."""
        st.title("Gestión de Jugadores")

        # Estilo para los botones
        st.markdown("""
            <style>
                .css-1emrehy.edgvbvh3 { 
                    font-size: 50px; 
                    height: 60px; 
                    width: 100%;
                    border-radius: 10px;
                }
                .stButton > button {
                    width: 100%;
                    height: 60px;
                    border-radius: 10px;
                    font-size: 18px;
                    background-color: #4CAF50;
                    color: white;
                }
                .stButton > button:hover {
                    background-color: #45a049;
                }
            </style>
            """, unsafe_allow_html=True)

        # Dos botones para las opciones
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Agregar jugador"):
                nombre = st.text_input("Introduce el nombre del nuevo jugador")
                if st.button("Agregar"):
                    self.agregar_jugador(nombre)

        with col2:
            if st.button("Modificar nombre jugador"):
                nombre_actual = st.text_input("Introduce el nombre actual del jugador")
                nuevo_nombre = st.text_input("Introduce el nuevo nombre del jugador")
                if st.button("Modificar"):
                    self.modificar_nombre_jugador(nombre_actual, nuevo_nombre)

        # Botón para regresar al menú principal
        if st.button("Volver al Menú Principal"):
            st.experimental_set_query_params(page="main")
            st.rerun()




def run():
    """Ejecuta la gestión de jugadores."""
    gestor = GestorJugadores()
    gestor.menu_gestion_jugadores()







