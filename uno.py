import streamlit as st
import os
from gestionar_jugadores import GestorJugadores
import pandas as pd
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
        self.puntos = None
        self.partidas = None


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


    def menu_Uno(self):
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
            ("Selecciona una modalidad", "Incremento", "Partidas", "Libre")
        )
        # Dependiendo de la modalidad seleccionada, mostramos los parámetros específicos
        
        if modalidad == "Incremento":
            puntos = self.incremento_parametros()

        elif modalidad == "Partidas":
            partidas = self.partidas_parametros()

        # Mostrar el botón de "Confirmar" solo si se seleccionó una modalidad
        if modalidad != "Selecciona una modalidad" and modalidad is not None:
            if st.button("Confirmar"):
                self.modalidad = modalidad  # Guardamos la modalidad seleccionada
                parametros_str = ",".join(map(str, [puntos, partidas]))
                # Establece los parámetros en la URL
                st.experimental_set_query_params(page="jugar rondas", modalidad=self.modalidad, parametros=parametros_str)
                st.rerun()

        if st.button("Volver al Menú Principal"):
            st.experimental_set_query_params(page="main")
            st.rerun()




def run():
    """Ejecuta la gestión de jugadores."""
    uno = UNO()
    uno.menu_Uno()







