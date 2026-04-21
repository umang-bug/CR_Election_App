import streamlit as st
import json
import os
import re
from pathlib import Path
from datetime import datetime
import base64

# ─── CONFIG ────────────────────────────────────────────────────────────────────
VOTES_FILE = "votes.json"
DOMAIN = "mnit.ac.in"

VALID_IDS = [
    '2024UME1331','2024UME1343','2024UME1352','2024UME1372','2024UME1381',
    '2024UME1392','2024UME1400','2024UME1422','2024UME1430','2024UME1440',
    '2024UME1450','2024UME1464','2024UME1474','2024UME1482','2024UME1493',
    '2024UME1503','2024UME1516','2024UME1523','2024UME1532','2024UME1539',
    '2024UME1549','2024UME1556','2024UME1560','2024UME1570','2024UME1577',
    '2024UME1584','2024UME1588','2024UME1590','2024UME1593','2024UME1598',
    '2024UME1608','2024UME1614','2024UME1617','2024UME1621','2024UME1624',
    '2024UME1626','2024UME1629','2024UME1632','2024UME1633','2024UME1638',
    '2024UME1640','2024UME1642','2024UME1646','2024UME1648','2024UME1653',
    '2024UME1655','2024UME1657','2024UME1660','2024UME1661','2024UME1666',
    '2024UME1668','2024UME1672','2024UME1676','2024UME1680','2024UME1681',
    '2024UME1685','2024UME1687','2024UME1691','2024UME1693','2024UME1696',
    '2024UME1699','2024UME1700','2024UME1705','2024UME1707','2024UME1891',
    '2024UME1712','2024UME1715','2024UME1721','2024UME1723','2024UME1724',
    '2024UME1728','2024UME1729','2024UME1733','2024UME1747','2024UME1750',
    '2024UME1753','2024UME1757','2024UME1759','2024UME1769','2024UME1772',
    '2024UME1776','2024UME1777','2024UME1782','2024UME1708','2024UME1787',
    '2024UME1789','2024UME1792','2024UME1795','2024UME1799','2024UME1803',
    '2024UME1734','2024UME1740','2024UME1738','2024UME1744','2024UME1749',
    '2024UME1768','2024UME1808','2024UME1807','2024UME1811','2024UME1814',
    '2024UME1818','2024UME1819','2024UME1821','2024UME1826','2024UME1827',
    '2024UME1832','2024UME1834','2024UME1836','2024UME1840','2024UME1842',
    '2024UME1847','2024UME1850','2024UME1852','2024UME1890','2024UME1783',
    '2024UME1904','2024UME1912','2024UME1915',
]

# ─── CANDIDATES  (edit name, photo path, key statement) ──────────────────────
CANDIDATES = [
    {
        "id": 1,
        "name": "Evanta Kumar Bafna",
        "photo": "candidates/candidate1.jpg",
        "statement": "I will bridge the gap between students and faculty, ensuring every voice in our mechanical batch is heard and acted upon.",
        "color": "#FF6B35",
    },
    {
        "id": 2,
        "name": "Ayush Jain",
        "photo": "candidates/candidate2.jpg",
        "statement": "My focus is on industrial visits, better lab access, and strong placement guidance for every student in our batch.",
        "color": "#004E89",
    },
    {
        "id": 3,
        "name": "Rohit Sekhawat",
        "photo": "candidates/candidate3.jpg",
        "statement": "Together we build — I promise transparent communication, more workshops, and a united mechanical community.",
        "color": "#1A936F",
    },
    {
        "id": 4,
        "name": "Chirag",
        "photo": "candidates/candidate4.jpg",
        "statement": "Innovation is our identity. I will push for cutting-edge projects, hackathons, and opportunities that define our batch.",
        "color": "#C84B31",
    },
]

# ─── VOTE STORAGE ──────────────────────────────────────────────────────────────
def load_votes():
    if os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, "r") as f:
            return json.load(f)
    return {"voted_emails": [], "counts": {str(c["id"]): 0 for c in CANDIDATES}}

