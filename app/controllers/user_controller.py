import streamlit as st
from app.models.user_model import UserModel
from app.utils.i18n import get_text

class UserController:
    @staticmethod
    def render_login():
        st.title(get_text('login_title'))
        username = st.text_input(get_text('username'))
        password = st.text_input(get_text('password'), type="password")
        if st.button(get_text('login_button')):
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
                    st.error(get_text('login_error'))
            else:
                st.error(get_text('login_empty'))

    @staticmethod
    def render_user_mgmt():
        st.header(get_text('user_mgmt_title'))
        
        # Add User
        with st.expander(get_text('add_user')):
            username = st.text_input(get_text('username'), key="add_username")
            role = st.selectbox(get_text('role'), ["Admin", "Editor", "Viewer"], key="add_role")
            name = st.text_input(get_text('name'), key="add_name")
            email = st.text_input(get_text('email'), key="add_email")
            password = st.text_input(get_text('password'), type="password", key="add_password")
            if st.button(get_text('submit'), key="add_submit"):
                if username and UserModel.add_user(username, role, name, email, password):
                    st.success(get_text('add_success', username))
                    st.rerun()
                else:
                    st.error(get_text('add_fail'))

        # List & Delete & Edit
        st.subheader(get_text('user_list'))
        users = UserModel.get_all()
        for u in users:
            with st.expander(get_text('user_expander', u['username'])):
                col1, col2, col3 = st.columns([2, 2, 1])
                col1.write(get_text('username_label', u['username']))
                col2.write(get_text('role_label', u['role']))
                col3.write(get_text('name_label', u.get('name', '')))
                st.write(get_text('email_label', u.get('email', '')))
                
                # Edit form
                st.subheader(get_text('edit_title'))
                new_role = st.selectbox(get_text('role'), ["Admin", "Editor", "Viewer"], 
                                      index=["Admin", "Editor", "Viewer"].index(u['role']), 
                                      key=f"role_{u['username']}")
                new_name = st.text_input(get_text('name'), value=u.get('name', ''), key=f"name_{u['username']}")
                new_email = st.text_input(get_text('email'), value=u.get('email', ''), key=f"email_{u['username']}")
                new_password = st.text_input(get_text('password'), type="password", key=f"password_{u['username']}")
                if st.button(get_text('update'), key=f"update_{u['username']}"):
                    UserModel.update_user(u['username'], role=new_role, name=new_name, email=new_email, password=new_password)
                    st.success(get_text('update_success', u['username']))
                    st.rerun()
                
                if st.button(get_text('delete'), key=f"del_{u['username']}"):
                    UserModel.delete_user(u['username'])
                    st.success(get_text('delete_success', u['username']))
                    st.rerun()
