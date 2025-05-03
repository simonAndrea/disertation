#Importing the libraries
library(tidyverse)
library(fpp3)
library(fma)
library(dplyr)
library(forecast)
library(ggplot2)
library(gridExtra)
library(lubridate)
library(zoo)
library(tseries)
library(stats)
library(seasonal)
library(plotly)
library(fable)
library(jsonlite)

source("get_data.R")

colnames(data) <- c("date", "value")
data$date <- as.Date(data$date)
data$value <- as.numeric(data$value)
data$log_value <- log(data$value)
data <- tsibble(data, index=date)
data <- data %>% fill_gaps()

# Create seasonal plots using gg_season
weekly_plot <- data %>%
  mutate(wday = wday(date, label = TRUE)) %>%
  ggplot(aes(x = wday, y = value, group = yearweek(date))) +
  geom_line(alpha = 0.5) +
  labs(x = "Day of Week",
       y = "Value") +
  theme_minimal()

# Convert ggplot to plotly
plot1 <- ggplotly(weekly_plot) %>%
  layout(
    showlegend = FALSE
  )

# Return JSON of single plot
plot_json <- plotly_json(plot1, jsonedit = FALSE)
plot_json
