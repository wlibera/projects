import pandas as pd
import pickle
import os
import random
import numpy as np
from numpy.linalg import norm
from datetime import datetime



# open cleaned data
with open("userinterest.pkl", "rb") as file:
    userinterest = pickle.load(file)

with open("userguard.pkl", "rb") as file:
    userguard = pickle.load(file)

with open("data/articles_cleaned.pkl", "rb") as file:
    articles = pickle.load(file)

articles_topics = pd.read_csv('data/articles_topics.csv')
articles_topics = articles_topics.loc[:, articles_topics.columns != 'Unnamed: 0']

personas = pd.read_csv('data/personas.csv')
personas = personas.loc[:, personas.columns != 'persona']

article_scores_personas = pd.read_csv('data/article_scores_personas.csv')
article_scores_personas = article_scores_personas.loc[:, article_scores_personas.columns != 'Unnamed: 0']

articles_embeddings = pd.read_csv('data/articles_embeddings.csv')




def calculate_articlesInterest():
    #Calculate interest score for every article
    #needs topic df and uservector
    #Outputs series objects filled with scores for every article
    
    #Transform into arrays
    articles_matrix = articles_topics.to_numpy()

    #Only use cols that correspond to interests
    interest_cols = user.index[user.index.str.startswith('interest_')]
    user_vector = np.array(user[interest_cols])
    
    #Calculate new scores using matrix multiplication
    new_scores_matrix = np.dot(articles_matrix, user_vector)
    new_scores_series = pd.Series(new_scores_matrix)

    return new_scores_series




def calculate_articlesTimeliness(currentArticle_index):
    #Calculate timeliness score for every article compared to currently reading article
    #needs article df
    #Outputs series object filled with scores for every article
    
    #Get current date
    currentArticle = articles.loc[currentArticle_index]
    currentDate = currentArticle['datenumber']
    
    #Calculate the difference between current date and dates of all articles
    datenumbers_articles = np.array(articles['datenumber'])
    datedifferences = abs(datenumbers_articles - currentDate)
    
    #Normalize to values between 0 and 1
    latestdate = articles['datenumber'].iloc[-1]
    normalized_datedifferences = [x / latestdate for x in datedifferences]
    
    #Dates that have large differences should be scored lower than ones closeby
    #So invert these values by subtracting it from 1
    datescores = [abs(1-x) for x in normalized_datedifferences]
    
    #Return as a series
    datescores_series = pd.Series(datescores)
    
    return datescores_series




def calculate_articlesSimilarity(currentArticle_index):
    #Calculate similarity score for every article compared to currently reading article
    #needs topic df
    #Outputs series objects filled with scores for every article
    
    #Transform into arrays
    articles_matrix = articles_topics.to_numpy()
    currentArticle = articles_topics.loc[currentArticle_index]
    currentArticle_vector = np.array(currentArticle)
    
    #Calculate cosine similarity between current article and all others
    dot = np.dot(articles_matrix, currentArticle_vector)
    articles_matrix_norm = np.linalg.norm(articles_matrix, axis=1)
    currentArticle_vector_norm = np.linalg.norm(currentArticle_vector)
    norm = currentArticle_vector_norm * articles_matrix_norm
    cosinesims = dot / norm
    new_scores_series =  pd.Series(cosinesims)

    return new_scores_series




def calculate_articlesDistressed():
    #Calculate distressed score for every article
    #needs topic df and uservector
    #Outputs series objects filled with scores for every article
    
    #Transform into arrays
    articles_matrix = articles_topics.to_numpy()

    #Only use cols that correspond to distressed
    distressed_cols = user.index[user.index.str.startswith('distressed_')]
    user_vector = np.array(user[distressed_cols])
    
    #Calculate new scores using matrix multiplication
    new_scores_matrix = np.dot(articles_matrix, user_vector)
    new_scores_series = pd.Series(new_scores_matrix)
    
    #The scores need to be inverted as distress should have a negative
    #influence on recommendations
    return 1 - new_scores_series




