from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langserve import add_routes

import os
from dotenv import load_dotenv
load_dotenv()


groq_api_key=os.getenv("GROQ_API_KEY")

model=ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

#create prompt templte

system_templete="Translate the language into {language}:"

prompt_templete=ChatPromptTemplate.from_messages([
    ("system",system_templete),
    ("user","{text}")
])

parser=StrOutputParser()

chain=prompt_templete|model|parser

#app defination
app=FastAPI(
    title="Langchain server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces"
)


## Adding chain routes

add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )