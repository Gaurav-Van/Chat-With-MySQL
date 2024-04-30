# Chat-With-MySQL
Meet MySQL Assistant: Access database info seamlessly with natural language. No SQL expertise required. Simply ask questions, receive clear responses.<br><br>
YouTube Link of the Demo of the App: https://www.youtube.com/watch?v=HZ6WFniL8W8
<hr>

## Table of Contents
1. What it Does
2. How I Built it
3. Design
4. How to Run it Locally

<hr>

## What it Does
The MySQL Assistant revolutionizes data interaction by providing information in a user-friendly, natural language format. It accepts queries in everyday language, eliminating the need for SQL knowledge. For instance, if you ask, “How many countries have Spanish as an official language?”, the Assistant responds in plain English with the precise count. Additionally, it offers the corresponding SQL query as a reference. This innovative approach simplifies data extraction, making it accessible to all, regardless of their technical expertise. No more gatekeeping - just straightforward, effective data interaction.

https://github.com/Gaurav-Van/Chat-With-MySQL/assets/50765800/c3970c1e-64d7-41c1-a821-704752cf3273

## How I built it
Langchain: The mysql-connector plays a crucial role in Langchain by establishing a connection with the MySQL database, extracting the database schema, and executing database queries. The features of AI and Human Messages contribute to the creation of the app's chat-like interface.

Streamlit: Streamlit is a user-friendly tool that facilitates the creation of web apps and the showcasing of our work. It's a time-saver and was employed to construct the entire web app for this project.

Gemini and Gemini API: The seamless conversion from user-query to SQL-query and back from SQL-query response to natural language is made possible by the freeflow prompt functionality of Gemini and Gemini API.

1) get_sql Function: This function takes in the Database schema, chat history, and user query. It utilizes a well-curated template to convert the user query into an SQL query.

2) get_response Function: This function takes in the Database schema, chat history, user query, and the generated SQL query from the get_sql function. It runs the generated SQL query on the database and feeds the result into a well-curated prompt which also takes in the schema, chat history, and user query.

The process can be summarized as follows: User query + Data Schema -> LLM -> SQL query -> Run Query -> LLM -> Natural Language Answer. This flow represents the core functionality of Langchain.

## Design 
![Chat-with-SQL-Design](https://github.com/Gaurav-Van/Chat-With-MySQL/assets/50765800/3f6d23a3-853e-413c-a2ea-01424a05f35f)

## How to Run it Locally 
Windows
```
Folder
├── src
│   └── app.py
├── design
│   └── Chat-with-SQL-Design.png
├── requirements.txt
├── .env
└── README.md
```

```
create virtual env: python -m venv env
activate it: env\Scripts\activate
```
[inside the virtual env]<br>[Important installations] 

```
pip install streamlit langchain mysql-connector-python python-dotenv google.generativeai
```
or
```
pip install -r requirements.txt
```
[Store your gemini api key inside the .env file]<br>
[from command prompt or terminal run the following command to run the app] 
```
streamlit run src/app.py
```



