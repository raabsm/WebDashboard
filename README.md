OVERVIEW: I created a WebPage that asks the user to input a city name, and then queries data from three different APIs, then renders that API information onto a new WebPage once all the data is collected.

Initially, the mainPage.html is rendered, which asks the user to input a city. From there, I accumulate all of the JSON information using python requests library, then format that information onto the template dashboard.html.  When run without errors, the dashboard presents information on the weather, top 10 restaurants, and nearby airports of the user-inputted city.  

The Program also logs all GET/POST requests, API requests, and API errors on a seperate file named logFile.txt.  Also, all logs are stored in a mongoDB collection named "ServerActivity."  Each GET/POST request and all API response information are stored in this DB. 

Besides for obvious formatting issues of the dashboard, another limitation is that if one of the API calls fail, the dashboard doesn't render at all, and instead either presents the mainPage again propting the user to input another city, or displays a different webpage that elaborates on the error that was thrown.  For Example, if you input the city "glogovac", the weather API works normally, but the Restaurant API does not, so the dashboard.html page does not render.  You can see that this is the case by examining the log.

