import streamlit as st
import os
import sys
import time
import json
from datetime import datetime

class Main:
    def __init__(self, gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS):
        self.gestor_jugadores = gestor_jugadores
        self.gestor_UNO = gestor_UNO
        self.gestor_UNO_FLIP = gestor_UNO_FLIP
        self.gestor_DOS = gestor_DOS

    def menu_principal(self):
        """Menú principal del programa adaptado a Streamlit con botones apilados y estilizados."""
        st.title("Menú Principal")

        # Botones apilados verticalmente
        if st.button("UNO"):
            self.gestor_UNO.menu_principal()
        st.markdown("<br>", unsafe_allow_html=True)

        # if st.button("UNO FLIP"):
        #     self.gestor_UNO_FLIP.menu_principal()
        # st.markdown("<br>", unsafe_allow_html=True)

        # if st.button("DOS"):
        #     self.gestor_DOS.menu_principal()
        # st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Gestionar jugadores"):
            self.gestor_jugadores.menu_gestion_jugadores()
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Salir"):
            st.write("\n¡Gracias por jugar! Hasta luego.")
            try:
                os.remove(f"{self.gestor_jugadores.archivo_json}")
            except FileNotFoundError:
                pass
            sys.exit()

        # Estilización adicional para mejorar la apariencia de los botones
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


class GestorJugadores:
    def __init__(self, archivo_json="jugadores.json"):
        self.archivo_json = archivo_json
        self.jugadores = {}

    def agregar_jugador(self, nombre):
        """Agrega un jugador al diccionario de jugadores."""
        if nombre in self.jugadores:
            st.warning(f"{nombre} ya existe.")
        else:
            self.jugadores[nombre] = 0
            self.guardar_jugadores()

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

    def menu_gestion_jugadores(self):
        """Menú para gestionar jugadores."""
        st.title("Gestión de Jugadores")
        opcion = st.selectbox("Selecciona una opción", ["Agregar jugador", "Modificar nombre jugador"])

        if opcion == "Agregar jugador":
            nombre = st.text_input("Introduce el nombre del nuevo jugador")
            if st.button("Agregar"):
                self.agregar_jugador(nombre)
        elif opcion == "Modificar nombre jugador":
            nombre_actual = st.text_input("Introduce el nombre actual del jugador")
            nuevo_nombre = st.text_input("Introduce el nuevo nombre del jugador")
            if st.button("Modificar"):
                self.modificar_nombre_jugador(nombre_actual, nuevo_nombre)


class UNO:
    def __init__(self, gestor_jugadores):
        self.gestor_jugadores = gestor_jugadores
        self.valores = {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "+2": 20, "BLOQUEO": 20, "DIRECCION": 20, "COLOR": 50, "+4": 50
        }
        self.puntos_maximos = 100  # Establecer un valor por defecto
        self.n_partidas = 0
        self.ganador = None

    def menu_principal(self):
        """Menú principal para el juego UNO con botones."""
        st.title("Menú de Juego UNO")
        
        # Botones para elegir modalidad
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Partidas"):
                self.n_partidas = st.number_input("Número de partidas", min_value=1, value=3, step=1)
                self.jugar_partidas()
        with col2:
            if st.button("Incremento"):
                self.puntos_maximos = st.number_input("Puntos máximos para ganar", min_value=1, value=100, step=1)
                self.jugar_incremento()
        with col3:
            if st.button("Libre"):
                self.puntos_maximos = st.number_input("Puntos máximos para ganar", min_value=1, value=100, step=1)
                self.jugar_libre()

    def jugar_partidas(self):
        """Jugar por rondas hasta que un jugador gane el número de partidas necesarias."""
        st.subheader("Modo Partidas")
        c_partidas = 0
        while c_partidas < self.n_partidas:
            ganador = st.selectbox(f"Selecciona el ganador de la ronda #{c_partidas + 1}", list(self.gestor_jugadores.jugadores.keys()))
            if ganador:
                self.gestor_jugadores.jugadores[ganador] += 1
                c_partidas += 1
                st.success(f"{ganador} ha ganado la ronda #{c_partidas}")
                self.mostrar_estadisticas()

        max_partidas = max(self.gestor_jugadores.jugadores, key=self.gestor_jugadores.jugadores.get)
        st.success(f"El ganador del juego es {max_partidas} con {self.gestor_jugadores.jugadores[max_partidas]} partidas ganadas.")
        self.reset_juego()

    def jugar_incremento(self):
        """Jugar con incremento de puntos por carta."""
        st.subheader("Modo Incremento")
        while True:
            ganador = st.selectbox("Selecciona el ganador de la ronda", list(self.gestor_jugadores.jugadores.keys()))
            carta = st.selectbox("Selecciona la carta jugada", list(self.valores.keys()))
            if ganador and carta:
                self.gestor_jugadores.jugadores[ganador] += self.valores[carta]
                st.success(f"{ganador} ha jugado {carta} y ahora tiene {self.gestor_jugadores.jugadores[ganador]} puntos.")
                if self.gestor_jugadores.jugadores[ganador] >= self.puntos_maximos:
                    st.success(f"¡{ganador} ha ganado el juego! Enhorabuena.")
                    self.reset_juego()
                    break
            self.mostrar_estadisticas()

    def jugar_libre(self):
        """Jugar sin límite de puntos."""
        st.subheader("Modo Libre")
        while True:
            ganador = st.selectbox("Selecciona el ganador de la ronda", list(self.gestor_jugadores.jugadores.keys()))
            carta = st.selectbox("Selecciona la carta jugada", list(self.valores.keys()))
            if ganador and carta:
                self.gestor_jugadores.jugadores[ganador] += self.valores[carta]
                st.success(f"{ganador} ha jugado {carta} y ahora tiene {self.gestor_jugadores.jugadores[ganador]} puntos.")
            self.mostrar_estadisticas()

    def mostrar_estadisticas(self):
        """Muestra las estadísticas de puntos de los jugadores."""
        st.write("Estadísticas actuales de los jugadores:")
        for jugador, puntos in self.gestor_jugadores.jugadores.items():
            st.write(f"{jugador}: {puntos} puntos")

    def reset_juego(self):
        """Restablece los puntos de los jugadores."""
        for jugador in self.gestor_jugadores.jugadores:
            self.gestor_jugadores.jugadores[jugador] = 0
        self.gestor_jugadores.guardar_jugadores()









# Crear las instancias
gestor_jugadores = GestorJugadores()
gestor_UNO = UNO(gestor_jugadores)
#gestor_UNO_FLIP = UNO(gestor_jugadores)  # Similar a UNO, puedes agregar lógica de UNO FLIP aquí.
#gestor_DOS = UNO(gestor_jugadores)  # Similar a UNO, puedes agregar lógica de DOS aquí.

# Función principal de Streamlit
def main():
    try:
        # Cargar jugadores previamente
        gestor_jugadores.cargar_jugadores()

        # Crear la instancia de Main y mostrar el menú
        main_menu = Main(gestor_jugadores, gestor_UNO, None, None)
        main_menu.menu_principal()

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()
















