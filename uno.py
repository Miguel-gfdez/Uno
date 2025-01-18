import streamlit as st
import os
from gestionar_jugadores import GestorJugadores
import pandas as pd
import random
#from parameto import Parametos
import sys



class UNO:
    def __init__(self, gestor_jugadores):
        self.gestor_jugadores = gestor_jugadores
        self.valores = {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "+2": 20, "BLOQUEO": 20, "DIRECCION": 20, "COLOR": 50, "+4": 50
        }
        self.puntos_maximos = 100
        self.n_partidas = 1
        self.n_personas = 2
        self.juego_iniciado = False
        self.modalidad = None  # Para almacenar la modalidad seleccionada

    def menu_principal(self):
        """Menú principal del programa adaptado a Streamlit con botones estilizados."""
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

        # Selección de modalidad
        modalidad = st.selectbox(
            "Estilos de Juego:",
            ("Selecciona una modalidad", "Incremento", "Partidas", "Libre")
        )

        # Dependiendo de la modalidad seleccionada, mostramos los parámetros específicos
        puntos = None
        partidas = None
        flag = False
        if modalidad == "Incremento":
            puntos = self.incremento_parametros()

            # Crear un DataFrame con una sola fila de 0s para los jugadores
            df_incremento = pd.DataFrame([[0] * len(self.gestor_jugadores.jugadores)], columns=self.gestor_jugadores.jugadores.keys())
            # Mostrar la tabla de incremento
            st.subheader("Tabla de Puntuación")
            st.dataframe(df_incremento)

        elif modalidad == "Partidas":
            partidas = self.partidas_parametros()
            # Crear un DataFrame con "-" en lugar de ceros
            df_partidas = pd.DataFrame([[0] * len(self.gestor_jugadores.jugadores)] * partidas, columns=self.gestor_jugadores.jugadores.keys())
            # Mostrar la tabla de partidas
            st.subheader("Tabla de Puntuación")
            st.dataframe(df_partidas)

        elif modalidad == "Libre":
            df_libre = pd.DataFrame([[0] * len(self.gestor_jugadores.jugadores)], columns=self.gestor_jugadores.jugadores.keys())
            st.subheader("Tabla de Puntuación")
            st.dataframe(df_libre)

        # Mostrar el botón de "Confirmar" solo si se seleccionó una modalidad
        if modalidad != "Selecciona una modalidad" and modalidad is not None:
            if st.button("Confirmar"):
                flag = True
                self.modalidad = modalidad  # Guardamos la modalidad seleccionada
                parametros_str = ",".join(map(str, [puntos, partidas]))
                # Establece los parámetros en la URL
                st.experimental_set_query_params(page="jugar_rondas", modalidad=self.modalidad, parametros=parametros_str)
                
                # Forzar recarga de la página
                st.rerun()  # Este método recargará la página y navegará a "jugar_rondas"

        if flag:
            # Esta parte puede no ser necesaria si usas `st.experimental_rerun()` como ya lo has hecho
            if st.button("Jugar rondas"):
                st.experimental_set_query_params(page="jugar_rondas")

        if st.button("Menú Principal"):
            st.write("\n¡Gracias por jugar! Hasta luego.")
            sys.exit()
        

    def incremento_parametros(self):
        """Estilo de juego: incremento."""
        puntos_maximos = st.number_input("Introduce la cantidad máxima de puntos:", min_value=100, step=50)
        self.puntos_maximos = puntos_maximos
        return self.puntos_maximos
        #st.write(f"Modo Incremento activado. Puntos máximos establecidos en: {self.puntos_maximos}")

    def partidas_parametros(self):
        """Estilo de juego: Partidas."""
        n_partidas = st.number_input("Introduce el número de partidas:", min_value=1, step=2)
        while n_partidas % 2 == 0:
            st.warning("El número de partidas debe ser impar. Ajustando a 1.")
            n_partidas = 1
        self.n_partidas = n_partidas
        return self.n_partidas
        #st.write(f"Modo Partidas activado. Número de partidas establecido en: {self.n_partidas}")



    def jugar_rondas(self, modalidad, puntos, partidas):
        """Juega rondas hasta que haya un ganador."""
        st.write(f"Modalidad seleccionada: {modalidad}")
        st.write(f"Puntos máximos: {puntos}")
        st.write(f"Número de partidas: {partidas}")

        # c_partidas = 0
        # tabla_libre = pd.DataFrame(columns=self.gestor_jugadores.jugadores.keys())
        # tabla_incremento = pd.DataFrame(columns=self.gestor_jugadores.jugadores.keys())
        # tabla_partidas = pd.DataFrame('', index=range(self.n_partidas), columns=self.gestor_jugadores.jugadores.keys())

        # # Inicializar la clave de estado de sesión para el ganador si no está definida
        # if 'ganador' not in st.session_state:
        #     st.session_state.ganador = None

        # if 'c_partidas' not in st.session_state:
        #     st.session_state.c_partidas = 0

        # # Mostrar el selectbox fuera del bucle, para seleccionar al ganador de la ronda
        # ganador = st.selectbox(
        #     "Selecciona el ganador de la ronda:",
        #     list(self.gestor_jugadores.jugadores.keys()),
        #     key="ganador_selectbox"
        # )

        # # Botón para enviar la selección y avanzar al siguiente paso
        # if st.button("Enviar selección"):
        #     # Guardamos el ganador en session_state
        #     st.session_state.ganador = ganador

        #     # Llamar a otra función con la lógica de la ronda
        #     self.procesar_ronda(modalidad, tabla_partidas, tabla_libre, tabla_incremento)




    def procesar_ronda(self, modalidad, tabla_partidas, tabla_libre, tabla_incremento):
        """Procesa la lógica de la ronda después de seleccionar al ganador y hacer clic en Enviar."""
        # Obtiene el ganador desde session_state
        ganador = st.session_state.ganador
        c_partidas = st.session_state.c_partidas

        if ganador == "Done":
            max_partidas = max(self.gestor_jugadores.jugadores, key=self.gestor_jugadores.jugadores.get)
            os.system('cls' if os.name == 'nt' else 'clear')
            st.success(f"El ganador es {max_partidas} con {self.gestor_jugadores.jugadores[max_partidas]} puntos.")
            
            # Restablecer los valores de todos los jugadores a 0
            for jugador in self.gestor_jugadores.jugadores:
                self.gestor_jugadores.jugadores[jugador] = 0
            
            # Mostrar la tabla de "partidas"
            st.subheader("Modalidad Partidas")
            st.dataframe(tabla_partidas)
            return

        # Lógica del modo de juego "partidas"
        if modalidad == "partidas":
            self.gestor_jugadores.jugadores[ganador] += 1
            c_partidas += 1

            # Actualizar la tabla de "partidas" con una "X" en la celda correspondiente
            tabla_partidas.loc[c_partidas - 1, ganador] = 'X'
            
            # Mostrar la tabla de "partidas" después de cada ronda
            st.subheader("Modalidad Partidas")
            st.dataframe(tabla_partidas)

            # Si se alcanzan las partidas máximas o un jugador gana más de la mitad de las rondas, finalizar
            if c_partidas == self.n_partidas or self.gestor_jugadores.jugadores[ganador] > self.n_partidas // 2:
                max_partidas = max(self.gestor_jugadores.jugadores, key=self.gestor_jugadores.jugadores.get)
                st.success(f"El ganador es {max_partidas} con {self.gestor_jugadores.jugadores[max_partidas]} partidas ganadas.")
                
                # Restablecer los valores de todos los jugadores a 0
                for jugador in self.gestor_jugadores.jugadores:
                    self.gestor_jugadores.jugadores[jugador] = 0
                
                # Mostrar la tabla de "partidas" final
                st.subheader("Modalidad Partidas")
                st.dataframe(tabla_partidas)
                return

        # Lógica del modo de juego "incremento"
        elif modalidad == "incremento":
            carta = st.selectbox(f"Selecciona la carta jugada (o 'Done' para terminar):", list(self.valores.keys()), key=f"carta_ronda_{c_partidas}_{modalidad}")
            if carta == "Done":
                return

            # Incrementar puntos en "incremento"
            self.gestor_jugadores.jugadores[ganador] += self.valores[carta]
            if self.gestor_jugadores.jugadores[ganador] >= self.puntos_maximos:
                st.success(f"El ganador del juego es {ganador}. ¡Enhorabuena!")
                
                # Restablecer los valores de todos los jugadores a 0
                for jugador in self.gestor_jugadores.jugadores:
                    self.gestor_jugadores.jugadores[jugador] = 0
                
                # Añadir la fila correspondiente en la tabla de incremento
                tabla_incremento = tabla_incremento.append(self.gestor_jugadores.jugadores, ignore_index=True)
                st.subheader("Modalidad Incremento")
                st.dataframe(tabla_incremento)
                return

        # Lógica del modo de juego "libre"
        elif modalidad == "libre":
            carta = st.selectbox(f"Selecciona la carta jugada (o 'Done' para terminar):", list(self.valores.keys()), key=f"carta_ronda_{c_partidas}_{modalidad}")
            if carta == "Done":
                return
            
            self.gestor_jugadores.jugadores[ganador] += self.valores[carta]

            # Añadir la fila correspondiente en la tabla de libre
            tabla_libre = tabla_libre.append(self.gestor_jugadores.jugadores, ignore_index=True)
            st.subheader("Modalidad Libre")
            st.dataframe(tabla_libre)

        # Guardar los cambios después de cada ronda
        self.gestor_jugadores.guardar_jugadores()





# Punto de entrada principal
if __name__ == "__main__":
    # Crear instancias de las clases necesarias
    gestor_jugadores = {}  # Deberías agregar la lógica para gestionar los jugadores
    gestor_UNO = UNO(gestor_jugadores)

    # Obtener parámetros de la URL
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", ["main"])[0]

    # Redirigir según el parámetro `page`
    if page == "main":
        gestor_UNO.menu_principal()
    elif page == "jugar_rondas":
        st.write("Jugando rondas...")
        modalidad = query_params.get("modalidad", [""])[0]
        # Recupera el parámetro 'parametros' como una cadena
        parametros_str = query_params.get("parametros", [""])[0]
        # Convierte la cadena a lista
        parametros = list(map(int, parametros_str.split(",")))
        # Llama a la función de juego con los parámetros recuperados
        #gestor_UNO.jugar_rondas(modalidad, parametros[0], parametros[1])











