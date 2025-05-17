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

args <- commandArgs(trailingOnly = TRUE)
site_id <- as.integer(args[1])

colnames(data) <- c("date", "value")
data$date <- as.Date(data$date)
data$value <- as.numeric(data$value)
data$log_value <- log(data$value)
data <- tsibble(data, index=date)
data <- data %>% fill_gaps()

acf = data |> ACF() |> autoplot() + labs(title = 'Autocorrelation (ACF)')
pacf = data |> PACF() |> autoplot() + labs(title = 'Partial Autocorrelation (PACF)')

# Create subplot
p <- subplot(acf, pacf, nrows = 2, shareX = TRUE, titleY = TRUE) %>%
  layout(
    showlegend = FALSE,
    height = 900
  )

# Return JSON
plot_json <- plotly_json(p, jsonedit = FALSE)
plot_json
