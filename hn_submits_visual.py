from operator import itemgetter
import plotly.express as px
import requests

# Hace una llamada al API y checa el estado.
url = "https://hacker-news.firebaseio.com/v0/topstories.json"
r = requests.get(url)
print(f"Status: code: {r.status_code}")

# Procesa la informacion de cada submision
submission_ids = r.json()

# Convierte la respuesta del objeto a un diccionario y procesa el resultado final
submission_links, descendant_amount, hover_texts, scores = [], [], [], []
for submission_id in submission_ids[:2]:
    # Hace una nueva llamada al API for cada submision.
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"ID: {submission_id}\tStatus: {r.status_code}")
    response_dict = r.json()

    # Guarda la informacion para ser usada en los ejes.
    id_title = response_dict['title']
    id_url = response_dict['url']
    id_link = f"<a href='{id_url}'>{id_title}"
    id_descendants = response_dict['descendants']
    id_score = response_dict['score']
    submission_links.append(id_link)
    descendant_amount.append(id_descendants)
    scores.append(id_score)

    # Construye los textos hover
    owner = response_dict['by']
    types = response_dict['type']
    scores_hover = response_dict['score']
    hover_text = f"{owner}<br />{types}<br />{scores}"
    hover_texts.append(hover_text)

# Hace la visualziacion
# dict_keys(['by', 'descendants', 'id', 'kids', 'score', 'time', 'title', 'type', 'url'])
title = "Hacker-News Top Stories"
labels = {'x': 'Top Storie', 'y': 'Score'}
fig = px.bar(x=submission_links, y=scores, labels=labels, title=title,
             hover_name=hover_texts)

fig.update_layout(title_font_size=28, xaxis_title_font_size=20, 
                  yaxis_title_font_size=20)

fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6)
fig.show()