# Load required libraries
# Install and load required libraries
# Vous pouvez décommenter la ligne ci-dessous pour installer les packages si nécessaire
# install.packages(c("shiny", "leaflet", "sf", "DT"))
library(shiny)
library(leaflet)
library(sf)
library(DT)

# Load the data
my_df_all <- read.csv("dataframe/df_finale.csv", sep = ",")
data_sf <- st_read("france_departements.geojson", quiet = TRUE)
data_sf$data$id <- rownames(data_sf$data)

# Calcul des statistiques pour la choropleth
data_stats <- my_df_all %>%
  group_by(Departement) %>%
  summarize(mean_price = mean(price, na.rm = TRUE))
subset_df <- subset(my_df_all, Departement == 'Haute-Savoie')
print(subset_df)
# Fusionnez les données géospatiales avec vos statistiques
data_to_plot <- merge(data_sf, data_stats, by.x = "nom", by.y = "Departement")
# Créer une palette de couleurs basée sur les statistiques
pal <- colorNumeric(palette = "YlOrRd", domain = data_to_plot$mean_price)

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

# Define server logic
server <- function(input, output, session) {
  observe({
    if (!is.null(input$region)) {
      region_departements <- unique(my_df_all$Departement[my_df_all$region == input$region])
      updateSelectInput(session, "departement", choices = c("Région entière", region_departements))
    }
  })
  
  # Define a reactive dataframe based on filters
  my_df <- reactive({
    if (input$departement == "Région entière") {
      if (input$type_vehicule == "Tous les types") {
        filtered_df <- my_df_all[my_df_all$region == input$region, ]
      } else {
        filtered_df <- my_df_all[my_df_all$region == input$region & my_df_all$type_vehicule == input$type_vehicule, ]
      }
    } else {
      if (input$type_vehicule == "Tous les types") {
        filtered_df <- my_df_all[my_df_all$region == input$region & my_df_all$Departement == input$departement, ]
      } else {
        filtered_df <- my_df_all[my_df_all$region == input$region & my_df_all$Departement == input$departement & my_df_all$type_vehicule == input$type_vehicule, ]
      }
    }
    return(filtered_df)
  })
  # Price Distribution Plot
  output$price_distribution <- renderPlot({
    filtered_df <- my_df()  # en supposant que my_df() retourne un dataframe filtré
    if (is.numeric(filtered_df$price) && sum(!is.na(filtered_df$price)) > 0) {
      hist(filtered_df$price, main = "Distribution des prix", xlab = "Prix", 
           col = "blue", border = "black", breaks = "Sturges")  # Utilisation de la formule de Sturges pour les subdivisions
    }
  })
    # Construire la carte
  output$choropleth_map <- renderLeaflet({
    if (nrow(data_to_plot) > 0 && "sf" %in% class(data_to_plot)) {
      pal <- colorNumeric(palette = "YlOrRd", domain = data_to_plot$mean_price)
      
      leaflet(data_to_plot) %>%
        addTiles() %>%
        setView(lng = 2.2137, lat = 46.2276, zoom = 5) %>%
        addPolygons(
          fillColor = ~pal(mean_price),
          weight = 2,
          opacity = 1,
          color = 'white',
          dashArray = '3',
          fillOpacity = 0.7,
          label = ~paste(nom, ": ", mean_price),
          labelOptions = labelOptions(direction = 'auto')
        )%>%
        addLegend(pal = pal, values = ~mean_price, opacity = 0.7, title = "Mean Price", position = "bottomright")
    } else {
      print("data_to_plot est vide ou n'est pas un objet sf")
    }
})

  # Department Statistics Table
  output$department_stats <- renderDataTable({
    filtered_df <- my_df()
    if (input$departement != "All") {
      filtered_stats <- department_stats(input$departement)
      df_stats <- data.frame(
        Statistic = c("Mean Price", "Median Price", "Max Price", "Min Price", "Min City"),
        Value = c(
          ifelse(is.null(filtered_stats$d_mean), "", sprintf("%.2f", filtered_stats$d_mean)),
          ifelse(is.null(filtered_stats$d_median), "", sprintf("%.2f", filtered_stats$d_median)),
          ifelse(is.null(filtered_stats$d_max), "", sprintf("%.2f", filtered_stats$d_max)),
          ifelse(is.null(filtered_stats$d_min), "", sprintf("%.2f", filtered_stats$d_min)),
          ifelse(is.null(filtered_stats$d_min_city), "", filtered_stats$d_min_city)
        )
      )
      return(df_stats)
    }
    return(NULL)
  })
  
  # Department Statistics Function
  department_stats <- function(selected_department) {
    if (selected_department != "All") {
      data_dept <- my_df_all[my_df_all$Departement == selected_department, ]
      filtered_data_dept <- data_dept %>%
        filter(!is.na(price) & price != 'none')
      if (nrow(filtered_data_dept) > 0) {
        d_mean <- mean(filtered_data_dept$price)
        d_median <- median(filtered_data_dept$price)
        d_max <- max(filtered_data_dept$price)
        d_min <- min(filtered_data_dept$price)
        d_min_city <- filtered_data_dept[which.min(filtered_data_dept$price), "Ville"]
        return(list(d_mean = d_mean, d_median = d_median, d_max = d_max, d_min = d_min, d_min_city = d_min_city))
      }
    }
    return(NULL)
  }
}
# Run the application
shinyApp(ui, server)