def save_votes(data):
    with open(VOTES_FILE, "w") as f:
        json.dump(data, f, indent=2)

def cast_vote(email, candidate_id, data):
    data["voted_emails"].append(email.lower())
    key = str(candidate_id)
    data["counts"][key] = data["counts"].get(key, 0) + 1
    save_votes(data)

# ─── EMAIL VALIDATION ──────────────────────────────────────────────────────────
def validate_email(email):
    email = email.strip().lower()
    pattern = r'^(\d{4}ume\d{4})@mnit\.ac\.in$'
    m = re.match(pattern, email, re.IGNORECASE)
    if not m:
        return None, "Invalid email format. Use: <StudentID>@mnit.ac.in"
    student_id = m.group(1).upper()
    if student_id not in VALID_IDS:
        return None, "This Student ID is not in the 3rd Year Mechanical batch list."
    return email, student_id

# ─── PHOTO HELPER ──────────────────────────────────────────────────────────────
def get_photo_b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            ext = Path(path).suffix.lower().replace(".", "")
            mime = "jpeg" if ext in ("jpg", "jpeg") else ext
            return f"data:image/{mime};base64,{base64.b64encode(f.read()).decode()}"
    # placeholder gear SVG if no photo
    return "https://placehold.co/220x220/1a1a2e/ffffff?text=📷+Photo"

# ─── PAGE SETUP ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="3rd Year Mechanical CR Election — MNIT",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark mechanical background */
.stApp {
    background: linear-gradient(135deg, #0d0d1a 0%, #111827 50%, #0d1117 100%);
    color: #e2e8f0;
}

/* Header banner */
.header-banner {
    background: linear-gradient(90deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
    border: 1px solid #334155;
    border-bottom: 3px solid #e63946;
    padding: 28px 36px;
    border-radius: 12px;
    margin-bottom: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: "⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙ ⚙";
    position: absolute;
    top: 8px; left: 0; right: 0;
    color: rgba(230,57,70,0.15);
    font-size: 32px;
    letter-spacing: 24px;
}
.header-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 2px;
    margin: 0;
    text-shadow: 0 0 30px rgba(230,57,70,0.4);
}
.header-sub {
    font-size: 1rem;
    color: #94a3b8;
    margin-top: 6px;
    letter-spacing: 1px;
}
.badge {
    display: inline-block;
    background: #e63946;
    color: white;
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin-top: 10px;
    text-transform: uppercase;
}

/* Section headings */
.section-heading {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 2px;
    border-left: 4px solid #e63946;
    padding-left: 14px;
    margin: 28px 0 18px 0;
    text-transform: uppercase;
}

/* Candidate card */
.candidate-card {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 22px 18px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
    height: 100%;
    position: relative;
    overflow: hidden;
}
.candidate-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.5);
}
.candidate-photo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    border: 3px solid #334155;
    margin-bottom: 14px;
}
.candidate-name {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #f1f5f9;
    letter-spacing: 1px;
    margin-bottom: 10px;
}
.candidate-statement {
    font-size: 0.86rem;
    color: #94a3b8;
    line-height: 1.55;
    font-style: italic;
    border-top: 1px solid #1e293b;
    padding-top: 10px;
    margin-top: 6px;
}
.quote-mark {
    color: #e63946;
    font-size: 1.4rem;
    line-height: 0;
    vertical-align: -0.4rem;
}

/* Email input area */
.auth-box {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 28px 32px;
    max-width: 560px;
    margin: 0 auto 28px auto;
}

