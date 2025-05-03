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

source("get_data.R")

colnames(data) <- c("date", "value")
data$date <- as.Date(data$date)
data$value <- as.numeric(data$value)
data$log_value <- log(data$value)
data <- tsibble(data, index=date)
data <- data %>% fill_gaps()
# Calculate 80% index
split_index <- floor(0.8 * nrow(data))

# Split into train (80%) and test (20%)
train_data <- data[1:split_index, ]
test_data <- data[(split_index + 1):nrow(data), ]

# Fit SARIMA model to training data
fit_sarima <- auto.arima(train_data$value, seasonal = TRUE, d = 0, D = 0)

# Forecast the length of the test set
forecast_horizon <- nrow(test_data)
forecast_result_sarima <- forecast(fit_sarima, h = forecast_horizon)

# Exponentiate forecast components
forecast_result_sarima$mean <- exp(forecast_result_sarima$mean)
forecast_result_sarima$lower <- exp(forecast_result_sarima$lower)
forecast_result_sarima$upper <- exp(forecast_result_sarima$upper)

print("MEAN:", forecast_result_sarima$mean)


# Convert to data frame and add forecast dates
forecast_result_df <- as.data.frame(forecast_result_sarima)
forecast_result_df$date <- test_data$date
forecast_result_df <- forecast_result_df %>%
  rename(forecast_value = `Point Forecast`)

# Transform original values for plotting
original_data <- data %>%
  mutate(original_value = exp(value))  # if value is log-transformed

plot_data <- list(
  original = list(
    date = original_data$date,
    value = original_data$original_value
  ),
  forecast = list(
    date = forecast_result_df$date,
    value = forecast_result_df$forecast_value
  )
)

# Return JSON
plot_json <- plotly_json(plot_data, jsonedit = FALSE)
plot_json