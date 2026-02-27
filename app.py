import streamlit as st
from groq import Groq

st.set_page_config(page_title="FLAVR - Biggs Food Innovation", page_icon="🍽️", layout="wide")

# Header
st.markdown("""
    <div style='background-color:#C0392B; padding: 20px; border-radius: 10px; margin-bottom: 20px'>
        <h1 style='color:white; text-align:center; margin:0'>🍽️ FLAVR</h1>
        <p style='color:white; text-align:center; margin:0; font-size:16px'>Biggs Food Innovation Engine — Powered by AI</p>
    </div>
""", unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Input section
st.subheader("📥 Enter Your Data")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**🗣️ Customer Reviews**")
    customer_review = st.text_area(
        label="customer_review",
        label_visibility="collapsed",
        placeholder="Paste customer reviews here...\n\nExample: I love Biggs lechon but wish there was a lighter wrap version I can eat on the go!",
        height=200
    )

with col2:
    st.markdown("**📰 Food Trend / Blog Excerpt**")
    food_trend = st.text_area(
        label="food_trend",
        label_visibility="collapsed",
        placeholder="Paste a food trend article here...\n\nExample: Filipino street food is going global with handheld formats trending on TikTok across Southeast Asia.",
        height=200
    )

st.divider()
generate_btn = st.button("🚀 Generate Product Idea", type="primary", use_container_width=True)

if generate_btn:
    if not customer_review.strip() or not food_trend.strip():
        st.error("⚠️ Please fill in both fields before generating.")
    else:
        with st.spinner("✨ Generating your product idea..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a food innovation consultant for Biggs Food Corporation,
a Filipino casual dining brand. Generate ONE new product idea based on customer reviews
and food trend data in this exact format:

PRODUCT NAME: [Creative Filipino-inspired name]
DESCRIPTION: [1-2 sentences about the dish]
KEY INGREDIENTS: [4-6 core ingredients]
TARGET MARKET: [Who it's for, age range, occasion]
POSITIONING: [One sentence brand statement]
ESTIMATED PRICE: [Price in PHP]

Always use authentic Filipino flavors. Be specific and feasible for a casual dining chain."""
                        },
                        {
                            "role": "user",
                            "content": f"""CUSTOMER REVIEW:
{customer_review}

FOOD TREND:
{food_trend}

Generate a new Biggs product idea based on the above."""
                        }
                    ]
                )

                result = response.choices[0].message.content

                # Parse and display result nicely
                st.divider()
                st.subheader("💡 Generated Product Idea")

                # Display each field in its own styled card
                lines = result.strip().split("\n")
                for line in lines:
                    if line.strip() == "":
                        continue
                    if ":" in line:
                        label, _, value = line.partition(":")
                        label = label.strip()
                        value = value.strip()

                        if "PRODUCT NAME" in label:
                            st.markdown(f"""
                                <div style='background-color:#C0392B; padding:15px; border-radius:10px; margin-bottom:10px'>
                                    <h2 style='color:white; margin:0'>🍴 {value}</h2>
                                </div>
                            """, unsafe_allow_html=True)

                        elif "DESCRIPTION" in label:
                            st.markdown(f"""
                                <div style='background-color:#f9f9f9; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #C0392B'>
                                    <p style='color:#555; margin:0; font-size:13px'><b>📝 DESCRIPTION</b></p>
                                    <p style='margin:5px 0 0 0'>{value}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        elif "KEY INGREDIENTS" in label:
                            st.markdown(f"""
                                <div style='background-color:#f9f9f9; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #C0392B'>
                                    <p style='color:#555; margin:0; font-size:13px'><b>🛒 KEY INGREDIENTS</b></p>
                                    <p style='margin:5px 0 0 0'>{value}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        elif "TARGET MARKET" in label:
                            st.markdown(f"""
                                <div style='background-color:#f9f9f9; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #C0392B'>
                                    <p style='color:#555; margin:0; font-size:13px'><b>🎯 TARGET MARKET</b></p>
                                    <p style='margin:5px 0 0 0'>{value}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        elif "POSITIONING" in label:
                            st.markdown(f"""
                                <div style='background-color:#f9f9f9; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #C0392B'>
                                    <p style='color:#555; margin:0; font-size:13px'><b>📣 POSITIONING</b></p>
                                    <p style='margin:5px 0 0 0'>{value}</p>
                                </div>
                            """, unsafe_allow_html=True)

                        elif "ESTIMATED PRICE" in label or "PRICE" in label:
                            st.markdown(f"""
                                <div style='background-color:#FEF9E7; padding:15px; border-radius:10px; margin-bottom:10px; border-left: 4px solid #F39C12'>
                                    <p style='color:#555; margin:0; font-size:13px'><b>💰 ESTIMATED PRICE</b></p>
                                    <p style='margin:5px 0 0 0; font-size:20px; font-weight:bold; color:#C0392B'>{value}</p>
                                </div>
                            """, unsafe_allow_html=True)

                st.divider()
                st.download_button(
                    label="⬇️ Download This Idea",
                    data=result,
                    file_name="biggs_idea.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

st.divider()
st.caption("FLAVR — Biggs Food Innovation Engine | Powered by Groq + LLaMA 3.3 | Biggs Food Corporation")