def calculate_articlesGuard():
    #Calculate guard score for every article
    #needs embeddings df and uservector
    #Outputs series objects filled with scores for every article
    
    #Transform into arrays
    articles_matrix = articles_embeddings.to_numpy()/6

    #Only use cols that correspond to guard
    guard_cols = user.index[user.index.str.startswith('guard_')]
    user_vector = np.array(user[guard_cols])

    #Calculate new scores using matrix multiplication
    new_scores_matrix = np.dot(articles_matrix, user_vector)
    new_scores_series = pd.Series(new_scores_matrix)

    #The scores need to be inverted as triggers should have a negative
    #influence on recommendations
    return 1 - new_scores_series




def calculate_articlesColab():
    
    #Outputs series objects filled with scores for every article
    
    # calculate the similarity between the user and each of the five personas
    # results in a similarity vector
    
    #Transform into matrix and array
    personas_matrix = personas.to_numpy()
    user_vector = np.array(user)
    
    #Calculate cosine similarity between user and all personas
    dot = np.dot(personas_matrix, user_vector)
    personas_matrix_norm = np.linalg.norm(personas_matrix, axis=1)
    user_vector_norm = np.linalg.norm(user_vector)
    norm = personas_matrix_norm * user_vector_norm
    cosinesims = dot / norm

    # get article scores per persona    
    # Transform into arrays
    articles_matrix = article_scores_personas.to_numpy()/5

    # Calculate new scores using matrix multiplication
    new_scores_matrix = np.dot(articles_matrix, cosinesims)
    new_scores_series = pd.Series(new_scores_matrix)

    return new_scores_series




def recommend(currentArticle, weights, k = 3):
    # calculate the scores for each article
    # the following functions should output a series with index = articles.index and the values corresponding to the recommendations (if solely based on this component; between 0 and 1)
    article_scores['interest'] = calculate_articlesInterest()
    article_scores['timeliness'] = calculate_articlesTimeliness(currentArticle)
    article_scores['similarity'] = calculate_articlesSimilarity(currentArticle)
    article_scores['distress'] = calculate_articlesDistressed()
    article_scores['guard'] = calculate_articlesGuard()
    article_scores['colab'] = calculate_articlesColab()

    scores_weighted = weights * article_scores.iloc[:,:len(weights)]
    article_scores['total'] = scores_weighted.apply(lambda row : row.sum(), axis=1)

    recommended = pd.Series(article_scores['total']).sort_values(ascending = False)
    recommended = recommended.drop(labels = currentArticle)

    return recommended[:k] # output k articles from the top




# make the Series 'popup_interest' to be called in the function
interest_cols = ['interest_EUPolitics', 'interest_crimes', 'interest_israelPalestine', 'interest_immigration', 'interest_sports', 'interest_war', 'interest_climateChange', 'interest_showArts', 'interest_covid', 'interest_britishBrexit', 'interest_instAbuse', 'interest_spaceTravel', 'interest_protests', 'interest_terrorism', 'interest_USPolitics', 'interest_naturalDisasters', 'interest_elections', 'interest_economy']
popup_interest = userinterest

# make the Series 'popup_guard' to be called in the function
guard_cols = ['guard_suicide', 'guard_accidents', 'guard_selfHarm', 'guard_depression', 'guard_racism', 'guard_eatingDisorders']
popup_guard = userguard

def newUser():
    global user
    allCols = ['interest_EUPolitics', 'interest_crimes', 'interest_israelPalestine', 'interest_immigration', 'interest_sports', 'interest_war', 'interest_climateChange', 'interest_showArts', 'interest_covid', 'interest_britishBrexit', 'interest_instAbuse', 'interest_spaceTravel', 'interest_protests', 'interest_terrorism', 'interest_USPolitics', 'interest_naturalDisasters', 'interest_elections', 'interest_economy', 'distressed_EUPolitics', 'distressed_crimes', 'distressed_israelPalestine', 'distressed_immigration', 'distressed_sports', 'distressed_war', 'distressed_climateChange', 'distressed_showArts', 'distressed_covid', 'distressed_britishBrexit', 'distressed_instAbuse', 'distressed_spaceTravel', 'distressed_protest', 'distressed_terrorism', 'distressed_USPolitics', 'distressed_naturalDisasters', 'distressed_elections', 'distressed_economy', 'guard_suicide', 'guard_accidents', 'guard_selfHarm', 'guard_depression', 'guard_racism', 'guard_eatingDisorders']
    user = pd.Series(index = allCols)

    interest_cols = user.index[user.index.str.startswith('interest_')]
    distressed_cols = user.index[user.index.str.startswith('distressed_')]
    guard_cols = user.index[user.index.str.startswith('guard_')]

    # initialise data from popup and mean responses from the survey
    user[interest_cols] = popup_interest
    user[distressed_cols] = [0.30492753623188407, 0.4394202898550725, 0.30818840579710144, 0.32768115942028986, 0.06818840579710145, 0.4698550724637681, 0.5271739130434783, 0.09978260869565217, 0.40050724637681157, 0.12144927536231885, 0.35594202898550725, 0.0722463768115942, 0.3279710144927536, 0.5227536231884058, 0.3071014492753623, 0.49130434782608695, 0.26057971014492753, 0.3505797101449275]
    user[guard_cols] = popup_guard


    global article_scores
    article_scores = pd.DataFrame(0, index = articles.index, columns = ['interest', 'timeliness', 'similarity', 'distress', 'guard', 'colab'])

    #currentArticle = int(articles.index[articles['url'] == 'https://nos.nl/artikel/2467501-dodental-ongeluk-met-veerboot-in-gabon-loopt-op-tot-21'][0])

