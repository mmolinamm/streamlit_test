import streamlit as st
import pandas as pd             # Para trabajar con tablas
import scipy.stats              # Para lanzar la moneda
import time                     # Para animación

# Inicializamos variables persistentes (solo la primera vez)
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0  # Contador de experimentos

if 'df_experiment_results' not in st.session_state:
    # Creamos un DataFrame vacío con columnas definidas
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Slider y botón para controlar la simulación
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

# Gráfico de línea que se irá actualizando
chart = st.line_chart([0.5])

# Función para lanzar la moneda n veces y graficar la media acumulada
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

# Cuando se presiona el botón, lanzamos la moneda y guardamos el resultado
if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    
    # Aumentamos el contador de experimentos
    st.session_state['experiment_no'] += 1

    # Ejecutamos el experimento
    mean = toss_coin(number_of_trials)

    # Creamos una fila nueva con los datos del experimento
    new_row = pd.DataFrame([[st.session_state['experiment_no'], number_of_trials, mean]],
                           columns=['no', 'iteraciones', 'media'])

    # Agregamos esa fila al historial (DataFrame)
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        new_row
    ], ignore_index=True)

# Mostramos la tabla con todos los resultados
st.subheader("Historial de resultados")
st.write(st.session_state['df_experiment_results'])


