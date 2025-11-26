import streamlit as st
import random
import time

# 页面配置
st.set_page_config(page_title="全球高考·语录互动", layout="wide", initial_sidebar_state="collapsed")

# 隐藏默认元素
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden !important;}
    body {overflow: hidden; margin: 0; padding: 0;}
    </style>
""", unsafe_allow_html=True)

# 初始化状态
if "initial_closed" not in st.session_state:
    st.session_state.initial_closed = False
if "screen_w" not in st.session_state:
    st.session_state.screen_w = 1920
if "screen_h" not in st.session_state:
    st.session_state.screen_h = 1080

# 配置
QUOTES = [
    "世界灿烂盛大，欢迎回家",
    "愿我们在硝烟散尽的世界里重逢",
    "这里的一切都有始有终，却能容纳所有的不期而遇和久别重逢"
]
COLORS = ["#FFB6C1", "#87CEEB", "#98FB98"]
CARD_COUNT = 300
DELAY = 0.1
CARD_SIZE = (280, 140)

# 1. 初始弹窗（点击任意位置关闭）
if not st.session_state.initial_closed:
    st.markdown(f"""
        <div id="initialCard" style="
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            background: #87CEEB; padding: 40px; border-radius: 12px;
            text-align: center; cursor: pointer; z-index: 9999;
        " onclick="
            document.getElementById('initialCard').style.display = 'none';
            window.parent.postMessage('initial_closed', '*');
        ">
            <h2 style="font-family: '华文行楷'; margin: 0 0 15px 0;">全球高考</h2>
            <h4 style="font-family: '华文行楷'; margin: 0;">by 木苏里</h4>
        </div>
    """, unsafe_allow_html=True)

    # 监听弹窗关闭信号
    st.markdown("""
        <script>
        window.addEventListener('message', function(e) {
            if (e.data === 'initial_closed') {
                window.location.href = '?start=1';
            }
        });
        </script>
    """, unsafe_allow_html=True)

# 2. 生成卡片
elif st.experimental_get_query_params().get("start") == ["1"]:
    # 获取屏幕尺寸
    st.markdown("""
        <script>
        window.parent.postMessage({
            type: 'screen_size',
            w: window.innerWidth,
            h: window.innerHeight
        }, '*');
        </script>
    """, unsafe_allow_html=True)

    # 逐个生成卡片
    card_container = st.container()
    with card_container:
        for _ in range(CARD_COUNT):
            x = random.randint(0, st.session_state.screen_w - CARD_SIZE[0])
            y = random.randint(0, st.session_state.screen_h - CARD_SIZE[1])
            st.markdown(f"""
                <div style="
                    position: absolute; left: {x}px; top: {y}px;
                    background: {random.choice(COLORS)}; width: {CARD_SIZE[0]}px; height: {CARD_SIZE[1]}px;
                    padding: 20px; border-radius: 10px; box-shadow: 0 3px 9px rgba(0,0,0,0.1);
                ">
                    <p style="font-family: '微软雅黑'; font-size: 15px; text-align: center; margin: 0;">
                        {random.choice(QUOTES)}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            time.sleep(DELAY)
            st.rerun(scope="app")
