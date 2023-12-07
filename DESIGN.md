# Design Document
For my stock research website, I coupled a Flask-based website with Plotly and LangChain to provide an enhanced user experience for those interested in exploring new stocks. 

### app.py
App.py manages the entirety of the project's logics. It creates a flask App, creates a connection to the stock_data database, and manages the routing between the stock page and index page. The routing is designed such that users can only access the stock page when searching for a stock, and they can go from the stock page back to the index page by either clicking the back button or adding/dropping a stock from their portfolio. 

All of this held together by the global variables last_stock_symbol and last_PR, which keep track of the user's last stock so that when they move from the stock page to the index page, the pie chart and stock list information is updated with the stock they had just added or dropped. 


### analysis_helper.py
The analysis helper code manages all of the data visualizations used throughout the site, and also retrieves the fundamental data about a stock that is displayed in the stock page. A lot of the stock visualization code invovled a strong sense of understanding how yfinance and Plotly work. 

Yfinance addressed the retrieval of a stock's information. Alot of this involved accessing the stock's information via the .info's dictionary-like object associated with a ticker Object and then selecting values withn that dictionary-like object for thigns such as the day's high and low. 

The Plotly library is used for each of the data visualizations. While the pie chart involves providing custom information based on a dictionary pairing sectors to their associated stock counts, the shares price graph uses yfinance to retrieve historical data about a particular stock. 

Creating a separate file for each of these functions makes the code much simpler as it separates data retrieval and graph generation from inputting that information into a new, rendered page. 

### ai_summary.py
This code uses LangChain and OpenAI to provide AI-generated text. LangChain in general is a very cool and powerful software that is capable of holding conversations through its ability to make new statements based on prior conversations or pieces of information. In this case, I leverage LangChain's yfinance tool to find relevant news about a stock and use that information to answer a prompt.

I found prompt engineering to be the most effective way to get a desired output from LangChain. Through prommpt engineering, I tasked the AI model to assume that they were a professional writer who had to summarize a company and its stock. Moreover, they couldn't speak in the first person or mention that they were an AI agent. I broke this prompt up into four different segments: (1) providng a a brief overview of the company and its stock, (2) bringing up any relevant news regarding the company, (3) discussing the stock's price, and (4) providing some commentary on the future of the company's stock. I also added that the AI agent incorporate real numbers about the company's stock information alongside mentioning how macroeconomic forces will impact the company. This gets at the strength of the sector, which ties back to this research website's focus on portfolio diversification across various sectors. 

Lastly, I added a configuration of LangChain that also supported OpenAI. While LangChain alone can be very limited in its data pool, incoporating OpenAI enabled the program to generate responses in numerous different ways based on a broader set of information. 

### layout.html, index.html, and styling
I chose to separate the layout code between index.html and stock.html since each had different layouts and required data. 

The layout.html code is fairly straightforward in that the main Portfolio Section is dynamically generated with inputted data. Depending on the stocks in somoene's portfolio, varying stock tiles and pie charts will be displayed. 

The styling for this project was best implemented using CSS Flexbox. Through flexbox, I was able to create a balanced layout. I also created a main class so that each section can have even margins. I found the dilineation between search functionality and stock presentation to be most effective as it makes routing much simpler and users have a clear understanding of what's going on. 

### stock_layout.html, stock.html, and styling

The stock layout provided a general framework for each of the conjured stock pages. The navigation bar was crucial in making the functionality of this site possible. Users have the option to simply go back, or add/drop the stock to or from their portfolio. By separating each of these functionalities between two different forms, it was much easier for me to manage each of them in app.py and check which form had been submitted. Since I generate and pass in the graphs from app.py to the javascript portion of my html code, I was able to effectivley incorporate the share price graph into my page. All of this is made possible using Jinja. By passing in a stock dictionary into the html page, I was easily able to refer to the specific fundmanetal information and ai-generated summary text using python dictioanry syntax.

Similarily to the stock_layou page, the styling for the page also invovled CSS flexbox. In particular, flexbox was useful in creating the navigation bar and the summary and fundamental data section. 

### Sqlite3 Database

The stock_data database utilzies the following schema:

CREATE TABLE stock_data (
    name TEXT NOT NULL,
    sector TEXT NOT NULL,
    PR TEXT NOT NULL, 
    PE NUMERIC NOT NULL, 
    high NUMERIC NOT NULL, 
    low NUMERIC NOT NULL, 
    isAdded BIT, 
    tickor TEXT);

I structured the database this way so that I can keep all of the information regarding a stock together. Moreover, since it takes a while for LangChain to generate a summary of a stock, this database was very helpful in ensuring that once a stock's summary had already been made, users wouldnt' have to wait again for it to show up. Moreover, since this website is focused on stock research, deletion functionalities weren't of importance as opposed to preserving previous stock information as someone could easily add a stock back to their portfolio. The isAdded BIT value enabled the index page to only show stocks that have been added. Thus, when a stock is dropped, the isAdded value goes to 0, but the stock data still remains preserved in the database, ready to be called again. All of this can be found in the add and buy functionality when handling post requests from a /stock.html file. 




