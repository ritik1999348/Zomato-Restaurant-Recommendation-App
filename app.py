import streamlit as st
import pandas as pd
import pickle
import base64

st.set_page_config(
    page_title="Zomato Restaurant Recommender",
    page_icon="🍽️",
    layout="wide",
)

# ---------------- Background SVG (wooden table + drink glasses, illustrative) ----------------
BG_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">
  <defs>
    <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#5a3a24"/>
      <stop offset="100%" stop-color="#3a2415"/>
    </linearGradient>
    <linearGradient id="glassRed" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#e8543f"/>
      <stop offset="100%" stop-color="#a8281c"/>
    </linearGradient>
    <linearGradient id="glassGreen" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#8fd16b"/>
      <stop offset="100%" stop-color="#4a9436"/>
    </linearGradient>
  </defs>

  <rect width="1600" height="900" fill="url(#wood)"/>
  <g opacity="0.18" stroke="#1c1410" stroke-width="2">
    <line x1="0" y1="120" x2="1600" y2="100"/>
    <line x1="0" y1="260" x2="1600" y2="245"/>
    <line x1="0" y1="400" x2="1600" y2="390"/>
    <line x1="0" y1="540" x2="1600" y2="535"/>
    <line x1="0" y1="680" x2="1600" y2="678"/>
    <line x1="0" y1="800" x2="1600" y2="800"/>
  </g>

  <g opacity="0.85" transform="translate(180,430)">
    <rect x="-55" y="0" width="110" height="190" rx="8" fill="url(#glassRed)" opacity="0.55"/>
    <rect x="-55" y="0" width="110" height="40" rx="8" fill="#ffffff" opacity="0.10"/>
    <line x1="-10" y1="-90" x2="-30" y2="10" stroke="#1c1410" stroke-width="6" stroke-linecap="round" opacity="0.5"/>
    <line x1="15" y1="-90" x2="-5" y2="10" stroke="#1c1410" stroke-width="6" stroke-linecap="round" opacity="0.5"/>
    <circle cx="-25" cy="40" r="8" fill="#ffffff" opacity="0.25"/>
    <circle cx="10" cy="80" r="6" fill="#ffffff" opacity="0.25"/>
    <circle cx="-15" cy="120" r="7" fill="#ffffff" opacity="0.25"/>
  </g>

  <g opacity="0.8" transform="translate(1340,460)">
    <rect x="-55" y="0" width="110" height="170" rx="8" fill="url(#glassGreen)" opacity="0.5"/>
    <rect x="-55" y="0" width="110" height="36" rx="8" fill="#ffffff" opacity="0.10"/>
    <line x1="0" y1="-85" x2="-15" y2="5" stroke="#1c1410" stroke-width="6" stroke-linecap="round" opacity="0.5"/>
    <circle cx="-20" cy="35" r="7" fill="#ffffff" opacity="0.25"/>
    <circle cx="15" cy="70" r="6" fill="#ffffff" opacity="0.25"/>
    <circle cx="-10" cy="110" r="6" fill="#ffffff" opacity="0.25"/>
  </g>

  <g opacity="0.55" transform="translate(800,180)">
    <ellipse cx="0" cy="0" rx="150" ry="40" fill="#1c1410" opacity="0.3"/>
    <ellipse cx="0" cy="-10" rx="140" ry="32" fill="#1c1410"/>
    <path d="M -120 -10 Q -90 -70 -40 -50 Q 0 -85 40 -50 Q 90 -70 120 -10 Z" fill="#e8a430" opacity="0.6"/>
    <circle cx="-60" cy="-30" r="10" fill="#d8443a" opacity="0.7"/>
    <circle cx="20" cy="-40" r="9" fill="#d8443a" opacity="0.7"/>
    <circle cx="70" cy="-25" r="8" fill="#3a7a3a" opacity="0.7"/>
  </g>
