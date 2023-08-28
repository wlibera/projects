import streamlit as st
import pandas as pd
import numpy as np
#import finalfunctions as ff
import random
import numpy as np
import os

# Page layout
st.set_page_config(layout="wide")
st.image('images/nostopbar.png', width=1300)


# This is the first page a user will see
# Here they can indicate their interests and if/how triggered they are by certain topics
st.subheader('State your preferences')
st.write('Thank you for visiting the NOS website. Before you start, please complete the form below for the best experience on the platform. The recommender algorithm will use this information to recommend the best articles for you')
st.write('After each article you are able to rate the article by liking/disliking it and stating if/how triggered you feel after reading it. It is highly suggested to answer those questions as often as possible as it will result in the best recommendations for you')

with st.form("my_form"):
	st.write("Please select all topics that you are interested in below:")
	EUpols = int(st.checkbox('EU Politics'))
	crimes = int(st.checkbox('Crimes'))
	israel = int(st.checkbox('Israel-Palestinian conflict'))
	immi = int(st.checkbox('Immigration'))
	sports = int(st.checkbox('Sports'))
	war = int(st.checkbox('War'))
	climate = int(st.checkbox('Climate change'))
	showart = int(st.checkbox('Showbusiness and Arts'))
	covid = int(st.checkbox('COVID-19'))
	british = int(st.checkbox('British politics/Brexit'))
	abuse = int(st.checkbox('Institutional abuse'))
	space = int(st.checkbox('Space travel'))
	protest = int(st.checkbox('Protests'))
	terror = int(st.checkbox('Terrorism'))
	USpols = int(st.checkbox('US Politics'))
	disaster = int(st.checkbox('Natural disasters'))
	elecs = int(st.checkbox('Elections'))
	econ = int(st.checkbox('Economy'))
	st.write("")
	st.write("Please indicate how triggered you are by the below subjects:")
	trig1 = (st.slider('Suicide', 0, 100))/100
	trig2 = (st.slider('Accidents', 0, 100))/100
	trig3 = (st.slider('Self harm', 0, 100))/100
	trig4 = (st.slider('Depression', 0, 100))/100
	trig5 = (st.slider('Racism', 0, 100))/100
	trig6 = (st.slider('Eating disorders', 0, 100))/100

	submitted = st.form_submit_button("Submit")
	if submitted:
   		st.write("Thank you for submitting your prefrences")

# State the column
interest_cols = ['interest_EUPolitics', 'interest_crimes', 'interest_israelPalestine', 'interest_immigration', 'interest_sports', 'interest_war', 'interest_climateChange', 'interest_showArts', 'interest_covid', 'interest_britishBrexit', 'interest_instAbuse', 'interest_spaceTravel', 'interest_protests', 'interest_terrorism', 'interest_USPolitics', 'interest_naturalDisasters', 'interest_elections', 'interest_economy']
guard_cols = ['guard_suicide', 'guard_accidents', 'guard_selfHarm', 'guard_depression', 'guard_racism', 'guard_eatingDisorders']

# Save data from the user into Series, then make two pickle files so we can access the information on the NOS website
datatopics = np.array([EUpols, crimes, israel, immi, sports, war, climate, showart, covid, british, abuse, space, protest, terror, USpols, disaster, elecs, econ])
popup_interest = pd.Series(datatopics, index=interest_cols)

datatrigs = np.array([trig1, trig2, trig3, trig4, trig5, trig6])
popup_guard = pd.Series(datatrigs, index=guard_cols)

popup_interest.to_pickle("userinterest.pkl")  
popup_guard.to_pickle("userguard.pkl")  

# Create a new user
#ff.newUser()

# After submitting their preferences, the user can click this button to continue to the NOS website
# Note that it can take some time (up to a minute) before everything is loaded
# This button will perform a command line that runs the second (main) Streamlit file, NOS.py
runbtn = st.button('Continue to the NOS website')

# If the button is not clicked, do nothing
if "runbtn_state" not in st.session_state:
    st.session_state.runbtn_state = False

# If the button is clicked, run the NOS.py file on Streamlit
if runbtn or st.session_state.runbtn_state:
   st.session_state.runbtn_state = True
   os.system('streamlit run NOS.py')