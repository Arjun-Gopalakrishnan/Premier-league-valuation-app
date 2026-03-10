import streamlit as st
import pandas as pd
import pickle

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="PL Elite Valuation", page_icon="🦁", layout="wide")

# ---------------- LOAD MODEL + DATA ----------------

@st.cache_resource
def load_assets():
with open('market_value_model.pkl', 'rb') as file:
model = pickle.load(file)

```
df = pd.read_csv('top_scorers.csv')
df.columns = df.columns.str.strip()

return model, df
```

try:
model, df = load_assets()
except Exception as e:
st.error(f"Error loading files: {e}")
st.stop()

# ---------------- GLOBAL STYLE ----------------

st.markdown(
"""

<style>

.stApp{
    background-image: url("https://th.bing.com/th/id/OIG1.fGz2fKzH_W5S2lU_N9z6?pid=ImgGn");
    background-size: cover;
    background-attachment: fixed;
}

/* Main card containers */
.main-container{
    background: rgba(255,255,255,0.95);
    padding:25px;
    border-radius:12px;
    border:2px solid #3d0052;
    box-shadow:0 5px 20px rgba(0,0,0,0.15);
}

/* Title section */
.title-area{
    background:rgba(255,255,255,0.92);
    padding:20px;
    border-radius:12px;
    border-left:8px solid #3d0052;
    margin-bottom:20px;
}

/* Subtitle fix */
.subtitle{
    color:#444;
    font-size:18px;
    font-weight:600;
}

/* Valuation box */
.value-box{
    background:#3d0052;
    padding:20px;
    border-radius:12px;
    border:2px solid #00ff87;
    text-align:center;
    margin-bottom:15px;
}

/* small label */
.value-label{
    color:#00ff87;
    font-size:14px;
    font-weight:700;
    letter-spacing:1px;
}

/* big price */
.value-number{
    color:white;
    font-size:48px;
    font-weight:900;
}

/* button */
.stButton>button{
    background:#3d0052;
    color:white;
    border-radius:8px;
    padding:10px 20px;
    font-weight:bold;
}

</style>

""",
unsafe_allow_html=True
)

# ---------------- HEADER ----------------

with st.container():

```
st.markdown('<div class="title-area">', unsafe_allow_html=True)

logo_col, title_col = st.columns([1,4])

with logo_col:
    st.image(
        "https://download.logo.wine/logo/Premier_League/Premier_League-Logo.wine.png",
        width=120
    )

with title_col:
    st.title("Premier League Elite Valuation Tool")
    st.markdown('<p class="subtitle">Professional Recruitment & Financial Audit System</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
```

# ---------------- LAYOUT ----------------

col1, col2 = st.columns(2)

# ---------------- INPUT PANEL ----------------

with col1:

```
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.header("🔍 Scout Input")

player_list = sorted(df['Player'].unique().tolist())

selected_player = st.selectbox(
    "Search Database",
    ["Manual Entry"] + player_list
)

if selected_player != "Manual Entry":
    player_row = df[df['Player'] == selected_player].iloc[0]
    initial_goals = int(player_row.get('Goals', 15))
    initial_age = 25
else:
    initial_goals = 15
    initial_age = 25

goals = st.slider("Season Goal Output",0,45,initial_goals)
age = st.slider("Player Age Profile",16,40,initial_age)

input_df = pd.DataFrame([[goals,age]],columns=['Goals','Age'])
prediction = model.predict(input_df)[0]

st.markdown('</div>', unsafe_allow_html=True)
```

# ---------------- RESULT PANEL ----------------

with col2:

```
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.header("💰 Valuation Result")

st.markdown(f"""
<div class="value-box">
    <div class="value-label">STATISTICAL FAIR VALUE</div>
    <div class="value-number">£{prediction:.2f}M</div>
</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("💼 Financial Audit")

asking_price = st.number_input(
    "Proposed Asking Price (£M)",
    value=float(round(prediction,2))
)

if st.button("Run ROI Analysis"):

    diff = prediction - asking_price

    if diff > 0:
        st.success(f"UNDERVALUED: Asset worth £{diff:.2f}M more")

    else:
        st.warning(f"OVERPRICED: £{abs(diff):.2f}M above fair value")

st.markdown('</div>', unsafe_allow_html=True)
```
