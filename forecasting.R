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
library(fable)
library(seasonal)
library(plotly)
library(fable)
library(randomForest)
library(xgboost)
library(keras)
library(jsonlite)
library(listviewer)

format_data <- function(data) {
    tryCatch({
        # Ensure column names are correct
        colnames(data) <- c("date", "value")
        
        # Convert date to proper format
        data$date <- as.Date(data$date)
        data$value <- as.numeric(data$value)
        data$log_value <- log(data$value)
        
        # Convert to tibble
        data <- as_tibble(data) 
        return(data)
    }, error = function(e) {
        print(paste("Error in format_data:", e))
        return(NULL)
    })
}

data_plotting <- function(data) {
    #Resample for Weekly Value (Sum) and Monthly value
    p1 <- ggplot(data, aes(x = as.Date(data$date), y = value)) + 
    geom_line(color = "dodgerblue") + 
    labs(title = "Daily Value", y = "Value", x = "Date") +
    scale_x_date(limits = c(as.Date("2020-07-01"), as.Date("2022-06-30"))) +
    theme_minimal()

    weekly_df <- data %>%
    mutate(date = as.Date(as.Date(data$date), origin = "1970-01-01")) %>%
    mutate(week = floor_date(as.Date(data$date), "week")) %>%
    group_by(week) %>%
    summarise(value = sum(value, na.rm = TRUE), .groups = "drop")

    p2 <- ggplot(weekly_df, aes(x = week, y = value)) + 
    geom_line(color = "dodgerblue") + 
    labs(title = "Weekly Value", y = "Value", x = "Date") +
    scale_x_date(limits = c(as.Date("2020-07-01"), as.Date("2022-06-30"))) +
    theme_minimal()

    monthly_df <- data %>%
    mutate(date = as.Date(as.Date(data$date), origin = "1970-01-01")) %>%
    mutate(month = floor_date(as.Date(data$date), "month")) %>%
    group_by(month) %>%
    summarise(value = sum(value, na.rm = TRUE), .groups = "drop") 

    p3 <- ggplot(monthly_df, aes(x = month, y = value)) + 
    geom_line(color = "dodgerblue") + 
    labs(title = "Monthly Value", y = "Value", x = "Date") +
    scale_x_date(limits = c(as.Date("2020-07-01"), as.Date("2022-06-30"))) +
    theme_minimal()

    # Combine plots
    subplot_obj <- subplot(p1, p2, p3, nrows = 3, shareX = TRUE) %>%
        layout(
            showlegend = FALSE,
            plot_bgcolor = "transparent",
            paper_bgcolor = "transparent"
        )

    plot_json <- plotly::plotly_json(subplot_obj)

    return(plot_json)
}


seasonality_checking <- function(data) {
    weekly_plot <- data |> gg_season(value, periold = "week") + labs(title='Weekly seasonality')

    monthly_plot <- data |> gg_season(value, pleriod = "monlth") +
    labs(title='Monthly seasonality')

    return (list(weekly_plot, monthly_plot, yearly_plot))
}

stationarity_checking <- function(data) {
    #Lag plot
    lag_plot <- data |> gg_lag(value, geom = "point") +
    labs(x = "lag(value, k)")

    #Autocorrelation (ACF) and Partial Autocorrelation (PACF): 
    acf <- data |> ACF() |> autoplot() + labs(title = 'Autocorrelation (ACF)')
    pacf(data, lag.max = 28, main = "PACF of Original Data")
    pacf <- data |> PACF() |> autoplot() + labs(title = 'Partial Autocorrelation (PACF)')

    #ADF test
    adf_test <- adf.test(data$value)

    return (list(lag_plot, acf, pacf, adf_test))
}

