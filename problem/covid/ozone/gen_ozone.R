#! /usr/bin/env Rscript

# cf https://rdrr.io/cran/mlbench/man/Ozone.html#heading-1

renv::activate()
if (!require("mlbench", quietly = TRUE)) {
  renv::install("mlbench")
}
library(mlbench)

data(Ozone)

write.csv(Ozone, file = '/tmp/ozone.csv')
