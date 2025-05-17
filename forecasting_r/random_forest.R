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
library(conflicted)
library(randomForest)

# Explicitly set function preferences
conflicted::conflict_prefer("filter", "dplyr")
conflicted::conflict_prefer("lag", "dplyr")
conflicted::conflict_prefer("layout", "plotly")
conflicted::conflict_prefer("last_plot", "plotly")
conflicted::conflict_prefer("flatten", "purrr")
conflict_prefer("intersect", "base")
conflict_prefer("union", "base")
conflict_prefer("setdiff", "base")
conflict_prefer("date", "base")
conflict_prefer("interval", "lubridate")
conflict_prefer("filter", "dplyr")
conflict_prefer("lag", "dplyr")
conflict_prefer("layout", "plotly")
conflict_prefer("last_plot", "plotly")
conflict_prefer("flatten", "purrr")
conflict_prefer("intersect", "base")

source("get_data.R")

colnames(data) <- c("date", "value")
data$date <- as.Date(data$date)
data$value <- as.numeric(data$value)
data <- tsibble(data, index=date)
data <- data %>% fill_gaps() 

data$value[is.na(data$value)] <- mean(data$value, na.rm = TRUE)
ts_data <- ts(data$value, frequency = 7)

ts_data <- data %>%
  mutate(
    day_of_week = as.factor(weekdays(date)),
    week_num = week(date),
    month = month(date),
    lag1 = lag(value, 1), 
    lag3 = lag(value, 3), 
    lag7 = lag(value, 7)   
  ) %>%
  na.omit()


# Split the data into training and testing sets (80/20 split)
train_size <- floor(0.8 * nrow(ts_data))
train_data <- ts_data[1:train_size, ]
test_data <- ts_data[(train_size + 1):nrow(ts_data), ]

forecast_horizon <- 60
last_date <- max(data$date)
forecast_dates <- seq(from = last_date + 1, by = "day", length.out = forecast_horizon)

# Train Random Forest model
rf_model <- randomForest(value ~ day_of_week + week_num + month + lag1 + lag3 + lag7, 
                         data = train_data)


# Make predictions
rf_predictions <- predict(rf_model, newdata = test_data)


# # Prepare plot data
plot_data <- list(
  original = list(
    date = data$date,
    value = format(as.numeric(data$value), nsmall = 2)
  ),
  forecast = list(
    date = forecast_dates,
    value = format(as.numeric(rf_predictions), nsmall = 2)
  )
)
# Return JSON
plot_json <- plotly_json(plot_data, jsonedit = FALSE)
plot_json

