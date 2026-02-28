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

# Number of ideas slider
num_ideas = st.slider("How many product ideas do you want?", min_value=1, max_value=5, value=3)

st.divider()
generate_btn = st.button("🚀 Generate Product Ideas", type="primary", use_container_width=True)

if generate_btn:
    if not customer_review.strip() and not food_trend.strip():
        st.error("⚠️ Please fill in at least one field before generating.")
    else:
        with st.spinner("✨ Generating your product ideas..."):
            try:
                # Step 1 — Check if input is food related
                check_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a content checker. Your only job is to determine if the user's input is related to food, drinks, recipes, restaurants, or dining.
Reply with only one word: YES or NO.
YES = the input is about food, drinks, dining, restaurants, ingredients, recipes, or eating.
NO = the input is about anything else like politics, technology, sports, or random topics."""
                        },
                        {
                            "role": "user",
                            "content": f"""Is this input food related?

CUSTOMER REVIEW: {customer_review if customer_review.strip() else "empty"}
FOOD TREND: {food_trend if food_trend.strip() else "empty"}

Reply YES or NO only."""
                        }
                    ]
                )

                is_food_related = check_response.choices[0].message.content.strip().upper()

                if "NO" in is_food_related:
                    st.error("⚠️ Your input doesn't seem to be food related. Please paste food reviews or food trend articles to generate Biggs product ideas.")

                else:
                    # Step 2 — Generate ideas
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "system",
                                "content": f"""You are a food innovation consultant for Biggs Food Corporation, a Filipino casual dining brand.

Generate exactly {num_ideas} different product ideas based on the inputs provided.

For EACH idea use EXACTLY this format and separate each idea with a line of dashes (---):

PRODUCT NAME: [Creative Filipino-inspired dish name]
DESCRIPTION: [Exactly 2 sentences describing the dish, how it is cooked, and what makes it special]
KEY INGREDIENTS: [Exactly 5 ingredients separated by commas]
TARGET MARKET: [Specific age range, who they are, and what occasion this suits]
POSITIONING: [One punchy sentence about the brand positioning]
ESTIMATED PRICE: [A specific price in Philippine Peso, e.g. PHP 189]

Rules you must follow:
- Generate exactly {num_ideas} ideas, no more no less
- Every idea must be different from each other
- You MUST fill in every single field for every idea, no exceptions
- Always use authentic Filipino flavors and cooking methods
- Keep it realistic and feasible for a casual dining chain
- Be specific, never use placeholder text or brackets in your answer
- Separate each idea with ---"""
                            },
                            {
                                "role": "user",
                                "content": f"""Generate {num_ideas} new Biggs product ideas based on these inputs:

CUSTOMER REVIEW:
{customer_review if customer_review.strip() else "No customer review provided, use general Filipino food preferences."}

FOOD TREND:
{food_trend if food_trend.strip() else "No food trend provided, use current popular Filipino food trends."}

Remember to generate exactly {num_ideas} ideas, each with ALL 6 fields filled in, separated by ---"""
                            }
                        ]
                    )

                    result = response.choices[0].message.content

                    # Split into individual ideas
                    ideas = result.strip().split("---")
                    ideas = [idea.strip() for idea in ideas if idea.strip()]

                    st.divider()
                    st.subheader(f"💡 {len(ideas)} Generated Product Ideas")

                    fields = {
                        "PRODUCT NAME": {"icon": "🍴", "color": "#C0392B", "text_color": "white", "is_title": True},
                        "DESCRIPTION": {"icon": "📝", "color": "#f9f9f9", "text_color": "#222"},
                        "KEY INGREDIENTS": {"icon": "🛒", "color": "#f9f9f9", "text_color": "#222"},
                        "TARGET MARKET": {"icon": "🎯", "color": "#f9f9f9", "text_color": "#222"},
                        "POSITIONING": {"icon": "📣", "color": "#f9f9f9", "text_color": "#222"},
                        "ESTIMATED PRICE": {"icon": "💰", "color": "#FEF9E7", "text_color": "#C0392B"},
                    }

                    def parse_and_display(idea_text, idea_number):
                        parsed = {}
                        lines = idea_text.strip().split("\n")
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

                        st.markdown(f"### Idea {idea_number}")

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

                    # Display each idea in its own tab
                    if len(ideas) > 1:
                        tabs = st.tabs([f"Idea {i+1}" for i in range(len(ideas))])
                        for i, (tab, idea) in enumerate(zip(tabs, ideas)):
                            with tab:
                                parse_and_display(idea, i+1)
                    else:
                        parse_and_display(ideas[0], 1)

                    st.divider()
                    st.download_button(
                        label="⬇️ Download All Ideas",
                        data=result,
                        file_name="biggs_ideas.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

st.divider()
st.caption("FLAVR — Biggs Food Innovation Engine | Powered by Groq + LLaMA 3.3 | Biggs Food Corporation")
