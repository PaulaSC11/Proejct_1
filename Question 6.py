import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "iframe"

# Ignorar advertencias
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# 1. Descargar datos bursátiles de GameStop (Pregunta 3)
gme = yf.Ticker("GME")
gme_data = gme.history(period="max").reset_index()
print("✅ Primeras 5 filas de gme_data:")
print(gme_data.head())

# 2. Web Scraping de los ingresos de GameStop (Pregunta 4)
url = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"
headers = {"User-Agent": "Mozilla/5.0"}
html_data = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_data, "html.parser")

gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
tables = soup.find_all("table", {"class": "historical_data_table table"})

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

print("\n✅ Últimas 5 filas de gme_revenue:")
print(gme_revenue.tail())

# 3. Función para graficar (la misma que usamos con Tesla)
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=.3
    )

    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig.add_trace(go.Scatter(
        x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
        y=stock_data_specific.Close.astype("float"),
        name="Share Price"), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
        y=revenue_data_specific.Revenue.astype("float"),
        name="Revenue"), row=2, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )

    fig.show()
    fig.write_html("gme_graph.html", auto_open=True)  # Abre en navegador

# 4. Llamar la función para graficar
make_graph(gme_data, gme_revenue, "GameStop Stock & Revenue")
