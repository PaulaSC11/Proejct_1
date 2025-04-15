import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL de Macrotrends para GameStop
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"

# Usar headers para evitar ser bloqueados
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Obtener el contenido de la página
html_data = requests.get(url, headers=headers).text

# Parsear HTML con BeautifulSoup
soup = BeautifulSoup(html_data, "html.parser")

# Buscar las tablas con clase específica
tables = soup.find_all("table", {"class": "historical_data_table table"})

# Crear un DataFrame vacío
gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])

# Buscar la tabla de "GameStop Quarterly Revenue"
for table in tables:
    if "GameStop Quarterly Revenue" in table.text:
        rows = table.find_all("tr")
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) == 2:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip().replace("$", "").replace(",", "")
                if revenue:
                    gme_revenue = pd.concat([
                        gme_revenue,
                        pd.DataFrame([{"Date": date, "Revenue": revenue}])
                    ], ignore_index=True)

# Mostrar las últimas 5 filas del DataFrame
print(gme_revenue.tail())
