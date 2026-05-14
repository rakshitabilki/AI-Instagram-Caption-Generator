import streamlit as st
from groq import Groq
from PIL import Image

# =========================
# GROQ CONFIGURATION
# =========================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Instagram Caption Generator",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

.main-title {
    font-size: 55px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 22px;
    color: #d1d5db;
    margin-bottom: 35px;
}

.caption-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid #334155;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}

.caption-text {
    font-size: 20px;
    color: white;
    font-weight: 500;
    line-height: 1.6;
}

div.stButton > button {
    background-color: #9333ea;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

div.stButton > button:hover {
    background-color: #7e22ce;
}

[data-testid="stFileUploader"] {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.markdown(
    '<div class="main-title">📸 AI Instagram Caption Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload an image and generate stylish AI captions instantly</div>',
    unsafe_allow_html=True
)

# =========================
# IMAGE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

# =========================
# IMAGE DESCRIPTION
# =========================

image_description = st.text_area(
    "Describe your image",
    placeholder="Example: luxury beach sunset vacation photo"
)

# =========================
# OPTIONS
# =========================

col1, col2 = st.columns(2)

with col1:

    style = st.selectbox(
        "Choose Caption Style",
        [
            "Aesthetic",
            "Funny",
            "Romantic",
            "Motivational",
            "Attitude",
            "Luxury",
            "Savage",
            "Travel"
        ]
    )

with col2:

    caption_length = st.selectbox(
        "Choose Caption Length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

# =========================
# GENERATE BUTTON
# =========================

if st.button("✨ Generate Captions"):

    if uploaded_file is not None and image_description:

        # Open image
        image = Image.open(uploaded_file)

        # =========================
        # IMAGE + SENTIMENT ANALYSIS
        # =========================

        left_col, right_col = st.columns([1, 1])

        # LEFT SIDE → IMAGE
        with left_col:

            st.image(
                image,
                caption="Uploaded Image",
                width=320
            )

        # RIGHT SIDE → SENTIMENT ANALYSIS
        with right_col:

            sentiment_prompt = f"""
Analyze this social media image description.

Image Description:
{image_description}

Give:
1. Overall Mood
2. Emotional Tone
3. Social Media Vibe
4. Virality Potential
5. Audience Appeal

Keep answer short and stylish.
"""

            sentiment_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": sentiment_prompt
                    }
                ]
            )

            sentiment = sentiment_response.choices[0].message.content

            st.markdown(
                f"""
                <div style="
                    background-color:#1e293b;
                    padding:20px;
                    border-radius:15px;
                    border:1px solid #334155;
                    min-height:320px;
                ">

                <h3 style="color:#c084fc;">
                    🧠 Sentiment Analysis
                </h3>

                <div style="
                    color:white;
                    font-size:16px;
                    line-height:1.8;
                ">
                    {sentiment.replace(chr(10), "<br>")}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        # =========================
        # PROMPT
        # =========================

        prompt = f"""
Generate 5 Instagram captions.

Image Description:
{image_description}

Style: {style}
Length: {caption_length}

Rules:
- Include emojis
- Trendy and engaging
- Stylish and modern
- Each caption on separate line
"""

        with st.spinner("🧠 AI is generating captions..."):

            try:

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                output = response.choices[0].message.content

                captions = output.split("\n")

                cleaned = []

                for cap in captions:

                    cap = cap.strip()

                    if (
                        not cap
                        or "caption" in cap.lower()
                        or "here are" in cap.lower()
                    ):
                        continue

                    cleaned.append(cap)

                # =========================
                # DISPLAY RESULTS
                # =========================

                st.subheader("✨ Generated Captions")

                for i, cap in enumerate(cleaned[:5], 1):

                    st.markdown(
                        f"""
                        <div class="caption-card">
                            <div class="caption-text">
                                {i}. {cap}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # =========================
                # DOWNLOAD BUTTON
                # =========================

                st.download_button(
                    label="📥 Download Captions",
                    data="\n".join(cleaned[:5]),
                    file_name="captions.txt",
                    mime="text/plain"
                )

            except Exception as e:

                st.error(f"Error: {e}")

    else:

        st.warning(
            "Please upload an image and enter image description!"
        )