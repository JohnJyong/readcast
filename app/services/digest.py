import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

# Load env vars
load_dotenv()

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
        # Truncate content to avoid token limits (basic truncation)
        snippet = art['content'][:3000] 
        context += f"Article {idx+1}: {art['title']}\nContent: {snippet}\n\n"

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "System: Error - OPENAI_API_KEY not found in .env file."

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # Use 3.5 for speed/cost in MVP, switch to 4 for quality
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Here are the articles for today:\n{context}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"System: Error generating script - {str(e)}"
