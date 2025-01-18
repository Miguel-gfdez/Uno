import streamlit as st
import pandas as pd



class UNO:
    def __init__(self, gestor_jugadores):
        self.gestor_jugadores = gestor_jugadores
        self.valores_UNO = {
            "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
            "+2": 20, "BLOQUEO": 20, "DIRECCION": 20, "COLOR": 50, "+4": 50
        }
        self.valores_UNO_FLIP = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "+1":10, "+5":20, "DIRECCION":20, "BLOQUEO":20, "FLIP":20, "RETORNO":30, "COLOR":40, "+2":50, "ELEGIR":60}
        self.valores_DOS = {"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "COMODIN":20, "#":40}
        

        self.valores = {}
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
        modalidad = st.session_state.modalidad
        if modalidad == "Libre":
            st.warning("Modalidad no disponible")

        """Juega rondas hasta que haya un ganador."""
        if st.session_state.juego == "UNO":
            self.valores = self.valores_UNO
        elif st.session_state.juego == "UNO FLIP":
            self.valores = self.valores_UNO_FLIP
        elif st.session_state.juego == "DOS":
            self.valores = self.valores_DOS

        # Actualizar `cartas_seleccionadas` con los nuevos valores
        if (
            "cartas_seleccionadas" not in st.session_state
            or not isinstance(st.session_state.cartas_seleccionadas, dict)
            or set(st.session_state.cartas_seleccionadas.keys()) != set(self.valores.keys())
        ):
            st.session_state.cartas_seleccionadas = {key: 0 for key in self.valores.keys()}

        st.markdown("""
            <style>
                .css-1emrehy.edgvbvh3 { 
                    font-size: 30px; 
                    height: 60px; 
                    width: 100%;
                    border-radius: 10px;
                }
                .stButton > button {
                    width: 100%;
                    height: 70px;
                    border-radius: 10px;
                    font-size: 15px;
                    background-color: #4CAF50;
                    color: white;
                }
                .stButton > button:hover {
                    background-color: #45a049;
                }
            </style>
            """, unsafe_allow_html=True)

        puntos_ronda = 0
        jugadores = self.gestor_jugadores.cargar_jugadores()

        if not jugadores:
            st.warning("No hay jugadores cargados. Por favor, añada jugadores antes de continuar.")
            return

        ganador = st.selectbox(
            "Selecciona el ganador de la ronda:",
            ["Selecciona un Jugador..."] + list(jugadores.keys()),
            key="ganador_selectbox"
        )

        st.session_state.jugadores = jugadores

        if modalidad == "Incremento":
            nombres_botones = list(self.valores.keys())
            nombres_botones = [key.replace("#", "&#35;") for key in self.valores.keys()]
        
            if 'historial' not in st.session_state:
                st.session_state.historial = []
            
            total_botones = len(nombres_botones)
            mitad = (total_botones + 1) // 2

            if mitad > 0:
                fila1 = st.columns(mitad)
                for i, col in enumerate(fila1):
                    if i < len(nombres_botones):
                        with col:
                            if st.button(nombres_botones[i]):
                                st.session_state.cartas_seleccionadas[nombres_botones[i]] += 1
                                st.session_state.historial.append(('incremento', nombres_botones[i]))

            restantes = total_botones - mitad
            if restantes > 0:
                fila2 = st.columns(restantes)
                for i, col in enumerate(fila2):
                    if i + mitad < len(nombres_botones):
                        with col:
                            if st.button(nombres_botones[i + mitad]):
                                st.session_state.cartas_seleccionadas[nombres_botones[i + mitad]] += 1
                                st.session_state.historial.append(('incremento', nombres_botones[i + mitad]))

            selected_values = list(st.session_state.cartas_seleccionadas.items())
            nombres = [key for key, _ in selected_values]
            veces_pulsadas = [value for _, value in selected_values]
            data = {"Botones": nombres, "": veces_pulsadas}
            df = pd.DataFrame(data)
            df_transpuesta = df.set_index("Botones").T
            st.table(df_transpuesta)

            puntos_ronda = sum(self.valores[key] * value for key, value in st.session_state.cartas_seleccionadas.items())
            st.write(f"Puntos Totales: {puntos_ronda}")

            if st.button("Deshacer"):
                if st.session_state.historial:
                    last_action = st.session_state.historial.pop()
                    if last_action[0] == 'incremento':
                        boton_presionado = last_action[1]
                        st.session_state.cartas_seleccionadas[boton_presionado] -= 1
                    st.write(f"Puntos Totales: {sum(self.valores[key] * value for key, value in st.session_state.cartas_seleccionadas.items())}")

        col1, col2 = st.columns(2)
        with col2:
            if st.button("Cancelar"):
                for jugador in st.session_state.jugadores:
                    st.session_state.jugadores[jugador] = 0
                self.gestor_jugadores.jugadores = st.session_state.jugadores
                self.gestor_jugadores.guardar_jugadores()
                del st.session_state["jugadores"]
                del st.session_state["modalidad"]
                del st.session_state["parametros"]
                del st.session_state["contador_partidas"]
                del st.session_state["ganadores_lista"]
                del st.session_state["juego"]
                st.session_state.page = "main"
                st.rerun()
        try:
            with col1:
                if st.button("Confirmar Datos"):
                    if ganador not in st.session_state.jugadores:
                        raise ValueError("¡Seleccione un jugador válido!")
                    
                    st.session_state.ganadores_lista.append(ganador)
                    if modalidad == "Partidas":
                        st.session_state.jugadores[ganador] += 1
                    elif modalidad == "Incremento":
                        st.session_state.jugadores[ganador] += puntos_ronda

                    self.gestor_jugadores.jugadores = st.session_state.jugadores
                    self.gestor_jugadores.guardar_jugadores()
                    st.session_state.page = "procesar rondas"
                    st.rerun()
        except Exception as e:
            st.warning("Por favor, seleccione un jugador válido para continuar.")
            st.warning(e)

                
    def procesar_ronda(self, ganador, puntos_ronda):
        n_partidas = int(st.session_state.parametros[1]) if st.session_state.parametros[1] is not None else None
        puntos_maximos = int(st.session_state.parametros[0]) if st.session_state.parametros[0] is not None else None
        puntos_ronda = int(puntos_ronda)
        modalidad = st.session_state.modalidad
        c_partidas = st.session_state.contador_partidas
        del st.session_state["cartas_seleccionadas"]

        # Lógica del modo de juego "partidas"
        jugadores = list(self.gestor_jugadores.jugadores.keys())  # Obtener los nombres de los jugadores

        # Crear un DataFrame con tantas filas como n_partidas y tantas columnas como jugadores
        tabla_partidas = pd.DataFrame("", index=range(self.n_partidas), columns=jugadores)

        if modalidad == "Partidas":
            if st.session_state.contador_partidas >= n_partidas or st.session_state.jugadores[ganador] > n_partidas // 2:  # Controlar el fin de la partida
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
                    # Limpiar el estado de sesión
                    keys_to_delete = [
                        "jugadores", "modalidad", "parametros", "contador_partidas", 
                        "ganadores_lista", "juego"
                    ]
                    for key in keys_to_delete:
                        del st.session_state[key]
                    st.session_state.page = "main"  # Actualizamos la página
                    st.rerun()
                else:
                    return
            else:
                # Usar la lista de ganadores para colocar las "X" en las filas correspondientes
                for i, ganador in enumerate(st.session_state.ganadores_lista):
                    tabla_partidas.loc[i, ganador] = 'X'

                # Mostrar la tabla actualizada
                st.dataframe(tabla_partidas.fillna(" "))

        elif modalidad == "Incremento":
            # Verificar si el jugador ha alcanzado los puntos máximos
            if st.session_state.jugadores[ganador] >= puntos_maximos:
                max_jugador = max(st.session_state.jugadores, key=st.session_state.jugadores.get)
                st.success(f"El ganador es {max_jugador} con {st.session_state.jugadores[max_jugador]} puntos.")
                st.subheader("Resultados Finales")

                # Crear la tabla de resultados con los puntos
                tabla_partidas = pd.DataFrame(index=jugadores, columns=["Puntos"])

                # Rellenar la tabla con los puntos de cada jugador
                for jugador in jugadores:
                    tabla_partidas.loc[jugador, "Puntos"] = st.session_state.jugadores[jugador]

                # Mostrar la tabla con los puntos
                st.dataframe(tabla_partidas)

                # Botón para finalizar el juego
                if st.button("Finalizar"):
                    # Resetear los puntajes de los jugadores
                    for jugador in st.session_state.jugadores:
                        st.session_state.jugadores[jugador] = 0
                    self.gestor_jugadores.jugadores = st.session_state.jugadores
                    self.gestor_jugadores.guardar_jugadores()
                    self.gestor_jugadores.guardar_historial(st.session_state.juego, modalidad, max_jugador)
                    # Limpiar el estado de sesión
                    keys_to_delete = [
                        "jugadores", "modalidad", "parametros", "contador_partidas", 
                        "ganadores_lista", "juego"
                    ]
                    for key in keys_to_delete:
                        del st.session_state[key]
                    st.session_state.page = "main"  # Actualizamos la página
                    st.rerun()
                else:
                    return
            else:
                # Mostrar la tabla actualizada con los puntos acumulados
                st.subheader("Puntos Acumulados")
                tabla_partidas = pd.DataFrame(index=jugadores, columns=["Puntos"])

                # Rellenar la tabla con los puntos de cada jugador
                for jugador in jugadores:
                    tabla_partidas.loc[jugador, "Puntos"] = st.session_state.jugadores[jugador]

                # Mostrar la tabla con los puntos
                st.dataframe(tabla_partidas)

        if st.button("Continuar"):
            st.session_state.contador_partidas += 1
            st.session_state.page = "seleccionar ganador"  # Actualizamos la página
            st.rerun()
        else:
            return



    def menu_Uno(self, juego):
        # Guardar el juego seleccionado en session_state
        st.session_state.juego = juego
        self.valores = (
            self.valores_UNO 
            if juego == "UNO" 
            else self.valores_UNO_FLIP 
            if juego == "UNO FLIP" 
            else self.valores_DOS
        )
        puntos = 0
        partidas = 0

        # Estilo personalizado
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
                # Guardar modalidad y parámetros en session_state
                st.session_state.modalidad = modalidad
                if modalidad == "Libre":
                    st.warning("Modalidad no disponible")
                else:
                    st.session_state.parametros = [puntos, partidas]
                    st.session_state.page = "seleccionar ganador"  # Actualizamos el estado de la página
                    st.rerun()

        # Botón para volver al menú principal
        if st.button("Volver al Menú Principal"):
            st.session_state.page = "main"  # Actualizamos el estado de la página
            st.rerun()



def run():
    """Ejecuta la gestión de jugadores."""
    uno = UNO()
    uno.menu_Uno()







