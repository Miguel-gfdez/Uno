import streamlit as st
from uno import UNO
from gestionar_jugadores import GestorJugadores
import os

import streamlit as st
import os

class Main:
    def __init__(self, gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS):
        self.gestor_jugadores = gestor_jugadores
        self.gestor_UNO = gestor_UNO
        self.gestor_UNO_FLIP = gestor_UNO_FLIP
        self.gestor_DOS = gestor_DOS
        self.juego = ""
        
    def menu_principal(self):
        st.title("Menú Principal")
        
        # Botones estilizados y navegación
        if st.button("UNO"):
            st.session_state.page = "uno"
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros
        
        if st.button("UNO FLIP"):
            st.session_state.page = "uno flip"
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros
        
        if st.button("DOS"):
            st.session_state.page = "dos"
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros

        if st.button("Gestionar jugadores"):
            st.session_state.page = "gestionar_jugadores"
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros
        
        if st.button("Salir"):
            if os.path.exists("jugadores.json"):
                os.remove("jugadores.json")
            st.session_state.page = "inicio"
            st.rerun()
            st.stop()

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

    def inicio(self):
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
        
        if st.button("INICIAR"):
            if os.path.exists("jugadores.json"):
                os.remove("jugadores.json")
            st.session_state.page = "main"
            st.rerun()

    def control_jugadores(self, juego):
        if not os.path.exists(self.gestor_jugadores.archivo_json):
            num_jugadores = st.number_input("Introduce el número de jugadores:", min_value=2, step=1)
            
            jugadores_historial = list(self.gestor_jugadores.obtener_jugadores_historial())
            opciones_selectbox = ["Selecciona un jugador o añade uno nuevo"] + jugadores_historial + ["Añadir nuevo jugador..."]

            nombres_jugadores = []

            if num_jugadores > 0:
                for i in range(num_jugadores):
                    nombre = st.selectbox(f"Selecciona el jugador {i + 1}", options=opciones_selectbox, key=f"jugador_{i+1}")
                    if nombre == "Añadir nuevo jugador...":
                        nuevo_nombre = st.text_input(f"Introduce el nombre del jugador {i + 1}")
                        if nuevo_nombre and nuevo_nombre.strip() != "" and nuevo_nombre not in jugadores_historial + nombres_jugadores:
                            nombres_jugadores.append(nuevo_nombre)
                            st.session_state.jugadores[nuevo_nombre] = 0
                    elif nombre != "Selecciona un jugador o añade uno nuevo" and nombre and nombre not in nombres_jugadores:
                        nombres_jugadores.append(nombre)
                        st.session_state.jugadores[nombre] = 0

            if len(nombres_jugadores) != num_jugadores or "Selecciona un jugador o añade uno nuevo" in nombres_jugadores:
                st.warning("Existen jugadores repetidos.")
            else:
                if st.button("Añadir Jugadores"):
                    for nombre in nombres_jugadores:
                        if nombre not in self.gestor_jugadores.jugadores:
                            nombre = nombre.capitalize()
                            self.gestor_jugadores.agregar_jugador(nombre)
                        else:
                            st.warning(f"{nombre} ya está en el juego y no se ha agregado nuevamente.")
                    st.session_state.page = "menu uno"
                    st.session_state.juego = juego
                    st.rerun()
        else:
            if os.path.exists(self.gestor_jugadores.archivo_json) or len(self.gestor_jugadores.jugadores) > 0:
                if juego == "uno":
                    self.gestor_UNO.menu_Uno(juego)
                elif juego == "uno flip":
                    self.gestor_UNO_FLIP.menu_Uno(juego)
                elif juego == "dos":
                    self.gestor_DOS.menu_Uno(juego)

# Punto de entrada principal
if __name__ == "__main__":
    try:
        gestor_jugadores = GestorJugadores()
        gestor_UNO = UNO(gestor_jugadores)
        gestor_UNO_FLIP = UNO(gestor_jugadores)
        gestor_DOS = UNO(gestor_jugadores)

        if "page" not in st.session_state:
            st.session_state.page = "inicio"

        main_app = Main(gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS)
        if st.session_state.page == "inicio":
            main_app.inicio()
        elif st.session_state.page == "main":
            main_app.menu_principal()
        elif st.session_state.page == "gestionar_jugadores":
            gestor_jugadores.menu_gestion_jugadores()
        elif st.session_state.page == "menu uno":
            juego = st.session_state.juego
            gestor_UNO.menu_Uno(juego)
        elif st.session_state.page == "uno":
            juego = st.session_state.page.upper()
            st.title("Bienvenidos al UNO")
            main_app.control_jugadores(juego)
        elif st.session_state.page == "uno flip":
            juego = st.session_state.page.upper()
            st.title("Bienvenidos al UNO FLIP")
            main_app.control_jugadores(juego)
        elif st.session_state.page == "dos":
            juego = st.session_state.page.upper()
            st.title("Bienvenidos al DOS")
            main_app.control_jugadores(juego)
        elif st.session_state.page == "seleccionar ganador":
            gestor_UNO.seleccionar_ganador()
        elif st.session_state.page == "procesar rondas":
            st.title("Resultados")
            ganador = st.session_state.ganador
            puntos_ronda = st.session_state.puntos_ronda
            gestor_UNO.procesar_ronda(ganador, puntos_ronda)
    except:
        pass




        

        






















