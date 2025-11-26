import streamlit as st
import random
import time

# 页面配置
st.set_page_config(
    page_title="全球高考",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 隐藏所有Streamlit默认元素 */
    #MainMenu, footer, header {visibility: hidden;}
    .stApp {
        background: #f0f2f6;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }
    .main .block-container {
        padding: 0;
        max-width: 100%;
    }
    
    /* 弹窗样式 */
    .tk-window {
        position: fixed;
        border: 2px solid #2f2f2f;
        background: white;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        z-index: 1;
        font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
        display: flex;
        flex-direction: column;
        opacity: 0;
        transform: scale(0.9);
        animation: windowPop 0.15s ease-out forwards;
        width: 350px;
        height: 120px;
    }
    
    .window-title {
        height: 25px;
        background: #2f2f2f;
        color: white;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .window-content {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        padding: 10px;
        font-size: 14px;
        text-align: center;
        line-height: 1.4;
    }
    
    /* 初始卡片 */
    .initial-card {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
        border: 2px solid #2f2f2f;
        background: skyblue;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
        width: 350px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        font-family: "华文行楷", sans-serif;
    }
    
    @keyframes windowPop {
        0% { opacity: 0; transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    .initial-close {
        animation: initialClose 0.2s ease-out forwards;
    }
    
    @keyframes initialClose {
        to { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'app_state' not in st.session_state:
    st.session_state.app_state = "initial"
if 'windows' not in st.session_state:
    st.session_state.windows = []
if 'initial_closed' not in st.session_state:
    st.session_state.initial_closed = False

# 语录和颜色
tips_list = [
    "世界灿烂盛大，欢迎回家",
    "愿我们在硝烟散尽的世界里重逢",
    "这里的一切都有始有终，却能容纳所有的不期而遇和久别重逢",
    "两千三百一十二天，他们相遇在寒风朔雪中，以为是初见，其实是重逢",
    "镜子里的世界一片虚幻，但却可以找到真实",
    "我叫秦究，我来找我的真实",
    "亲爱的，我把自己放在你耳边，你会听到的吧",
    "久违的太阳喷薄而出，给这条强行开出的海路引航，白雾奔涌，天使归乡"
]

color_list = ["lightpink", "lightblue", "lightgreen", "lavender", "peachpuff", "palegoldenrod"]

# 生成确保铺满全屏的位置
def generate_fullscreen_positions():
    positions = []
    window_width = 350
    window_height = 120
    
    # 计算可以容纳的行列数
    screen_width = 1920
    screen_height = 1080
    
    cols = screen_width // window_width  # 约5列
    rows = screen_height // window_height  # 约9行
    
    # 生成网格基础位置
    for row in range(rows + 2):  # +2 确保超出边界
        for col in range(cols + 2):
            base_x = col * window_width - 50  # -50 让部分超出左边界
            base_y = row * window_height - 30  # -30 让部分超出上边界
            
            # 在每个网格内随机微调位置
            for _ in range(2):  # 每个网格生成2个弹窗
                x = base_x + random.randint(-20, 20)
                y = base_y + random.randint(-15, 15)
                positions.append((x, y))
    
    # 如果位置不够450个，补充随机位置
    while len(positions) < 450:
        x = random.randint(-100, screen_width - window_width + 100)
        y = random.randint(-100, screen_height - window_height + 100)
        positions.append((x, y))
    
    # 随机打乱顺序并取前450个
    random.shuffle(positions)
    return positions[:450]

# 创建弹窗HTML
def create_window_html(window_id, left, top, content, bg_color, is_initial=False):
    if is_initial:
        return f"""
        <div class="initial-card">
            <div style="font-size: 24px; font-weight: bold;">全球高考</div>
            <div style="font-size: 18px;">by 木苏里</div>
        </div>
        """
    else:
        animation_delay = window_id * 0.05
        return f"""
        <div class="tk-window" style="left: {left}px; top: {top}px; background-color: {bg_color}; animation-delay: {animation_delay}s;">
            <div class="window-title">温馨提示</div>
            <div class="window-content">{content}</div>
        </div>
        """

# 主程序
def main():
    if st.session_state.app_state == "initial":
        st.markdown(create_window_html("initial", 0, 0, "", "", True), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            if st.button("点击开始", key="start", use_container_width=True):
                st.session_state.app_state = "creating"
                st.session_state.initial_closed = True
                st.rerun()
    
    elif st.session_state.app_state == "creating":
        if st.session_state.initial_closed:
            st.markdown('<div class="initial-card initial-close"></div>', unsafe_allow_html=True)
            st.session_state.initial_closed = False
            
            # 生成确保铺满全屏的位置
            positions = generate_fullscreen_positions()
            st.session_state.windows = []
            
            for i, (left, top) in enumerate(positions):
                color = random.choice(color_list)
                tip = random.choice(tips_list)
                st.session_state.windows.append({
                    'id': i, 'left': left, 'top': top, 'color': color, 'tip': tip
                })
            
            time.sleep(0.2)
            st.session_state.app_state = "batch"
            st.rerun()
    
    elif st.session_state.app_state == "batch":
        for window in st.session_state.windows:
            st.markdown(create_window_html(
                window['id'], window['left'], window['top'],
                window['tip'], window['color']
            ), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("关闭所有弹窗", key="close", use_container_width=True):
                st.session_state.app_state = "closed"
                st.rerun()
    
    elif st.session_state.app_state == "closed":
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("重新开始", key="restart", use_container_width=True):
                st.session_state.app_state = "initial"
                st.session_state.windows = []
                st.session_state.initial_closed = False
                st.rerun()

if __name__ == "__main__":
    main()
