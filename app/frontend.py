import streamlit as st
import requests
import json

# Configuration
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="ReadCast AI", page_icon="🎙️", layout="wide")

st.title("🎙️ ReadCast AI")
st.caption("Your personalized AI podcast generator")

# Sidebar - Ingest
with st.sidebar:
    st.header("📥 Add Content")
    url_input = st.text_input("Article URL", placeholder="https://...")
    if st.button("Add to Queue"):
        if url_input:
            try:
                res = requests.post(f"{API_URL}/ingest", json={"url": url_input, "source": "streamlit"})
                if res.status_code == 200:
                    st.success("Added successfully!")
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")
        else:
            st.warning("Please enter a URL")

    st.divider()
    st.markdown("### 📊 Status")
    try:
        articles = requests.get(f"{API_URL}/articles").json()
        pending_count = len(articles)
        st.metric("Articles in Queue", pending_count)
    except:
        st.metric("Articles in Queue", "Offline")

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📰 Reading Queue")
    if pending_count > 0:
        for art in articles:
            with st.expander(f"{art['title']}", expanded=False):
                st.markdown(f"**Source:** {art['url']}")
                st.text(art['status'])
    else:
        st.info("Queue is empty. Add some articles from the sidebar!")

with col2:
    st.subheader("🎧 Generate Episode")
    if st.button("🎙️ Create New Podcast", type="primary", disabled=(pending_count==0)):
        with st.spinner("Reading articles, writing script, and recording audio..."):
            try:
                res = requests.post(f"{API_URL}/generate")
                if res.status_code == 200:
                    data = res.json()
                    st.success("Episode Generated!")
                    
                    st.markdown(f"### {data['title']}")
                    st.audio(data['audio_path']) # In MVP this is dummy audio
                    
                    with st.expander("View Script"):
                        st.markdown(data['script'])
                else:
                    st.error(f"Generation failed: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.markdown("Powered by **FastAPI** & **Streamlit**")
