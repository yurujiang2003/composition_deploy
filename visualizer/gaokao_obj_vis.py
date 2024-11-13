import streamlit as st
import json

st.set_page_config(
    page_title="GAOKAO_Subjective_Questions_Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* 全局样式 */
    .main {
        padding: 30px;
        background-color: #f8f9fa;
    }
    
    /* 标题样式 */
    .big-title {
        color: #2c3e50;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 30px;
        padding-bottom: 10px;
        border-bottom: 3px solid #3498db;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background-color: #ffffff;
    }
    
    /* 文本样式 */
    .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
        color: #2c3e50;
    }
    
    /* 题目框样式 */
    .question-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #3498db;
    }
    
    /* 答案框样式 */
    .answer-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #2ecc71;
    }
    
    /* 解析框样式 */
    .analysis-box {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #e74c3c;
    }
    
    /* 元数据框样式 */
    .metadata-box {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* 子标题样式 */
    .subheader {
        color: #34495e;
        font-size: 1.3rem;
        font-weight: 500;
        margin: 10px 0;
    }
    
    /* LaTeX 公式容器样式 */
    .latex-container {
        padding: 10px;
        background-color: #f8f9fa;
        border-radius: 5px;
        margin: 10px 0;
    }
    
    /* 分割线样式 */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #3498db, transparent);
        margin: 30px 0;
    }
    
    /* 按钮样式美化 */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    /* 选择框样式 */
    .stSelectbox {
        background-color: white;
        border-radius: 5px;
        border: 1px solid #e0e0e0;
    }
    
    /* 标注工具样式 */
    .label-tool {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #9b59b6;  # 使用紫色区分标注工具
    }
    
    .label-section {
        margin-bottom: 20px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .hint-box {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

math_1_fill = load_data('/Users/tintin/Desktop/BabyMath/GAOKAO_Data/Subjective_Questions/2010-2022_Math_I_Fill-in-the-Blank.json')
math_2_fill = load_data('/Users/tintin/Desktop/BabyMath/GAOKAO_Data/Subjective_Questions/2010-2022_Math_II_Fill-in-the-Blank.json')

question_type = st.sidebar.radio(
    "Select Math Type",
    ["Math I Fill-in-the-Blank", "Math II Fill-in-the-Blank"]
)

data = math_1_fill if question_type == "Math I Fill-in-the-Blank" else math_2_fill

st.sidebar.title("Guide")
st.sidebar.markdown(f"**Keywords**: {data['keywords']}")

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
**Dataset Info**:
- Math I Fill-in-the-Blank: {len(math_1_fill['example'])} questions
- Math II Fill-in-the-Blank: {len(math_2_fill['example'])} questions
""")

selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(list(set(q['year'] for q in data['example'])))
)

year_questions = [q for q in data['example'] if q['year'] == selected_year]
selected_index = st.sidebar.selectbox(
    "Select Question",
    range(len(year_questions)),
    format_func=lambda x: f"Question {year_questions[x]['index'] + 1}"
)

question = year_questions[selected_index]

title_prefix = "Easy" if question_type == "Math I Fill-in-the-Blank" else "Hard"
st.markdown(f"<h1 class='big-title'>{selected_year}年高考{title_prefix}</h1>", unsafe_allow_html=True)

st.markdown(f"""
<div class='metadata-box'>
    <b style='color: #3498db;'>Category</b>: {question['category']}<br>
    <b style='color: #3498db;'>Question Number</b>: {question['index'] + 1}<br>
    <b style='color: #3498db;'>Type</b>: {title_prefix}
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='question-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>Question</h3>", unsafe_allow_html=True)
st.markdown("<div class='latex-container'>", unsafe_allow_html=True)
st.latex(question['question'])
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='answer-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>Answer</h3>", unsafe_allow_html=True)
st.markdown("<div class='latex-container'>", unsafe_allow_html=True)
st.latex(question['answer'])
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='analysis-box'>", unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>Analysis</h3>", unsafe_allow_html=True)
st.markdown("<div class='latex-container'>", unsafe_allow_html=True)
st.latex(question['analysis'])
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"""
<p style='text-align: center; color: #7f8c8d;'>
    <b>Current Type</b>: {title_prefix}<br>
    <b>Total Questions in Current Type</b>: {len(data['example'])}
</p>
""", unsafe_allow_html=True)

search_term = st.sidebar.text_input("Search questions")
if search_term:
    year_questions = [q for q in year_questions 
                     if search_term.lower() in q['question'].lower()]


st.markdown("<div class='label-tool'>", unsafe_allow_html=True)
st.markdown("<h3 class='subheader'>Problem Annotation Tool</h3>", unsafe_allow_html=True)

# 创建标注数据结构
label_data = {}

# 1. Hints 输入
st.markdown("<div class='label-section'>", unsafe_allow_html=True)
st.subheader("Step-by-Step Hints")

num_hints = st.number_input("Number of Hints", min_value=1, max_value=5, value=1)
hints = []
for i in range(num_hints):
    hint = st.text_area(
        f"Hint {i+1}",
        help=f"Enter step-by-step hint {i+1}",
        key=f"hint_{i}"
    )
    if hint:
        hints.append(hint)
label_data['hints'] = hints

# 2. 难度评估
st.markdown("<div class='label-section'>", unsafe_allow_html=True)
st.subheader("Difficulty Assessment")

# 难度评级
difficulty = st.select_slider(
    "Difficulty Level",
    options=['Very Easy', 'Easy', 'Medium', 'Medium-Hard', 'Hard', 'Very Hard'],
    value='Medium'
)
label_data['difficulty'] = difficulty

# 难度评估理由
difficulty_reason = st.text_area(
    "Reason for Difficulty Rating",
    help="Explain why you gave this difficulty rating"
)
label_data['difficulty_reason'] = difficulty_reason

# 添加标注者信息
col1, col2 = st.columns(2)
with col1:
    annotator = st.text_input("Annotator Name", help="Enter your name")
with col2:
    annotation_date = st.date_input("Annotation Date")

label_data['metadata'] = {
    'annotator': annotator,
    'annotation_date': str(annotation_date),
    'question_info': {
        'year': question['year'],
        'category': question['category'],
        'index': question['index'],
        'type': title_prefix
    }
}

# 合并原始数据和标注数据
output_data = {
    'original_data': {
        'question': question['question'],
        'answer': question['answer'],
        'analysis': question['analysis'],
        'year': question['year'],
        'category': question['category']
    },
    'annotations': label_data
}

# 导出功能
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("Export Annotation", key='export'):
        # 创建JSON字符串
        json_output = json.dumps(output_data, ensure_ascii=False, indent=2)
        
        # 生成文件名
        filename = f"gaokao_{question['year']}_math{title_prefix}_q{question['index']}_annotated.json"
        
        # 显示JSON预览
        st.markdown("### Annotation Preview")
        st.code(json_output, language='json')
        
        # 提供下载按钮
        st.download_button(
            label="Download JSON",
            data=json_output,
            file_name=filename,
            mime="application/json"
        )

with col2:
    if st.button("Clear Form", key='clear'):
        st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)
