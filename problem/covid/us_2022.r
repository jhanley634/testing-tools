#! /usr/bin/env Rscript

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
states <- read.csv(fspec)
