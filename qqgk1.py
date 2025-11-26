import streamlit as st
import random
import time

# 页面配置
st.set_page_config(
    page_title="全球高考500弹窗",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式
st.markdown("""
<style>
    /* 隐藏所有Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background: #f0f2f6;
        overflow: hidden;
    }
    
    /* 模拟Tkinter窗口样式 - 保持原始尺寸 */
    .tk-window {
        position: fixed;
        border: 2px solid #2f2f2f;
        border-radius: 0px;
        background: white;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        overflow: hidden;
        z-index: 1;
        font-family: "Microsoft YaHei", "微软雅黑", sans-serif;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 0px;
        margin: 0px;
        opacity: 0;
        transform: scale(0.9);
        animation: windowPop 0.5s ease-out forwards;
        cursor: default;
        width: 350px;
        height: 120px;
    }
    
    /* 窗口标题栏 */
    .window-title {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 25px;
        background: #2f2f2f;
        color: white;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* 窗口内容 */
    .window-content {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        padding: 10px;
        box-sizing: border-box;
        word-wrap: break-word;
        overflow: hidden;
        font-size: 10px;
        font-family: "微软雅黑", sans-serif;
    }
    
    /* 初始窗口特殊样式 - 可点击 */
    .initial-window {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
        animation: none;
        opacity: 1;
        transform: scale(1);
        border: 2px solid #2f2f2f;
        background: skyblue;
        box-shadow: 3px 3px 10px rgba(0,0,0,0.3);
        width: 350px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-family: "华文行楷", sans-serif;
        font-size: 18px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .initial-window:hover {
        transform: translate(-50%, -50%) scale(1.05);
        box-shadow: 5px 5px 15px rgba(0,0,0,0.4);
    }
    
    /* 弹窗出现动画 */
    @keyframes windowPop {
        0% {
            opacity: 0;
            transform: scale(0.9);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    /* 初始窗口关闭动画 */
    @keyframes initialClose {
        to {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }
    }
    
    .initial-close {
        animation: initialClose 0.5s ease-out forwards;
    }
    
    /* 控制面板 */
    .control-panel {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 2000;
        background: rgba(255,255,255,0.95);
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        text-align: center;
        min-width: 300px;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'app_state' not in st.session_state:
    st.session_state.app_state = "initial"  # initial, creating, batch, closed
if 'windows' not in st.session_state:
    st.session_state.windows = []
if 'initial_clicked' not in st.session_state:
    st.session_state.initial_clicked = False

# 你指定的8条语录
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

# 原始背景颜色
color_list = [
    "lightpink", "lightblue", "lightgreen",
    "lavender", "peachpuff", "palegoldenrod"
]

# 生成随机窗口位置（考虑大尺寸窗口）
def generate_random_position():
    screen_width = 1600  # 增加屏幕宽度适应大窗口
    screen_height = 1000  # 增加屏幕高度
    window_width = 350   # 保持原始尺寸
    window_height = 120
    
    left = random.randint(0, screen_width - window_width)
    top = random.randint(0, screen_height - window_height)
    
    return left, top

# 创建单个弹窗的HTML
def create_window_html(window_id, left, top, title, content, bg_color, is_initial=False):
    if is_initial:
        return f"""
        <div class="initial-window">
            <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <div style="font-size: 20px; font-weight: bold;">全球高考</div>
                <div style="font-size: 16px;">by 木苏里</div>
                <div style="font-size: 12px; margin-top: 10px; color: #666;">点击我开始500个弹窗</div>
            </div>
        </div>
        """
    else:
        # 为批量弹窗添加随机延迟
        animation_delay = random.uniform(0, 2)  # 随机延迟0-2秒
        return f"""
        <div class="tk-window" style="left: {left}px; top: {top}px; background-color: {bg_color}; animation-delay: {animation_delay}s;">
            <div class="window-title">{title}</div>
            <div class="window-content">
                {content}
            </div>
        </div>
        """

# 主程序逻辑
def main():
    # 初始窗口
    if st.session_state.app_state == "initial":
        # 创建初始窗口
        st.markdown(
            create_window_html("initial", 0, 0, "", "", "", True),
            unsafe_allow_html=True
        )
        
        # 控制面板
        st.markdown(
            """
            <div class="control-panel">
                <h4 style="margin:0; color:#333;">全球高考 · 500弹窗效果</h4>
                <p style="margin:5px 0; color:#666; font-size:14px;">点击中央卡片开始500个弹窗效果</p>
                <p style="margin:0; color:#888; font-size:12px;">使用8条指定语录 · 350×120原始尺寸</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 使用透明按钮覆盖在卡片上（实现点击效果）
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            if st.button("点击卡片开始", key="hidden_click", help="点击初始卡片"):
                st.session_state.app_state = "creating"
                st.session_state.initial_clicked = True
                st.rerun()
    
    # 创建弹窗中
    elif st.session_state.app_state == "creating":
        # 初始窗口关闭效果
        if st.session_state.initial_clicked:
            st.markdown(
                '<div class="initial-window initial-close"></div>',
                unsafe_allow_html=True
            )
            st.session_state.initial_clicked = False
            
            # 生成500个弹窗数据
            st.info("🎯 正在生成500个弹窗，请稍候...")
            
            # 清空之前的窗口数据
            st.session_state.windows = []
            
            # 创建500个弹窗（使用指定的8条语录）
            for i in range(500):
                left, top = generate_random_position()
                color = random.choice(color_list)  # 随机选择颜色
                tip = random.choice(tips_list)     # 从指定8条语录中随机选择
                
                st.session_state.windows.append({
                    'id': i,
                    'left': left,
                    'top': top,
                    'color': color,
                    'tip': tip
                })
            
            # 短暂延迟后切换到批量显示
            time.sleep(0.5)
            st.session_state.app_state = "batch"
            st.rerun()
    
    # 批量弹窗模式
    elif st.session_state.app_state == "batch":
        # 显示所有弹窗
        for window in st.session_state.windows:
            st.markdown(
                create_window_html(
                    window['id'],
                    window['left'],
                    window['top'],
                    "温馨提示",
                    window['tip'],
                    window['color']
                ),
                unsafe_allow_html=True
            )
        
        # 控制面板
        st.markdown(
            f"""
            <div class="control-panel">
                <h4 style="margin:0; color:#333;">🎉 500个弹窗创建完成！</h4>
                <p style="margin:5px 0; color:#666; font-size:14px;">共创建了 {len(st.session_state.windows)} 个弹窗</p>
                <p style="margin:0; color:#888; font-size:12px;">使用8条指定语录 · 语录会重复出现</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 控制按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("关闭所有弹窗", use_container_width=True, type="primary"):
                st.session_state.app_state = "closed"
                st.rerun()
        with col2:
            if st.button("重新开始", use_container_width=True):
                st.session_state.app_state = "initial"
                st.session_state.windows = []
                st.session_state.initial_clicked = False
                st.rerun()
    
    # 关闭状态
    elif st.session_state.app_state == "closed":
        st.balloons()
        st.success("🎊 所有500个弹窗已关闭！")
        
        if st.button("重新开始体验", use_container_width=True, type="primary"):
            st.session_state.app_state = "initial"
            st.session_state.windows = []
            st.session_state.initial_clicked = False
            st.rerun()

if __name__ == "__main__":
    main()
