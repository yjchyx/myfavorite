import streamlit as st
import time

# 初始化会话状态，记录弹窗点击状态和语录显示索引
if "dialog_closed" not in st.session_state:
    st.session_state.dialog_closed = False
if "show_index" not in st.session_state:
    st.session_state.show_index = 0

# 定义要显示的语录列表
quotes = [
    "全球高考——这里的一切都有始有终，却能容纳所有不期而遇和久别重逢。",
    "世界灿烂盛大，欢迎回家。",
    "两千三百一十二天，他们相遇在寒风朔雪中。 那是他们的初见。",
    "监考结束，恭喜各位考生，顺利通关。",
    "他想，他见过一个光明炽热的人，靠着这个，他可以走过所有寒冬。",
    "别回头，一直往前走，永远。",
    "这里风遇山止，船到岸停。 他身后的陆地绵延一亿多公顷，脚下的海有三百多万平方公里。 再往南，至多不过穿于云上，绕地而行。 这里的一切都有始有终，却能容纳所有的不期而遇和久别重逢。 世界灿烂盛大。 欢迎回家。",
    "你是我的人，就算我死了，也得是我的鬼。",
    "我不是来救你的，我是来爱你的。",
    "于这浮华世间，寻一知己，共赴山海，便是此生所幸。"
]

# 初始弹窗：点击后关闭并触发后续内容
if not st.session_state.dialog_closed:
    with st.dialog("全球高考", width="small"):
        st.write("点击任意位置开始展示语录")
        # 隐藏默认关闭按钮，点击弹窗区域即触发
        if st.button(" ", key="init_click", use_container_width=True, help="点击开始"):
            st.session_state.dialog_closed = True
else:
    # 逐个显示语录，点击页面任意位置加载下一条，铺满全屏不消失
    col1, col2, col3 = st.columns(3)
    display_index = 0
    while display_index < st.session_state.show_index and display_index < len(quotes):
        # 循环布局显示语录
        if display_index % 3 == 0:
            with col1:
                st.info(quotes[display_index])
        elif display_index % 3 == 1:
            with col2:
                st.success(quotes[display_index])
        else:
            with col3:
                st.warning(quotes[display_index])
        display_index += 1

    # 未铺满全屏时，提供点击加载下一条的按钮
    if st.session_state.show_index < len(quotes):
        if st.button("点击加载下一条语录", key="load_next", use_container_width=True):
            st.session_state.show_index += 1
            st.rerun()
    else:
        st.success("所有语录已全部展示，铺满全屏！")
