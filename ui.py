import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,520;9..144,640&family=Source+Sans+3:wght@400;600;700&display=swap');

html, body, [class*="css"]  { font-family: "Source Sans 3", sans-serif; }
.block-container { padding-top: 1.4rem; padding-bottom: 3rem; max-width: 1280px; }

h1, h2, h3, .hero-kicker {
  font-family: "Fraunces", serif;
  letter-spacing: -0.02em;
}

.hero {
  background: linear-gradient(135deg, #10233d 0%, #1b365d 55%, #2a4a73 100%);
  color: #f6efe2;
  padding: 1.6rem 1.8rem 1.5rem;
  border-radius: 18px;
  margin-bottom: 1.3rem;
  border: 1px solid #c9a22755;
  box-shadow: 0 16px 40px rgba(16, 35, 61, 0.18);
}
.hero h1 { color: #fbf6ea !important; font-size: 2.05rem; margin: 0.15rem 0 0.4rem 0; }
.hero p { color: #e7dcc4; font-size: 1.05rem; margin: 0; }
.hero-kicker {
  color: #d4b45a;
  font-size: 0.78rem;
  text-transform: uppercase;
  letter-spacing: 0.16em;
  margin: 0;
}

.card {
  background: #fffdf8;
  border: 1px solid #e4d8c0;
  border-left: 5px solid #c9a227;
  border-radius: 12px;
  padding: 0.95rem 1.1rem;
  height: 100%;
}
.card h3 { margin: 0 0 0.35rem 0; color: #1b365d; font-size: 1.05rem; }
.card p { margin: 0; color: #3d4454; font-size: 0.95rem; }

.reco {
  background: linear-gradient(90deg, #14301c, #1f4d2c);
  color: #f3f7ef;
  padding: 1.15rem 1.3rem;
  border-radius: 14px;
  border: 1px solid #c9a22766;
  margin: 0.6rem 0 1.1rem 0;
}
.reco strong { color: #f0d78c; }

div[data-testid="stMetric"] {
  background: #fffdf8;
  border: 1px solid #e4d8c0;
  border-radius: 12px;
  padding: 0.55rem 0.75rem;
}

[data-testid="stSidebar"] {
  background: #10233d;
}
[data-testid="stSidebar"] * { color: #f4ead6 !important; }
[data-testid="stSidebar"] a { color: #e8c872 !important; }

footer { visibility: hidden; }
</style>
"""


def aplicar():
    st.markdown(CSS, unsafe_allow_html=True)


def hero(kicker: str, titulo: str, texto: str):
    st.markdown(
        f'<div class="hero"><p class="hero-kicker">{kicker}</p>'
        f"<h1>{titulo}</h1><p>{texto}</p></div>",
        unsafe_allow_html=True,
    )


def tarjeta(titulo: str, texto: str):
    st.markdown(f'<div class="card"><h3>{titulo}</h3><p>{texto}</p></div>', unsafe_allow_html=True)


def reco(html_texto: str):
    st.markdown(f'<div class="reco">{html_texto}</div>', unsafe_allow_html=True)
