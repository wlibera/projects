library(tidyverse)

data <- read.csv('surveyData_raw.csv')

data <- subset(data, Progress == 100)
data <- subset(data, Status == 'IP Address')
data <- subset(data, age >= 18)
data <- subset(data, age <= 30)

data$introquestion <- as.factor(data$introquestion)
data$pushnotifications <- as.factor(data$pushnotifications)
data$readarticles <- as.factor(data$readarticles)

# turn NAs into 0 (the default in the survey)
data <- replace(data, is.na(data), 0)

# turn the interest variable into multiple boolean variables
data$interest_EUPolitics <- grepl('EU politics', data$topicsinterested, ignore.case = TRUE)
data$interest_crimes <- grepl('Crimes', data$topicsinterested, ignore.case = TRUE)
data$interest_israelPalestine <- grepl('Israeli-Palestinian conflict', data$topicsinterested, ignore.case = TRUE)
data$interest_immigration <- grepl('Immigration', data$topicsinterested, ignore.case = TRUE)
data$interest_sports <- grepl('Sports', data$topicsinterested, ignore.case = TRUE)
data$interest_war <- grepl('Ukrainian', data$topicsinterested, ignore.case = TRUE)
data$interest_climateChange <- grepl('Climate Change', data$topicsinterested, ignore.case = TRUE)
data$interest_showArts <- grepl('Show Business & Arts', data$topicsinterested, ignore.case = TRUE)
data$interest_covid <- grepl('COVID-19', data$topicsinterested, ignore.case = TRUE)
data$interest_britishBrexit <- grepl('Brexit', data$topicsinterested, ignore.case = TRUE)
data$interest_instAbuse <- grepl('Institutional abuse', data$topicsinterested, ignore.case = TRUE)
data$interest_spaceTravel <- grepl('Space-Travel', data$topicsinterested, ignore.case = TRUE)
data$interest_protests <- grepl('Protests', data$topicsinterested, ignore.case = TRUE)
data$interest_terrorism <- grepl('Terrorism', data$topicsinterested, ignore.case = TRUE)
data$interest_USPolitics <- grepl('US Politics', data$topicsinterested, ignore.case = TRUE)
data$interest_naturalDisasters <- grepl('Natural Disasters', data$topicsinterested, ignore.case = TRUE)
data$interest_elections <- grepl('Elections', data$topicsinterested, ignore.case = TRUE)
data$interest_economy <- grepl('Economy', data$topicsinterested, ignore.case = TRUE)

data <- select(data, !topicsinterested)

# make the variables on how often a participants consumes news numeric
data$pushnotifications <- recode_factor(data$pushnotifications, `Multiple times per day` = 3, `Every day` = 1, `2-3 times per week` = 2.5/7, `Once per week` = 1/7, `Never` = 0)
data$readarticles <- recode_factor(data$readarticles, `Multiple times per day` = 3, `Every day` = 1, `2-3 times per week` = 2.5/7, `Once per week` = 1/7, `Never` = 0)

# save dataframe
write.csv(data, file = 'surveyData_cleaned.csv', row.names = FALSE)
