import os
import asyncio
import streamlit as st
from crawl4ai import AsyncWebCrawler
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY missing")
    st.stop()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")

async def _crawl(url: str) -> str:
    async with AsyncWebCrawler(verbose=False) as crawler:
        res = await crawler.arun(url=url)
        return res.markdown

def crawl(url: str) -> str:
    return asyncio.run(_crawl(url))

def hindi_summary(text: str) -> str:
    prompt = f"""
Tum ek explainer ho.

Niche ek web page ka content diya gaya hai:

----------------
{text}
----------------

TASK (sirf HINDI me likho):

Is page ka 5–8 paragraph ka clear aur simple summary banao.
"""
    resp = model.generate_content(prompt)
    return resp.text

def main():
    st.title("Crawl4AI + Gemini (Hindi Analyzer)")

    url = st.text_input("URL दर्ज करें:",
        "https://lexfridman.com/peter-steinberger-transcript")

    if st.button("Analyze (Hindi Summary)"):
        if not url.strip():
            st.warning("कृपया URL दर्ज करें।")
        else:
            with st.spinner("Crawling + Analyzing..."):
                text = crawl(url)
                result = hindi_summary(text)
                st.markdown(result)

if __name__ == "__main__":
    main()