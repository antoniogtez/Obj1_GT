# =========================================
# 📌 Google Trends Data Download Script
# Script to download and save search trends data 
# for sustainable mobility analysis
# =========================================

# 📌 Load required libraries
library(trendecon)
library(tidyverse)
library(lubridate)

# 📌 Define parameters
keywords <- c("bike routes", "public transport", "car rental", "taxi near me")  # Change as needed
geo <- "US"   # Change country code (e.g., "ES" for Spain, "DE" for Germany)
from_date <- "2018-01-01"   # Start date (Google Trends allows max ~5 years)
to_date <- "2023-12-31"     # End date
frequency <- "month"        # Options: "day", "week", "month"

# 📌 Function to download Google Trends data
download_trends <- function(keywords, geo, from_date, to_date, frequency) {
  
  # Loop through each keyword
  for (keyword in keywords) {
    print(paste("Downloading:", keyword, "for", geo))
    
    # Check if the file already exists to avoid unnecessary API calls
    file_path <- paste0("data/raw/", geo, "_", gsub(" ", "_", keyword), ".csv")
    
    if (!file.exists(file_path)) {
      # Download data using trendecon
      df <- get_trends(
        terms = keyword,
        geo = geo,
        from = from_date,
        to = to_date,
        frequency = frequency
      )
      
      # Save data
      write.csv(df, file_path, row.names = FALSE)
      print(paste("Saved:", file_path))
    } else {
      print(paste("File already exists:", file_path))
    }
  }
  
  print("✅ Download completed!")
}

# 📌 Run the function
download_trends(keywords, geo, from_date, to_date, frequency)
