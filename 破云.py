import streamlit as st
import random
import time

# 页面配置 - 隐藏所有元素
st.set_page_config(
    page_title="破云",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义CSS样式 - 隐藏所有不必要元素
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
    /* 隐藏所有Streamlit组件容器 */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    /* 隐藏其他可能出现的元素 */
    .stAlert {
        display: none;
    }
    .stSuccess {
        display: none;
    }
    .stInfo {
        display: none;
    }
    
    /* 弹窗样式 */
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
        animation: windowPop 0.15s ease-out forwards; /* 大幅加快动画 */
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
    
    /* 窗口内容 - 增大字体 */
    .window-content {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        padding: 15px;
        box-sizing: border-box;
        word-wrap: break-word;
        overflow: hidden;
        font-size: 14px;
        font-family: "微软雅黑", sans-serif;
        line-height: 1.4;
    }
    
    /* 初始卡片样式 */
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
        text-align: center;
        font-family: "华文行楷", sans-serif;
        cursor: pointer;
    }
    
    /* 弹窗出现动画 - 极速 */
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
    
    /* 初始卡片关闭动画 */
    @keyframes initialClose {
        to {
            opacity: 0;
            transform: translate(-50%, -50%) scale(0.5);
        }
    }
    
    .initial-close {
        animation: initialClose 0.2s ease-out forwards; /* 加快关闭动画 */
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

# 语录列表
tips_list = [
“你想怎么样都行，我这么喜欢你，当然希望你开心”
“我从未拥有过来自父母手足的亲情，不曾体验过男女之间的爱情，甚至没交过什么朋友，连友情都相当匮乏。如果说曾有人最接近我心里那个位置的话，那个人是你。”
“请你不要辜负我的期待，请你如我坚信的那样，睁开双眼，活着回来。”
“最讽刺的是，在如此四面楚歌的绝境中，当他看到这张照片时，内心竟然还能感觉到丝丝缕缕不受控制的爱意。”
“就算曾经做错过什么也无所谓，如果你想付出代价，至少不会独自一人面对未来。”
“——谢谢你还在，至少到最后一天，还有你站在我身边。”
“是看一眼少一眼。就算咱俩一块活到九十九，不也是过一天少一天吗？没毛病。” 
“我活到九十九，你九十七就够了。”
“我从未如此爱过任何人，一如我爱你。”
“停云霭霭，时雨濛濛，八表同昏，平陆成江”
“纵使千疮百孔，年华老去，我还有你寻遍千山万水，踏破生死之际——再次相聚之前，谢谢你带我回到这人世间。”
“抱最好的希望，做最坏的打算，尽最大的努力”
“我想跟你一起从战场上手拉手凯旋，再不济肩并肩马革裹尸，你不明白吗江停？”
“我从未拥有过来自父母手足的亲情，不曾体验过男女之间的爱情，甚至没交过什么朋友，连友情都相当匮乏。如果说曾有人最接近我心里那个位置的话，那个人是你。”
“我爱你，严峫。”他说，“我想让你也成为那个不可超越的胜利者。”
“回忆，情感，心理印记，这些细节都随着离别被反复升华，死亡是最好的滤镜。”
“不论前方是否樯倾楫摧，踏出一步便将粉身碎骨；所有罪恶与仇恨，都将在你我的手中了结。我来接你了，江停”
你只能做你自己，永远都无法取代任何人，哪怕那个人死了都一样。
“死人不可超越，死人永远是胜利者，就是这么个道理。”
“处对象吗，江队？
“……开慢点，你对象来接你回家”
“哪怕有一天我死了，我都会在天上看着你，我会一直看着你好好的活下去。”
“是我，江停。”严峫把他冰凉的脸紧紧埋在自己颈窝里，声音战栗不成句：“我来接你了，我总算来接你了……再看我一眼，啊？江停？”
“——严峫，”苍穹云海全数倒映在江停眼底，而他只定定望着爱人近在咫尺的身影，说：“我爱你”
“我希望江停永远爱我”
“纵使千疮百孔，年华老去，我还有你寻遍千山万水，踏破生死之际——再次相聚之前，谢谢你带我回到这人世间”
“我把你带在身边，不是因为相信你，是希望能相信我自己”
“我从未拥有过来自父母手足的亲情，不曾体验过男女之间的爱情，甚至没交过什么朋友，连友情都相当匮乏。如果说曾有人最接近我心里那个位置的话，那个人是你”
“你想怎么样都行，我这么喜欢你，当然希望你开心”
“喝了我的媳妇茶就要给我当小媳妇，要给我做饭按摩洗袜子”
“你我本无缘，全靠我砸钱”
]

# 背景颜色
color_list = [
    "lightpink", "lightblue", "lightgreen",
    "lavender", "peachpuff", "palegoldenrod"
]

# 生成随机窗口位置 - 往左和往上移动
def generate_random_position():
    screen_width = 1600
    screen_height = 1000
    window_width = 350
    window_height = 120
    # 往左移动：从-100开始，消除左边留白
    left = random.randint(-100, screen_width - window_width - 50)
    # 往上移动：从-80开始，消除上边留白
    top = random.randint(-80, screen_height - window_height - 50)
    return left, top

# 创建弹窗HTML
def create_window_html(window_id, left, top, title, content, bg_color, is_initial=False):
    if is_initial:
        return f"""
        <div class="initial-card">
            <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <div style="font-size: 24px; font-weight: bold;">破云</div>
                <div style="font-size: 18px;">by 淮上</div>
            </div>
        </div>
        """
    else:
        # 极速：每个弹窗间隔0.05秒
        animation_delay = window_id * 0.05
        return f"""
        <div class="tk-window" style="left: {left}px; top: {top}px; background-color: {bg_color}; animation-delay: {animation_delay}s;">
            <div class="window-title">{title}</div>
            <div class="window-content">
                {content}
            </div>
        </div>
        """

# 主程序
def main():
    # 初始状态 - 只显示卡片和按钮
    if st.session_state.app_state == "initial":
        # 创建初始卡片
        st.markdown(
            create_window_html("initial", 0, 0, "", "", "", True),
            unsafe_allow_html=True
        )
        
        # 开始按钮 - 使用空白列居中
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            # 添加一些空白空间让按钮在卡片下方
            st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
            if st.button("点击开始", key="start", use_container_width=True):
                st.session_state.app_state = "creating"
                st.session_state.initial_closed = True
                st.rerun()
    
    # 创建弹窗
    elif st.session_state.app_state == "creating":
        # 初始卡片关闭
        if st.session_state.initial_closed:
            st.markdown(
                '<div class="initial-card initial-close"></div>',
                unsafe_allow_html=True
            )
            st.session_state.initial_closed = False
            
            # 生成弹窗数据 - 500个
            st.session_state.windows = []
            for i in range(500):
                left, top = generate_random_position()
                color = random.choice(color_list)
                tip = random.choice(tips_list)
                st.session_state.windows.append({
                    'id': i, 'left': left, 'top': top, 'color': color, 'tip': tip
                })
            
            time.sleep(0.2)
            st.session_state.app_state = "batch"
            st.rerun()
    
    # 显示弹窗
    elif st.session_state.app_state == "batch":
        # 显示所有弹窗
        for window in st.session_state.windows:
            st.markdown(
                create_window_html(
                    window['id'], window['left'], window['top'],
                    "温馨提示", window['tip'], window['color']
                ),
                unsafe_allow_html=True
            )
        
        # 只显示关闭按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("关闭所有弹窗", key="close", use_container_width=True):
                st.session_state.app_state = "closed"
                st.rerun()
    
    # 关闭状态
    elif st.session_state.app_state == "closed":
        # 只显示重新开始按钮
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("重新开始", key="restart", use_container_width=True):
                st.session_state.app_state = "initial"
                st.session_state.windows = []
                st.session_state.initial_closed = False
                st.rerun()

if __name__ == "__main__":
    main()
