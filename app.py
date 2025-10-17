import os
import streamlit as st
import pandas as pd
st.set_page_config(page_title='EdgeLine — Bet Smarter. Win Sharper.', layout='wide')
st.title('EdgeLine — CFB +EV Finder (Cloud Starter)')
if 'age_ok' not in st.session_state:
    st.session_state['age_ok'] = False
if not st.session_state['age_ok']:
    st.warning('You must confirm you are of legal age (21+, or 18+ where allowed). Wager responsibly.')
    c1, c2 = st.columns([1,1])
    if c1.button('I am of legal age'): st.session_state['age_ok'] = True
    if c2.button('Exit'): st.stop()
    st.stop()
with st.sidebar:
    st.header('Connection')
    API_BASE = st.text_input('API_BASE', os.getenv('API_BASE', ''))
    API_KEY  = st.text_input('API_KEY', os.getenv('API_KEY', ''))
status = st.empty()
if API_BASE:
    try:
        import requests
        r = requests.get(API_BASE.rstrip('/') + '/health', timeout=4, headers={'X-API-Key': API_KEY} if API_KEY else {})
        status.success('API connected: ' + API_BASE) if (r.ok and r.json().get('ok') is True) else status.warning('API reachable but not healthy: ' + API_BASE)
    except Exception as e:
        status.error('API not reachable: ' + API_BASE + ' — ' + str(e))
else:
    status.info('API_BASE not set — running in standalone demo mode.')
tab1, tab2 = st.tabs(['+EV (demo)', 'Upload board'])
with tab1:
    demo = pd.DataFrame({'date':['2025-10-18']*3,'home':['ALABAMA','GEORGIA','MICHIGAN'],'away':['TENNESSEE','KENTUCKY','PENN STATE'],'market':['FT Spread','FT Total','1H Spread'],'pick':['HOME','OVER','AWAY'],'line':[-6.5,51.5,3.0],'odds':[-110,-105,102],'kelly':[0.012,0.009,0.006]})
    st.dataframe(demo, use_container_width=True)
with tab2:
    st.write('Upload a BetOnline CSV/TSV to preview the board (no modeling in this starter).')
    f = st.file_uploader('betonline_lines.csv', type=['csv','tsv','txt'])
    if f is not None:
        import pandas as _pd
        try:
            df = _pd.read_csv(f, sep=None, engine='python')
        except Exception:
            f.seek(0); df = _pd.read_csv(f)
        st.success('File loaded'); st.dataframe(df.head(200), use_container_width=True)
