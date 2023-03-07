import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_white"

control_data = pd.read_csv("control_group.csv", sep = ";")
test_data = pd.read_csv("test_group.csv", sep = ";")

print(control_data.head())
print(test_data.head())

#готовим данные
control_data.columns = ["Campaign Name", "Date", "Amount Spent","Number of Impressions", "Reach", "Website Clicks","Searches Received", "Content Viewed", "Added to Cart", "Purchases"]

test_data.columns = ["Campaign Name", "Date", "Amount Spent", "Number of Impressions", "Reach", "Website Clicks", "Searches Received", "Content Viewed", "Added to Cart", "Purchases"]

print(control_data.isnull().sum())
print(test_data.isnull().sum())

#заполняем пустые значения
control_data["Number of Impressions"].fillna(value=control_data["Number of Impressions"].mean(), inplace=True)
control_data["Reach"].fillna(value=control_data["Reach"].mean(), inplace=True)
control_data["Website Clicks"].fillna(value=control_data["Website Clicks"].mean(), inplace=True)
control_data["Searches Received"].fillna(value=control_data["Searches Received"].mean(), inplace=True)
control_data["Content Viewed"].fillna(value=control_data["Content Viewed"].mean(), inplace=True)
control_data["Added to Cart"].fillna(value=control_data["Added to Cart"].mean(), inplace=True)
control_data["Purchases"].fillna(value=control_data["Purchases"].mean(), inplace=True)

#создаю новый датасет
ab_data = control_data.merge(test_data, how="outer").sort_values(["Date"])
ab_data = ab_data.reset_index(drop=True)
print(ab_data.head())

print(ab_data["Campaign Name"].value_counts())

#А/Б тесты, чтобы найти лучшую маркетинговую стратегию

#сумма, затраченная на обе кампании
figure = px.scatter(data_frame = ab_data,
                    x="Number of Impressions",
                    y="Amount Spent",
                    size="Amount Spent",
                    color= "Campaign Name",
                    trendline="ols")
figure.show()

#количество поисковых запросов, выполненных на веб-сайте в рамках обеих кампаний
label = ["Total Searches from Control Campaign",
         "Total Searches from Test Campaign"]
counts = [sum(control_data["Searches Received"]),
          sum(test_data["Searches Received"])]
colors = ['gold','lightgreen']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Searches')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30,marker=dict(colors=colors,line=dict(color='black', width=3)))
fig.show()

#количество кликов по веб-сайту в обеих кампаниях
label = ["Website Clicks from Control Campaign",
         "Website Clicks from Test Campaign"]
counts = [sum(control_data["Website Clicks"]),
          sum(test_data["Website Clicks"])]
colors = ['gold','lightgreen']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Website Clicks')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30, marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()

#количество контента, просмотренного после перехода на веб-сайт в обеих кампаниях
label = ["Content Viewed from Control Campaign",
         "Content Viewed from Test Campaign"]
counts = [sum(control_data["Content Viewed"]),
          sum(test_data["Content Viewed"])]
colors = ['gold','lightgreen']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Content Viewed')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30, marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()

#количество товаров, добавленных в корзину в рамках обеих кампаний
label = ["Products Added to Cart from Control Campaign",
         "Products Added to Cart from Test Campaign"]
counts = [sum(control_data["Added to Cart"]),
          sum(test_data["Added to Cart"])]
colors = ['gold','lightgreen']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Added to Cart')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30, marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()

#сумма, потраченная на обе кампании
label = ["Amount Spent in Control Campaign",
         "Amount Spent in Test Campaign"]
counts = [sum(control_data["Amount Spent"]),
          sum(test_data["Amount Spent"])]
colors = ['gold','lightgreen']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Amount Spent')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30,marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()

#покупки, сделанные в рамках обеих кампаний
label = ["Purchases Made by Control Campaign",
         "Purchases Made by Test Campaign"]
counts = [sum(control_data["Purchases"]),
          sum(test_data["Purchases"])]
colors = ['gold','lightgreen']
fig = go.Figure(data=[go.Pie(labels=label, values=counts)])
fig.update_layout(title_text='Control Vs Test: Purchases')
fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=30,marker=dict(colors=colors, line=dict(color='black', width=3)))
fig.show()

#анализируем метрики

#количество кликов по веб-сайту и просмотренный контент в обеих кампаниях. control campaign побеждает!!!
figure = px.scatter(data_frame = ab_data,
                    x="Content Viewed",
                    y="Website Clicks",
                    size="Website Clicks",
                    color= "Campaign Name",
                    trendline="ols")
figure.show()

#количество просмотренного контента и количество товаров, добавленных в корзину в обеих кампаниях. control campaign снова побеждает!
figure = px.scatter(data_frame = ab_data,
                    x="Added to Cart",
                    y="Content Viewed",
                    size="Added to Cart",
                    color= "Campaign Name",
                    trendline="ols")
figure.show()

#количество товаров, добавленных в корзину, и количество продаж в обеих кампаниях
figure = px.scatter(data_frame = ab_data,
                    x="Purchases",
                    y="Added to Cart",
                    size="Purchases",
                    color= "Campaign Name",
                    trendline="ols")
figure.show()

'''Из приведенных выше A/B-тестов мы обнаружили, что контрольная кампания привела к увеличению продаж и вовлеченности посетителей. 
В рамках контрольной кампании было просмотрено больше товаров, что привело к увеличению количества товаров в корзине и увеличению продаж. Но частота разговоров о товарах в корзине выше в тестовой кампании. 
Тестовая кампания привела к увеличению продаж в зависимости от просмотренных и добавленных в корзину товаров. А контрольная кампания в целом приводит к увеличению продаж. 
Таким образом, тестовая кампания может быть использована для продвижения конкретного продукта определенной аудитории, а контрольная кампания может быть использована для продвижения нескольких продуктов более широкой аудитории '''