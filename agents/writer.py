import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm


def writer_agent(state: dict) -> dict:
    log = state.get("processing_log", [])
    log.append("✍️ Writer Agent: Writing blog post and YouTube script...")

    try:
        llm = get_llm(temperature=0.7)

        blog_messages = [
            SystemMessage(content="""You are an expert content writer who creates
engaging, informative blog posts that rank on Google and get shared widely.
Your writing is clear, structured, and valuable."""),
            HumanMessage(content=f"""
Topic: {state['topic']}
Target Audience: {state.get('target_audience', 'Tech professionals')}
Content Angle: {state['content_angle']}
Tone: {state['tone']}
Research Data: {state['research_data']}
Trending Points: {state['trending_points']}

Write a complete blog post with:
- Compelling headline
- Strong opening hook (2-3 sentences)
- Introduction (1 paragraph)
- 4-5 main sections with subheadings
- Real examples and data points
- Conclusion with key takeaways
- Call to action

Target length: 800-1000 words.
IMPORTANT: Write ENTIRE content in {state.get('language', 'English')} language only.
""")
        ]
        blog_response = llm.invoke(blog_messages)

        youtube_messages = [
            SystemMessage(content="""You are a YouTube script writer who creates
engaging video scripts. You know how to hook viewers in the first 30 seconds."""),
            HumanMessage(content=f"""
Topic: {state['topic']}
Research: {state['research_data']}
Key Messages: {state['key_messages']}

Write a YouTube video script (5-7 minutes) with:
- HOOK (first 30 seconds - grab attention immediately)
- INTRO (introduce what they will learn)
- MAIN CONTENT (3-4 sections with clear transitions)
- EXAMPLES (real world applications)
- OUTRO (summary + subscribe CTA)

Include [PAUSE], [SHOW GRAPHIC], [CUT TO] directions.
""")
        ]
        youtube_response = llm.invoke(youtube_messages)

        log.append("✅ Writer Agent: Blog post and YouTube script ready!")
        return {
            "blog_post": blog_response.content,
            "youtube_script": youtube_response.content,
            "processing_log": log,
            "current_step": "writer_done",
        }

    except Exception as e:
        log.append(f"⚠️ Writer Error: {str(e)}")
        return {
            "blog_post": f"# {state['topic']}\n\nA comprehensive guide to understanding {state['topic']} in today's world...",
            "youtube_script": f"Hey everyone! Today we are talking about {state['topic']}...",
            "processing_log": log,
            "current_step": "writer_done",
        }