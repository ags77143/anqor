import streamlit as st
import os
from supabase import create_client, Client


def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_ANON_KEY", "")

    # Fall back to Streamlit secrets
    if not url:
        try:
            url = st.secrets["SUPABASE_URL"]
        except Exception:
            pass
    if not key:
        try:
            key = st.secrets["SUPABASE_ANON_KEY"]
        except Exception:
            pass

    if not url or not key:
        st.error("⚠️ Supabase credentials not found. Check your .env or Streamlit secrets.")
        st.stop()
    return create_client(url, key)


def get_current_user(supabase: Client):
    """Return current user from session state, or None."""
    if "access_token" in st.session_state:
        try:
            session = supabase.auth.set_session(
                st.session_state["access_token"],
                st.session_state["refresh_token"]
            )
            return session.user
        except Exception:
            # Token expired or invalid — clear it
            for k in ["access_token", "refresh_token"]:
                st.session_state.pop(k, None)
    return None


def show_auth_page(supabase: Client):
    st.markdown("""
    <style>
    .auth-wrap {
        max-width: 420px;
        margin: 6vh auto 0 auto;
    }
    </style>
    <div class="auth-wrap">
    """, unsafe_allow_html=True)

    st.markdown('<div class="sf-logo" style="text-align:center;">Anqorr</div>', unsafe_allow_html=True)
    st.markdown('<div class="sf-tagline" style="text-align:center;margin-bottom:2rem;">Your lectures. Your notes. Always saved.</div>', unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

    with tab_login:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Sign In", key="signin_btn"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state["access_token"] = res.session.access_token
                st.session_state["refresh_token"] = res.session.refresh_token
                st.rerun()
            except Exception as e:
                st.markdown(f'<div class="sf-warn">⚠️ {str(e)}</div>', unsafe_allow_html=True)

    with tab_signup:
        email2 = st.text_input("Email", key="signup_email")
        password2 = st.text_input("Password (min 6 chars)", type="password", key="signup_pass")
        if st.button("Create Account", key="signup_btn"):
            try:
                res = supabase.auth.sign_up({"email": email2, "password": password2})
                if res.user:
                    st.markdown('<div class="sf-info">✓ Account created! Check your email to confirm, then sign in.</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="sf-warn">Something went wrong. Try again.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="sf-warn">⚠️ {str(e)}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
