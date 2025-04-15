import yfinance as yf
import pandas as pd

# Descargar los datos bursátiles de GameStop (GME)
gme = yf.Ticker("GME")

# Obtener el historial completo y restablecer el índice
gme_history = gme.history(period="max")
gme_data = gme_history.reset_index()

# Mostrar las primeras 5 filas
print(gme_data.head())