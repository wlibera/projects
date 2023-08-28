library(qualtRics)
data <- qualtRics::read_survey('surveyData.csv')

library(tidyverse)
data <- select(data, !c('StartDate', 
                        'EndDate', 
                        'IPAddress', 
                        'RecordedDate', 
                        'RecipientFirstName',
                        'RecipientLastName',
                        'RecipientEmail',
                        'ExternalReference',
                        'LocationLatitude',
                        'LocationLongitude',
                        'DistributionChannel',
                        'UserLanguage'))

data <- rename(data, durationSec = `Duration (in seconds)`)

data <- rename(data, c(distressed_EUPolitics = distressed_1, 
                       distressed_crimes = distressed_2, 
                       distressed_israelPalestine = distressed_3,
                       distressed_immigration = distressed_4,
                       distressed_sports = distressed_5,
                       distressed_war = distressed_6,
                       distressed_climateChange = distressed_7,
                       distressed_showArts = distressed_8,
                       distressed_covid = distressed_9,
                       distressed_britishBrexit = distressed_10,
                       distressed_instAbuse = distressed_11,
                       distressed_spaceTravel = distressed_12,
                       distressed_protest = distressed_13,
                       distressed_terrorism = distressed_14,
                       distressed_USPolitics = distressed_15,
                       distressed_naturalDisasters = distressed_16,
                       distressed_elections = distressed_17,
                       distressed_economy = distressed_18))

data <- rename(data, c(guard_suicide = guarding_1,
                       guard_accidents = guarding_2,
                       guard_physicalAbuse = guarding_3,
                       guard_sexualAbuse = guarding_4,
                       guard_selfHarm = guarding_5,
                       guard_depression = guarding_6,
                       guard_racism = guarding_7,
                       guard_LGBTQ = guarding_8,
                       guard_eatingDisorders = guarding_9,
                       guard_disability = guarding_10,
                       guard_animalCruelty = guarding_11,
                       guard_other1 = guarding_12,
                       guard_other1_text = guarding_12_TEXT,
                       guard_other2 = guarding_13,
                       guard_other2_text = guarding_13_TEXT,
                       guard_other3 = guarding_14,
                       guard_other3_text = guarding_14_TEXT))

write.csv(data, file = 'surveyData_raw.csv', row.names = FALSE)

