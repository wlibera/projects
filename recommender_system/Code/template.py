import streamlit as st
from random import random

# set episode session state
def select_article(article_url):
  st.session_state['url'] = article_url

def tile_item(column, item):
  with column:
    st.button('View article', key=random(), on_click=select_article, args=(item['url'], ))
    if item['image']:
      st.image(item['image'], use_column_width='always')
    else:
      st.image('images/placeholder.jpeg', use_column_width='always')
    st.subheader(item['title'])

def recommendations(df):

  # check the number of items
  nbr_items = df.shape[0]

  if nbr_items != 0:    

    # create columns with the corresponding number of items
    columns = st.columns(nbr_items)

    # convert df rows to dict lists
    items = df.to_dict(orient='records')

    # apply tile_item to each column-item tuple (created with python 'zip')
    any(tile_item(x[0], x[1]) for x in zip(columns, items))