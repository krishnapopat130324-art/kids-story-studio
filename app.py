# app.py - Kids Story Studio (NO FLOWERS - NEUTRAL)

import streamlit as st
import time
import os
from datetime import datetime
from story_generator import StoryGenerator
from config import AGE_GROUPS, STORY_THEMES, VALUES, STORIES_DIR

# Page config
st.set_page_config(
    page_title="✨ Kids Story Studio",
    page_icon="✨",
    layout="wide"
)

# ============================================
# LIGHT BROWN PASTEL CSS
# ============================================

st.markdown("""
    <style>
        /* Main background - Warm beige/brown */
        .stApp {
            background: linear-gradient(135deg, #f5ebe0, #e8d5c4, #f0e0d0, #f5e6d3) !important;
            animation: gradientShift 15s ease infinite !important;
            background-size: 400% 400% !important;
            min-height: 100vh !important;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        /* ALL TEXT - Warm brown */
        * {
            color: #6b4c3b !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #8b6b4a !important;
            font-weight: 600 !important;
        }
        
        /* Main title - Warm brown gradient */
        .main-title {
            text-align: center;
            font-size: 3.8em;
            font-weight: bold;
            background: linear-gradient(135deg, #d4a373, #b8896c, #a67c52) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 5px;
        }
        
        .subtitle {
            text-align: center;
            color: #a88972 !important;
            font-size: 1.2em;
            margin-bottom: 30px;
            font-weight: 300;
            letter-spacing: 2px;
        }
        
        /* Story container - Warm beige glass */
        .story-container {
            background: rgba(255, 248, 240, 0.85) !important;
            backdrop-filter: blur(20px) !important;
            border-radius: 30px !important;
            padding: 30px !important;
            border: 2px solid rgba(200, 170, 140, 0.3) !important;
            box-shadow: 0 20px 60px rgba(180, 150, 120, 0.15) !important;
            max-height: 500px !important;
            overflow-y: auto !important;
            margin: 20px 0 !important;
            font-family: 'Georgia', serif !important;
            line-height: 1.8 !important;
        }
        
        .story-container * {
            color: #5a3f2e !important;
        }
        
        .story-container h1, .story-container h2 {
            color: #b8896c !important;
            text-align: center !important;
        }
        
        .story-container p {
            color: #5a3f2e !important;
            font-size: 1.05em !important;
        }
        
        /* Character preview - Warm beige */
        .character-preview {
            text-align: center !important;
            font-size: 4em !important;
            padding: 30px !important;
            background: rgba(255, 248, 240, 0.6) !important;
            border-radius: 25px !important;
            border: 2px solid rgba(200, 170, 140, 0.25) !important;
        }
        
        .character-preview * {
            color: #7a5f4a !important;
        }
        
        /* Buttons - Warm brown */
        .stButton > button {
            background: linear-gradient(135deg, #d4a373, #b8896c) !important;
            color: white !important;
            border: none !important;
            padding: 15px 40px !important;
            border-radius: 50px !important;
            font-size: 1.2em !important;
            font-weight: bold !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 10px 30px rgba(180, 150, 120, 0.3) !important;
            width: 100% !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 40px rgba(180, 150, 120, 0.4) !important;
            background: linear-gradient(135deg, #ddb08a, #c4997a) !important;
        }
        
        .stButton > button * {
            color: white !important;
        }
        
        /* Input fields - Warm beige */
        .stTextInput > div > div > input {
            background: rgba(255, 248, 240, 0.8) !important;
            border: 2px solid rgba(200, 170, 140, 0.3) !important;
            border-radius: 15px !important;
            padding: 12px 20px !important;
            color: #5a3f2e !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #b8896c !important;
            box-shadow: 0 0 20px rgba(184, 137, 108, 0.15) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #b8a090 !important;
        }
        
        /* Select boxes - Warm beige */
        .stSelectbox > div > div {
            background: rgba(255, 248, 240, 0.8) !important;
            border: 2px solid rgba(200, 170, 140, 0.3) !important;
            border-radius: 15px !important;
        }
        
        .stSelectbox > div > div > div {
            color: #5a3f2e !important;
        }
        
        /* Custom theme buttons - Warm brown */
        .theme-btn {
            background: rgba(255, 248, 240, 0.8) !important;
            border: 2px solid rgba(200, 170, 140, 0.3) !important;
            border-radius: 15px !important;
            padding: 10px 15px !important;
            margin: 5px !important;
            color: #6b4c3b !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            font-size: 1em !important;
            width: 100% !important;
        }
        
        .theme-btn:hover {
            background: linear-gradient(135deg, #d4a373, #b8896c) !important;
            color: white !important;
            transform: scale(1.02) !important;
        }
        
        .theme-btn.active {
            background: linear-gradient(135deg, #d4a373, #b8896c) !important;
            color: white !important;
            border-color: #b8896c !important;
        }
        
        /* Value buttons - Warm brown */
        .value-btn {
            background: rgba(255, 248, 240, 0.8) !important;
            border: 2px solid rgba(200, 170, 140, 0.3) !important;
            border-radius: 15px !important;
            padding: 10px 15px !important;
            margin: 5px !important;
            color: #6b4c3b !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            font-size: 1em !important;
            width: 100% !important;
        }
        
        .value-btn:hover {
            background: linear-gradient(135deg, #d4a373, #b8896c) !important;
            color: white !important;
            transform: scale(1.02) !important;
        }
        
        .value-btn.active {
            background: linear-gradient(135deg, #d4a373, #b8896c) !important;
            color: white !important;
            border-color: #b8896c !important;
        }
        
        /* Selected display - Warm beige */
        .selected-display {
            background: rgba(255, 248, 240, 0.9) !important;
            border: 2px solid rgba(200, 170, 140, 0.3) !important;
            border-radius: 15px !important;
            padding: 12px 20px !important;
            margin: 10px 0 !important;
            color: #5a3f2e !important;
            font-size: 1.1em !important;
        }
        
        /* Slider - Warm brown */
        .stSlider > div {
            background: rgba(255, 248, 240, 0.5) !important;
            border-radius: 15px !important;
            padding: 10px !important;
        }
        
        .stSlider > div > div > div {
            background: linear-gradient(135deg, #d4a373, #b8896c) !important;
        }
        
        /* Sidebar - Warm beige */
        .css-1d391kg, .sidebar-content {
            background: rgba(245, 235, 224, 0.95) !important;
            border-right: 1px solid rgba(200, 170, 140, 0.1) !important;
        }
        
        .css-1d391kg *, .sidebar-content * {
            color: #6b4c3b !important;
        }
        
        /* Alerts - Warm tones */
        .stAlert {
            background: rgba(255, 248, 240, 0.9) !important;
            border: 1px solid rgba(200, 170, 140, 0.2) !important;
            border-radius: 15px !important;
        }
        
        .stAlert * {
            color: #7a5f4a !important;
        }
        
        .stSuccess {
            background: rgba(220, 210, 190, 0.7) !important;
            border: 1px solid rgba(200, 180, 160, 0.3) !important;
        }
        
        .stSuccess * {
            color: #5a4a3a !important;
        }
        
        .stWarning {
            background: rgba(240, 225, 210, 0.7) !important;
            border: 1px solid rgba(220, 200, 180, 0.3) !important;
        }
        
        .stWarning * {
            color: #7a604a !important;
        }
        
        .stInfo {
            background: rgba(235, 225, 215, 0.7) !important;
            border: 1px solid rgba(210, 195, 180, 0.3) !important;
        }
        
        .stInfo * {
            color: #5a4a3a !important;
        }
        
        /* Footer */
        .footer {
            text-align: center !important;
            color: #b8a090 !important;
            font-size: 0.8em !important;
            margin-top: 30px !important;
            padding: 20px !important;
            background: rgba(255, 248, 240, 0.2) !important;
            border-radius: 20px !important;
        }
        
        .footer * {
            color: #b8a090 !important;
        }
        
        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Scrollbar - Warm brown */
        .story-container::-webkit-scrollbar {
            width: 5px;
        }
        .story-container::-webkit-scrollbar-track {
            background: rgba(200, 170, 140, 0.1);
            border-radius: 10px;
        }
        .story-container::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #d4a373, #b8896c);
            border-radius: 10px;
        }
        
        /* Checkbox and radio */
        .stCheckbox > label, .stRadio > label {
            color: #6b4c3b !important;
        }
        
        .stCheckbox > label > div, .stRadio > label > div {
            background: rgba(200, 170, 140, 0.2) !important;
        }
        
        /* Tabs - Warm brown */
        .stTabs > div > div {
            background: rgba(255, 248, 240, 0.2) !important;
            border-radius: 15px !important;
            padding: 5px !important;
        }
        
        .stTabs > div > div > button {
            color: #6b4c3b !important;
            border-radius: 12px !important;
        }
        
        .stTabs > div > div > button[aria-selected="true"] {
            background: linear-gradient(135deg, #d4a373, #b8896c) !important;
            color: white !important;
        }
        
        .stTabs > div > div > button[aria-selected="true"] * {
            color: white !important;
        }
        
        /* Metrics */
        .stMetric > div {
            background: rgba(255, 248, 240, 0.5) !important;
            border-radius: 15px !important;
            padding: 10px !important;
            border: 1px solid rgba(200, 170, 140, 0.1) !important;
        }
        
        .stMetric > div * {
            color: #6b4c3b !important;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(255, 248, 240, 0.3) !important;
            border-radius: 15px !important;
        }
        
        .streamlit-expanderHeader * {
            color: #7a5f4a !important;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================
# INITIALIZE
# ============================================

if 'story_generator' not in st.session_state:
    st.session_state.story_generator = StoryGenerator()
    st.session_state.current_story = ""
    st.session_state.story_generated = False
    st.session_state.selected_theme = STORY_THEMES[0]
    st.session_state.selected_value = VALUES[0]

os.makedirs(STORIES_DIR, exist_ok=True)

# ============================================
# HEADER - NO FLOWERS
# ============================================

st.markdown('<div class="main-title">✨ Kids Story Studio ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">✨ Create magical, personalized stories for the little ones you love ✨</div>', unsafe_allow_html=True)

# ============================================
# MAIN CONTENT
# ============================================

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📝 Story Details")
    
    child_name = st.text_input("👶 Child's Name:", placeholder="Enter the child's name...", max_chars=30)
    
    st.markdown("### 📅 Age")
    age = st.slider(" ", min_value=3, max_value=12, value=7, step=1, label_visibility="collapsed")
    
    # Theme selector
    st.markdown("### 🎭 Story Theme")
    st.markdown(f'<div class="selected-display">✨ Selected: <strong>{st.session_state.selected_theme}</strong></div>', unsafe_allow_html=True)
    
    theme_cols = st.columns(3)
    for idx, theme in enumerate(STORY_THEMES):
        col_idx = idx % 3
        with theme_cols[col_idx]:
            if st.button(f"🎨 {theme}", key=f"theme_{theme}", use_container_width=True):
                st.session_state.selected_theme = theme
                st.rerun()
    
    # Value selector
    st.markdown("### 💎 Value to Teach")
    st.markdown(f'<div class="selected-display">💫 Selected: <strong>{st.session_state.selected_value}</strong></div>', unsafe_allow_html=True)
    
    value_cols = st.columns(3)
    for idx, value in enumerate(VALUES):
        col_idx = idx % 3
        with value_cols[col_idx]:
            if st.button(f"💎 {value}", key=f"value_{value}", use_container_width=True):
                st.session_state.selected_value = value
                st.rerun()
    
    st.markdown("---")
    
    if st.button("✨ Suggest a Character Name", use_container_width=True):
        import random
        from config import CHARACTER_NAMES
        suggested = random.choice(CHARACTER_NAMES)
        st.success(f"💡 Try: **{suggested}**")
    
    st.markdown("---")
    generate_clicked = st.button("🌟 Generate Story 🌟", use_container_width=True)

with col2:
    st.markdown("### 👑 Character Preview")
    
    if child_name:
        if age <= 5:
            emoji = "👶"
        elif age <= 8:
            emoji = "🧒"
        else:
            emoji = "🧑"
        
        st.markdown(f"""
            <div class="character-preview">
                {emoji} {child_name}
                <div style="font-size: 1em; margin-top: 10px; color: #8a7a6a !important;">
                    🌟 Age: {age} | 🎭 {st.session_state.selected_theme} | 💎 {st.session_state.selected_value}
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="character-preview" style="font-size: 1.2em;">
                ✨ Enter a name to begin!
                <div style="font-size: 0.9em; margin-top: 10px; color: #b8a090 !important;">
                    Your personalized story awaits...
                </div>
            </div>
        """, unsafe_allow_html=True)

# ============================================
# GENERATE STORY
# ============================================

if generate_clicked:
    if not child_name:
        st.warning("💫 Please enter the child's name first!")
    else:
        with st.spinner("✨ Weaving a magical story..."):
            story = st.session_state.story_generator.generate_story(
                child_name, 
                age, 
                st.session_state.selected_theme, 
                st.session_state.selected_value
            )
            st.session_state.current_story = story
            st.session_state.story_generated = True
            
            filename = f"{STORIES_DIR}{child_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"🌟 {child_name}'s {st.session_state.selected_value} Adventure\n")
                f.write(f"Created for: {child_name} (Age: {age})\n")
                f.write(f"Theme: {st.session_state.selected_theme} | Value: {st.session_state.selected_value}\n")
                f.write("="*50 + "\n\n")
                f.write(story)

# ============================================
# DISPLAY STORY
# ============================================

if st.session_state.story_generated and st.session_state.current_story:
    st.markdown("---")
    st.markdown("### 📖 Your Magical Story")
    
    st.markdown(f"""
        <div class="story-container">
            {st.session_state.current_story}
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔄 New Story", use_container_width=True):
            st.session_state.story_generated = False
            st.session_state.current_story = ""
            st.rerun()
    
    with col2:
        if st.button("💾 Save Story", use_container_width=True):
            st.success("📖 Story saved to your library!")
    
    with col3:
        if st.button("📥 Download", use_container_width=True):
            if st.session_state.current_story:
                st.download_button(
                    label="📥 Download Now",
                    data=st.session_state.current_story,
                    file_name=f"{child_name}_story.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    with col4:
        if st.button("🎉 Share", use_container_width=True):
            st.balloons()
            st.success("✨ Story shared with love! ✨")

# ============================================
# SIDEBAR - NO FLOWERS
# ============================================

with st.sidebar:
    st.markdown("### 📖 Story Library")
    
    if os.path.exists(STORIES_DIR):
        stories = [f for f in os.listdir(STORIES_DIR) if f.endswith('.txt')]
        if stories:
            st.write(f"✨ **{len(stories)} stories saved**")
            st.markdown("---")
            st.markdown("### 📖 Recent Stories")
            recent = sorted(stories, reverse=True)[:5]
            for story in recent:
                name = story.replace('.txt', '').split('_')[0]
                st.markdown(f"📄 {name}'s story")
        else:
            st.info("📖 No stories saved yet")
    else:
        st.info("📖 Your story collection will appear here")
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
        🌟 **For Best Stories:**
        - Use the child's real name
        - Choose a value they need to learn
        - Pick a theme they love
        - Stories are saved automatically
    """)
    
    st.markdown("---")
    st.markdown("### 🎨 Story Themes")
    for theme in STORY_THEMES[:4]:
        st.write(f"• {theme}")
    st.caption(f"✨ + {len(STORY_THEMES)-4} more themes")
    
    st.markdown("---")
    st.markdown("### 💎 Values")
    for value in VALUES[:4]:
        st.write(f"• 💫 {value}")
    st.caption(f"✨ + {len(VALUES)-4} more values")

# ============================================
# FOOTER - NO FLOWERS
# ============================================

st.markdown("""
    <div class="footer">
        ✨ Made with love for children everywhere | Every story teaches a valuable lesson ✨
    </div>
""", unsafe_allow_html=True)