import streamlit as st
import random
import time

# 页面基础配置
st.set_page_config(
    page_title="全球高考·语录互动",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏Streamlit默认元素（顶部栏、页脚等）
hide_default_ui = """
    <style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}
    .stApp {overflow: hidden !important;}
    </style>
"""
st.markdown(hide_default_ui, unsafe_allow_html=True)

# 语录与样式配置（可直接使用）
QUOTES_LIST = [
    "世界灿烂盛大，欢迎回家",
    "愿我们在硝烟散尽的世界里重逢",
    "这里的一切都有始有终，却能容纳所有的不期而遇和久别重逢",
    "两千三百一十二天，他们相遇在寒风朔雪中，以为是初见，其实是重逢",
    "镜子里的世界一片虚幻，但却可以找到真实"
]
COLOR_LIST = ["#FFB6C1", "#87CEEB", "#98FB98", "#E6E6FA", "#FFDAB9"]
CARD_TOTAL = 80  # 卡片数量（减少数量加快加载）
DELAY_TIME = 0.12  # 生成间隔（秒）
CARD_WIDTH = 260
CARD_HEIGHT = 130

# 通过URL参数控制流程（核心逻辑）
query_params = st.experimental_get_query_params()

if "start" not in query_params:
    # 初始卡片：点击后跳转（纯HTML实现，无Streamlit交互依赖）
    st.markdown("""
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #87CEEB;
            padding: 45px 60px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            z-index: 9999;
        " onclick="window.location.href = window.location.href + '?start=1'">
            <h2 style="
                font-family: 'STKaiti', '华文楷体', serif;
                color: #2C3E50;
                margin: 0 0 10px 0;
                font-size: 32px;
            ">全球高考</h2>
            <h4 style="
                font-family: 'STKaiti', '华文楷体', serif;
                color: #34495E;
                margin: 0;
                font-size: 18px;
            ">by 木苏里</h4>
        </div>
    """, unsafe_allow_html=True)

else:
    # 生成卡片逻辑（URL含start参数时执行）
    # 获取屏幕尺寸（适配不同设备）
    st.markdown("""
        <script>
        const screenWidth = window.innerWidth;
        const screenHeight = window.innerHeight;
        window.parent.postMessage({
            type: 'screen_size',
            width: screenWidth,
            height: screenHeight
        }, '*');
        </script>
    """, unsafe_allow_html=True)

    # 初始化屏幕尺寸（防止首次加载异常）
    if "screen_w" not in st.session_state:
        st.session_state.screen_w = 1920
        st.session_state.screen_h = 1080

    # 逐个生成卡片
    card_container = st.container()
    with card_container:
        for _ in range(CARD_TOTAL):
            # 随机位置（确保卡片在屏幕内）
            pos_x = random.randint(0, st.session_state.screen_w - CARD_WIDTH)
            pos_y = random.randint(0, st.session_state.screen_h - CARD_HEIGHT)
            # 随机样式
            bg_color = random.choice(COLOR_LIST)
            quote_text = random.choice(QUOTES_LIST)
            
            # 渲染卡片
            st.markdown(f"""
                <div style="
                    position: absolute;
                    left: {pos_x}px;
                    top: {pos_y}px;
                    width: {CARD_WIDTH}px;
                    height: {CARD_HEIGHT}px;
                    background-color: {bg_color};
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <p style="
                        font-family: 'Microsoft YaHei', '微软雅黑', sans-serif;
                        font-size: 15px;
                        color: #2C3E50;
                        text-align: center;
                        line-height: 1.6;
                        margin: 0;
                    ">{quote_text}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # 延迟生成（逐个出现效果）
            time.sleep(DELAY_TIME)
            st.rerun(scope="app")

    # 保持页面高度（防止卡片被截断）
    st.markdown(f"""
        <div style="height: {st.session_state.screen_h}px;"></div>
    """, unsafe_allow_html=True)
