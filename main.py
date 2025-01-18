import streamlit as st
from uno import UNO
from gestionar_jugadores import GestorJugadores
import sys
import os

class Main:
    def __init__(self, gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS):
        self.gestor_jugadores = gestor_jugadores
        self.gestor_UNO = gestor_UNO
        self.gestor_UNO_FLIP = gestor_UNO_FLIP
        self.gestor_DOS = gestor_DOS

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

        if st.button("Salir"):
            st.write("\n¡Gracias por jugar! Hasta luego.")
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

    def control_jugadores(self, page):
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
                    # Excluir los jugadores ya seleccionados en otros selectboxes
                    opciones_filtradas = [opcion for opcion in opciones_selectbox if opcion not in selectbox_values]

                    # Usar un selectbox con búsqueda de jugadores previos o escribir para filtrar
                    nombre = st.selectbox(
                        f"Selecciona el jugador {i + 1}",
                        options=opciones_filtradas,  # Solo mostrar jugadores no seleccionados previamente
                        key=f"jugador_{i+1}"
                    )

                    selectbox_values.append(nombre)  # Guardar la selección para evitar duplicados

                    if nombre == "Añadir nuevo jugador...":
                        # Solo mostrar un text_input si se selecciona la opción "Añadir nuevo jugador..."
                        nuevo_nombre = st.text_input(f"Introduce el nombre del jugador {i + 1}")
                        if nuevo_nombre and nuevo_nombre.capitalize() not in jugadores_historial + nombres_jugadores:
                            # Verificar si el nuevo nombre ya está en el archivo JSON
                            if nuevo_nombre.capitalize() not in gestor_jugadores.jugadores:
                                # Si el nombre es único, agregarlo
                                #gestor_jugadores.agregar_jugador(nuevo_nombre.capitalize())
                                jugadores_historial.append(nuevo_nombre.capitalize())  # Añadir al historial para reutilizarlo
                                nombres_jugadores.append(nuevo_nombre.capitalize())
                            else:
                                st.warning(f"{nuevo_nombre.capitalize()} ya está en el juego y no se ha agregado.")
                        elif nuevo_nombre:
                            st.warning(f"{nuevo_nombre.capitalize()} ya ha sido añadido o ya existe.")
                    elif nombre != "Selecciona un jugador o añade uno nuevo" and nombre.capitalize() not in nombres_jugadores:
                        # Si se selecciona un jugador del historial y no está en la lista
                        if nombre.capitalize() not in gestor_jugadores.jugadores:
                            nombres_jugadores.append(nombre.capitalize())

            # Verificar si hay duplicados antes de habilitar el botón
            duplicados = [jugador for jugador in nombres_jugadores if nombres_jugadores.count(jugador) > 1]
            if duplicados:
                # Mostrar un mensaje de advertencia si hay duplicados
                st.warning(f"Los siguientes jugadores están repetidos: {', '.join(set(duplicados))}. Corrige antes de continuar.")
                # Deshabilitar el botón si hay duplicados
                st.button("Añadir Jugadores", disabled=True)
            else:
                # Mostrar el botón para agregar jugadores solo si no hay duplicados
                if st.button("Añadir Jugadores"):
                    # Agregar los jugadores al gestor si no están en el archivo JSON
                    for nombre in nombres_jugadores:
                        if nombre not in gestor_jugadores.jugadores:
                            gestor_jugadores.agregar_jugador(nombre)  # Llamamos al método para agregar jugadores
                        else:
                            st.warning(f"{nombre} ya está en el juego y no se ha agregado nuevamente.")

        # Si ya existe el archivo JSON, se omite la entrada de jugadores y se muestra el menú principal
        if os.path.exists(gestor_jugadores.archivo_json) or len(gestor_jugadores.jugadores) > 0:
            if page=="uno":
                gestor_UNO.menu_Uno()
            elif page=="uno flip":
                pass
            elif page=="dos":
                pass

# Punto de entrada principal
if __name__ == "__main__":
    # Crear instancias de las clases necesarias
    gestor_jugadores = GestorJugadores()
    gestor_UNO = UNO(gestor_jugadores)
    gestor_UNO_FLIP = UNO(gestor_jugadores)  # Ajusta si `UNO_FLIP` tiene lógica diferente.
    gestor_DOS = UNO(gestor_jugadores)  # Ajusta si `DOS` tiene lógica diferente.

    # Obtener parámetros de la URL
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["main"])[0]

    # Redirigir según el parámetro `page`
    main_app = Main(gestor_jugadores, gestor_UNO, gestor_UNO_FLIP, gestor_DOS)
    if page == "main":
        main_app.menu_principal()
    elif page == "gestionar_jugadores":
        gestor_jugadores.menu_gestion_jugadores()
    elif page == "uno":
        st.title("Bienvenidos al UNO")
        main_app.control_jugadores(page)
    elif page == "uno flip":
        st.title("Bienvenidos al UNO FLIP")
    elif page == "dos":
        st.title("Bienvenidos al DOS")
    elif page == "jugar rondas":
        st.title("Jugando Rondas...")
        modalidad = query_params.get("modalidad", [""])[0]
        parametros_str = query_params.get("parametros", [""])[0]
        parametros = list(map(str, parametros_str.split(",")))

        if len(parametros) < 2:
            st.error("Faltan parámetros necesarios para jugar rondas.")
            st.warning(parametros_str)
        else:
            gestor_UNO.jugar_rondas(modalidad, parametros[0], parametros[1])
        
        

        






















