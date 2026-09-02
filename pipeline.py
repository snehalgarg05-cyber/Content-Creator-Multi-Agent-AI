import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langgraph.graph import StateGraph, END
from state import ContentState
from agents.researcher import researcher_agent
from agents.strategist import strategist_agent
from agents.writer import writer_agent
from agents.adapter import adapter_agent
from agents.seo_optimizer import seo_agent


def should_continue(state: dict) -> str:
    if state.get("error") and not state.get("research_data"):
        return "error"
    return "continue"


def error_handler(state: dict) -> dict:
    log = state.get("processing_log", [])
    log.append("⚠️ Error handler: Using fallback data, continuing pipeline...")
    return {**state, "processing_log": log, "current_step": "error_handled"}


def build_pipeline():
    graph = StateGraph(ContentState)

    graph.add_node("researcher", researcher_agent)
    graph.add_node("strategist", strategist_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("adapter", adapter_agent)
    graph.add_node("seo", seo_agent)
    graph.add_node("error_handler", error_handler)

    graph.set_entry_point("researcher")

    graph.add_conditional_edges(
        "researcher",
        should_continue,
        {"continue": "strategist", "error": "error_handler"}
    )

    graph.add_edge("strategist", "writer")
    graph.add_edge("writer", "adapter")
    graph.add_edge("adapter", "seo")
    graph.add_edge("seo", END)
    graph.add_edge("error_handler", "strategist")

    return graph.compile()


def run_pipeline(topic: str, target_audience: str = "Tech professionals", language: str = "English"):
    pipeline = build_pipeline()

    initial_state = {
        "topic": topic,
        "target_audience": target_audience,
        "language": language,
        "research_data": "",
        "trending_points": "",
        "content_angle": "",
        "tone": "",
        "key_messages": "",
        "blog_post": "",
        "youtube_script": "",
        "linkedin_post": "",
        "twitter_thread": "",
        "instagram_caption": "",
        "seo_keywords": "",
        "final_blog": "",
        "meta_description": "",
        "seo_score": "",
        "current_step": "starting",
        "processing_log": [f"🚀 Starting pipeline for: {topic}"],
        "error": None
    }

    result = pipeline.invoke(initial_state)
    return result