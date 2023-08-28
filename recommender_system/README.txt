This is how you start up the streamlit app:
1. Run the preferences.py file in your terminal: streamlit run preferences.py
2. Enter your preferences and click "Continue to the NOS website"
3. Your browser will open a new streamlit webpage (NOS.py), please note that this can take up to 1-2 minutes
3. Now you can read, rate & open recommended articles

There is also a video file streamlit_walkthrough. It shows how the app works and what its functionalities are. 

Explanation of files:
- webscrape_NOS.ipynb: Code for scraping NOS
- Cleaning.ipynb: Cleans the scraped articles
- LDA.ipynb: Performs LDA and tunes for the best LDA parameters.
- 01_prepData.R: Takes the raw survey data and reads it into an R dataframe.
- 02_cleanData.R: Cleans the survey data and prepares it for clustering. 
- 03_analyseData.R: Does a clustering algorithm to get the personas and their averages. 
- create_articlestopicDF.ipynb: Creates the dataframe that has the topic distributions per article based on the LDA model found earlier. 
- create_personasDF.ipynb: Takes the dataframe found in the clustering and formats it to be used later. 
- create_articlesscoresPersonas.ipynb: Calculates scores per article for each persona. 
- create_articlesEmbeddings.ipynb: Calculates trigger scores based on word embeddings for each article. 
- functions.ipynb: Defines all functions used to generate the recommendations. 
- finalfunctions.py: Contains all functions for the recommender algorithm
- NOS.py: Contains code for the main streamlit page
- preferences.py: Runs the streamlit app (first page)
- template.py: Used to display the recommended articles (code comes from lab week 1 and is slightly adjusted)

