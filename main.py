import streamlit as st
import sys
import os

# 核心：确保 Streamlit 能识别 app 包
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.controllers.user_controller import UserController

# 初始化 Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def main():
    if not st.session_state.logged_in:
        UserController.render_login()
    else:
        st.sidebar.title(f"你好, {st.session_state.user}")
        menu = st.sidebar.radio("菜单", ["首页", "用户管理", "注销"])

        if menu == "首页":
            st.title("🏠 MVC 应用主页")
            st.info("这个应用展示了如何在 Streamlit 中使用模块化目录结构。")
        elif menu == "用户管理":
            UserController.render_user_mgmt()
        elif menu == "注销":
            st.session_state.logged_in = False
            st.rerun()

if __name__ == "__main__":
    main()