</svg>
"""
bg_b64 = base64.b64encode(BG_SVG.encode("utf-8")).decode("utf-8")

# ---------------- Styling ----------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600..800&family=Manrope:wght@400;500;700&display=swap');

html, body, [class*="css"]  {{
    font-family: 'Manrope', sans-serif;
}}

.stApp {{
    color: #f4ecdf;
    background-image:
        linear-gradient(rgba(20,14,10,0.82), rgba(20,14,10,0.88)),
        url("data:image/svg+xml;base64,{bg_b64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.hero {{
    position: relative;
    padding: 2.2rem 2rem 1.8rem 2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(42,29,20,0.92) 0%, rgba(28,20,16,0.92) 100%);
    border: 1px solid rgba(244,236,223,0.12);
    margin-bottom: 1.8rem;
    overflow: hidden;
}}

.hero h1 {{
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 2.4rem;
    color: #f4ecdf;
    margin-bottom: 0.3rem;
}}

.hero p {{
    color: #d8c9b5;
    font-size: 1.05rem;
    margin: 0;
    max-width: 32rem;
}}

.eyebrow {{
    color: #f0935c;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: 0.78rem;
    margin-bottom: 0.4rem;
}}

div[data-baseweb="select"] {{
    border-radius: 10px;
}}

.stButton > button {{
    background: #e8743b;
    color: #1c1410;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.6rem;
    font-size: 1rem;
    transition: transform 0.15s ease, background 0.15s ease;
}}

.stButton > button:hover {{
    background: #f08a55;
    transform: translateY(-1px);
}}

.result-header {{
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f4ecdf;
    margin: 1.6rem 0 1rem 0;
    border-bottom: 1px solid rgba(244,236,223,0.15);
    padding-bottom: 0.6rem;
}}

.r-card {{
    position: relative;
    background: linear-gradient(135deg, rgba(37,28,21,0.93) 0%, rgba(30,22,17,0.93) 100%);
    border: 1px solid rgba(244,236,223,0.12);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.15s ease, transform 0.15s ease;
    overflow: hidden;
}}

.r-card:hover {{
    border-color: #e8743b;
    transform: translateY(-2px);
}}

.r-name {{
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f4ecdf;
    margin-bottom: 0.25rem;
}}

.r-cuisine {{
    color: #d8c9b5;
    font-size: 0.88rem;
    margin-bottom: 0.55rem;
}}

.r-badge {{
    display: inline-block;
    background: rgba(244,236,223,0.08);
    color: #f0a06b;
    border-radius: 6px;
    padding: 0.18rem 0.6rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.5rem;
}}

.r-rating {{
    background: rgba(120,200,120,0.15);
    color: #b7e0b7;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- Load data ----------------
@st.cache_resource
def load_data():
    with open("similarity.pkl", "rb") as f:
        sim_data = pickle.load(f)
    restaurants_info = pd.read_pickle("restaurants.pkl")
    return sim_data, restaurants_info

sim_data, restaurants_info = load_data()
names = sim_data["restaurant_names"]

# ---------------- Hero ----------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">Bengaluru · Content-Based Recommender</div>
    <h1>Find your next favourite restaurant</h1>
    <p>Pick a place you already love — we'll match it to others with a similar cuisine and review profile.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    selected_name = st.selectbox("Choose a restaurant you like", sorted(set(names)))
with col2:
    st.write("")
    st.write("")
    go = st.button("Recommend →", use_container_width=True)


def recommend_restaurant(name):
    if name not in names:
        return None
    idx = names.index(name)
    rec_indices = sim_data["indices"][idx]
    rec_scores = sim_data["scores"][idx]

    result = restaurants_info.iloc[rec_indices][["name", "cuisines", "Mean Rating", "cost"]].copy()
    result["similarity_score"] = rec_scores
    result = result.drop_duplicates(subset=["name"])
    result = result.sort_values(by="Mean Rating", ascending=False)
    return result.head(10)


if go:
    result = recommend_restaurant(selected_name)
    if result is None or len(result) == 0:
        st.warning("Koi similar restaurant nahi mila.")
    else:
        st.markdown(f"<div class='result-header'>Because you liked {selected_name}</div>", unsafe_allow_html=True)

        cols = st.columns(2)
        for i, (_, row) in enumerate(result.iterrows()):
            with cols[i % 2]:
                cost_text = f"₹{int(row['cost'])} for two" if pd.notna(row['cost']) else "Cost N/A"
                st.markdown(f"""
                <div class="r-card">
                    <div class="r-name">{row['name']}</div>
                    <div class="r-cuisine">{row['cuisines']}</div>
                    <span class="r-badge r-rating">★ {row['Mean Rating']:.1f}</span>
                    <span class="r-badge">{cost_text}</span>
                </div>
                """, unsafe_allow_html=True)
