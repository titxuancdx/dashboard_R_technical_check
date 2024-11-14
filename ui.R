library(shiny)
library(leaflet)
library(DT)


my_df_all <- read.csv("dataframe/df_finale.csv", sep = ",")
# Define UI
ui <- fluidPage(
  titlePanel("Dashboard Module"),
  sidebarLayout(
    sidebarPanel(
      selectInput("region", "Select a Region:", choices = unique(my_df_all$region)),
      selectInput("departement", "Select a Department:", choices = NULL),
      selectInput("type_vehicule", "Select a Vehicle Type:", 
                  choices = c("Tous les types", unique(my_df_all$type_vehicule)))
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("Price Distribution", plotOutput("price_distribution")),
        tabPanel("Choropleth Map", leafletOutput("choropleth_map")),
        tabPanel("Department Statistics", dataTableOutput("department_stats"))
      )
    )
  )
)
