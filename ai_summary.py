# Import necessary libraries or modules
import os

# set up your OpenAI API KEY
os.environ["OPENAI_API_KEY"] = os.environ["OPENAI_API_KEY"] # referring to the OPEN_API_KEY in my environment for secure referencing


# importing stuff for langchain
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool

# trying the chat gpt version
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

"""
The stock_purchase_reasoning function takes in a string parameter of the stock's name and returns
a paragraph of AI-generated text summarizing the stock, incorporating company overview, recent news, stock price,
and future outlook. If information is insufficient, a relevant message is returned. This is all made possible
by LangChain, OpenAI, and prompt-engeineeering
"""
def stock_purchase_reasoning(stock_name):

    # Create a list containing an instance of the YahooFinanceNewsTool
    tools = [YahooFinanceNewsTool()]

    # Create a ConversationBufferMemory instance for storing chat history
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # Create a ChatOpenAI instance for language generation
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], temperature=0)

    # Initialize an agent chain with specified tools, llm, agent type, verbosity, and memory
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
    )
    response = agent_chain.run(
        f" Assume that you are a professional writer. Write a paragraph summarizing the {stock_name} stock. You can't mention that you are a professionar writer or AI system in your response, and you can't talk in the first person. The first section of the paragraph should be a brief overview of the company. The second section should talk about any recent news on the company. The third section should talk about the stock's price. And the fourth section should talk about the future of the company and the stock. Within this paragraph you should incorporate the stock's price, the company's earnings, and how macroeconomic forces will impact the position of the company. If you can't find recent news on the company or stock, then simply provide a general summary about the company and its stock. If no information can be found, simply ouput that there is too little information to provide a sufficient summary on {stock_name}.",
    )

    # return the response
    return response

# if someone just runs this individual program, retrieve a summary on Apple
if __name__ == "__main__": 
    stock_purchase_reasoning("Apple")