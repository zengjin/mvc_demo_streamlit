import os

# 定义符合 Streamlit 运行机制的 MVC 结构
project_files = {
    # 1. 模型层：处理 NoSQL 数据
    "app/models/user_model.py": """import os
from tinydb import TinyDB, Query

# 动态获取路径，确保在云端也能找到 db.json
db_path = os.path.join(os.path.dirname(__file__), '../../db.json')
db = TinyDB(db_path)
User = Query()

class UserModel:
    @staticmethod
    def get_all():
        return db.all()

    @staticmethod
    def add_user(username, role):
        if not db.search(User.username == username):
            db.insert({'username': username, 'role': role})
            return True
        return False

    @staticmethod
    def delete_user(username):
        db.remove(User.username == username)
""",

    # 2. 控制器层：业务逻辑与 UI 调度
    "app/controllers/user_controller.py": """import streamlit as st
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
""",

    # 3. 入口文件：状态路由
    "main.py": """import streamlit as st
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
""",

    # 4. 依赖文件
    "requirements.txt": "streamlit\\ntinydb",
    
    # 5. 包初始化文件
    "app/__init__.py": "",
    "app/models/__init__.py": "",
    "app/controllers/__init__.py": ""
}

def build():
    print("🚀 正在创建 Streamlit MVC 项目结构...")
    for path, content in project_files.items():
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            print(f"✅ 已生成: {path}")
    
    print("\\n✨ 构建完成！")
    print("------------------------------------")
    print("本地运行命令:")
    print("1. pip install -r requirements.txt")
    print("2. streamlit run main.py")
    print("------------------------------------")

if __name__ == "__main__":
    build()