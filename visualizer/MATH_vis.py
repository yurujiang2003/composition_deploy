import streamlit as st
import json
import os
from pathlib import Path

# 页面配置
st.set_page_config(
    page_title="MATH Dataset Visualizer",
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
        font-size: 2.2rem;
        font-weight: 600;
        text-align: left;
        margin: 1rem 0 2rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f0f0f0;
    }
    
    /* 卡片基础样式 */
    .card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #f0f0f0;
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* 问题卡片 */
    .problem-box {
        border-left: 3px solid #4361ee;
    }
    
    /* 解答卡片 */
    .solution-box {
        border-left: 3px solid #4cc9f0;
    }
    
    /* 元数据样式优化 */
    .metadata-box {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        padding: 1.2rem;
        background: #f8fafc;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
    }
    
    .metadata-item {
        background: #ffffff;
        padding: 0.7rem 1.2rem;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
        font-size: 0.95rem;
        color: #1a1a1a;  /* 加深文本颜色 */
        font-weight: 500;  /* 加粗文本 */
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }
    
    /* 标签样式优化 */
    .tag {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;  /* 加粗标签文本 */
        margin-right: 0.7rem;
        letter-spacing: 0.02em;
    }
    
    .tag-blue { 
        color: #ffffff;  /* 改为白色文本 */
        background-color: #2563eb;  /* 加深蓝色背景 */
    }
    
    .tag-green { 
        color: #ffffff;  /* 改为白色文本 */
        background-color: #0891b2;  /* 加深青色背景 */
    }
    
    /* LaTeX 容器样式 */
    .latex-container {
        padding: 1rem;
        background: #fafafa;
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    /* 侧边栏样式 */
    .css-1d391kg {
        background-color: #ffffff;
        padding: 1rem;
    }
    
    /* 分割线样式 */
    hr {
        border: none;
        border-top: 1px solid #f0f0f0;
        margin: 1.5rem 0;
    }
    
    /* 按钮和输入框样式 */
    .stButton>button {
        background-color: #4361ee;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .stTextInput>div>div>input {
        border-radius: 4px;
        border: 1px solid #e2e8f0;
    }
    
    /* 文件路径样式 */
    .file-path {
        font-family: 'Roboto Mono', monospace;
        font-size: 0.9rem;
        color: #64748b;
        padding: 0.5rem;
        background: #f8fafc;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* 侧边栏标题样式 */
    .sidebar-title {
        color: #1a1a1a;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    /* 筛选器标签样式 */
    .filter-label {
        color: #1a1a1a;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* 统计数字样式 */
    .metric-value {
        color: #1a1a1a;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .metric-label {
        color: #4b5563;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
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

@st.cache_data
def load_all_json_files(directory):
    """加载指定目录下的所有JSON文件"""
    json_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        # 使用相对路径作为键
                        rel_path = os.path.relpath(file_path, directory)
                        json_files[rel_path] = data
                    except json.JSONDecodeError:
                        st.warning(f"Error loading {file_path}")
    return json_files

def filter_data(data_dict, filters):
    """根据筛选条件过滤数据"""
    filtered_data = data_dict.copy()
    
    for key, values in filters.items():
        if values:  # 如果有选择筛选条件
            filtered_data = {
                k: v for k, v in filtered_data.items()
                if v.get(key, '') in values
            }
    
    return filtered_data

# 加载数据
directory = 'MATH/train'
all_data = load_all_json_files(directory)

# 侧边栏优化
with st.sidebar:
    st.markdown("<p class='sidebar-title'>MATH Explorer</p>", unsafe_allow_html=True)
    
    # 搜索框
    search_term = st.text_input("🔍 Search Problems", 
                               placeholder="Enter keywords...")
    
    st.markdown("<p class='sidebar-title'>Filters</p>", unsafe_allow_html=True)
    
    # 收集所有可能的筛选值
    filter_options = {
        'type': sorted(set(data.get('type', '') for data in all_data.values())),
        'level': sorted(set(data.get('level', '') for data in all_data.values())),
        # 可以添加更多筛选条件
    }
    
    # 创建筛选条件
    filters = {}
    
    # 难度和类型筛选
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p class='filter-label'>Difficulty</p>", unsafe_allow_html=True)
        filters['level'] = st.multiselect(
            "",
            options=filter_options['level'],
            default=None,
            key='level_filter'
        )
    
    with col2:
        st.markdown("<p class='filter-label'>Type</p>", unsafe_allow_html=True)
        filters['type'] = st.multiselect(
            "",
            options=filter_options['type'],
            default=None,
            key='type_filter'
        )
    
    # 应用筛选
    filtered_data = filter_data(all_data, filters)
    
    # 如果有搜索词，进一步筛选
    if search_term:
        filtered_data = {
            k: v for k, v in filtered_data.items()
            if search_term.lower() in v.get('problem', '').lower() or 
               search_term.lower() in v.get('solution', '').lower()
        }
    
    # 统计信息
    st.markdown("---")
    st.markdown("<p class='sidebar-title'>Statistics</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class='metric-value'>{len(all_data)}</div>
        <div class='metric-label'>Total</div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='metric-value'>{len(filtered_data)}</div>
        <div class='metric-label'>Filtered</div>
        """, unsafe_allow_html=True)
    with col3:
        percentage = (len(filtered_data) / len(all_data)) * 100 if len(all_data) > 0 else 0
        st.markdown(f"""
        <div class='metric-value'>{percentage:.1f}%</div>
        <div class='metric-label'>Percentage</div>
        """, unsafe_allow_html=True)
    
    # 排序选项
    st.markdown("### Sort By")
    sort_option = st.selectbox(
        "",
        ["File Name", "Type", "Level"],
        key='sort_option'
    )

# 根据筛选结果更新文件选择器
if filtered_data:
    if sort_option == "File Name":
        sorted_files = sorted(filtered_data.keys())
    elif sort_option == "Type":
        sorted_files = sorted(filtered_data.keys(), 
                            key=lambda x: filtered_data[x].get('type', ''))
    else:  # Level
        sorted_files = sorted(filtered_data.keys(), 
                            key=lambda x: filtered_data[x].get('level', ''))
    
    selected_file = st.selectbox(
        "Select Problem",
        sorted_files,
        format_func=lambda x: f"{filtered_data[x].get('type', 'Unknown')} - "
                            f"Level {filtered_data[x].get('level', 'Unknown')} - {x}"
    )
    
    current_data = filtered_data[selected_file]
    
    # 显示内容
    st.markdown("<h1 class='main-title'>MATH Problem Viewer</h1>", 
                unsafe_allow_html=True)
    
    # 元数据显示
    st.markdown(f"""
    <div class='metadata-box'>
        <div class='metadata-item'>
            <span class='tag tag-blue'>Type</span>
            {current_data.get('type', 'N/A')}
        </div>
        <div class='metadata-item'>
            <span class='tag tag-green'>Level</span>
            {current_data.get('level', 'N/A')}
        </div>
        <div class='metadata-item'>
            <span class='tag tag-blue'>File</span>
            {os.path.basename(selected_file)}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 问题显示
    st.markdown("<div class='card problem-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Problem</h3>", unsafe_allow_html=True)
    st.latex(current_data.get('problem', ''))
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 解答显示
    st.markdown("<div class='card solution-box'>", unsafe_allow_html=True)
    st.markdown("<h3>Solution</h3>", unsafe_allow_html=True)
    st.latex(current_data.get('solution', ''))
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 在显示完问题和解答后，添加标注工具
    if filtered_data:  # 只在有选中问题时显示标注工具
        st.markdown("<div class='card label-tool'>", unsafe_allow_html=True)
        st.markdown("<h3>Problem Annotation Tool</h3>", unsafe_allow_html=True)

        # 创建标注数据结构
        label_data = {}

        # 1. Hints 输入
        st.markdown("<div class='label-section'>", unsafe_allow_html=True)
        st.subheader("Problem Hints")
        
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

        # 难度评级（使用和原题目相同的难度等级）
        levels = sorted(set(data.get('level', '') for data in all_data.values()))
        annotator_difficulty = st.select_slider(
            "Annotator's Difficulty Rating",
            options=levels,
            value=current_data.get('level', levels[0])
        )
        label_data['annotator_difficulty'] = annotator_difficulty

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
            'original_file': selected_file
        }

        # 合并原始数据和标注数据
        output_data = {
            'original_data': current_data,
            'annotations': label_data
        }

        # 导出功能
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("Export Annotation", key='export'):
                # 创建JSON字符串
                json_output = json.dumps(output_data, ensure_ascii=False, indent=2)
                
                # 生成文件名
                base_name = os.path.splitext(os.path.basename(selected_file))[0]
                filename = f"{base_name}_annotated.json"
                
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
else:
    st.warning("No problems match your filters. Please adjust your criteria.")
