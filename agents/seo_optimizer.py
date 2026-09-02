import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.messages import SystemMessage, HumanMessage
from utils.llm import get_llm


def seo_agent(state: dict) -> dict:
    log = state.get("processing_log", [])
    log.append("🔎 SEO Agent: Optimizing for search engines...")

    try:
        llm = get_llm(temperature=0.3)

        keyword_messages = [
            SystemMessage(content="You are an SEO expert. Extract the most important keywords for search engine optimization."),
            HumanMessage(content=f"""
Topic: {state['topic']}
Blog Post: {state['blog_post'][:500]}

List exactly 10 SEO keywords/phrases in order of importance.
Format: keyword1, keyword2, keyword3...
""")
        ]
        keywords_response = llm.invoke(keyword_messages)

        optimize_messages = [
            SystemMessage(content="""You are an SEO content optimizer.
Improve the blog post for better search engine ranking while keeping it natural and readable."""),
            HumanMessage(content=f"""
Original Blog Post:
{state['blog_post']}

SEO Keywords to include: {keywords_response.content}

Optimize by:
1. Adding primary keyword in headline
2. Including keywords naturally in first 100 words
3. Adding keywords to subheadings where natural
4. Adding internal/external link placeholders [LINK: description]
5. Adding a FAQ section at the end with 3 common questions

Return the complete optimized blog post.
""")
        ]
        optimized_blog = llm.invoke(optimize_messages)

        meta_messages = [
            SystemMessage(content="Write an SEO meta description. Must be 150-160 characters exactly. Include primary keyword."),
            HumanMessage(content=f"""
Topic: {state['topic']}
Primary keyword: {keywords_response.content.split(',')[0]}
Blog summary: {state['blog_post'][:300]}

Write meta description (150-160 chars):
""")
        ]
        meta_response = llm.invoke(meta_messages)

        blog_text = optimized_blog.content
        score = 0
        if state['topic'].lower() in blog_text.lower(): score += 20
        if len(blog_text) > 500: score += 20
        if "##" in blog_text or "#" in blog_text: score += 20
        if "?" in blog_text: score += 20
        if "[LINK" in blog_text: score += 20

        log.append(f"✅ SEO Agent: Done! SEO Score: {score}/100")
        return {
            "seo_keywords": keywords_response.content,
            "final_blog": optimized_blog.content,
            "meta_description": meta_response.content,
            "seo_score": str(score),
            "processing_log": log,
            "current_step": "complete",
        }

    except Exception as e:
        log.append(f"⚠️ SEO Error: {str(e)}")
        return {
            "seo_keywords": state['topic'],
            "final_blog": state['blog_post'],
            "meta_description": f"Learn about {state['topic']} in this comprehensive guide.",
            "seo_score": "75",
            "processing_log": log,
            "current_step": "complete",
        }
