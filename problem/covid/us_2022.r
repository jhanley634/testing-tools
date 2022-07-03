#! /usr/bin/env Rscript

library(dplyr, warn.conflicts = FALSE)
library(ggplot2)
library(ggrepel)

options(scipen = 999) # turn off scientific notation like 1e+06
data("midwest", package = "ggplot2")
if (FALSE) {
  ggplot(midwest, aes(x = area, y = poptotal, label = state)) +
    geom_text_repel() +
    geom_point()
}

fspec <- "../covid-19-data/us-states.csv"
states <- read.csv(fspec) %>%
  mutate(date = as.Date(date))

g <- ggplot(states, aes(x = date, y = cases)) +
  geom_point() +
  scale_x_date(breaks ="2 months") +
  theme(axis.text.x = element_text(angle = 90))
g
