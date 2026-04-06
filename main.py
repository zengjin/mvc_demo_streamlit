import streamlit as st
import sys
import os

# 核心：确保 Streamlit 能识别 app 包
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.controllers.user_controller import UserController
from app.utils.i18n import get_text, set_language

# 初始化 Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'language' not in st.session_state:
    st.session_state.language = 'zh'

def main():
    # 语言选择器
    if st.session_state.logged_in:
        with st.sidebar:
            lang_options = {'zh': '中文', 'ja': '日本語', 'en': 'English'}
            selected_lang = st.selectbox(get_text('language'), list(lang_options.keys()), 
                                       format_func=lambda x: lang_options[x], 
                                       index=list(lang_options.keys()).index(st.session_state.language))
            if selected_lang != st.session_state.language:
                set_language(selected_lang)
                st.rerun()

    if not st.session_state.logged_in:
        UserController.render_login()
    else:
        st.sidebar.title(get_text('welcome', st.session_state.user))
        menu = st.sidebar.radio(get_text('menu'), [get_text('home'), get_text('user_management'), get_text('logout')])

        if menu == get_text('home'):
            st.title(get_text('home_title'))
            st.info(get_text('home_description'))
        elif menu == get_text('user_management'):
            UserController.render_user_mgmt()
        elif menu == get_text('logout'):
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
