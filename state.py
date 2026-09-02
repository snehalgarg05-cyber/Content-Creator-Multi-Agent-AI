from typing import TypedDict, Optional

class ContentState(TypedDict):
    topic: str
    target_audience: str
    language: str
    research_data: str
    trending_points: str
    content_angle: str
    tone: str
    key_messages: str
    blog_post: str
    youtube_script: str
    linkedin_post: str
    twitter_thread: str
    instagram_caption: str
    seo_keywords: str
    final_blog: str
    meta_description: str
    seo_score: str
    current_step: str
    processing_log: list
    error: Optional[str]