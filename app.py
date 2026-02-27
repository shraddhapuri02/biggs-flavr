import streamlit as st
from groq import Groq

st.set_page_config(page_title="FLAVR - Biggs Food Innovation", page_icon="🍽️")
st.title("🍽️ FLAVR — Biggs Food Innovation Engine")
st.markdown("Paste customer reviews and food trends to generate new product ideas for **Biggs Food Corporation**.")
st.divider()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.subheader("Enter Your Data")

customer_review = st.text_area(
    "Customer Reviews",
    placeholder="Paste customer reviews here...",
    height=150
)

food_trend = st.text_area(
    "Food Trend / Blog Excerpt",
    placeholder="Paste a food trend article here...",
    height=150
)

if st.button("Generate Product Idea", type="primary", use_container_width=True):
    if not customer_review.strip() or not food_trend.strip():
        st.error("Please fill in both fields before generating.")
    else:
        with st.spinner("Generating idea..."):
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

                st.divider()
                st.subheader("💡 Generated Product Idea")
                st.success(result)

                st.download_button(
                    label="Download This Idea",
                    data=result,
                    file_name="biggs_idea.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")

st.divider()
st.caption("FLAVR — Biggs Food Innovation Engine | Powered by Groq + LLaMA 3.3")
