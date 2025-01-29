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
            st.success(f"{nombre} agregado.")

    def guardar_jugadores(self):
        """Guarda los jugadores en el archivo JSON."""
        with open(self.archivo_json, "w") as archivo:
            json.dump(self.jugadores, archivo, indent=4)

    def cargar_jugadores(self):
        """Carga los jugadores desde el archivo JSON si existe."""
        if os.path.exists(self.archivo_json):
            with open(self.archivo_json, "r") as archivo:
                self.jugadores = json.load(archivo)
        else:
            self.jugadores = {}

        return self.jugadores  # Asegúrate de devolver los jugadores cargados

    def eliminar_jugador(self, nombre_jugador):
        """Elimina un jugador del archivo JSON."""
        if nombre_jugador in self.jugadores:
            del self.jugadores[nombre_jugador]
            self.guardar_jugadores()
            st.success(f"{nombre_jugador} eliminado correctamente.")
        else:
            st.warning(f"{nombre_jugador} no existe en la lista.")

    def modificar_nombre_jugador(self, nombre_actual, nuevo_nombre):
        """Modifica el nombre de un jugador existente."""
        if nombre_actual not in self.jugadores:
            st.warning(f"{nombre_actual} no se encuentra en la lista de jugadores.")
            return

        if nuevo_nombre in self.jugadores:
            st.warning(f"El nombre {nuevo_nombre} ya está en uso.")
            return

        self.jugadores[nuevo_nombre] = self.jugadores.pop(nombre_actual)
        self.guardar_jugadores()
        st.success(f"{nombre_actual} ha sido cambiado a {nuevo_nombre}.")

    def obtener_jugadores_historial(self):
        """Obtiene todos los jugadores registrados en historial.json."""
        jugadores = set()
        try:
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)
                for datos in historial.values():
                    for modalidad, partidas in datos.items():
                        for jugador in partidas:
                            jugadores.add(jugador)
            return list(jugadores)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def guardar_historial(self, juego, modalidad, ganador):
        """Guarda la partida en el historial."""
        if os.path.exists(self.archivo_historial):
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)
        else:
            historial = {}

        if juego not in historial:
            historial[juego] = {}

        if modalidad not in historial[juego]:
            historial[juego][modalidad] = {}

        fecha_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        if ganador not in historial[juego][modalidad]:
            historial[juego][modalidad][ganador] = []
        historial[juego][modalidad][ganador].append(fecha_hora)

        with open(self.archivo_historial, "w") as archivo:
            json.dump(historial, archivo, indent=4)

    def menu_gestion_jugadores(self):
        """Menú para gestionar jugadores."""
        st.title("Gestión de Jugadores")

        col1, col2, col3 = st.columns(3)

        # Agregar jugador
        with col1:
            nombre = st.text_input("Nombre del nuevo jugador").capitalize()
            if st.button("Agregar jugador") and nombre.strip():
                self.agregar_jugador(nombre)

        # Modificar nombre jugador
        with col2:
            nombre_actual = st.text_input("Nombre actual del jugador").capitalize()
            nuevo_nombre = st.text_input("Nuevo nombre del jugador").capitalize()
            if st.button("Modificar nombre jugador") and nombre_actual.strip() and nuevo_nombre.strip():
                self.modificar_nombre_jugador(nombre_actual, nuevo_nombre)

        # Eliminar jugador
        with col3:
            nombre_jugador = st.text_input("Nombre del jugador a eliminar").capitalize()
            if st.button("Eliminar jugador") and nombre_jugador.strip():
                self.eliminar_jugador(nombre_jugador)

        # Mostrar jugadores actuales
        st.subheader("Jugadores registrados:")
        if self.jugadores:
            for nombre, puntos in self.jugadores.items():
                st.write(f"{nombre}: {puntos} puntos")
        else:
            st.write("No hay jugadores registrados.")

        # Volver al menú principal
        if st.button("Volver al Menú Principal"):
            st.query_params = {"page": "main"}
            st.rerun()

    def menu_gestion_partidas(self):
        """Menú de gestión de partidas (aún en desarrollo)."""
        st.title("Gestión de Partidas")

        # Mensaje temporal mientras se desarrolla la funcionalidad
        st.info("Funcionalidad en desarrollo.")

        # Volver al menú principal
        if st.button("Volver al Menú Principal"):
            st.query_params = {"page": "main"}
            st.rerun()


def run():
    """Ejecuta la gestión de jugadores."""
    gestor = GestorJugadores()
    gestor.menu_gestion_jugadores()







