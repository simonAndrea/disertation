#Importing the libraries
library(tidyverse)
library(fpp3)
library(fma)
library(dplyr)
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
        

# Data preparation for different time scales
weekly_df <- data %>%
  index_by(week = ~ yearweek(.)) %>%  # Use yearweek for proper weekly grouping
  summarise(value = mean(value, na.rm = TRUE)) %>%  # Use mean for weekly average
  mutate(week = as.Date(week))  # Convert yearweek to Date for plotting

monthly_df <- data %>%
  index_by(month = ~ yearmonth(.)) %>%  # Use yearmonth for proper monthly grouping
  summarise(value = mean(value, na.rm = TRUE)) %>%  # Use mean for monthly average
  mutate(month = as.Date(month))  # Convert yearmonth to Date for plotting

# Create plots with proper data
plot1 <- plot_ly(data = data, x = ~date, y = ~value, type = 'scatter', mode = 'lines',
                 name = "Daily", line = list(color = 'dodgerblue')) %>%
  layout(title = "Daily Values",
         xaxis = list(title = "Date"),
         yaxis = list(title = "Daily Value"))

plot2 <- plot_ly(data = weekly_df, x = ~week, y = ~value, type = 'scatter', mode = 'lines',
                 name = "Weekly", line = list(color = 'dodgerblue')) %>%
  layout(title = "Weekly Average",
         xaxis = list(title = "Date"),
         yaxis = list(title = "Weekly Average"))

plot3 <- plot_ly(data = monthly_df, x = ~month, y = ~value, type = 'scatter', mode = 'lines',
                 name = "Monthly", line = list(color = 'dodgerblue')) %>%
  layout(title = "Monthly Average",
         xaxis = list(title = "Date"),
         yaxis = list(title = "Monthly Average"))

# Create subplot
p <- subplot(plot1, plot2, plot3, nrows = 3, shareX = TRUE, titleY = TRUE) %>%
  layout(
    title = "Sales Values Over Time",
    showlegend = FALSE,
    height = 900
  )

# Return JSON
plot_json <- plotly_json(p, jsonedit = FALSE)
plot_json
