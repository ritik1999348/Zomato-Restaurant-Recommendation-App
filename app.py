import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Zomato Recommendation System", layout="centered")

# ---- Load data (chhoti files, fast load) ----
@st.cache_resource
def load_data():
    with open("similarity.pkl", "rb") as f:
        sim_data = pickle.load(f)
    restaurants_info = pd.read_pickle("restaurants.pkl")
    return sim_data, restaurants_info

sim_data, restaurants_info = load_data()
names = sim_data["restaurant_names"]

st.title("Zomato Restaurant Recommendation System")
st.write("Apna favorite restaurant chuniye, hum aap ko similar restaurants recommend karenge.")

selected_name = st.selectbox("Restaurant chuniye:", sorted(set(names)))

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

if st.button("Recommend Similar Restaurants"):
    result = recommend_restaurant(selected_name)
    if result is None or len(result) == 0:
        st.warning("Koi similar restaurant nahi mila.")
    else:
        st.subheader(f"Top Restaurants similar to '{selected_name}':")
        st.dataframe(result.reset_index(drop=True))