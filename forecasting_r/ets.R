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
# data$log_value <- log(data$value)
data <- tsibble(data, index=date)
data <- data %>% fill_gaps() 

data$value[is.na(data$value)] <- mean(data$value, na.rm = TRUE)


ts_data <- ts(data$value, frequency = 7)  # Weekly seasonality

# Split using direct indexing
split_point <- floor(0.8 * length(ts_data))

# Slice the ts and re-wrap each as ts objects
train_data <- ts(ts_data[1:split_point], frequency = 7)
test_data <- ts(ts_data[(split_point + 1):length(ts_data)], frequency = 7)
forecast_horizon <- 60

# Fit ETS model
fit_ets <- HoltWinters(train_data, gamma = TRUE)

# Forecast for length of test set
forecast_result_ets <- forecast(fit_ets, h = forecast_horizon)

print(forecast_result_ets)

# Convert to data frame
forecast_result_ets_df <- as.data.frame(forecast_result_ets)

last_date <- max(data$date)
forecast_dates <- seq(from = last_date + 1, by = "day", length.out = forecast_horizon)

# Rename for consistency
forecast_result_ets_df <- forecast_result_ets_df %>%
  rename(forecast_value = `Point Forecast`)

# Prepare plot data
plot_data <- list(
  original = list(
    date = data$date,
    value = format(as.numeric(data$value), nsmall = 2)
  ),
  forecast = list(
    date = forecast_dates,
    value = format(as.numeric(forecast_result_ets_df$forecast_value), nsmall = 2)
  )
)
# Return JSON
plot_json <- plotly_json(plot_data, jsonedit = FALSE)
plot_json
