import streamlit as st
from app.models.user_model import UserModel

class UserController:
    @staticmethod
    def render_login():
        st.title("🔐 系统登录")
        user = st.text_input("请输入用户名登录 (任意名称)")
        if st.button("进入系统"):
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.rerun()

    @staticmethod
    def render_user_mgmt():
        st.header("👤 用户维护 (CRUD)")
        
        # Add User
        with st.expander("➕ 添加新用户"):
            name = st.text_input("用户名")
            role = st.selectbox("角色", ["Admin", "Editor", "Viewer"])
            if st.button("提交"):
                if name and UserModel.add_user(name, role):
                    st.success(f"用户 {name} 已添加")
                    st.rerun()
                else:
                    st.error("添加失败（可能已存在）")

        # List & Delete
        st.subheader("当前用户列表")
        users = UserModel.get_all()
        for u in users:
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(f"**{u['username']}**")
            col2.write(f"角色: {u['role']}")
            if col3.button("删除", key=f"del_{u['username']}"):
                UserModel.delete_user(u['username'])
                st.rerun()
