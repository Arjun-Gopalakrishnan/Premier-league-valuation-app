import streamlit as st
import pandas as pd
import pickle

# 1. Page Configuration
st.set_page_config(page_title="PL Elite Valuation", page_icon="🦁", layout="wide")

# 2. Load Assets
@st.cache_resource
def load_assets():
    with open('market_value_model.pkl', 'rb') as file:
        model = pickle.load(file)
    df = pd.read_csv('top_scorers.csv')
    df.columns = df.columns.str.strip()
    return model, df

try:
    model, df = load_assets()
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.stop()

# 3. UI Global Styling
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://th.bing.com/th/id/OIG1.fGz2fKzH_W5S2lU_N9z6?pid=ImgGn");
        background-attachment: fixed;
        background-size: cover;
    }}
    
    .main-container {{
        background: rgba(255, 255, 255, 0.95); 
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #3d0052;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }}

    .title-area {{
        background: rgba(255, 255, 255, 0.9);
        padding: 15px;
        border-radius: 12px;
        border-left: 8px solid #3d0052;
        margin-bottom: 20px;
    }}

    h1, h2, h3, p, label, .stSelectbox label, div[data-baseweb="slider"] label {{
        color: #3d0052 !important; 
        font-weight: 800 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 4. App Header
with st.container():
    st.markdown('<div class="title-area">', unsafe_allow_html=True)
    logo_col, title_col = st.columns([1, 4])
    with logo_col:
        st.image("https://download.logo.wine/logo/Premier_League/Premier_League-Logo.wine.png", width=120)
    with title_col:
        st.title("Premier League Elite Valuation Tool")
        st.markdown("##### Professional Recruitment & Financial Audit System")
    st.markdown('</div>', unsafe_allow_html=True)

# 5. Dashboard Grid
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.header("🔍 Scout Input")
    
    player_list = sorted(df['Player'].unique().tolist())
    selected_player = st.selectbox("Search Database:", ["Manual Entry"] + player_list)
    
    if selected_player != "Manual Entry":
        player_row = df[df['Player'] == selected_player].iloc[0]
        initial_goals = int(player_row.get('Goals', 15))
        initial_age = 25
    else:
        initial_goals = 15
        initial_age = 25

    goals = st.slider("Season Goal Output", 0, 45, initial_goals)
    age = st.slider("Player Age Profile", 16, 40, initial_age)
    
    input_df = pd.DataFrame([[goals, age]], columns=['Goals', 'Age'])
    prediction = model.predict(input_df)[0]
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.header("💰 Valuation Result")
    
    # FINAL COMPACT VALUATION BOX
    st.markdown(f"""
        <div style="
            background-color: #3d0052; 
            padding: 15px; 
            border-radius: 10px; 
            border: 2px solid #00ff87; 
            text-align: center;
            margin-bottom: 20px;">
            <p style="color: #00ff87; font-size: 0.9rem; font-weight: bold; margin: 0; text-transform: uppercase;">
                Statistical Fair Value
            </p>
            <h2 style="color: #ffffff !important; font-size: 3rem !important; margin: 5px 0; font-family: Arial, sans-serif; font-weight: 900; line-height: 1.1;">
                £{prediction:.2f}M
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("💼 Financial Audit")
    asking_price = st.number_input("Proposed Asking Price (£M)", value=float(round(prediction, 2)))
    
    if st.button("Run ROI Analysis"):
        diff = prediction - asking_price
        if diff > 0:
            st.success(f"✅ UNDERVALUED: Asset is worth £{diff:.2f}M more.")
        else:
            st.warning(f"⚠️ OVERPRICED: £{abs(diff):.2f}M above fair value.")
    st.markdown('</div>', unsafe_allow_html=True)
