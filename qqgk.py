import streamlit as st
import random
import time

# 页面核心配置（适配Web端显示）
st.set_page_config(
    page_title="全球高考·语录互动",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏Streamlit默认元素（顶部栏、页脚）
hide_default_style = """
    <style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    </style>
"""
st.markdown(hide_default_style, unsafe_allow_html=True)

# 全局配置（可自定义）
QUOTES = [
    "世界灿烂盛大，欢迎回家",
    "愿我们在硝烟散尽的世界里重逢",
    "这里的一切都有始有终，却能容纳所有的不期而遇和久别重逢",
    "两千三百一十二天，他们相遇在寒风朔雪中，以为是初见，其实是重逢",
    "镜子里的世界一片虚幻，但却可以找到真实",
    "我叫秦究，我来找我的真实",
    "亲爱的，我把自己放在你耳边，你会听到的吧",
    "久违的太阳喷薄而出，给这条强行开出的海路引航，白雾奔涌，天使归乡"
]
COLORS = ["#FFB6C1", "#87CEEB", "#98FB98", "#E6E6FA", "#FFDAB9", "#FAFAD2"]
CARD_COUNT = 200  # 语录卡片数量
DELAY = 0.03  # 生成间隔（秒，Web端更流畅）

# 初始化Session State（管理应用状态）
if "app_state" not in st.session_state:
    st.session_state.app_state = "initial"  # initial:初始页 / generating:生成中 / ended:结束页

# 键盘监听（空格关闭所有卡片）
st.markdown("""
    <script>
    document.addEventListener('keydown', function(e) {
        if (e.code === 'Space') {
            window.parent.postMessage({type: 'space_pressed'}, '*');
        }
    });
    </script>
""", unsafe_allow_html=True)

# 处理空格按键信号
if st.experimental_get_query_params().get("space", [False])[0]:
    st.session_state.app_state = "ended"

# 核心逻辑：不同状态显示不同内容
def render_initial_page():
    """渲染初始提示页"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="
                background-color: #87CEEB;
                padding: 40px;
                border-radius: 12px;
                text-align: center;
                margin-top: 180px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            ">
                <h2 style="font-family: '华文行楷', serif; color: #2C3E50; margin: 0 0 15px 0;">全球高考</h2>
                <h4 style="font-family: '华文行楷', serif; color: #34495E; margin: 0 0 30px 0;">by 木苏里</h4>
                <a href="?start=1" style="
                    padding: 10px 30px;
                    background-color: #2980B9;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    cursor: pointer;
                    text-decoration: none;
                ">生成语录卡片</a>
                <p style="margin-top: 20px; color: #7F8C8D; font-size: 14px;">按空格可关闭所有卡片</p>
            </div>
        """, unsafe_allow_html=True)

def render_generating_page():
    """渲染卡片生成页"""
    card_container = st.container()
    with card_container:
        for _ in range(CARD_COUNT):
            quote = random.choice(QUOTES)
            color = random.choice(COLORS)
            left = random.randint(0, 85)
            top = random.randint(0, 200)
            z_index = random.randint(1, 200)
            
            # 渲染浮动卡片
            st.markdown(f"""
                <div style="
                    position: absolute;
                    left: {left}%;
                    top: {top}px;
                    z-index: {z_index};
                    background-color: {color};
                    padding: 22px;
                    border-radius: 10px;
                    width: 260px;
                    height: 130px;
                    box-shadow: 0 3px 9px rgba(0,0,0,0.08);
                ">
                    <p style="
                        font-family: '微软雅黑', sans-serif;
                        font-size: 15px;
                        text-align: center;
                        line-height: 1.7;
                        color: #2C3E50;
                        margin: 0;
                    ">
                        {quote}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(DELAY)
            st.rerun(scope="app")

def render_ended_page():
    """渲染结束页"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="
                text-align: center;
                margin-top: 220px;
                font-family: '微软雅黑', sans-serif;
            ">
                <h3 style="color: #2C3E50; margin: 0 0 15px 0;">语录展示结束 🌟</h3>
                <p style="color: #7F8C8D; font-size: 16px;">愿你永远记得这份热烈与重逢</p>
                <a href="/" style="
                    margin-top: 20px;
                    padding: 8px 25px;
                    background-color: #3498DB;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 14px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                ">重新体验</a>
            </div>
        """, unsafe_allow_html=True)

# 启动应用
if __name__ == "__main__":
    if st.session_state.app_state == "initial":
        render_initial_page()
        # 检测启动信号
        if st.experimental_get_query_params().get("start", [False])[0]:
            st.session_state.app_state = "generating"
            st.rerun()
    elif st.session_state.app_state == "generating":
        render_generating_page()
    elif st.session_state.app_state == "ended":
        render_ended_page()
