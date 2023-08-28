import streamlit as st
import pandas as pd
import template as t
import pickle
from random import random
import finalfunctions as ff
from streamlit_extras.switch_page_button import switch_page


# Page layout
st.set_page_config(layout="wide")
st.image('images/nostopbar.png', width=1300)

# Load articles data from the pickle file
df = pd.read_pickle("data/articles_cleaned.pkl")

# Change style of radio buttons. Horizontal & hide first (preselected) option so that users are also able to now answer a question
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
st.markdown(
    """ <style>
            div[role="radiogroup"] >  :first-child{
                display: none !important;
            }
        </style>
        """,
    unsafe_allow_html=True
)


# Define start state. This is always first the most recent article we scraped
if 'url' not in st.session_state:
	st.session_state['url'] = 'https://nos.nl/artikel/2467501-dodental-ongeluk-met-veerboot-in-gabon-loopt-op-tot-21'


# Store the index of the current article, we need this later on.
df2 = df[df['url'] == st.session_state['url']]
currentArticle = df[df['url'] == st.session_state['url']].index[0]

# We update the click when a user clicks (visits) an article
ff.updateClick(currentArticle)

# Layout of the page, consisting of three columns (left is the smallest, right is widest column)
sidebar, cover, info = st.columns([1,2,3])

# Side bar containing static images from the NOS website

with sidebar:
	st.write("")
	st.write("")
	st.image('images/nosmidbar.png', width=300)
	st.image('images/nossidebar.png', width=200)

# Middle containing the current article's image & the top bar from the NOS website 
with cover:
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	if df2['image'].iloc[0]:
		st.image(df2['image'].iloc[0])
	else:
		st.image('images/placeholder.jpeg', use_column_width='always')

	#st.image(df2['image'].iloc[0])

# Right side: article title, date, text & rating
with info:
	st.write("")
	st.write("")
	st.write("")
	st.write("")
	st.title(df2['title'].iloc[0])
	st.markdown(df2['date'].iloc[0])
	st.write(df2['article'].iloc[0])


	# Form for user to submit their trigger score & rating (like/dislike)
	with st.form(key="rating", clear_on_submit = True):
		rating = st.slider("Did this article trigger you?", 0, 100)
		like_dislike = st.radio('Did you like this article?', ['no answer', 'like', 'dislike'])
		submitted = st.form_submit_button("Submit")

		# If the user submits their rating(s), give their input to two functions: updateLike and updateDistress
		if submitted:
   			st.write("Thank you for submitting your rating(s)")
   			if like_dislike == 'no answer':
   				likeval = 0
   			if like_dislike == 'like':
   				likeval = 1
   			if like_dislike == 'dislike':
   				likeval = -1
   			ff.updateLike(likeval, currentArticle)
   			ff.updateDistress(currentArticle, rating)


# Recommend 3 articles below the current article
st.subheader('Recommended articles')

# Assign recommended articles here with predetermined weights
weights1 = [0.40, 0.25, 0.00, 0.10, 0.15, 0.10]
weights2 = [0.15, 0.25, 0.25, 0.125, 0.125, 0.10]
currentArticle = df[df['url'] == st.session_state['url']].index[0]


# If the user is on the first article, we give slightly different weights
if st.session_state['url'] == 'https://nos.nl/artikel/2467501-dodental-ongeluk-met-veerboot-in-gabon-loopt-op-tot-21':
	recommended_articles = ff.recommend(currentArticle, weights1, 3)

# After this, we use weights2 to recommend articles
else:
	recommended_articles = ff.recommend(currentArticle, weights2, 3)

# Make a list of the three recommended articles
recommended_articles = recommended_articles.index
rec1 = recommended_articles[0]
rec2 = recommended_articles[1]
rec3 = recommended_articles[2]
reclist = [rec1, rec2, rec3]


# Showcase recommendations using the template.py function "recommendations" from the Lab
recommendations = df.loc[[reclist[0], reclist[1], reclist[2]]]
t.recommendations(recommendations)


# Just to check if the scores change :)
#st.subheader('Check if user values change with every activity')
#st.write(ff.user[ff.interest_cols])
#st.write(ff.user[ff.distressed_cols])
#st.write(ff.user[ff.guard_cols])



