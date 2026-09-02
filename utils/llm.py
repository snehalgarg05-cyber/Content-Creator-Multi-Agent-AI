import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

def get_llm(temperature: float = 0.7):
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=temperature,
        api_key=os.getenv("GROQ_API_KEY"),
    )

def get_search_tool(max_results: int = 5):
    return TavilySearchResults(
        max_results=max_results,
        api_key=os.getenv("TAVILY_API_KEY"),
    )
