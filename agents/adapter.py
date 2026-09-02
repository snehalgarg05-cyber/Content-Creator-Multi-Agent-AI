import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm


def adapter_agent(state: dict) -> dict:
    log = state.get("processing_log", [])
    log.append("📱 Adapter Agent: Creating platform-specific content...")

    try:
        llm = get_llm(temperature=0.7)

        linkedin_messages = [
            SystemMessage(content="""You are a LinkedIn content expert.
LinkedIn posts that perform best: start with a hook, use line breaks,
tell a story, end with a question or CTA."""),
            HumanMessage(content=f"""
Topic: {state['topic']}
Blog Post: {state['blog_post'][:1000]}
Key Messages: {state['key_messages']}
Tone: {state['tone']}

Write a LinkedIn post that:
- Starts with a BOLD hook
- Uses short paragraphs (1-2 lines max)
- Includes 3-5 key insights as bullet points
- Ends with an engaging question
- Includes 5 relevant hashtags
- Length: 200-300 words
""")
        ]
        linkedin_response = llm.invoke(linkedin_messages)

        twitter_messages = [
            SystemMessage(content="""You are a Twitter/X content expert.
Each tweet must be under 280 characters. Number them as 1/ 2/ 3/ etc."""),
            HumanMessage(content=f"""
Topic: {state['topic']}
Key Points: {state['trending_points']}
Research: {state['research_data'][:600]}

Write a Twitter thread with 8-10 tweets:
- Tweet 1: Bold hook/claim
- Tweets 2-8: One insight per tweet
- Tweet 9: Summary of key takeaways
- Tweet 10: CTA + relevant hashtags

Format as:
1/ [tweet text]
2/ [tweet text]

Each tweet MUST be under 280 characters.
""")
        ]
        twitter_response = llm.invoke(twitter_messages)

        instagram_messages = [
            SystemMessage(content="""You are an Instagram content creator.
Write captions that drive engagement and saves."""),
            HumanMessage(content=f"""
Topic: {state['topic']}
Key Message: {state['key_messages'][:500]}
Tone: {state['tone']}

Write an Instagram caption that:
- Opens with an attention-grabbing first line
- Shares 3-4 valuable insights with emojis
- Ends with a question to drive comments
- Includes 15-20 relevant hashtags in a separate block
- Length: 150-200 words plus hashtags
""")
        ]
        instagram_response = llm.invoke(instagram_messages)

        log.append("✅ Adapter Agent: All platform content ready!")
        return {
            "linkedin_post": linkedin_response.content,
            "twitter_thread": twitter_response.content,
            "instagram_caption": instagram_response.content,
            "processing_log": log,
            "current_step": "adapter_done",
        }

    except Exception as e:
        log.append(f"⚠️ Adapter Error: {str(e)}")
        return {
            "linkedin_post": f"Excited to share insights about {state['topic']}! #AI #Tech",
            "twitter_thread": f"1/ Let us talk about {state['topic']}\n2/ Here is what you need to know...",
            "instagram_caption": f"Learning about {state['topic']} today! #Tech #Learning",
            "processing_log": log,
            "current_step": "adapter_done",
        }
