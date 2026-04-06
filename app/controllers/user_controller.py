import streamlit as st
from app.models.user_model import UserModel

class UserController:
    @staticmethod
    def render_login():
        st.title("🔐 系统登录")
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        if st.button("进入系统"):
            if username == "admin" and password == "admin":
                st.session_state.logged_in = True
                st.session_state.user = username
                st.session_state.role = "Admin"
                st.rerun()
            elif username and password:
                # For other users, check username and password in database
                users = UserModel.get_all()
                user_data = next((u for u in users if u['username'] == username), None)
                if user_data and user_data.get('password') == password:
                    st.session_state.logged_in = True
                    st.session_state.user = username
                    st.session_state.role = user_data.get('role', 'Viewer')
                    st.rerun()
                else:
                    st.error("用户名或密码错误")
            else:
                st.error("请输入用户名和密码")

    @staticmethod
    def render_user_mgmt():
        st.header("👤 用户维护 (CRUD)")
        
        # Add User
        with st.expander("➕ 添加新用户"):
            username = st.text_input("用户名")
            role = st.selectbox("角色", ["Admin", "Editor", "Viewer"], key="add_role")
            name = st.text_input("姓名")
            email = st.text_input("邮箱地址")
            password = st.text_input("密码", type="password")
            if st.button("提交"):
                if username and UserModel.add_user(username, role, name, email, password):
                    st.success(f"用户 {username} 已添加")
                    st.rerun()
                else:
                    st.error("添加失败（可能已存在）")

        # List & Delete & Edit
        st.subheader("当前用户列表")
        users = UserModel.get_all()
        for u in users:
            with st.expander(f"用户: {u['username']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                col1.write(f"**用户名:** {u['username']}")
                col2.write(f"**角色:** {u['role']}")
                col3.write(f"**姓名:** {u.get('name', '')}")
                st.write(f"**邮箱:** {u.get('email', '')}")
                
                # Edit form
                st.subheader("编辑用户信息")
                new_role = st.selectbox("角色", ["Admin", "Editor", "Viewer"], index=["Admin", "Editor", "Viewer"].index(u['role']), key=f"role_{u['username']}")
                new_name = st.text_input("姓名", value=u.get('name', ''), key=f"name_{u['username']}")
                new_email = st.text_input("邮箱地址", value=u.get('email', ''), key=f"email_{u['username']}")
                new_password = st.text_input("密码", type="password", key=f"password_{u['username']}")
                if st.button("更新", key=f"update_{u['username']}"):
                    UserModel.update_user(u['username'], role=new_role, name=new_name, email=new_email, password=new_password)
                    st.success(f"用户 {u['username']} 已更新")
                    st.rerun()
                
                if st.button("删除", key=f"del_{u['username']}"):
                    UserModel.delete_user(u['username'])
                    st.success(f"用户 {u['username']} 已删除")
                    st.rerun()
