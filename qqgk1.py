import streamlit as st
import random
import time

# 页面配置
st.set_page_config(
    page_title="全球高考重叠弹窗",
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式 - 实现重叠交错效果
st.markdown("""
<style>
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 卡片基础样式 */
    .overlap-card {
        position: fixed;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        min-height: 110px;
        min-width: 220px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
        border: 2px solid rgba(255,255,255,0.6);
        opacity: 0;
        transform: scale(0.3) rotate(-15deg);
        animation: overlapPop 1s ease-out forwards;
        z-index: 1;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    /* 重叠弹出动画 */
    @keyframes overlapPop {
        0% {
            opacity: 0;
            transform: scale(0.3) rotate(-15deg);
        }
        60% {
            opacity: 0.9;
            transform: scale(1.05) rotate(5deg);
        }
        100% {
            opacity: 1;
            transform: scale(1) rotate(0deg);
        }
    }
    
    /* 初始卡片样式 */
    .initial-card {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
        opacity: 1;
        animation: gentlePulse 2s infinite;
        cursor: pointer;
        padding: 30px;
        border-radius: 15px;
        background-color: skyblue;
        color: #333;
        font-size: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        border: 3px solid rgba(255,255,255,0.7);
        font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
    }
    
    @keyframes gentlePulse {
        0% { transform: translate(-50%, -50%) scale(1); }
        50% { transform: translate(-50%, -50%) scale(1.08); }
        100% { transform: translate(-50%, -50%) scale(1); }
    }
    
    /* 初始卡片消失动画 */
    .fade-out {
        animation: fadeOutOverlap 0.6s ease forwards;
    }
    
    @keyframes fadeOutOverlap {
        to {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.3);
        }
    }
    
    /* 卡片悬停效果 */
    .overlap-card:hover {
        transform: scale(1.1) !important;
        z-index: 100 !important;
        box-shadow: 0 12px 30px rgba(0,0,0,0.5);
    }
    
    /* 控制面板 */
    .control-panel {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 2000;
        background: rgba(255,255,255,0.9);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'app_state' not in st.session_state:
    st.session_state.app_state = "initial"  # initial, overlapping, complete
if 'cards_popped' not in st.session_state:
    st.session_state.cards_popped = 0
if 'card_data' not in st.session_state:
    st.session_state.card_data = []
if 'initial_removed' not in st.session_state:
    st.session_state.initial_removed = False

# 全球高考语录
quotes = [
    "世界灿烂盛大，欢迎回家",
    "愿我们在硝烟散尽的世界里重逢",
    "这里的一切都有始有终，却能容纳所有的不期而遇和久别重逢",
    "两千三百一十二天，他们相遇在寒风朔雪中，以为是初见，其实是重逢",
    "镜子里的世界一片虚幻，但却可以找到真实",
    "我叫秦究，我来找我的真实",
    "亲爱的，我把自己放在你耳边，你会听到的吧",
    "久违的太阳喷薄而出，给这条强行开出的海路引航，白雾奔涌，天使归乡",
    "我不是来救你的，我是来爱你的",
    "所以说爱恨真是奇怪的东西，有的早早腐烂入土，有的刻骨",
    "公理之下，正义不朽",
    "别对我闭上眼睛，不要，简松意，别对我闭上眼睛",
    "你眸中有山川河流，胜过我行经路过的一切不朽",
    "上天从未眷顾人类，我们将独自走完征程",
    "星河璀璨，阳光干净，在人间所有美好的存在里，不论是活着或者死去，我总是最爱你"
]

# 背景颜色 - 更多颜色选择
colors = [
    "#FFB6C1", "#98FB98", "#87CEEB", "#DDA0DD", "#FFD700",
    "#FFA07A", "#20B2AA", "#DEB887", "#F0E68C", "#B0E0E6",
    "#FF69B4", "#00FA9A", "#1E90FF", "#BA55D3", "#FFA500",
    "#DC143C", "#00FF7F", "#4682B4", "#D8BFD8", "#F0FFF0"
]

# 生成重叠的随机位置
def generate_overlap_position():
    # 创建一个重叠密集的区域
    screen_width = 1200
    screen_height = 700
    card_width = 220
    card_height = 110
    
    # 70%的卡片集中在中心区域，30%散落在边缘
    if random.random() < 0.7:
        # 中心密集区域
        left = random.randint(200, screen_width - card_width - 200)
        top = random.randint(150, screen_height - card_height - 150)
    else:
        # 边缘区域
        left = random.randint(50, screen_width - card_width - 50)
        top = random.randint(50, screen_height - card_height - 50)
    
    # 随机旋转角度，增加重叠感
    rotation = random.randint(-8, 8)
    
    return left, top, rotation

# 预生成所有卡片数据
def generate_all_card_data():
    card_data = []
    for i in range(len(quotes)):
        left, top, rotation = generate_overlap_position()
        color = colors[i % len(colors)]
        # 随机z-index，创建层次感
        z_index = random.randint(1, 50)
        
        card_data.append({
            'left': left,
            'top': top,
            'rotation': rotation,
            'color': color,
            'z_index': z_index,
            'quote': quotes[i]
        })
    
    return card_data

# 主标题
st.markdown("<h1 style='text-align: center; color: #1f77b4; margin-bottom: 20px;'>📚 全球高考 · 重叠弹窗效果</h1>", unsafe_allow_html=True)

# 初始卡片
if st.session_state.app_state == "initial":
    st.markdown(
        """
        <div class='initial-card'>
            全球高考<br>by 木苏里<br><br>
            <span style='font-size: 16px;'>点击我开始重叠弹窗</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 使用按钮模拟卡片点击
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("点击开始重叠效果", key="start_overlap", use_container_width=True):
            st.session_state.app_state = "overlapping"
            st.session_state.initial_removed = True
            st.session_state.card_data = generate_all_card_data()
            st.rerun()

# 卡片重叠弹出效果
elif st.session_state.app_state == "overlapping":
    # 初始卡片消失
    if st.session_state.initial_removed:
        st.markdown(
            """
            <div class='initial-card fade-out'>
                全球高考<br>by 木苏里
            </div>
            """,
            unsafe_allow_html=True
        )
        st.session_state.initial_removed = False
        # 短暂延迟后开始显示其他卡片
        time.sleep(0.5)
    
    # 逐步显示卡片
    if st.session_state.cards_popped < len(st.session_state.card_data):
        # 每次显示一个卡片
        st.session_state.cards_popped += 1
        st.rerun()
    
    # 显示已弹出的卡片
    for i in range(st.session_state.cards_popped):
        if i < len(st.session_state.card_data):
            card = st.session_state.card_data[i]
            
            st.markdown(
                f"""
                <div class='overlap-card' style='
                    background-color: {card['color']}; 
                    color: #333; 
                    font-size: 14px; 
                    left: {card['left']}px; 
                    top: {card['top']}px;
                    z-index: {card['z_index']};
                    animation-delay: {i * 0.15}s;
                    transform: rotate({card['rotation']}deg);
                '>
                    {card['quote']}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # 当所有卡片都显示后，切换到完成状态
    if st.session_state.cards_popped >= len(st.session_state.card_data):
        time.sleep(1)  # 等待最后一个卡片动画完成
        st.session_state.app_state = "complete"
        st.rerun()

# 完成状态
elif st.session_state.app_state == "complete":
    st.balloons()
    
    # 显示所有卡片
    for i, card in enumerate(st.session_state.card_data):
        st.markdown(
            f"""
            <div class='overlap-card' style='
                background-color: {card['color']}; 
                color: #333; 
                font-size: 14px; 
                left: {card['left']}px; 
                top: {card['top']}px;
                z-index: {card['z_index']};
                opacity: 1;
                animation: none;
                transform: rotate({card['rotation']}deg);
            '>
                {card['quote']}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # 控制面板
    st.markdown(
        """
        <div class='control-panel'>
            <h4 style='margin:0; color:#333;'>重叠弹窗效果完成！</h4>
            <p style='margin:5px 0; color:#666; font-size:14px;'>鼠标悬停在卡片上查看效果</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 重新开始按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("重新开始重叠效果", use_container_width=True):
            st.session_state.app_state = "initial"
            st.session_state.cards_popped = 0
            st.session_state.card_data = []
            st.session_state.initial_removed = False
            st.rerun()

# 页脚
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; margin-top: 30px;'>"
    "基于《全球高考》by 木苏里 | 重叠交错弹窗效果"
    "</div>",
    unsafe_allow_html=True
)

# 添加一些说明
if st.session_state.app_state == "overlapping":
    st.info("✨ 卡片正在以重叠交错的方式弹出中...")
