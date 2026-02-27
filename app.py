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
    if not customer_review.strip() and not food_trend.strip():
        st.error("⚠️ Please fill in at least one field before generating.")
    else:
        with st.spinner("✨ Generating your product idea..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a food innovation consultant for Biggs Food Corporation, a Filipino casual dining brand.

You MUST ALWAYS respond using EXACTLY this format with ALL 6 fields filled in. Never skip any field. Never add extra commentary before or after.

PRODUCT NAME: [Creative Filipino-inspired dish name]
DESCRIPTION: [Exactly 2 sentences describing the dish, how it is cooked, and what makes it special]
KEY INGREDIENTS: [Exactly 5 ingredients separated by commas]
TARGET MARKET: [Specific age range, who they are, and what occasion this suits]
POSITIONING: [One punchy sentence about the brand positioning]
ESTIMATED PRICE: [A specific price in Philippine Peso, e.g. PHP 189]

Rules you must follow:
- You MUST fill in every single field, no exceptions
- Always use authentic Filipino flavors and cooking methods
- Keep it realistic and feasible for a casual dining chain
- Be specific, never use placeholder text or brackets in your answer"""
                        },
                        {
                            "role": "user",
                            "content": f"""Generate a new Biggs product idea based on these inputs:

CUSTOMER REVIEW:
{customer_review if customer_review.strip() else "No customer review provided, use general Filipino food preferences."}

FOOD TREND:
{food_trend if food_trend.strip() else "No food trend provided, use current popular Filipino food trends."}

Remember to fill in ALL 6 fields: PRODUCT NAME, DESCRIPTION, KEY INGREDIENTS, TARGET MARKET, POSITIONING, and ESTIMATED PRICE."""
                        }
                    ]
                )

                result = response.choices[0].message.content

                # Parse result into a dictionary
                fields = {
                    "PRODUCT NAME": {"icon": "🍴", "color": "#C0392B", "text_color": "white", "is_title": True},
                    "DESCRIPTION": {"icon": "📝", "color": "#f9f9f9", "text_color": "#222"},
                    "KEY INGREDIENTS": {"icon": "🛒", "color": "#f9f9f9", "text_color": "#222"},
                    "TARGET MARKET": {"icon": "🎯", "color": "#f9f9f9", "text_color": "#222"},
                    "POSITIONING": {"icon": "📣", "color": "#f9f9f9", "text_color": "#222"},
                    "ESTIMATED PRICE": {"icon": "💰", "color": "#FEF9E7", "text_color": "#C0392B"},
                }

                parsed = {}
                lines = result.strip().split("\n")
                current_key = None
                for line in lines:
                    if ":" in line:
                        for field in fields:
                            if line.upper().startswith(field):
                                current_key = field
                                parsed[field] = line.partition(":")[2].strip()
                                break
                    elif current_key and line.strip():
                        parsed[current_key] += " " + line.strip()

                st.divider()
                st.subheader("💡 Generated Product Idea")

                for field, style in fields.items():
                    value = parsed.get(field, "Not provided")

                    if style.get("is_title"):
                        st.markdown(f"""
                            <div style='background-color:{style["color"]}; padding:18px; border-radius:10px; margin-bottom:10px'>
                                <h2 style='color:{style["text_color"]}; margin:0'>{style["icon"]} {value}</h2>
                            </div>
                        """, unsafe_allow_html=True)
                    elif field == "ESTIMATED PRICE":
                        st.markdown(f"""
                            <div style='background-color:{style["color"]}; padding:15px; border-radius:10px; margin-bottom:10px; border-left:4px solid #F39C12'>
                                <p style='color:#555; margin:0; font-size:12px'><b>{style["icon"]} {field}</b></p>
                                <p style='margin:5px 0 0 0; font-size:24px; font-weight:bold; color:{style["text_color"]}'>{value}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style='background-color:{style["color"]}; padding:15px; border-radius:10px; margin-bottom:10px; border-left:4px solid #C0392B'>
                                <p style='color:#555; margin:0; font-size:12px'><b>{style["icon"]} {field}</b></p>
                                <p style='margin:5px 0 0 0; color:{style["text_color"]}'>{value}</p>
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
