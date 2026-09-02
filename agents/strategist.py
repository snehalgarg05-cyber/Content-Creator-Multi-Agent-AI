import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm


def strategist_agent(state: dict) -> dict:
    log = state.get("processing_log", [])
    log.append("🎯 Strategist Agent: Planning content strategy...")

    try:
        llm = get_llm(temperature=0.5)

        messages = [
            SystemMessage(content="""You are a senior content strategist with 10+ years of experience.
You understand what resonates with different audiences on different platforms."""),
            HumanMessage(content=f"""
Topic: {state['topic']}
Target Audience: {state.get('target_audience', 'Tech professionals')}
Research Data: {state['research_data']}
Trending Points: {state['trending_points']}

Create a content strategy with:
1. CONTENT ANGLE: What unique angle should we take?
2. TONE: What tone works best for this audience?
3. KEY MESSAGES: What are the 3 most important things to communicate?
4. HOOK: What opening line will grab attention immediately?
5. CALL TO ACTION: What should the audience do after reading?

Be specific and actionable.
""")
        ]
        response = llm.invoke(messages)

        tone_messages = [
            SystemMessage(content="Extract only the tone recommendation in 2-3 words from this strategy."),
            HumanMessage(content=f"Strategy: {response.content}\n\nTone (2-3 words only):")
        ]
        tone_response = llm.invoke(tone_messages)

        log.append("✅ Strategist Agent: Strategy ready!")
        return {
            "content_angle": response.content,
            "tone": tone_response.content.strip(),
            "key_messages": response.content,
            "processing_log": log,
            "current_step": "strategist_done",
        }

    except Exception as e:
        log.append(f"⚠️ Strategist Error: {str(e)}")
        return {
            "content_angle": f"Educational and insightful perspective on {state['topic']}",
            "tone": "Professional and engaging",
            "key_messages": f"Key insights about {state['topic']} for modern professionals",
            "processing_log": log,
            "current_step": "strategist_done",
        }
