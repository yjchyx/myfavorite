import streamlit as st
import random
import time

# 页面配置：铺满全屏
st.set_page_config(
    page_title="全球高考·语录互动",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏默认元素
hide_style = """
    <style>
    #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
    body {overflow: hidden; margin: 0; padding: 0;}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# 配置
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
CARD_COUNT = 300  # 铺满全屏的卡片数量
DELAY = 0.1  # 每个卡片的生成间隔（秒）
CARD_SIZE = (280, 140)  # 卡片尺寸

# 初始化状态：记录是否已关闭初始弹窗
if "initial_closed" not in st.session_state:
    st.session_state.initial_closed = False

# 1. 初始卡片（点击任意位置消失）
if not st.session_state.initial_closed:
    st.markdown("""
        <div id="initialCard" style="
            position: fixed;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            background-color: #87CEEB;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            cursor: pointer;
            z-index: 9999;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        " onclick="
            document.getElementById('initialCard').style.display = 'none';
            window.parent.postMessage({type: 'start_generation'}, '*');
        ">
            <h2 style="font-family: '华文行楷', serif; margin: 0 0 15px 0;">全球高考</h2>
            <h4 style="font-family: '华文行楷', serif; margin: 0;">by 木苏里</h4>
        </div>
    """, unsafe_allow_html=True)

# 2. 监听点击信号，启动卡片生成
st.markdown("""
    <script>
    document.addEventListener('message', function(e) {
        if (e.data.type === 'start_generation') {
            window.location.href = '?generate=1';
        }
    });
    </script>
""", unsafe_allow_html=True)

# 3. 生成后续卡片
if st.experimental_get_query_params().get("generate") == ["1"]:
    st.session_state.initial_closed = True

    # 获取屏幕尺寸
    st.markdown("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            window.parent.postMessage({
                type: 'screen_info',
                width: window.innerWidth,
                height: window.innerHeight
            }, '*');
        });
        </script>
    """, unsafe_allow_html=True)

    if "screen_w" not in st.session_state:
        st.session_state.screen_w = 1920
        st.session_state.screen_h = 1080

    # 逐个生成卡片
    card_container = st.container()
    with card_container:
        for _ in range(CARD_COUNT):
            x = random.randint(0, st.session_state.screen_w - CARD_SIZE[0])
            y = random.randint(0, st.session_state.screen_h - CARD_SIZE[1])
            z_index = random.randint(1, CARD_COUNT)

            st.markdown(f"""
                <div style="
                    position: absolute;
                    left: {x}px;
                    top: {y}px;
                    z-index: {z_index};
                    background-color: {random.choice(COLORS)};
                    width: {CARD_SIZE[0]}px;
                    height: {CARD_SIZE[1]}px;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 3px 9px rgba(0,0,0,0.1);
                ">
                    <p style="
                        font-family: '微软雅黑', sans-serif;
                        font-size: 15px;
                        text-align: center;
                        line-height: 1.8;
                        margin: 0;
                        color: #2C3E50;
                    ">
                        {random.choice(QUOTES)}
                    </p>
                </div>
            """, unsafe_allow_html=True)

            time.sleep(DELAY)
            st.rerun(scope="app")

    st.markdown("<div style='height: 100vh;'></div>", unsafe_allow_html=True)
