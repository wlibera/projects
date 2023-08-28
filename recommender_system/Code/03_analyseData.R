library(tidyverse)

data <- read.csv('surveyData_cleaned.csv')

set.seed(123)

data_analysis <- select(data, !c('Status',
                                 'Progress',
                                 'durationSec',
                                 'Finished',
                                 'ResponseId',
                                 'introquestion',
                                 'guard_other1_text',
                                 'guard_other1',
                                 'guard_other2_text',
                                 'guard_other2',
                                 'guard_other3_text',
                                 'guard_other3', 
                                 'additional'))


################################################################################


makeScreeplot <- function(data, maxClusters = 20){
  # tune for the number of clusters
  # https://www.datacamp.com/tutorial/k-means-clustering-r
  
  # Initialize total within sum of squares error: wss
  wss <- numeric(maxClusters)
  

  
  # Look over 1 to n possible clusters
  for (i in 1:maxClusters) {
    # Fit the model: km.out
    km.out <- kmeans(data, centers = i, nstart = 20)
    # Save the within cluster sum of squares
    wss[i] <- km.out$tot.withinss
  }
  
  # Produce a scree plot
  wss_df <- tibble(clusters = 1:maxClusters, wss = wss)
  
  scree_plot <- ggplot(wss_df, aes(x = clusters, y = wss, group = 1)) +
    geom_point(size = 4)+
    geom_line() +
    scale_x_continuous() +
    xlab('Number of clusters')
  print(scree_plot)
}

makeScreeplot(data_analysis, 20)
# no ellbow visible; we will stick to 5 clusters


################################################################################


# fit k-means
fit <- kmeans(data_analysis, 5)

results <- data.frame(data, fit$cluster)
results$fit.cluster <- as.factor(results$fit.cluster)
summary(results$fit.cluster)

cluster1 <- subset(results, fit.cluster == 1)
cluster2 <- subset(results, fit.cluster == 2)
cluster3 <- subset(results, fit.cluster == 3)
cluster4 <- subset(results, fit.cluster == 4)
cluster5 <- subset(results, fit.cluster == 5)


################################################################################


# look at characteristics of clusters
densityPerCluster <- function(data, variable){
  plot <- ggplot(data, mapping = aes(color = fit.cluster, fill = fit.cluster)) + 
    geom_density(mapping = aes_string(x = variable), alpha = 0.1)
  
  return(plot)
}

densityPerCluster(results, 'pushnotifications')
densityPerCluster(results, 'readarticles')











interest_vars <- grep('interest', colnames(data), value = TRUE)
distressed_vars <- grep('distressed', colnames(data), value = TRUE)


results_long <- reshape(results, varying = interest_vars, v.names = 'interest', timevar = 'topic', direction = 'long')

results_long$topic <- recode(results_long$topic, 
                             `1` = 'EUPolitics',
                             `2` = 'crimes',
                             `3` = 'israelPalestine',
                             `4` = 'immigration',
                             `5` = 'sports',
                             `6` = 'war',
                             `7` = 'climateChange',
                             `8` = 'showArts',
                             `9` = 'covid',
                             `10` = 'britishBrexit',
                             `11` = 'instAbuse',
                             `12` = 'spaceTravel',
                             `13` = 'protest',
                             `14` = 'terrorism',
                             `15` = 'USPolitics',
                             `16` = 'naturalDisasters',
                             `17` = 'elections',
                             `18` = 'economy')

results_long$distressed <- NA
for(var in distressed_vars){
  thisTopic <- gsub('distressed_', '', var)
  results_long$distressed[which(results_long$topic == thisTopic)] <- results_long[,var]
}

# distressed plot
ggplot(results_long, mapping = aes(color = fit.cluster, fill = fit.cluster)) +
  geom_density(mapping = aes(x = distressed), alpha = 0.1) +
  facet_wrap(~ topic) +
  coord_cartesian(ylim = c(0, 0.05))

# distressed by US Politics plot
distressed_USPolitics <- results_long[which(results_long$topic == 'USPolitics'),] %>%
  ggplot(mapping = aes(color = fit.cluster, fill = fit.cluster)) +
  geom_density(mapping = aes(x = distressed), alpha = 0.1) + 
  coord_cartesian(ylim = c(0, 0.05)) +
  theme_classic() +
  labs(x = 'Distressed by US Politics', y = 'Density', color = 'Persona', fill = 'Persona')

ggsave('distressed_USPolitics.png', distressed_USPolitics)
  



# interest plot
ggplot(subset(results_long, results_long$interest), mapping = aes(x = interest, fill = fit.cluster)) +
  geom_bar(position = 'dodge') +
  facet_wrap(~ topic)

ggplot(subset(results_long, results_long$interest), mapping = aes(y = topic, fill = topic)) +
  geom_bar(position = 'dodge') +
  facet_wrap(~ fit.cluster) +
  labs(x = 'Interest in Topic', y = 'Topic', fill = 'Topic') +
  theme_minimal()

ggsave('interest_03.png', interestPlot)

subset(results_long, results_long$interest) %>%
  ggplot(interest_ordered, mapping = aes(x = reorder(topic, topic, function(x)length(x)))) +
  geom_bar(position = 'dodge') +
  coord_flip() +
  theme_classic()

subset(results_long, (results_long$interest & results_long$topic == 'USPolitics')) %>%
  ggplot(interest_ordered, mapping = aes(x = fit.cluster, fill = fit.cluster)) +
  geom_bar(position = 'dodge') +
  theme_classic()



# distressed by US Politics plot
# distressed_USPolitics <- results_long[which(results_long$topic == 'USPolitics'),] %>%
  ggplot(data = results_long, mapping = aes(color = fit.cluster, fill = fit.cluster)) +
  geom_density(mapping = aes(x = interest), alpha = 0.1) + 
  coord_cartesian(ylim = c(0, 0.05)) +
  theme_classic() +
  labs(x = 'Distressed by US Politics', y = 'Density', color = 'Persona', fill = 'Persona')

ggsave('distressed_USPolitics.png', distressed_USPolitics)




# save results
write.csv(results, file = 'surveyResults_clustered.csv', row.names = FALSE)
write.csv(results_long, file = 'surveyResults_clustered_long.csv', row.names = FALSE)
