getwd()
setwd("redacted, this is the workspace of a friend working for MLB.")

install.packages("xml2")
install.packages("rvest")
install.packages('tidyverse')

# Packages
library(xml2)
library(rvest)
library(tidyverse)

# This helper function is being used to get rid of potentially messy / unknown data.
# If it tries to find an HTML tag and can't find it, it will return "NA".

helper_function <- function(entry, node) {
  entry %>% html_node(node) %>% html_text() -> name
  if (length(name) == 0) {
    return('NA')
  }
  name
}

# Read the HTML file.
rawHTML <- paste(readLines("ba.html"), collapse="\n")
BA_Ama_Rankings <- read_html(rawHTML, skip = 0, remove.empty = TRUE, trim = TRUE)

# Get all player information stored in a single list.
BA_Ama_Rankings %>% html_nodes("div.player-details-container") -> player_data

# From that list, use the vapply() function in conjunction with helper_function()
# to get a column's worth of information. Finally, use the cbind() function to put this
# all together into a DataFrame and write it to a CSV file.

vapply(player_data, helper_function, 'h3', FUN.VALUE = 'character') -> name
vapply(player_data, helper_function, 'span.team', FUN.VALUE = 'character') -> team
vapply(player_data, helper_function, 'span.position', FUN.VALUE = 'character') -> position
vapply(player_data, helper_function, 'div.player-notes', FUN.VALUE = 'character') -> notes
1:length(player_data) -> rank
df <- cbind(rank, name, team, position, notes)

write.csv(df, 'BA Ama Rankings.csv', row.names = FALSE)
