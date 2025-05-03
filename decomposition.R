# Load conflicted first to manage package conflicts
library(conflicted)

# Suppress package startup messages
suppressPackageStartupMessages({
  library(tidyverse)
  library(fpp3)
  library(plotly)
  library(jsonlite)
  library(tsibble)
  library(zoo)
})

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

# Convert and clean data with explicit NA handling
data <- data %>%
  mutate(
    date = as.Date(Date),
    value = as.numeric(TotalSales)
  ) %>%
  as_tsibble(index = date) %>%
  fill_gaps(value = median(value, na.rm = TRUE)) %>%
  mutate(log_value = log(value))


# Perform decompositions with explicit period
dataDecomp <- data %>%
  model(
    classical = classical_decomposition(value ~ season(period = 7))
  )

classical <- components(dataDecomp)

stl_decomp <- data %>%
  model(
    stl = STL(value ~ season(period = 7))
  ) %>%
  components()

# Create plots
classical_plot <- classical %>%
  autoplot() +
  theme_minimal() +
  ggtitle("Classical Decomposition")

stl_plot <- stl_decomp %>%
  autoplot() +
  theme_minimal() +
  ggtitle("STL Decomposition")

# Convert to plotly and create subplot
plot1 <- ggplotly(classical_plot)
plot2 <- ggplotly(stl_plot)
subplot <- subplot(plot1, plot2, nrows = 2, heights = c(0.5, 0.5))

# Return JSON
plotly_json(subplot, jsonedit = FALSE)

