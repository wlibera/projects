# Projects
This repository contains all of the projects that were a part of my Master in Applied Data Science at Utrecht University. Since the projects were made as a form of assessment for courses, the exact papers with the results are not posted. In order to see specific papers, please contact me.  

### About "price_prediction_HPM_GWR" project

This team project was developed in collaboration with my colleagues Hassan Ali and Sahar Pourahmad. It is a comparative study of Airbnb price prediction in Amsterdam. Two geographical models are considered: the Hedonic Price Model (HPM) and the Geographically Weighted Regression (GWR). The goal was to demonstrate that spatial variation matters when it comes to pricing Airbnb spaces. 

This project includes a R script *("project_final.RMD")* that handles all data and model processing. The *"listings_clean.csv"* file is required to run it. It is a cleaned data frame with all variables considered that has already been cleaned and pre-processed. The *"Neighborhood.shp"* file allows us to present the spatial variation of the variables to be displayed in the Amsterdam neighbourhood map. 

### About "wind_turbines" project

This team project was developed in collaboration with my colleagues Hassan Ali, Danya Mawed and Jelle Prins. The aim was to determine the suitable areas for wind turbines and evaluate the theoretical maximum energy production within these places. 

This project was entirely done in the QGIS program and the tools available. The workflow below shows all the steps required to achieve the final result.  

<img width="312" alt="image" src="https://github.com/wlibera/projects/assets/136256381/820fb42a-9375-486f-8379-dadea9a961bf">

The folder includes all the shape files (.shp) with all the steps and restrictions needed to achieve the final map that contains the suitable areas *("Final_Suitable_AreasV5")*. Unfortunately, some of the files are too big, and therefore I attached the table, that contains the sources where the data can be found.

<img width="454" alt="image" src="https://github.com/wlibera/projects/assets/136256381/e51fb194-2872-4cfb-a876-de1f6eec1857">

### About "recommender_system" project

This project was made together with [Maike L. V. Weiper](https://github.com/MWeiper), Carmen Timmerman, Xeniah Sillie and [Camilla Kuijper](https://github.com/CamillaKuijper)

We created the personalized recommender system for the Dutch public media service NOS, which takes into account that news
can be experienced as distressing or triggering. We wanted to create a system that would "protect" users from those sensitive topics if the user opts into it. It relies on the user’s explicit feedback and communication with the recommender system. To avoid the creation of the "information bubble" we tried to implement multiple factors, such as timeliness,
collaborative filtering, similarity, distress, and interest, in addition to triggers, in order to balance the recommendation while still providing the user with interesting and personalised content.

This project utilises scraped data from [NOS webside](https://nos.nl/) as well as the [Streamlit](https://streamlit.io/) application in order to create the recommender system. 


