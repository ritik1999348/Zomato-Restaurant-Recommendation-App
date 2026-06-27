import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Zomato Restaurant Recommender",
    page_icon="🍽️",
    layout="wide",
)

# ---------------- Styling ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600..800&family=Manrope:wght@400;500;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Manrope', sans-serif;
}

/* Layered background: deep base + warm radial glows (mango/chili + cola-bubble feel) + faint food emoji texture */
.stApp {
    color: #f4ecdf;
    background-color: #1c1410;
    background-image:
        radial-gradient(circle at 12% 18%, rgba(232,116,59,0.16) 0%, transparent 38%),
        radial-gradient(circle at 88% 12%, rgba(216,68,53,0.14) 0%, transparent 42%),
        radial-gradient(circle at 75% 85%, rgba(58,120,140,0.12) 0%, transparent 40%),
        radial-gradient(circle at 8% 80%, rgba(184,140,40,0.10) 0%, transparent 35%),
        repeating-linear-gradient(135deg, rgba(255,255,255,0.012) 0px, rgba(255,255,255,0.012) 2px, transparent 2px, transparent 26px);
    background-attachment: fixed;
}

/* faint emoji texture band behind hero, purely decorative */
.food-strip {
    font-size: 1.4rem;
    letter-spacing: 1.1rem;
    opacity: 0.18;
    white-space: nowrap;
    overflow: hidden;
    margin-bottom: -0.6rem;
    user-select: none;
}

.hero {
    position: relative;
    padding: 2.2rem 2rem 1.8rem 2rem;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(42,29,20,0.92) 0%, rgba(28,20,16,0.92) 100%);
    border: 1px solid #3a2c1f;
    margin-bottom: 1.8rem;
    overflow: hidden;
}

.hero::after {
    content: "🍹";
    position: absolute;
    right: 1.6rem;
    top: 1.2rem;
    font-size: 3.2rem;
    opacity: 0.22;
    transform: rotate(8deg);
}

.hero h1 {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    font-size: 2.4rem;
    color: #f4ecdf;
    margin-bottom: 0.3rem;
}

.hero p {
    color: #c9b8a3;
    font-size: 1.05rem;
    margin: 0;
    max-width: 32rem;
}

.eyebrow {
    color: #e8743b;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-size: 0.78rem;
    margin-bottom: 0.4rem;
}

div[data-baseweb="select"] {
    border-radius: 10px;
}

.stButton > button {
    background: #e8743b;
    color: #1c1410;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.6rem;
    font-size: 1rem;
    transition: transform 0.15s ease, background 0.15s ease;
}

.stButton > button:hover {
    background: #f08a55;
    transform: translateY(-1px);
}

.result-header {
    font-family: 'Fraunces', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f4ecdf;
    margin: 1.6rem 0 1rem 0;
    border-bottom: 1px solid #3a2c1f;
    padding-bottom: 0.6rem;
}

.r-card {
    position: relative;
    background: linear-gradient(135deg, rgba(37,28,21,0.95) 0%, rgba(30,22,17,0.95) 100%);
    border: 1px solid #3a2c1f;
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.15s ease, transform 0.15s ease;
    overflow: hidden;
}

.r-card:hover {
    border-color: #e8743b;
    transform: translateY(-2px);
}

.r-card::before {
    content: "🍽";
    position: absolute;
    right: 0.7rem;
    bottom: 0.4rem;
    font-size: 2.1rem;
    opacity: 0.10;
}

.r-name {
    font-family: 'Fraunces', serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #f4ecdf;
    margin-bottom: 0.25rem;
}

.r-cuisine {
    color: #c9b8a3;
    font-size: 0.88rem;
    margin-bottom: 0.55rem;
}

.r-badge {
    display: inline-block;
    background: #2f2419;
    color: #e8a06b;
    border-radius: 6px;
    padding: 0.18rem 0.6rem;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.5rem;
}

.r-rating {
    background: #2f4a32;
    color: #b7e0b7;
}
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

# ---------------- Decorative strip ----------------
st.markdown(
    '<div class="food-strip">🍕 🍔 🍹 🍜 🥗 🍰 🍣 🥘 🍕 🍔 🍹 🍜 🥗 🍰 🍣 🥘 🍕 🍔 🍹 🍜 🥗 🍰 🍣 🥘</div>',
    unsafe_allow_html=True,
)

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
