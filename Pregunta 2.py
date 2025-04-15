import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL de Macrotrends con ingresos de Tesla
url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"

# Usar headers para evitar bloqueo
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Obtener contenido de la página
html_data = requests.get(url, headers=headers).text

# Parsear HTML
soup = BeautifulSoup(html_data, "html.parser")

# Buscar todas las tablas con clase específica
tables = soup.find_all("table", {"class": "historical_data_table table"})

# Crear DataFrame vacío
tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Buscar la tabla con "Tesla Quarterly Revenue"
for table in tables:
    if "Tesla Quarterly Revenue" in table.text:
        rows = table.find_all("tr")
        for row in rows[1:]:  # Saltar la cabecera
            cols = row.find_all("td")
            if len(cols) == 2:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip().replace("$", "").replace(",", "")
                if revenue:
                    tesla_revenue = pd.concat([
                        tesla_revenue,
                        pd.DataFrame([{"Date": date, "Revenue": revenue}])
                    ], ignore_index=True)

# Mostrar las últimas 5 filas
print(tesla_revenue.tail())