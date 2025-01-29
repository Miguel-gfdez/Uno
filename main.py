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
            st.experimental_set_query_params(page="uno")
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros
        
        if st.button("UNO FLIP"):
            st.experimental_set_query_params(page="uno flip")
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros
        
        if st.button("DOS"):
            st.experimental_set_query_params(page="dos")
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros

        if st.button("Gestionar jugadores"):
            st.experimental_set_query_params(page="gestionar_jugadores")
            st.rerun()  # Forzar recarga de la página con los nuevos parámetros
        
        # if st.button("Gestionar partidas"):
        #     st.experimental_set_query_params(page="gestionar_partidas")
        #     st.rerun()  # Forzar recarga de la página con los nuevos parámetros

        if st.button("Salir"):
            if os.path.exists("jugadores.json"):
                os.remove("jugadores.json")
            st.experimental_set_query_params(page="inicio")
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
        if st.button("INICIAR"):
            if os.path.exists("jugadores.json"):
                os.remove("jugadores.json")
                
            st.experimental_set_query_params(page="main")
            st.rerun()


    def control_jugadores(self, juego):
        # Verificar si el archivo JSON ya existe
        if not os.path.exists(gestor_jugadores.archivo_json):
            # Si no existe, pedir al usuario el número de jugadores y sus nombres
            num_jugadores = st.number_input("Introduce el número de jugadores:", min_value=2, step=1)

            # Crear una lista de jugadores del historial (si existen)
            jugadores_historial = list(gestor_jugadores.obtener_jugadores_historial())  # Asumiendo que esta función devuelve una lista de jugadores

            # Opciones para el selectbox: empezamos con un mensaje neutral
            opciones_selectbox = ["Selecciona un jugador o añade uno nuevo"] + jugadores_historial + ["Añadir nuevo jugador..."]

            nombres_jugadores = []
            selectbox_values = []  # Para guardar los valores seleccionados de los selectbox

            if num_jugadores > 0:
                for i in range(num_jugadores):                                                   
                    nombre = st.selectbox(
                        f"Selecciona el jugador {i + 1}",
                        options=opciones_selectbox,  # Mostrar todas las opciones
                        key=f"jugador_{i+1}"
                    )

                    selectbox_values.append(nombre)  # Guardar la selección para evitar duplicados

                    if nombre == "Añadir nuevo jugador...":                                                                                                      
                        nuevo_nombre = st.text_input(f"Introduce el nombre del jugador {i + 1}")
                        if nuevo_nombre and nuevo_nombre.strip() != "" and nuevo_nombre not in jugadores_historial + nombres_jugadores:                                                                                    
                            nombres_jugadores.append(nuevo_nombre)  # Añadir el nombre tal como se introdujo
                            if "jugadores" not in st.session_state:
                                st.session_state.jugadores = {}  # Inicializar la sesión de jugadores si no existe
                            st.session_state.jugadores[nuevo_nombre] = 0  # Inicializar el puntaje del jugador                                                                   
                    elif nombre != "Selecciona un jugador o añade uno nuevo" and nombre and nombre not in nombres_jugadores:
                        nombres_jugadores.append(nombre)  # Añadir el nombre tal como se seleccionó
                        if "jugadores" not in st.session_state:
                            st.session_state.jugadores = {}  # Inicializar la sesión de jugadores si no existe
                        st.session_state.jugadores[nombre] = 0  # Inicializar el puntaje del jugador

            # Verificar si hay duplicados antes de habilitar el botón
            if len(nombres_jugadores) != num_jugadores or "Selecciona un jugador o añade uno nuevo" in nombres_jugadores:
                st.warning(f"Existen jugadores repetidos.")
            else:
                # Mostrar el botón para agregar jugadores solo si no hay duplicados
                if st.button("Añadir Jugadores"):
                    # Agregar los jugadores al gestor si no están en el archivo JSON
                    for nombre in nombres_jugadores:
                        if nombre not in gestor_jugadores.jugadores:
                            nombre = nombre.capitalize()
                            gestor_jugadores.agregar_jugador(nombre)  # Llamamos al método para agregar jugadores
                            
                        else:
                            st.warning(f"{nombre} ya está en el juego y no se ha agregado nuevamente.")
                    st.experimental_set_query_params(page="menu uno", juego=juego)
                    st.rerun()           
        else:
            # Si ya existe el archivo JSON, se omite la entrada de jugadores y se muestra el menú principal
            if os.path.exists(gestor_jugadores.archivo_json) or len(gestor_jugadores.jugadores) > 0:
                if page == "uno":
                    gestor_UNO.menu_Uno(juego)
                elif page == "uno flip":
                    gestor_UNO.menu_Uno(juego)
                elif page == "dos":
                    gestor_UNO.menu_Uno(juego)


# Punto de entrada principal
if __name__ == "__main__":
    # Crear instancias de las clases necesarias
    gestor_jugadores = GestorJugadores()
    gestor_UNO = UNO(gestor_jugadores)
    gestor_UNO_FLIP = UNO(gestor_jugadores)
    gestor_DOS = UNO(gestor_jugadores)

    # Obtener parámetros de la URL
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["inicio"])[0]

    # Redirigir según el parámetro `page`
    main_app = Main(gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS)
    if page == "inicio":
        main_app.inicio()
    elif page == "main":
        main_app.menu_principal()
    elif page == "gestionar_jugadores":
        gestor_jugadores.menu_gestion_jugadores()
    # elif page == "gestionar_partidas":
    #     gestor_jugadores.menu_gestion_partidas()
    elif page == "menu uno":
        juego = query_params.get("juego", [""])[0]
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
        ganador = query_params.get("ganador", [""])[0]
        puntos_ronda = query_params.get("puntos_ronda", [""])[0]
        gestor_UNO.procesar_ronda(ganador,puntos_ronda)






        

        






















