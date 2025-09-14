import streamlit as st
from openai import OpenAI
from PIL import Image
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎨 Custom CSS styling
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f8d3f0, #d3e4ff);
        font-family: 'Trebuchet MS', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 40px !important;
        color: #8a2be2;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .friend-card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .friend-photo img {
        border-radius: 50%;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .poem-box {
        background: #fef6ff;
        border-left: 5px solid #8a2be2;
        padding: 15px;
        border-radius: 10px;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Friend Data
# ----------------------------
friends = {
    "shashwat": {
        "name": "Shashwat",
        "photo": "photos/shashwat.jpg",
        "description": "Shashwat is my best friend, always there when I need him. A brother more than a friend.",
        "keywords": ["shashwat", "best friend", "brother"]
    },
    "saloni": {
        "name": "Saloni",
        "photo": "photos/saloni.jpg",
        "description": "Saloni is one of the best people in my life, full of kindness, strength, and warmth.",
        "keywords": ["saloni", "kind", "helping", "girlfriend"]
    },
    "shivani": {
        "name": "Shivani",
        "photo": "photos/shivani.jpg",
        "description": "Shivani, though I met her recently, already feels like a true friend with a pure heart.",
        "keywords": ["shivani", "sister", "sweet"]
    }
}

# ----------------------------
# Streamlit UI
# ----------------------------
st.markdown("<div class='title'>🌸 My Friendship Gift 🌸</div>", unsafe_allow_html=True)
st.write("💌 Type a keyword about my friends and see the magic!")

keyword = st.text_input("👉 Enter a keyword (e.g., helping, caring, sister, best friend):")

if keyword:
    keyword = keyword.lower()
    friend = None

    for f in friends.values():
        if any(kw in keyword for kw in f["keywords"]):
            friend = f
            break

    if friend:
        st.markdown("<div class='friend-card'>", unsafe_allow_html=True)

        st.subheader(friend["name"])

        # Show photo
        try:
            image = Image.open(friend["photo"])
            st.image(image, caption=friend["name"], use_container_width=False, width=250)
        except:
            st.warning("Photo not found yet. Add it in the 'photos' folder!")

        st.write(friend["description"])

        # Generate poem with GPT
        with st.spinner("✍️ Writing something special..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a poetic and emotional writer."},
                        {"role": "user", "content": f"Write a short, emotional poem dedicated to {friend['name']} based on this description: {friend['description']}"}
                    ],
                    max_tokens=150
                )
                # 👇 different OpenAI clients sometimes use slightly different formats
                if hasattr(response.choices[0].message, "content"):
                    poem = response.choices[0].message.content
                else:
                    poem = response.choices[0].text

                st.markdown(f"<div class='poem-box'>{poem}</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ Error generating poem: {e}")

    else:
        st.write("Hmm 🤔 I don't recognize this keyword. Try another one!")
