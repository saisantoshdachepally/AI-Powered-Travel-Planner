import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
 
# ✅ Access Hugging Face Secret API Key
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY")

# ✅ Function to fetch AI-generated travel options
def get_travel_options(source, destination, travel_date):
    system_prompt = SystemMessage(
        content="You are an AI-powered travel assistant. Provide multiple travel options (cab, train, bus, flight) with estimated costs, duration, and relevant travel tips. Also, consider travel date for availability and price fluctuations. and also give the best tourist places with good tips also"
    )
    user_prompt = HumanMessage(
        content=f"I am traveling from {source} to {destination} on {travel_date}. Suggest travel options with estimated cost, duration, and important details."
    )

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)

    try:
        response = llm.invoke([system_prompt, user_prompt])
        return response.content if response else "⚠️ No response from AI."
    except Exception as e:
        return f"❌ Error fetching travel options: {str(e)}"


# ✅ Streamlit UI
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="wide")

# 🔹 Stylish Header (Compact)
st.markdown(
    """
    <style>
        .title-container { text-align: center; margin-bottom: -10px; } 
        .footer { text-align: center; margin-top: -20px; padding-bottom: 5px; }
    </style>
    <div class="title-container">
        <h1>🚀 AI-Powered Travel Planner</h1>
        <p style="font-size:16px;">Plan your trip with AI-powered recommendations.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ✅ Use Columns to Minimize Space
col1, col2, col3 = st.columns([1.5, 3, 1.5])

with col2:
    st.subheader("🛫 Find the Best Travel Options")
    
    source = st.text_input("📍 Enter Source Location", placeholder="Your Location")
    destination = st.text_input("📍 Enter Destination", placeholder="Your Destination")
    travel_date = st.date_input("📅 Select Travel Date", min_value=datetime.today())

    if st.button("🔍 Find Travel Options"):
        if source.strip() and destination.strip():
            with st.spinner("🔄 Fetching best travel options..."):
                travel_info = get_travel_options(source, destination, travel_date)
                st.success("✅ Travel Recommendations:")
                st.markdown(travel_info)
        else:
            st.warning("⚠️ Please enter both source and destination locations.")

# 🔹 Footer (Compact)
st.markdown(
    """
    <hr>
    <div class="footer">
        <p>🌟 Built with ❤️ using Streamlit & AI-powered by Google Gemini 🌟</p>
    </div>
    """,
    unsafe_allow_html=True,
)

