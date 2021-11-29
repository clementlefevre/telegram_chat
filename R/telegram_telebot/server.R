#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(data.table)
library(openxlsx)
library(lubridate)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  output$value <- renderText({
    input$caption
  })

  DT <-  fread(cmd = 'unzip -p df_all.zip', encoding = "UTF-8")
  DT[,date:=ymd_hms(date)]
  DT <- DT[order(-date)]
  DT <- DT[, c("date", "user_id", "total_posts_of_user_id", "message")]

  filtered_data <- reactive({
    DT[grepl(input$search_terms, message, ignore.case = T)]
  })



  output$mytable <- DT::renderDT(
    filtered_data(),
    server = TRUE, extensions = "Scroller", options = list(
      deferRender = TRUE,
      scrollX = FALSE,
      scrollY = 800,
      scroller = FALSE,
     
      searchHighlight = TRUE,
      dom = 'ltipr',
      search = list(regex = TRUE, caseInsensitive = TRUE, search = input$search_terms)
    )
  )
  
  output$downloadData <- downloadHandler(
    filename = function() {
      "export.xlsx"
    },
    content = function(file) {
      openxlsx::write.xlsx(filtered_data(),file)
    })
})

