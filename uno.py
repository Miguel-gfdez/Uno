import streamlit as st
import os
from gestionar_jugadores import GestorJugadores
import pandas as pd
import sys
import time



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

        if "juego" not in st.session_state:
            st.session_state.juego = None
        if "modalidad" not in st.session_state:
            st.session_state.modalidad = None
        if "parametros" not in st.session_state:
            st.session_state.parametros = []
        if "cartas_seleccionadas" not in st.session_state or not isinstance(st.session_state.cartas_seleccionadas, dict):
            st.session_state.cartas_seleccionadas = {key: 0 for key in self.valores.keys()}
        if "contador_partidas" not in st.session_state:
            st.session_state.contador_partidas = 0
        if "jugadores" not in st.session_state:
            st.session_state.jugadores = self.gestor_jugadores.jugadores
        if "ganadores_lista" not in st.session_state:
            st.session_state.ganadores_lista = []





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


    def seleccionar_ganador(self):
        """Juega rondas hasta que haya un ganador."""
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


        # Mostrar el selectbox fuera del bucle, para seleccionar al ganador de la ronda
        puntos_ronda = 0
        ganador = st.selectbox(
                "Selecciona el ganador de la ronda:",
                ["Selecciona un Jugador..."] + list(self.gestor_jugadores.jugadores.keys()),  # El primer elemento es una cadena vacía
                key="ganador_selectbox"
            )
        

        modalidad = st.session_state.modalidad

        if modalidad == "Incremento":
            # Nombres de los botones
            nombres_botones = list(self.valores.keys())

            # Contenedor para la primera fila de botones
            fila1 = st.columns(7)
            for i, col in enumerate(fila1):
                with col:
                    if st.button(nombres_botones[i]):
                        st.session_state.cartas_seleccionadas[nombres_botones[i]] += 1  # Incrementa el valor

            # Contenedor para la segunda fila de botones
            fila2 = st.columns(7)
            for i, col in enumerate(fila2):
                with col:
                    if st.button(nombres_botones[i + 7]):
                        st.session_state.cartas_seleccionadas[nombres_botones[i + 7]] += 1  # Incrementa el valor

            # Convertir los valores cartas_seleccionadas a un formato adecuado para mostrar en tabla
            selected_values = list(st.session_state.cartas_seleccionadas.items())  # Convertir a lista de tuplas

            # Crear un DataFrame para mostrar los valores de manera estructurada
            nombres = [key for key, _ in selected_values]
            veces_pulsadas = [value for _, value in selected_values]

            # Crear un DataFrame donde los nombres de los botones sean las columnas
            data = {
                "Botones": nombres,  # Columna con los nombres de los botones
                "": veces_pulsadas  # Columna con los valores de veces pulsadas
            }
            df = pd.DataFrame(data)

            # Transponer el DataFrame para hacerlo horizontal
            df_transpuesta = df.set_index("Botones").T  # Transponemos el DataFrame
            # Mostrar la tabla horizontal
            st.table(df_transpuesta)

            puntos_ronda = sum(self.valores[key] * value for key, value in st.session_state.cartas_seleccionadas.items())

            # Mostrar los puntos totales
            st.write(f"Puntos Totales: {puntos_ronda}")

        # Mostrar dos botones seguidos
        col1, col2 = st.columns(2)  # Crear dos columnas para los botones

        # Primer botón
        with col1:
            if st.button("Confirmar Datos"):
                st.session_state.ganadores_lista.append(ganador)
                if modalidad == "Partidas":
                    st.session_state.jugadores[ganador] += 1
                    self.gestor_jugadores.jugadores = st.session_state.jugadores
                    self.gestor_jugadores.guardar_jugadores()
                    st.experimental_set_query_params(page="procesar rondas", ganador=ganador, puntos_ronda=puntos_ronda)
                    st.rerun()
                elif modalidad == "Incremento":
                    st.session_state.jugadores[ganador] += puntos_ronda
                    self.gestor_jugadores.jugadores = st.session_state.jugadores
                    self.gestor_jugadores.guardar_jugadores()
                    st.experimental_set_query_params(page="procesar rondas", ganador=ganador, puntos_ronda=puntos_ronda)
                    st.rerun()
                elif modalidad == "Libre":
                    pass

        # Segundo botón
        with col2:
            if st.button("Cancelar"):
                st.experimental_set_query_params(page="main")
                st.rerun()
                


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


    def procesar_ronda(self, ganador, puntos_ronda):
        n_partidas = int(st.session_state.parametros[1]) if st.session_state.parametros[1] is not None else None
        puntos_maximos = int(st.session_state.parametros[0]) if st.session_state.parametros[0] is not None else None
        puntos_ronda = int(puntos_ronda)
        modalidad = st.session_state.modalidad
        c_partidas = st.session_state.contador_partidas
        del st.session_state['cartas_seleccionadas']

        # Lógica del modo de juego "partidas"
        jugadores = list(self.gestor_jugadores.jugadores.keys())  # Obtener los nombres de los jugadores

        # Crear un DataFrame con tantas filas como n_partidas y tantas columnas como jugadores
        tabla_partidas = pd.DataFrame("", index=range(self.n_partidas), columns=jugadores)


        if modalidad == "Partidas":
            if st.session_state.contador_partidas >= n_partidas or st.session_state.jugadores[ganador] > n_partidas // 2: # Controlar el fin de la partida
                max_partidas = max(st.session_state.jugadores, key=st.session_state.jugadores.get)
                st.success(f"El ganador es {max_partidas} con {st.session_state.jugadores[max_partidas]}/{n_partidas} partidas ganadas.")
                st.subheader("Resultados Finales")
                # Usar la lista de ganadores para colocar las "X" en las filas correspondientes
                for i, ganador in enumerate(st.session_state.ganadores_lista):
                    tabla_partidas.loc[i, ganador] = 'X'

                # Mostrar la tabla actualizada
                st.dataframe(tabla_partidas.fillna(" "))
                if st.button("Finalizar"):
                    for jugador in st.session_state.jugadores:
                        st.session_state.jugadores[jugador] = 0
                    self.gestor_jugadores.jugadores = st.session_state.jugadores
                    self.gestor_jugadores.guardar_jugadores()
                    self.gestor_jugadores.guardar_historial(st.session_state.juego, modalidad, max_partidas)
                    del st.session_state["jugadores"]
                    del st.session_state["modalidad"]
                    del st.session_state["parametros"]
                    del st.session_state["contador_partidas"]
                    del st.session_state["ganadores_lista"]
                    del st.session_state["juego"]
                    st.experimental_set_query_params(page="main")
                    st.rerun()
                else:
                    return
            else:
                
                # Usar la lista de ganadores para colocar las "X" en las filas correspondientes
                for i, ganador in enumerate(st.session_state.ganadores_lista):
                    tabla_partidas.loc[i, ganador] = 'X'

                # Mostrar la tabla actualizada
                st.dataframe(tabla_partidas)
                
                
        if st.button("Continuar"):
            st.session_state.contador_partidas += 1
            st.experimental_set_query_params(page="seleccionar ganador")
            st.rerun()
        else:
            return


            # Si se alcanzan las partidas máximas o un jugador gana más de la mitad de las rondas, finalizar
            # if c_partidas == n_partidas or self.gestor_jugadores.jugadores[ganador] > n_partidas // 2:
            #     max_partidas = max(self.gestor_jugadores.jugadores, key=self.gestor_jugadores.jugadores.get)
            #     st.success(f"El ganador es {max_partidas} con {self.gestor_jugadores.jugadores[max_partidas]} partidas ganadas.")
                
            #     # Restablecer los valores de todos los jugadores a 0
            #     for jugador in self.gestor_jugadores.jugadores:
            #         self.gestor_jugadores.jugadores[jugador] = 0
                
            #     # Mostrar la tabla de "partidas" final
            #     st.subheader("Modalidad Partidas (Final)")
            #     st.dataframe(tabla_partidas)
            #     return
            





            

        # Lógica del modo de juego "incremento"
        # elif modalidad == "incremento":
        #     carta = st.selectbox(f"Selecciona la carta jugada (o 'Done' para terminar):", list(self.valores.keys()), key=f"carta_ronda_{c_partidas}_{modalidad}")
        #     if carta == "Done":
        #         return

        #     # Incrementar puntos en "incremento"
        #     self.gestor_jugadores.jugadores[ganador] += self.valores[carta]
        #     if self.gestor_jugadores.jugadores[ganador] >= self.puntos_maximos:
        #         st.success(f"El ganador del juego es {ganador}. ¡Enhorabuena!")
                
        #         # Restablecer los valores de todos los jugadores a 0
        #         for jugador in self.gestor_jugadores.jugadores:
        #             self.gestor_jugadores.jugadores[jugador] = 0
                
        #         # Añadir la fila correspondiente en la tabla de incremento
        #         tabla_incremento = tabla_incremento.append(self.gestor_jugadores.jugadores, ignore_index=True)
        #         st.subheader("Modalidad Incremento")
        #         st.dataframe(tabla_incremento)
        #         return

        # # Lógica del modo de juego "libre"
        # elif modalidad == "libre":
        #     carta = st.selectbox(f"Selecciona la carta jugada (o 'Done' para terminar):", list(self.valores.keys()), key=f"carta_ronda_{c_partidas}_{modalidad}")
        #     if carta == "Done":
        #         return
            
        #     self.gestor_jugadores.jugadores[ganador] += self.valores[carta]

        #     # Añadir la fila correspondiente en la tabla de libre
        #     tabla_libre = tabla_libre.append(self.gestor_jugadores.jugadores, ignore_index=True)
        #     st.subheader("Modalidad Libre")
        #     st.dataframe(tabla_libre)

        # # Guardar los cambios después de cada ronda
        # self.gestor_jugadores.guardar_jugadores()


    def menu_Uno(self, juego):
        st.session_state.juego = juego
        puntos = 0
        partidas = 0
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
            ["Selecciona una modalidad..."] + ["Incremento", "Partidas", "Libre"],  # Lista correcta de modalidades
            key="modalidad_selectbox"
        )

        # Dependiendo de la modalidad seleccionada, mostramos los parámetros específicos
        if modalidad == "Incremento":
            puntos = self.incremento_parametros()

        elif modalidad == "Partidas":
            partidas = self.partidas_parametros()

        # Mostrar el botón de "Confirmar" solo si se seleccionó una modalidad válida
        if modalidad != "Selecciona una modalidad..." and modalidad is not None:
            if st.button("Confirmar"):                
                # Guardamos los valores en session_state
                st.session_state.modalidad = modalidad
                st.session_state.parametros = [puntos, partidas]
                st.experimental_set_query_params(page="seleccionar ganador")
                st.rerun()

        if st.button("Volver al Menú Principal"):
            st.experimental_set_query_params(page="main")
            st.rerun()





def run():
    """Ejecuta la gestión de jugadores."""
    uno = UNO()
    uno.menu_Uno()







