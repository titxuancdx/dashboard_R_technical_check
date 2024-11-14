# app.R
library(shiny)
library(leaflet)
library(sf)
library(DT)

source("ui.R")
source("server.R")

# Lancer l'application
shinyApp(ui = ui, server = server)
