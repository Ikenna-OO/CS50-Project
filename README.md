## Documentation

Youtube Video Link: https://youtu.be/xBuuXQlhJZo.

### Overview
This website primarily uses Flask, Plotly, Sqlite3, OpenAI, and LangChain to create a stock research website that allows you to learn more about stocks and keep track of your personal portfolio. With Langchain and OpenAI, the program provides an AI-generated summary of the stock in the manner of a professional writer.

### Open API Key and Virtual Environment Setup
This program requires that you have an OpenAI account and configure your OpenAI API key to the os.environ["OPENAI_API_KEY"] value in program.py. To set up an OpenAI API key, please refer to this page: https://platform.openai.com/docs/quickstart?context=python. This project worked best when following the python installation, virtual environment setup, openai python library installation, and recommended API key for all projects steps as outlined in the link above. 

For ensuring that your OpenAI API key is properly setup, you can run echo $OPENAI_API_KEY in the terminal if you are a mac user and echo %OPENAI_API_KEY% if you are a Windows user. It should display your API key. If that fails to work, make sure that you followed the installation set ups as outlined by OpenAI at the following link: https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key.

To figure out how to set up the virtual environment, simply refer to https://docs.python.org/3/tutorial/venv.html on managing virtual environments. For ease of use, the project worked best when pip was upgraded to pip-23.3.1, which can be done by typing 
pip install --upgrade pip==23.3.1 into the command line. When setting up my OpenAI API key, I found it useful to move my .zshrc file to the home directory by inputting mv .zshrc ~/ into the command line. While this program does cost money (about $0.002 per transaction), OpenAI offers around $5 of credit when first creating an account, and the program itself only makes 1 transaction per ticker. 

### Requirements

To get started, you'll need to download the code. Next, you'll need to create an OpenAI virtual environment for this project such that all of the requirements are met. The requirements are outlined in requirements.txt. 

### Setting Up the Sqlite3 Database

Next, you're going to want to ensure that the Sqlite3 database is set up. Enter the database by typing sqlite3 stock_data.db. Afterward, type in .schema. You should see a table that states the following: 
CREATE TABLE stock_data (
name TEXT NOT NULL,
sector TEXT NOT NULL,
PR TEXT NOT NULL, PE NUMERIC NOT NULL, high NUMERIC NOT NULL, low NUMERIC NOT NULL, isAdded BIT, tickor TEXT);

Next, you'll want to make sure that there isn't anything in the table. in the sqlite3 command line, type SELECT * FROM stock_data;. If it returns nothing, than that's good. If there is something in this table, then simply type DELETE FROM stock_data;. That way, you'll be able to start with an up to date portfolio. Next you'll wan to exit out of the sqlite3 command line so that you can begin running your program. You can either try creating another terminal, typing control-d for a mac user, or, for Windows users, type .exit or .quit. 


### Running the program

To run the program, you must prompt the command line python app.py as opposed to flask run. The latter will run into issues in which the flask version won't refer to the OpenAI virtual environment containing the proper flask, openai, and other crucial, additional libraries for running this program. However, running python app.py will resolve these issues by referring to the libraries within the virtual environment that you had set up prior. 

After running python app.py in the command line, you should see a link to click on, which will take you to your locally run website. Use Command-click on that link to access the website. This site is best suited towards computers. All of the css was custom-made. Unfortunately, plotly has very strict, arbtirary stylings for its graphs, which is why the mobile experience is subpart relative to the computer and desktop experience. The graphs are made possible by creating and explortig plotly figures in python in the back end, transforming them into JSON code via the JSONEncoder in app.py, and finally visualizing them in the HTML code with plotly. 

Whe typing in stocks, the website will simply reload if you inputted an invalid stock ticker. Moreover, when first coming across a new ticker, the website will take sometime to create the stock-specific page as the LangChain program will be conjuring its summary. This summary can be found when observing the terminal. Once the summary is finished, the new page will be produced, and the summary will be stored into the database such that the next time the ticker is inputted, it will take signficantly less time to create the webstie. 

All buying and selling functionality takes place within the individual page of a stock's information. To add or drop a stock to your research's portfolio, simply use the selection feature at the top-right of the page. If you want to go back to the home page without adding or dropping the page, simply click the Back button at the top left of the page. 



