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
tab1, tab2, tab3 = st.tabs(["📚 Reading Queue", "🎙️ Podcast Library", "🗄️ Archives"])

with tab1:
    st.subheader("Pending Articles")
    if pending_count > 0:
        for art in articles:
            col_text, col_act = st.columns([4, 1])
            with col_text:
                st.markdown(f"**[{art['title']}]({art['url']})**")
                st.caption(f"Source: {art['url'][:50]}...")
            with col_act:
                if st.button("🗑️", key=f"del_{art['id']}"):
                    requests.delete(f"{API_URL}/articles/{art['id']}")
                    st.rerun()
        
        st.divider()
        if st.button("🎙️ Generate Podcast from Queue", type="primary"):
            with st.spinner("Processing... Alex and Jamie are reading your articles..."):
                try:
                    res = requests.post(f"{API_URL}/generate")
                    if res.status_code == 200:
                        st.balloons()
                        st.success("Episode ready! Check the Library tab.")
                    else:
                        st.error(f"Failed: {res.text}")
                except Exception as e:
                    st.error(str(e))
    else:
        st.info("Queue is empty. Add links via the sidebar!")

with tab2:
    st.subheader("Your Episodes")
    try:
        podcasts = requests.get(f"{API_URL}/podcasts").json()
        if podcasts:
            for pod in podcasts:
                with st.expander(f"🎧 {pod['title']}", expanded=False):
                    st.audio(pod['audio_path'])
                    st.caption("Script Preview:")
                    st.text(pod['script'][:500] + "...")
                    if st.button("Delete Episode", key=f"del_pod_{pod['id']}"):
                        requests.delete(f"{API_URL}/podcasts/{pod['id']}")
                        st.rerun()
        else:
            st.write("No podcasts yet.")
    except Exception as e:
        st.error("Could not load library.")

with tab3:
    st.subheader("All Articles")
    # Placeholder for a full history view
    st.write("History of all processed links will appear here.")

st.divider()
st.markdown("Powered by **FastAPI** & **Streamlit**")
