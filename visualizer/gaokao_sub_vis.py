import streamlit as st
import json
import os

st.set_page_config(
    page_title="GAOKAO Math Subjective Questions",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 样式设置
st.markdown("""
    <style>
    /* 全局样式 */
    .main {
        padding: 2rem;
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* 标题样式 */
    .main-title {
        color: #1a1a1a;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    /* 卡片基础样式 */
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #eaeaea;
        transition: all 0.3s ease;
    }
    
    /* 题目卡片 */
    .question-box {
        border-left: 4px solid #4361ee;
    }
    
    /* 答案卡片 */
    .answer-box {
        border-left: 4px solid #2cb67d;
    }
    
    /* 解析卡片 */
    .analysis-box {
        border-left: 4px solid #f72585;
    }
    
    /* 元数据样式 */
    .metadata-box {
        display: flex;
        gap: 1rem;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 8px;
        margin-bottom: 1.5rem;
    }
    
    .metadata-item {
        background: #ffffff;
        padding: 0.75rem 1.25rem;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        font-size: 0.95rem;
        font-weight: 500;
        color: #1a1a1a;
    }
    
    /* 标签样式 */
    .tag {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .tag-blue { background-color: #1e40af; }
    .tag-green { background-color: #166534; }
    .tag-red { background-color: #be123c; }
    
    /* 元数据项中的文本样式 */
    .metadata-item span {
        display: block;
        margin-bottom: 0.3rem;
    }
    
    .metadata-item br + text {
        color: #1a1a1a;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* 可以为不同类型的数据使用不同的颜色（可选） */
    .metadata-item:nth-child(1) br + text {
        color: #1e3a8a;
    }
    
    .metadata-item:nth-child(2) br + text {
        color: #14532d;
    }
    
    .metadata-item:nth-child(3) br + text {
    .tag-blue { background-color: #4361ee; }
    .tag-green { background-color: #2cb67d; }
    .tag-red { background-color: #f72585; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 加载所有数据文件
math_1_fill = load_data('GAOKAO_Data/Subjective_Questions/2010-2022_Math_I_Fill-in-the-Blank.json')
math_1_open = load_data('GAOKAO_Data/Subjective_Questions/2010-2022_Math_I_Open-ended_Questions.json')
math_2_fill = load_data('GAOKAO_Data/Subjective_Questions/2010-2022_Math_II_Fill-in-the-Blank.json')
math_2_open = load_data('GAOKAO_Data/Subjective_Questions/2010-2022_Math_II_Open-ended_Questions.json')

# 修改问题类型选择
question_type = st.sidebar.radio(
    "Select Math Type",
    ["Math I Fill-in-the-Blank", 
     "Math I Open-ended",
     "Math II Fill-in-the-Blank",
     "Math II Open-ended"]
)

# 根据选择加载相应数据
data = {
    "Math I Fill-in-the-Blank": math_1_fill,
    "Math I Open-ended": math_1_open,
    "Math II Fill-in-the-Blank": math_2_fill,
    "Math II Open-ended": math_2_open
}[question_type]

st.sidebar.title("Guide")
st.sidebar.markdown(f"**Keywords**: {data['keywords']}")

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
**Dataset Info**:
- Math I Fill-in-the-Blank: {len(math_1_fill['example'])} questions
- Math I Open-ended: {len(math_1_open['example'])} questions
- Math II Fill-in-the-Blank: {len(math_2_fill['example'])} questions
- Math II Open-ended: {len(math_2_open['example'])} questions
""")

# 侧边栏
with st.sidebar:
    st.title("高考数学题库")
    st.markdown(f"**数据集**: {data['keywords']}")
    
    # 年份选择
    years = sorted(list(set(q['year'] for q in data['example'])))
    selected_year = st.selectbox(
        "选择年份",
        years,
        format_func=lambda x: f"{x}年"
    )
    
    # 题目筛选
    year_questions = [q for q in data['example'] if q['year'] == selected_year]
    selected_index = st.selectbox(
        "选择题目",
        range(len(year_questions)),
        format_func=lambda x: f"第{year_questions[x]['index'] + 1}题 ({year_questions[x]['score']}分)"
    )
    
    # 统计信息
    st.markdown("---")
    st.markdown("### 统计信息")
    st.metric("总题目数", len(data['example']))
    st.metric(f"{selected_year}年题目数", len(year_questions))

# 获取选中的题目
question = year_questions[selected_index]

# 主标题
st.markdown(f"<h1 class='main-title'>{selected_year}年高考数学主观题</h1>", unsafe_allow_html=True)

# 元数据显示
st.markdown(f"""
<div class='metadata-box'>
    <div class='metadata-item'>
        <span class='tag tag-blue'>类型</span>
        <br>{question['category']}
    </div>
    <div class='metadata-item'>
        <span class='tag tag-green'>题号</span>
        <br>第 {question['index'] + 1} 题
    </div>
    <div class='metadata-item'>
        <span class='tag tag-red'>分值</span>
        <br>{question['score']} 分
    </div>
</div>
""", unsafe_allow_html=True)

# 题目显示
st.markdown("<div class='card question-box'>", unsafe_allow_html=True)
st.markdown("<h3>题目</h3>", unsafe_allow_html=True)
st.latex(question['question'])
st.markdown("</div>", unsafe_allow_html=True)

# 答案显示
st.markdown("<div class='card answer-box'>", unsafe_allow_html=True)
st.markdown("<h3>答案</h3>", unsafe_allow_html=True)
st.latex(question['answer'])
st.markdown("</div>", unsafe_allow_html=True)

# 解析显示
st.markdown("<div class='card analysis-box'>", unsafe_allow_html=True)
st.markdown("<h3>解析</h3>", unsafe_allow_html=True)
st.latex(question['analysis'])
st.markdown("</div>", unsafe_allow_html=True)

# 添加标注工具
st.markdown("""
<style>
/* 标注工具样式 */
.label-tool {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 2rem;
    border: 1px solid #e2e8f0;
}

.label-section {
    margin-bottom: 1.5rem;
}

.hint-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='card label-tool'>", unsafe_allow_html=True)
st.markdown("<h3>题目标注工具</h3>", unsafe_allow_html=True)

# 创建标注数据结构
label_data = {}

# 1. Hints 输入
st.markdown("<div class='label-section'>", unsafe_allow_html=True)
st.subheader("解题提示")

num_hints = st.number_input("提示数量", min_value=1, max_value=5, value=1)
hints = []
for i in range(num_hints):
    hint = st.text_area(
        f"提示 {i+1}",
        help=f"输入第 {i+1} 个解题提示",
        key=f"hint_{i}"
    )
    if hint:
        hints.append(hint)
label_data['hints'] = hints

# 2. 难度评估
st.markdown("<div class='label-section'>", unsafe_allow_html=True)
st.subheader("难度评估")

# 难度评级
difficulty = st.select_slider(
    "难度等级",
    options=['简单', '中等偏易', '中等', '中等偏难', '困难'],
    value='中等'
)
label_data['difficulty'] = difficulty

# 难度评估理由
difficulty_reason = st.text_area(
    "难度评估理由",
    help="请说明为什么给出这个难度评级"
)
label_data['difficulty_reason'] = difficulty_reason

# 添加标注者信息
col1, col2 = st.columns(2)
with col1:
    annotator = st.text_input("标注者姓名", help="输入你的名字")
with col2:
    annotation_date = st.date_input("标注日期")

label_data['metadata'] = {
    'annotator': annotator,
    'annotation_date': str(annotation_date),
    'question_info': {
        'year': question['year'],
        'category': question['category'],
        'index': question['index'],
        'score': question['score']
    }
}

# 合并原始数据和标注数据
output_data = {
    'original_data': {
        'question': question['question'],
        'answer': question['answer'],
        'analysis': question['analysis']
    },
    'annotations': label_data
}

# 导出功能
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("导出标注", key='export'):
        # 创建JSON字符串
        json_output = json.dumps(output_data, ensure_ascii=False, indent=2)
        
        # 生成文件名
        filename = f"gaokao_{question['year']}_{'math1' if 'Math I' in question_type else 'math2'}_{'fill' if 'Fill' in question_type else 'open'}_q{question['index']}_annotated.json"
        
        # 显示JSON预览
        st.markdown("### 标注预览")
        st.code(json_output, language='json')
        
        # 提供下载按钮
        st.download_button(
            label="下载JSON文件",
            data=json_output,
            file_name=filename,
            mime="application/json"
        )

with col2:
    if st.button("清空表单", key='clear'):
        st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)
