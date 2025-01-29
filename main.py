import streamlit as st
from uno import UNO
from gestionar_jugadores import GestorJugadores
import os


class Main:
    def __init__(self, gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS):
        self.gestor_jugadores = gestor_jugadores
        self.gestor_UNO = gestor_UNO
        self.gestor_UNO_FLIP = gestor_UNO_FLIP
        self.gestor_DOS = gestor_DOS
        self.juego = ""

    def menu_principal(self):
        """Menú principal del programa adaptado a Streamlit con botones apilados y estilizados."""
        st.title("Menú Principal")

        # Botones estilizados y navegación
        if st.button("UNO"):
            st.query_params = {"page": "uno"}
            st.rerun()

        if st.button("UNO FLIP"):
            st.query_params = {"page": "uno flip"}
            st.rerun()

        if st.button("DOS"):
            st.query_params = {"page": "dos"}
            st.rerun()

        if st.button("Gestionar jugadores"):
            st.query_params = {"page": "gestionar_jugadores"}
            st.rerun()

        if st.button("Salir"):
            if os.path.exists("jugadores.json"):
                os.remove("jugadores.json")
            st.query_params = {"page": "inicio"}
            st.rerun()
            st.stop()

    def inicio(self):
        st.title("Bienvenido al Juego")

        # Agregar estilos para los botones
        st.markdown("""
            <style>
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

            # Actualizar los parámetros de la URL
            st.query_params = {"page": "main"}
            
            # Forzar la recarga de la aplicación
            st.rerun()

    def control_jugadores(self, juego):
        # Verificar si el archivo JSON ya existe
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
                    elif nombre != "Selecciona un jugador o añade uno nuevo" and nombre not in nombres_jugadores:
                        nombres_jugadores.append(nombre)

            if len(nombres_jugadores) != num_jugadores or "Selecciona un jugador o añade uno nuevo" in nombres_jugadores:
                st.warning("Existen jugadores repetidos.")
            else:
                if st.button("Añadir Jugadores"):
                    for nombre in nombres_jugadores:
                        if nombre not in self.gestor_jugadores.jugadores:
                            self.gestor_jugadores.agregar_jugador(nombre.capitalize())
                    st.query_params = {"page": "menu uno", "juego": juego}
                    st.rerun()
        else:
            if os.path.exists(self.gestor_jugadores.archivo_json) or len(self.gestor_jugadores.jugadores) > 0:
                self.gestor_UNO.menu_Uno(juego)


# Punto de entrada principal
if __name__ == "__main__":
    # Crear instancias de las clases necesarias
    gestor_jugadores = GestorJugadores()
    gestor_UNO = UNO(gestor_jugadores)
    gestor_UNO_FLIP = UNO(gestor_jugadores)
    gestor_DOS = UNO(gestor_jugadores)

    # Obtener parámetros de la URL
    page = st.query_params.get("page", ["inicio"])[0]

    # Crear la instancia principal
    main_app = Main(gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS)

    # Redirigir según el parámetro page
    if page == "inicio":
        main_app.inicio()
    elif page == "main":
        main_app.menu_principal()
    elif page == "gestionar_jugadores":
        gestor_jugadores.menu_gestion_jugadores()
    elif page == "menu uno":
        juego = st.query_params.get("juego", [""])[0]
        gestor_UNO.menu_Uno(juego)
    elif page == "uno":
        juego = page.upper()
        st.title("Bienvenidos al UNO")
        main_app.control_jugadores(juego)
    elif page == "uno flip":
        juego = page.upper()
        st.title("Bienvenidos al UNO FLIP")
        main_app.control_jugadores(juego)
    elif page == "dos":
        juego = page.upper()
        st.title("Bienvenidos al DOS")
        main_app.control_jugadores(juego)
    elif page == "seleccionar ganador":
        gestor_UNO.seleccionar_ganador()
    elif page == "procesar rondas":
        st.title("Resultados")
        ganador = st.query_params.get("ganador", [""])[0]
        puntos_ronda = st.query_params.get("puntos_ronda", [""])[0]
        gestor_UNO.procesar_ronda(ganador, puntos_ronda)






        

        






















