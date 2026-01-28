import os
from typing import List
# import openai  # In a real scenario, we'd use the openai client

# Mocking the LLM interaction for MVP to avoid API key dependency issues immediately
# In prod: from openai import OpenAI

SYSTEM_PROMPT = """
You are the producer of "ReadCast", a daily podcast where two AI hosts, Alex (energetic, curious) and Jamie (analytical, calm), discuss articles the user has saved.

Your goal is to synthesize the provided articles into a natural, engaging conversation. 
- Don't just read the summary; discuss the implications.
- Find connections between different articles if possible.
- Keep it under 1000 words.
- Format the output as a script:
  Alex: [text]
  Jamie: [text]
"""

def generate_podcast_script(articles: List[dict]) -> str:
    """
    Takes a list of article dicts {'title': str, 'content': str} and returns a dialogue script.
    """
    if not articles:
        return "Alex: Looks like there's nothing to read today! \nJamie: Time to go find some good articles."

    # Prepare context
    context = ""
    for idx, art in enumerate(articles):
        # Truncate content to avoid token limits in MVP
        snippet = art['content'][:2000] 
        context += f"Article {idx+1}: {art['title']}\nContent: {snippet}\n\n"

    # In a real implementation:
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # response = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": SYSTEM_PROMPT},
    #         {"role": "user", "content": f"Here are the articles for today:\n{context}"}
    #     ]
    # )
    # return response.choices[0].message.content

    # MOCK RESPONSE for MVP demonstration
    return f"""
Alex: Welcome back to ReadCast! Today we have some interesting stuff on the list.
Jamie: That's right. We're looking at {len(articles)} articles today.
Alex: Let's dive into the first one: "{articles[0]['title']}". 
Jamie: It seems to cover some key points about... (AI summarizes content here based on: {articles[0]['content'][:50]}...)
Alex: fascinating!
"""
