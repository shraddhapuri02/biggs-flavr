import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="FLAVR - Biggs Food Innovation", page_icon="🍽️")
st.title("🍽️ FLAVR — Biggs Food Innovation Engine")
st.markdown("Paste customer reviews and food trends to generate new product ideas for **Biggs Food Corporation**.")
st.divider()

api_key = st.text_input("Paste your Gemini API key:", type="password")
if not api_key:
    st.info("Get a free key at aistudio.google.com")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are a food innovation consultant for Biggs Food Corporation,
a Filipino casual dining brand. Generate ONE new product idea based on customer reviews
and food trend data in this exact format:

PRODUCT NAME: [Creative Filipino-inspired name]
DESCRIPTION: [1-2 sentences about the dish]
KEY INGREDIENTS: [4-6 core ingredients]
TARGET MARKET: [Who it's for, age range, occasion]
POSITIONING: [One sentence brand statement]
ESTIMATED PRICE: [Price in PHP]

Always use authentic Filipino flavors. Be specific and feasible for a casual dining chain."""
)

st.subheader("📥 Enter Your Data")

customer_review = st.text_area(
    "Customer Reviews",
    placeholder="Paste customer reviews here... e.g. I love Biggs lechon but wish there was a lighter wrap version!",
    height=150
)

food_trend = st.text_area(
    "Food Trend / Blog Excerpt",
    placeholder="Paste a food trend article here... e.g. Filipino street food is going global with handheld formats trending on TikTok.",
    height=150
)

if st.button("🚀 Generate Product Idea", type="primary", use_container_width=True):
    if not customer_review.strip() or not food_trend.strip():
        st.error("Please fill in both fields before generating.")
    else:
        with st.spinner("Generating idea with Gemini..."):
            prompt = f"""CUSTOMER REVIEW:
{customer_review}

FOOD TREND:
{food_trend}

Generate a new Biggs product idea based on the above."""
            response = model.generate_content(prompt)
            result = response.text

        st.divider()
        st.subheader("💡 Generated Product Idea")
        st.success(result)

        st.divider()
        st.download_button(
            label="⬇️ Download This Idea",
            data=result,
            file_name="biggs_idea.txt",
            mime="text/plain",
            use_container_width=True
        )

st.divider()
st.caption("FLAVR — Biggs Food Innovation Engine | Powered by Gemini 1.5 Flash")
```

4. Click the green **Commit changes** button → **Commit changes** again

---

**STEP 5 — Deploy on Streamlit**

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **Sign in with GitHub** → authorize it
3. Click **Create app**
4. Fill in:
   - Repository: `biggs-flavr`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **Deploy** — wait about 2 minutes

---

**STEP 6 — Get your live link**

Once deployed you'll see your app live at a link like:
```
https://yourname-biggs-flavr.streamlit.app
