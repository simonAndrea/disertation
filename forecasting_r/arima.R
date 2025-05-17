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

split_point <- floor(0.8 * nrow(data))
train_data <- data[1:split_point, ]
test_data <- data[(split_point + 1):nrow(data), ]
forecast_horizon <- 60

# Fit the best ARIMA model using auto.arima
model <- auto.arima(train_data$value, seasonal = TRUE, stepwise = FALSE, approximation = FALSE)

# Forecasting with the model
forecast_result_sarima <- forecast(model, h = forecast_horizon)

last_date <- max(data$date)
forecast_dates <- seq(from = last_date + 1, by = "day", length.out = forecast_horizon)


forecast_result_df <- data.frame(
  date = forecast_dates,
  forecast_value = (as.numeric(forecast_result_sarima$mean)),
  lower_80 = (as.numeric(forecast_result_sarima$lower[, 1])),
  upper_80 = (as.numeric(forecast_result_sarima$upper[, 1]))
)


# Convert to data frame and add forecast dates
forecast_result_df <- as.data.frame(forecast_result_sarima)
forecast_result_df$date <- forecast_dates
forecast_result_df <- forecast_result_df %>%
  rename(forecast_value = `Point Forecast`)

plot_data <- list(
  original = list(
    date = data$date,
    value = format(data$value, nsmall = 2)
  ),
  forecast = list(
    date = forecast_result_df$date,
    value = format(forecast_result_df$forecast_value, nsmall = 2)
  )
)

# Return JSON
plot_json <- plotly_json(plot_data, jsonedit = FALSE)
plot_json