newUser()


def updateLike(likevalue, currentArticle_index, weight = 0.05):
    #update user interest scores based on liked/disliked article
    #The likevalue is 1 or -1, for like or dilike respectively
    #The weight corresponds to how fast the user interest scores change after one rating
    
    currentArticle = articles_topics.loc[currentArticle_index]
    
    #Make values negative or positive, based on like/dislike
    topicsvalues = list(currentArticle)
    topicsvalues = [i * likevalue for i in currentArticle]
    
    #Make changes based on weight
    topicsvalues = [i * weight for i in topicsvalues]
    
    #Get current interest scores of user
    interest_cols = user.index[user.index.str.startswith('interest_')]
    interestlist = np.array(user[interest_cols])
    
    #Change interest scores in user vector
    new_interests = []
    for topic, interest in zip(topicsvalues, interestlist):
        newvalue = topic+interest
        if newvalue > 1.0:
            newvalue = 1.0
        if newvalue < 0.0:
            newvalue = 0.0
        new_interests.append(newvalue)
    
    user[interest_cols] = new_interests
    
    return None

interest_cols = user.index[user.index.str.startswith('interest_')]




def updateDistress(ratedArticle_index, rating, weight = 0.05):
    #update user distress based on distressed articles
    #The weight corresponds to how fast the user distress scores change after one distress
    
    ratedArticle = articles_topics.loc[ratedArticle_index]
    
    #Make changes based on weight and rating
    topicsvalues = list(ratedArticle)
    rating = rating/100
    topicsratings = [topic * rating for topic in topicsvalues]
    
    #Get current distressed scores of user
    distressed_cols = user.index[user.index.str.startswith('distressed_')]
    distressedlist = np.array(user[distressed_cols])
    
    #Change distressed scores in user vector
    new_distressed = []
    for topicrating, distress in zip(topicsratings, distressedlist):
        if not topicrating == 0:
            newvalue = weight*topicrating + (1-weight)*distress
        else:
            newvalue = distress

        new_distressed.append(newvalue)
        
    user[distressed_cols] = new_distressed
    
    return None

distressed_cols = user.index[user.index.str.startswith('distressed_')]




def updateClick(clickedArticle_index, weight = 0.01):
    #update user interests based on clicked articles
    #The weight corresponds to how fast the user interest scores change after one click
    
    clickedArticle = articles_topics.loc[clickedArticle_index]
    
    #Make changes based on weight
    topicsvalues = list(clickedArticle)
    topicsvalues = [i * weight for i in topicsvalues]
    
    #Get current interest scores of user
    interest_cols = user.index[user.index.str.startswith('interest_')]
    interestlist = np.array(user[interest_cols])
    
    #Change interest scores in user vector
    new_interests = []
    for topic, interest in zip(topicsvalues, interestlist):
        newvalue = topic+interest
        if newvalue > 1.0:
            newvalue = 1.0
        if newvalue < 0.0:
            newvalue = 0.0
        new_interests.append(newvalue)
        
    user[interest_cols] = new_interests
    
    return None

interest_cols = user.index[user.index.str.startswith('interest_')]






