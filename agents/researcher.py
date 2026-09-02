import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm


def researcher_agent(state: dict) -> dict:
    topic = state["topic"]
    log = state.get("processing_log", [])
    log.append("🔍 Researcher Agent: Analyzing topic and gathering insights...")

    try:
        llm = get_llm(temperature=0.4)

        messages = [
            SystemMessage(content="""You are an expert research analyst and content specialist.
Provide rich, detailed research insights. Write at least 400-500 words."""),
            HumanMessage(content=f"""
Topic: {topic}
Target Audience: {state.get('target_audience', 'General public')}
Language: {state.get('language', 'English')}

Provide DETAILED research covering:
1. OVERVIEW: What is this topic? Why does it matter? (100 words)
2. KEY FACTS: At least 5-7 specific facts or important points
3. CURRENT TRENDS: Latest developments
4. BENEFITS: Why should people care?
5. COMMON MISCONCEPTIONS: What do people get wrong?
6. PRACTICAL APPLICATIONS: How can people use this knowledge?

IMPORTANT: Write in {state.get('language', 'English')} language only.
Write at least 400-500 words total.
""")
        ]
        response = llm.invoke(messages)

        trend_messages = [
            SystemMessage(content="You are a trend analyst. Extract key trending points."),
            HumanMessage(content=f"""
From this research about {topic}, extract exactly 7 key trending points.
Research: {response.content}
Language: {state.get('language', 'English')}
List 7 specific trending bullet points in {state.get('language', 'English')}:
""")
        ]
        trending = llm.invoke(trend_messages)

        log.append("✅ Researcher Agent: Deep research complete!")
        return {
            "research_data": response.content,
            "trending_points": trending.content,
            "processing_log": log,
            "current_step": "researcher_done",
            "error": None
        }

    except Exception as e:
        log.append(f"⚠️ Researcher Error: {str(e)}")
        return {
            "research_data": f"Research on {topic}: Analysis of current trends and opportunities.",
            "trending_points": f"- {topic} is evolving rapidly\n- Growing adoption\n- New developments emerging\n- Increasing interest\n- Positive future outlook",
            "processing_log": log,
            "current_step": "researcher_done",
            "error": str(e)
        }