#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(DT)



# Define UI for application that draws a histogram
shinyUI(fluidPage(

  # Application title
  #titlePanel("Telegram VV Volosin Post #220"),

  # Sidebar with a slider input for number of bins
  sidebarLayout(
    sidebarPanel(width = 0),

    # Show a plot of the generated distribution
    mainPanel(
      
      textInput("search_terms", "Search (use the pipe \"|\" character to separate the search terms", "свободный|заговор"),
      DT::dataTableOutput("mytable"),
      downloadButton("downloadData", "Download")
      
    )
  )
))
