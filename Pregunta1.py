import yfinance as yf
import pandas as pd

# Descargar datos bursátiles de Tesla
tesla = yf.Ticker("TSLA")

# Obtener el historial completo y restablecer el índice
tesla_history = tesla.history(period="max")
tesla_data = tesla_history.reset_index()

# Mostrar las primeras 5 filas
print(tesla_data.head())