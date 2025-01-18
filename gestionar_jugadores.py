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
            st.write(self.jugadores)
            self.guardar_jugadores()
            st.success(f"{nombre} agregado.")

    def guardar_jugadores(self):
        """Guarda los jugadores en el archivo JSON."""
        with open(self.archivo_json, "w") as archivo:
            json.dump(self.jugadores, archivo, indent=4)

    def cargar_jugadores(self):
        """Carga los jugadores desde el archivo JSON si existe, si no inicializa un diccionario vacío."""
        if os.path.exists(self.archivo_json):
            with open(self.archivo_json, "r") as archivo:
                self.jugadores = json.load(archivo)
        else:
            self.jugadores = {}  # Inicializa como un diccionario vacío si no existe el archivo

        return self.jugadores  # Asegúrate de devolver los jugadores cargados

    def eliminar_jugador(self, nombre_jugador):
        """Elimina un jugador de la lista de jugadores y del archivo JSON."""
        if nombre_jugador in self.jugadores:
            # Eliminar jugador del diccionario de jugadores
            del self.jugadores[nombre_jugador]
            
            # Guardar los cambios en el archivo JSON
            self.guardar_jugadores()
            st.write(self.jugadores)
            st.success(f"{nombre_jugador} eliminado correctamente.")
        else:
            st.warning(f"{nombre_jugador} no existe en la lista.")

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
            st.warning(f"Ya existe un jugador {nuevo_nombre}.")
            return

        self.jugadores[nuevo_nombre] = self.jugadores.pop(nombre_actual)
        st.success(f"{nombre_actual} ha sido modificado a {nuevo_nombre}.")
        self.guardar_jugadores()




    def obtener_jugadores_historial(self):
        """Obtiene todos los jugadores registrados en el archivo historial.json."""
        jugadores = set()  # Usamos un set para evitar duplicados

        try:
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)

                # Iterar sobre todos los juegos en el historial (por ejemplo, "UNO", "Incremento")
                for juego, datos in historial.items():
                    # Iterar sobre las modalidades de cada juego (por ejemplo, "Partidas", "Incremento")
                    for modalidad, partidas in datos.items():
                        # Iterar sobre los jugadores registrados en cada modalidad
                        for jugador in partidas:
                            jugadores.add(jugador)

            return list(jugadores)  # Convertir el set a lista para devolverlo
        except FileNotFoundError:
            print("El archivo historial.json no se encuentra.")
            return []
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
            return []

    def obtener_juegos_historial(self):
        """Obtiene todos los juegos registrados en el archivo historial.json."""
        juegos = set()  # Usamos un set para evitar duplicados

        try:
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)

                # Iterar sobre todos los juegos en el historial (primer nivel)
                for juego in historial.keys():
                    juegos.add(juego)

            return list(juegos)  # Convertir el set a lista para devolverlo
        except FileNotFoundError:
            print("El archivo historial.json no se encuentra.")
            return []
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
            return []

    def obtener_modalidades(self, juego):
        """Obtiene todas las modalidades de un juego registrado en el archivo historial.json."""
        modalidades = set()  # Usamos un set para evitar duplicados

        try:
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)

                # Verificar si el juego existe en el historial
                if juego in historial:
                    # Iterar sobre las modalidades de ese juego (segundo nivel)
                    for modalidad in historial[juego].keys():
                        modalidades.add(modalidad)
                else:
                    print(f"El juego {juego} no se encuentra en el historial.")

            return list(modalidades)  # Convertir el set a lista para devolverlo
        except FileNotFoundError:
            print("El archivo historial.json no se encuentra.")
            return []
        except json.JSONDecodeError:
            print("Error al leer el archivo JSON.")
            return []

    def obtener_jugadores_modalidad(self, juego, modalidad):
        """Obtiene todos los jugadores de una modalidad de un juego específico registrado en el archivo historial.json."""
        jugadores = set()  # Usamos un set para evitar duplicados

        try:
            with open(self.archivo_historial, "r") as archivo:
                historial = json.load(archivo)

                # Verificar si el juego y modalidad existen en el historial
                if juego in historial and modalidad in historial[juego]:
                    # Iterar sobre los jugadores de la modalidad seleccionada
                    jugadores = set(historial[juego][modalidad].keys())
                else:
                    print(f"No se encontraron jugadores para el juego {juego} y la modalidad {modalidad}.")

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
        col1, col2, col3 = st.columns(3)

        # Agregar jugador
        with col1:
            nombre = st.text_input("Introduce el nombre del nuevo jugador").capitalize()

            if st.button("Agregar jugador"):
                if nombre.strip() != "":  # Verificar si el nombre no está vacío
                    self.agregar_jugador(nombre)
                    st.session_state["jugador_agregado"] = nombre  # Guardar el estado en session_state para que no se reinicie

        # Modificar nombre jugador
        with col2:
            nombre_actual = st.text_input("Introduce el nombre actual del jugador").capitalize()
            nuevo_nombre = st.text_input("Introduce el nuevo nombre del jugador").capitalize()

            if st.button("Modificar nombre jugador"):
                if nombre_actual.strip() != "" and nuevo_nombre.strip() != "":
                    self.modificar_nombre_jugador(nombre_actual, nuevo_nombre)
                    st.session_state["jugador_modificado"] = (nombre_actual, nuevo_nombre)  # Guardar el estado de la modificación

            if "jugador_modificado" in st.session_state:
                nombre_actual, nuevo_nombre = st.session_state["jugador_modificado"]

        with col3:
            nombre_jugador = st.text_input("Introduce el nombre del jugador a eliminar").capitalize()
            if st.button("Eliminar jugador"):
                if nombre_jugador.strip() != "":  # Verificar que el nombre no esté vacío
                    self.eliminar_jugador(nombre_jugador)

        # Botón para regresar al menú principal
        if st.button("Volver al Menú Principal"):
            st.session_state.page = "main"  # Cambiar la página en session_state
            st.rerun()


    def menu_gestion_partidas(self):
        st.title("Gestión de Partidas")
        # Estilo para los botones
        # st.markdown("""
        #     <style>
        #         .css-1emrehy.edgvbvh3 { 
        #             font-size: 50px; 
        #             height: 60px; 
        #             width: 100%;
        #             border-radius: 10px;
        #         }
        #         .stButton > button {
        #             width: 100%;
        #             height: 60px;
        #             border-radius: 10px;
        #             font-size: 18px;
        #             background-color: #4CAF50;
        #             color: white;
        #         }
        #         .stButton > button:hover {
        #             background-color: #45a049;
        #         }
        #     </style>
        #     """, unsafe_allow_html=True)
        
        # # Dos botones para las opciones
        # col1, col2 = st.columns(2)

        # with col1:
        #     # Crear una lista de jugadores del historial (si existen)
        #     juegos_historial = list(self.obtener_juegos_historial())
        #     jugadores_historial = list(self.obtener_jugadores_historial())  # Asumiendo que esta función devuelve una lista de jugadores
        #     # Opciones para el selectbox: empezamos con un mensaje neutral
        #     opciones_juegos = ["Selecciona un juego o añade uno nuevo"] + juegos_historial + ["Añadir nuevo juego..."]
        #     opciones_jugadores = ["Selecciona un jugador o añade uno nuevo"] + jugadores_historial + ["Añadir nuevo jugador..."]

        #     # Usar un selectbox con búsqueda de jugadores previos o escribir para filtrar
        #     juego = st.selectbox(
        #         f"Selecciona el juego",
        #         options=opciones_juegos,  # Solo mostrar jugadores no seleccionados previamente
        #         key=f"juego"
        #     )
            
        #     if juego == "Añadir nuevo juego...":
        #         # Solo mostrar un text_input si se selecciona la opción "Añadir nuevo jugador..."
        #         nuevo_nombre = st.text_input(f"Introduce el nombre del juego")
        #         if nuevo_nombre and nuevo_nombre.capitalize() not in juegos_historial:
        #             juegos_historial.append(nuevo_nombre.capitalize())
        #             nombres_jugadores.append(nuevo_nombre.capitalize())
        #         elif nuevo_nombre:
        #             st.warning(f"{nuevo_nombre.capitalize()} ya ha sido añadido o ya existe.")
        #     elif nombre != "Selecciona un jugador o añade uno nuevo" and nombre.capitalize() not in nombres_jugadores:
        #         # Si se selecciona un jugador del historial y no está en la lista
        #         if nombre.capitalize() not in self.jugadores:
        #             nombres_jugadores.append(nombre.capitalize())

        #     nombre = st.selectbox(
        #         f"Selecciona el jugador",
        #         options=opciones_jugadores,  # Solo mostrar jugadores no seleccionados previamente
        #         key=f"jugador"
        #     )

        #     if nombre == "Añadir nuevo jugador...":
        #         # Solo mostrar un text_input si se selecciona la opción "Añadir nuevo jugador..."
        #         nuevo_nombre = st.text_input(f"Introduce el nombre del jugador")
        #         if nuevo_nombre and nuevo_nombre.capitalize() not in jugadores_historial:
        #             # Verificar si el nuevo nombre ya está en el archivo JSON
        #             if nuevo_nombre.capitalize() not in self.jugadores:
        #                 # Si el nombre es único, agregarlo
        #                 #gestor_jugadores.agregar_jugador(nuevo_nombre.capitalize())
        #                 jugadores_historial.append(nuevo_nombre.capitalize())  # Añadir al historial para reutilizarlo
        #                 nombres_jugadores.append(nuevo_nombre.capitalize())
        #             else:
        #                 st.warning(f"{nuevo_nombre.capitalize()} ya está en el juego y no se ha agregado.")
        #         elif nuevo_nombre:
        #             st.warning(f"{nuevo_nombre.capitalize()} ya ha sido añadido o ya existe.")
        #     elif nombre != "Selecciona un jugador o añade uno nuevo" and nombre.capitalize() not in nombres_jugadores:
        #         # Si se selecciona un jugador del historial y no está en la lista
        #         if nombre.capitalize() not in self.jugadores:
        #             nombres_jugadores.append(nombre.capitalize())

        # with col2:
        #     if st.button("Modificar nombre jugador"):
        #         nombre_actual = st.text_input("Introduce el nombre actual del jugador")
        #         nuevo_nombre = st.text_input("Introduce el nuevo nombre del jugador")
        #         if st.button("Modificar"):
        #             self.modificar_nombre_jugador(nombre_actual, nuevo_nombre)

        # Botón para regresar al menú principal
        if st.button("Volver al Menú Principal"):
            st.query_params(page="main")
            st.rerun()






def run():
    """Ejecuta la gestión de jugadores."""
    gestor = GestorJugadores()
    gestor.menu_gestion_jugadores()
    gestor.menu_gestion_partidas()







