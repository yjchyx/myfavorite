import streamlit as st
import random
import time

# 页面配置
st.set_page_config(
    page_title="全球高考200弹窗",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式 - 优化性能
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
    
    /* 模拟Tkinter窗口样式 - 简化版本提高性能 */
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
    }
    
    /* 窗口标题栏 */
    .window-title {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 20px;
        background: #2f2f2f;
        color: white;
        font-size: 11px;
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
        padding: 8px;
        box-sizing: border-box;
        word-wrap: break-word;
        overflow: hidden;
    }
    
    /* 初始窗口特殊样式 */
    .initial-window {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
        animation: none;
        opacity: 1;
        transform: scale(1);
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
    
    /* 窗口关闭动画 */
    @keyframes windowClose {
        to {
            opacity: 0;
            transform: scale(0.8);
        }
    }
    
    .close-animation {
        animation: windowClose 0.3s ease-out forwards;
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
    
    /* 进度指示器 */
    .progress-info {
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'app_state' not in st.session_state:
    st.session_state.app_state = "initial"  # initial, creating, batch, closed
if 'windows' not in st.session_state:
    st.session_state.windows = []
if 'initial_closed' not in st.session_state:
    st.session_state.initial_closed = False
if 'windows_created' not in st.session_state:
    st.session_state.windows_created = 0
if 'creation_started' not in st.session_state:
    st.session_state.creation_started = False

# 扩展全球高考语录 - 200条不同的语录
base_tips_list = [
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
    "星河璀璨，阳光干净，在人间所有美好的存在里，不论是活着或者死去，我总是最爱你",
    "这里风遇山止，船到岸停",
    "他身后悬挂着漫天星河，眼睛里隐有笑意",
    "未经允许，擅自特别喜欢你，不好意思了",
    "所有苦难与背负的尽头，都是行云流水般的此世光阴",
    "往前走，往前看，哪怕前途一片迷惘，哪怕只是凭着惯性继续往前走",
    "阳光依然干净，星河依然灿烂，世界也依然在长久深情中缓缓地朝前走",
    "深渊之下，红尘万丈",
    "只要他还要我，我必定死生不负",
    "我很好，除了很想你",
    "想买束花给你，可路口的花店没开，我又实在想念",
    "少年心动是仲夏夜的荒原，割不完烧不尽",
    "长风一吹，野草就连了天",
    "我喜欢你，所以希望你被簇拥包围，所以你走的路要繁花盛开，要人声鼎沸",
    "台下的掌声热烈而经久，就像一场盛大的祝福",
    "因为太喜欢你，所以我如临深渊、如履薄冰",
    "被人拉起来，跟自己站起来是两码事",
    "无人知晓他们在一起，但人人都曾见过他们在一起的样子",
    "江添不再是哥哥，也不再是男朋友，兜来转去，又成了盛望不知该怎么称呼的人",
    "我的骨骼说，我还是爱你",
    "那一年，他喜欢的那个人在台上弹完一首歌，转身下台的时候，背上印着他的名字",
    "台下的掌声热烈而经久，就像一场盛大的祝福",
    "那个夏天的蝉鸣比哪一年都聒噪，教室窗外枝桠疯长，却总也挡不住烈阳",
]

# 生成200条语录（重复基础语录但添加变化）
def generate_200_tips():
    tips = []
    for i in range(200):
        base_tip = random.choice(base_tips_list)
        # 为重复的语录添加序号或轻微变化，使其看起来不同
        if base_tip in tips:
            variation = random.choice(["", "✨", "🌟", "💫", "❤️", "📚"])
            tips.append(f"{base_tip} {variation}")
        else:
            tips.append(base_tip)
    return tips

# 扩展背景颜色
base_color_list = [
    "lightpink", "lightblue", "lightgreen", "lavender", 
    "peachpuff", "palegoldenrod", "lightcyan", "lightyellow",
    "thistle", "mistyrose", "powderblue", "navajowhite",
    "lemonchiffon", "azure", "aliceblue", "honeydew"
]

# 生成200种颜色（重复基础颜色但添加轻微变化）
def generate_200_colors():
    colors = []
    for i in range(200):
        base_color = random.choice(base_color_list)
        # 为重复的颜色添加轻微变化
        if base_color in colors:
            # 添加轻微的颜色变化
            colors.append(base_color)
        else:
            colors.append(base_color)
    return colors

# 生成随机窗口位置
def generate_random_position():
    screen_width = 1200
    screen_height = 700
    window_width = 300  # 稍微缩小窗口以适应更多弹窗
    window_height = 100
    
    left = random.randint(0, screen_width - window_width)
    top = random.randint(0, screen_height - window_height)
    
    return left, top

# 创建单个弹窗的HTML
def create_window_html(window_id, left, top, title, content, bg_color, is_initial=False):
    if is_initial:
        return f"""
        <div class="initial-window" style="width: 350px; height: 120px; background-color: {bg_color};">
            <div class="window-title">{title}</div>
            <div class="window-content" style="font-size: 16px; font-family: '华文行楷';">
                {content}
            </div>
        </div>
        """
    else:
        # 为批量弹窗添加延迟动画，避免同时出现造成卡顿
        animation_delay = random.uniform(0, 2)  # 随机延迟0-2秒
        return f"""
        <div class="tk-window" style="left: {left}px; top: {top}px; width: 300px; height: 100px; background-color: {bg_color}; animation-delay: {animation_delay}s;">
            <div class="window-title">{title}</div>
            <div class="window-content" style="font-size: 10px; font-family: '微软雅黑';">
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
            create_window_html(
                "initial", 
                0, 0,  # 位置由CSS控制
                "专属提示", 
                "全球高考<br>by 木苏里<br><br><span style='font-size: 12px;'>点击开始200个弹窗</span>", 
                "skyblue", 
                True
            ),
            unsafe_allow_html=True
        )
        
        # 控制面板
        st.markdown(
            """
            <div class="control-panel">
                <h4 style="margin:0; color:#333;">全球高考 · 200弹窗效果</h4>
                <p style="margin:5px 0; color:#666; font-size:14px;">点击开始体验200个弹窗效果</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 开始按钮
        if st.button("开始200个弹窗", key="start_200", use_container_width=True):
            st.session_state.app_state = "creating"
            st.session_state.creation_started = True
            st.rerun()
    
    # 创建弹窗中
    elif st.session_state.app_state == "creating":
        # 初始窗口关闭效果
        if st.session_state.creation_started:
            st.markdown(
                '<div class="initial-window close-animation"></div>',
                unsafe_allow_html=True
            )
            st.session_state.creation_started = False
            
            # 生成200个弹窗数据
            tips_list = generate_200_tips()
            color_list = generate_200_colors()
            
            for i in range(200):
                left, top = generate_random_position()
                color = color_list[i]
                tip = tips_list[i]
                
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
                <h4 style="margin:0; color:#333;">200个弹窗已创建完成！</h4>
                <p class="progress-info">共创建了 {len(st.session_state.windows)} 个弹窗</p>
                <p style="margin:5px 0; color:#666; font-size:14px;">弹窗正在随机时间出现...</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 控制按钮
        col1, col2 = st.columns(2)
        with col1:
            if st.button("关闭所有弹窗", use_container_width=True):
                st.session_state.app_state = "closed"
                st.rerun()
        with col2:
            if st.button("重新开始", use_container_width=True):
                st.session_state.app_state = "initial"
                st.session_state.windows = []
                st.session_state.windows_created = 0
                st.session_state.initial_closed = False
                st.rerun()
    
    # 关闭状态
    elif st.session_state.app_state == "closed":
        st.success("所有200个弹窗已关闭！")
        
        if st.button("重新开始", use_container_width=True):
            st.session_state.app_state = "initial"
            st.session_state.windows = []
            st.session_state.windows_created = 0
            st.session_state.initial_closed = False
            st.rerun()

if __name__ == "__main__":
    main()