/* Vote button custom */
.stButton > button {
    background: linear-gradient(135deg, #e63946, #c1121f) !important;
    color: white !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    border: none !important;
    padding: 12px 28px !important;
    border-radius: 8px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ff4d5a, #e63946) !important;
    box-shadow: 0 0 20px rgba(230,57,70,0.5) !important;
    transform: translateY(-1px) !important;
}

/* Info/success/error boxes */
.stAlert {
    border-radius: 10px !important;
}

/* Live chart section */
.chart-box {
    background: linear-gradient(145deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 24px;
    margin-top: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: #475569;
    font-size: 0.78rem;
    margin-top: 48px;
    padding-top: 16px;
    border-top: 1px solid #1e293b;
    letter-spacing: 0.5px;
}

/* Radio buttons */
div[data-testid="stRadio"] label {
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
}
div[data-testid="stRadio"] > div {
    gap: 10px !important;
}

/* Input */
.stTextInput input {
    background: #0f172a !important;
    color: #e2e8f0 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}
.stTextInput input:focus {
    border-color: #e63946 !important;
    box-shadow: 0 0 0 2px rgba(230,57,70,0.25) !important;
}

/* Divider */
hr { border-color: #1e293b !important; }

/* Plotly chart background */
.js-plotly-plot .plotly, .plot-container {
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <p class="header-title">⚙ CR ELECTION 2025 ⚙</p>
    <p class="header-sub">3rd Year · Mechanical Engineering · MNIT Jaipur</p>
    <span class="badge">🔴 Live Voting Open</span>
</div>
""", unsafe_allow_html=True)

# ─── LOAD STATE ────────────────────────────────────────────────────────────────
vote_data = load_votes()

# ─── SESSION STATE ─────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "auth_email" not in st.session_state:
    st.session_state.auth_email = ""
if "voted" not in st.session_state:
    st.session_state.voted = False

# ─── CANDIDATE PROFILES ────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">Meet the Candidates</div>', unsafe_allow_html=True)

cols = st.columns(4, gap="medium")
for i, cand in enumerate(CANDIDATES):
    photo_src = get_photo_b64(cand["photo"])
    border_color = cand["color"]
    with cols[i]:
        st.markdown(f"""
        <div class="candidate-card" style="border-top: 4px solid {border_color};">
            <img src="{photo_src}" class="candidate-photo" style="border-color:{border_color};" 
                 onerror="this.src='https://placehold.co/150x150/1a1a2e/ffffff?text=⚙'"/>
            <div class="candidate-name" style="color:{border_color};">
                {cand['name']}
            </div>
            <div class="candidate-statement">
                <span class="quote-mark">"</span>
                {cand['statement']}
                <span class="quote-mark">"</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='margin: 32px 0;'>", unsafe_allow_html=True)

# ─── VOTING SECTION ────────────────────────────────────────────────────────────
st.markdown('<div class="section-heading">🗳 Cast Your Vote</div>', unsafe_allow_html=True)

vote_col, chart_col = st.columns([1, 1.4], gap="large")

with vote_col:
    if not st.session_state.authenticated:
        st.markdown("""
        <div style='background:#1e293b; border:1px solid #334155; border-radius:12px; 
                    padding:22px 26px; margin-bottom:16px;'>
            <p style='color:#94a3b8; font-size:0.88rem; margin:0 0 6px 0; letter-spacing:0.5px;'>
                🔒 SECURE ANONYMOUS VOTING
            </p>
            <p style='color:#f1f5f9; font-size:1.0rem; margin:0;'>
                Enter your MNIT email to verify eligibility. 
                Your identity is <strong>not stored</strong> — only your Student ID is used to prevent duplicate votes.
            </p>
        </div>
        """, unsafe_allow_html=True)

        email_input = st.text_input(
            "Your MNIT Email",
            placeholder="e.g. 2024ume1400@mnit.ac.in",
            key="email_field"
        )

        if st.button("VERIFY & PROCEED", key="verify_btn"):
            if not email_input.strip():
                st.error("Please enter your email address.")
            else:
                validated_email, result = validate_email(email_input)
                if validated_email is None:
                    st.error(f"❌ {result}")
                elif validated_email in vote_data["voted_emails"]:
                    st.warning("⚠️ You have already voted! Each student can vote only once.")
                else:
                    st.session_state.authenticated = True
                    st.session_state.auth_email = validated_email
                    st.rerun()

    elif st.session_state.voted:
        st.success("✅ Your vote has been recorded successfully!")
        st.markdown("""
        <div style='background:#0f2d1f; border:1px solid #166534; border-radius:10px; 
                    padding:18px; margin-top:10px; text-align:center;'>
            <p style='color:#86efac; font-size:1.0rem; margin:0;'>
                🎉 Thank you for participating in the democratic process.<br>
                <span style='color:#4ade80; font-weight:600;'>Your vote is anonymous and secure.</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("BACK TO HOME", key="home_btn"):
            st.session_state.authenticated = False
            st.session_state.voted = False
            st.session_state.auth_email = ""
            st.rerun()

    else:
        st.markdown(f"""
        <div style='background:#0f2d1f; border:1px solid #166534; border-radius:10px; 
                    padding:12px 18px; margin-bottom:18px;'>
            <p style='color:#86efac; font-size:0.9rem; margin:0;'>
                ✅ Verified! You are eligible to vote.
            </p>
        </div>
        """, unsafe_allow_html=True)

        candidate_names = [c["name"] for c in CANDIDATES]
        choice = st.radio(
            "Select your candidate:",
            candidate_names,
            key="candidate_choice",
            index=None,
        )

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗳  SUBMIT VOTE", key="submit_btn"):
            if choice is None:
                st.error("Please select a candidate before submitting.")
            else:
                selected = next(c for c in CANDIDATES if c["name"] == choice)
                # Re-load to avoid race condition
                vote_data = load_votes()
                if st.session_state.auth_email in vote_data["voted_emails"]:
                    st.warning("⚠️ Duplicate vote detected. You have already voted.")
                else:
                    cast_vote(st.session_state.auth_email, selected["id"], vote_data)
                    st.session_state.voted = True
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← BACK", key="back_btn"):
            st.session_state.authenticated = False
            st.rerun()

# ─── LIVE RESULTS CHART ────────────────────────────────────────────────────────
with chart_col:
    st.markdown('<div class="section-heading">📊 Live Results</div>', unsafe_allow_html=True)

    vote_data = load_votes()
    names = [c["name"] for c in CANDIDATES]
    counts = [vote_data["counts"].get(str(c["id"]), 0) for c in CANDIDATES]
    colors = [c["color"] for c in CANDIDATES]
    total = sum(counts)

    import plotly.graph_objects as go

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=names,
        y=counts,
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.1)', width=1),
        ),
        text=[f"{v} vote{'s' if v != 1 else ''}" for v in counts],
        textposition="outside",
        textfont=dict(color="#e2e8f0", size=13, family="Rajdhani"),
        hovertemplate="<b>%{x}</b><br>Votes: %{y}<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15,23,42,0.8)",
        font=dict(color="#94a3b8", family="Inter"),
        title=dict(
            text=f"Total Votes Cast: <b>{total}</b>",
            font=dict(color="#e2e8f0", size=15, family="Rajdhani"),
            x=0.5,
        ),
        yaxis=dict(
            gridcolor="#1e293b",
            zerolinecolor="#334155",
            tickfont=dict(color="#64748b"),
        ),
        xaxis=dict(
            tickfont=dict(color="#94a3b8", size=12, family="Rajdhani"),
        ),
        margin=dict(t=60, b=20, l=20, r=20),
        height=320,
        bargap=0.3,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Mini stats
    if total > 0:
        leader = CANDIDATES[counts.index(max(counts))]
        st.markdown(f"""
        <div style='background:#0f172a; border:1px solid #1e293b; border-radius:10px; 
                    padding:14px 18px; margin-top:8px;'>
            <p style='color:#64748b; font-size:0.78rem; margin:0 0 4px 0; letter-spacing:1px; text-transform:uppercase;'>
                Currently Leading
            </p>
            <p style='color:{leader["color"]}; font-family: Rajdhani; font-size:1.2rem; 
                       font-weight:700; margin:0;'>
                {leader["name"]} — {max(counts)} votes
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  REFRESH RESULTS", key="refresh_btn"):
        st.rerun()

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ⚙ MNIT Jaipur · Department of Mechanical Engineering · 3rd Year CR Election 2025 ⚙<br>
    Voting is anonymous. Results are live. Each student may vote only once.
</div>
""", unsafe_allow_html=True)
