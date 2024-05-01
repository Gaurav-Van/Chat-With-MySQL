import os
import streamlit as st
import google.generativeai as genai
from langchain_community.utilities import sql_database
from langchain_core.messages import AIMessage, HumanMessage

#from dotenv import load_dotenv # when you are using it locally uncomment the import

# ------------ Loading environment, api_keys and Initializing the Gemini Model configuration files --------------------

#load_dotenv() # when you are using it locally uncomment this line

genai.configure(api_key=st.secrets["GEMINI_API_KEY_ID_1"]) # extracting api_key from streamlit cloud. But if you are # when you are using it locally get the api key from .env file. 

generation_config = {
    "temperature": 0.2,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 3000,
}

# -----------------------------------------------------------------------------------------------------------------------

st.set_page_config(page_title="Chat with MySQL", page_icon=":speech_ballon:") # streamlit page configuration 

st.title("Chat with MySQL")


# Initializing chat history. Useful in context understanding of LLMs 

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
         AIMessage(content="Hello! I'm a MySQL assistant. Ask me anything about your database.")
    ]

# Function: connects the database to the app using mysql-connector. Input given from sidebar
def init_database(user:str, password:str, host:str, port:str, database:str) -> sql_database.SQLDatabase:
    db_uri = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
    return sql_database.SQLDatabase.from_uri(db_uri)

# Function: Generates the sql query. Reads the Database Schema and chat_history and generates the sql query based on the user_question. 
# This sql_query will be the input for getting response in natural language. 
def get_sql(schema, chat_history, question):
    template = f"""
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
    
        <SCHEMA>{schema}</SCHEMA>
    
        Conversation History: {chat_history}
    
        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
    
        For example:
        Question: which 3 artists have the most tracks?
        SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
        Question: Name 10 artists
        SQL Query: SELECT Name FROM Artist LIMIT 10;
    
        Your turn:
    
        Question: {question}
        SQL Query:
        """

    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config) #init the gemini model 

    try:
        response = model.generate_content(template) #generating and parsing the response with error handling
        if response.text is not None:
                answer = response.text
        else:
            answer = "no response generated"

    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    return answer

#Function: Generates the Natural Language response based on input sql query from function get_sql. Reads the schema, chat_history, question and runs the sql_query using db.run
def get_response(schema, chat_history, question, sql_result, response):

    template = f"""
        You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
        Based on the table schema below, question, sql query, and sql response, write a natural language response.Take the conversation history into account
        <SCHEMA>{schema}</SCHEMA>

        Conversation History: {chat_history}
        User question: {question}
        SQL Query: <SQL>{sql_result}</SQL>
        SQL Response: {response}
        """  
    
    model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)

    try:
        result = model.generate_content(template)
        if result.text is not None:
                answer = result.text
        else:
            answer = "no response generated"

    except Exception as e:
        answer = f"An error occurred: {str(e)}"

    return answer

#Sidebar: Takes input required to connect the MySQL Database. 
with st.sidebar:
    st.subheader("Settings")
    st.write("This is a simple chat application using MySQL. Connect to the database and start chatting.")

    st.text_input("Host", help="Name of Host", key="Host")
    st.text_input("Port", help="Port Number", key="Port")
    st.text_input("User", help="Name of user", key="User")
    st.text_input("Password", type="password", help="Information is removed after every session", key="Password")
    st.text_input("Database", help="Name of the Database", key="Database")

    if st.button("Connect"):
        try:
            with st.spinner("Connecting to database..."):
                db=init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to database!")
        except Exception as e:
            st.warning(e)

#chat: Forms the chat-like interface
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

#User: Futher actions on user-query in chat-like interface. Place where input from user and output from the assistant takes place in natural language 
user_query = st.chat_input("Type a message...")
if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        sql_result = get_sql(st.session_state.db.get_table_info(), st.session_state.chat_history, user_query)
        try:
            response = get_response(st.session_state.db.get_table_info(), st.session_state.chat_history, user_query, sql_result, st.session_state.db.run(sql_result))
            st.markdown(response)
            st.caption(sql_result)
            st.session_state.chat_history.append(AIMessage(content=response))
        except:
            st.warning("I am Sorry. It looks like I made some mistake while trying to form logic or execute the correct logic. Please Try Again. I will try my best")
            st.warning("Tip: Either Check the Prompt or Try to Improve it.")



