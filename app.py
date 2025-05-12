# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 模拟数据库
supplier_db = {
    "suppliers": [
        {"id": "RF-202403", "name": "锐锋精密", "category": "电池托盘", 
         "qualification": "A级", "price": 15800, "delivery_score": 92}
    ],
    "conflicts": [
        {"event_id": "C-001", "supplier_id": "RF-202403", 
         "conflict_type": "三重冲突", "status": "已解决"}
    ],
    "arbitrations": [
        {"event_id": "C-001", "resolution": "有条件通过", 
         "conditions": ["试用期3个月", "首付30%", "补充尽调"]}
    ]
}

# 页面配置
st.set_page_config(page_title="链智审系统演示", layout="wide")

# 标题区
st.title("🛠️ 供应链AI协同审核系统 - 链智审")
st.markdown("---")

# 功能模块
with st.sidebar:
    st.header("导航")
    page = st.radio("选择演示模块", ["冲突场景模拟", "仲裁工作流", "实施案例库"])
    
    # 参数调节
    st.header("参数调节")
    base_price = st.slider("设定基准价格（万元）", 10.0, 20.0, 14.2)
    risk_threshold = st.slider("风险阈值（0-100）", 0, 100, 60)

# 场景模拟页
if page == "冲突场景模拟":
    st.header("🔍 供应商资质审核冲突模拟")
    
    current_price = supplier_db["suppliers"][0]["price"] / 10000
    price_deviation = (current_price - base_price) / base_price * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("采购部门AI")
        st.metric("交付能力评分", "92/100", delta="推荐等级A")
        st.progress(0.92)
        with st.expander("AI决策逻辑详情"):
            st.markdown("**模型架构**")
            st.code("""- 类型：随机森林
- 输入特征：
  ✓ 历史交付准时率(30%)
  ✓ 资质证书完整性(25%)
  ✓ 产能稳定性(25%)
  ✓ 合作年限(20%)""")
            st.markdown("**数据源**")
            st.write("ERP系统 + 供应商自填表单")
        
    with col2:
        st.subheader("法务部门AI")
        risk_level = "高" if risk_threshold < 70 else "中"
        st.metric("风险评级", risk_level, delta="1条关联诉讼", delta_color="inverse")
        with st.expander("AI决策逻辑详情"):
            st.markdown("**模型架构**")
            st.code("""- 类型：图神经网络
- 分析维度：
  ✓ 直接法律风险(40%)
  ✓ 关联方风险(30%)
  ✓ 行业合规趋势(20%)
  ✓ 舆情风险(10%)""")
            st.markdown("**数据源**")
            st.write("裁判文书网 + 企业关系图谱")
        
    with col3:
        st.subheader("财务部门AI")
        st.metric("价格偏离度", f"{price_deviation:.1f}%", 
                 delta="超出阈值" if abs(price_deviation)>5 else "在允许范围内", 
                 delta_color="inverse" if abs(price_deviation)>5 else "normal")
        with st.expander("AI决策逻辑详情"):
            st.markdown("**模型架构**")
            st.code("""- 类型：LSTM时序预测
- 考虑因素：
  ✓ 历史采购价格(50%)
  ✓ 原材料价格指数(30%)
  ✓ 汇率波动(15%)
  ✓ 运输成本(5%)""")
            st.markdown("**数据源**")
            st.write("财务系统 + 大宗商品交易平台")
    
    st.markdown("---")
    st.subheader("跨AI系统输出对比")
    
    # 新增AI输出对比雷达图
    radar_df = pd.DataFrame(dict(
        指标=["交付能力", "风险控制", "成本效益", "合规性", "可持续性"],
        采购AI=[92, 60, 85, 70, 65],
        法务AI=[75, 35, 60, 30, 55],
        财务AI=[80, 70, 68, 75, 60]
    ))
    
    fig = px.line_polar(radar_df, r='采购AI', theta='指标', line_close=True,
                        title="部门AI评估维度对比")
    fig.add_scatterpolar(r=radar_df['法务AI'], theta=radar_df['指标'], name='法务AI')
    fig.add_scatterpolar(r=radar_df['财务AI'], theta=radar_df['指标'], name='财务AI')
    st.plotly_chart(fig, use_container_width=True)

# 工作流页
elif page == "仲裁工作流":
    st.header("⚙️ 三阶治理工作流演示")
    
    tab1, tab2, tab3, tab4 = st.tabs(["冲突识别", "仲裁会议", "系统连携", "执行跟踪"])
    
    # 冲突识别标签页
    with tab1:
        st.subheader("阶段1：多AI输出分析")
        
        col1, col2 = st.columns([2,1])
        with col1:
            st.markdown("**冲突特征提取**")
            st.code("""识别到的AI输出差异：
1. 采购AI置信度：92% (高置信推荐)
2. 法务AI置信度：78% (中等风险)
3. 财务AI置信度：85% (高确定性超标)""")
            
            st.markdown("**差异类型判定**")
            st.write("""
            - 目标冲突：效率vs合规vs成本
            - 数据源差异：运营数据vs法律数据vs财务数据
            - 模型差异：监督学习vs图计算vs时序分析""")
            
        with col2:
            st.markdown("**冲突分类矩阵**")
            matrix_df = pd.DataFrame([
                ["单一指标超标", "自动补偿谈判", "2小时"],
                ["双重目标冲突", "部门联席预审", "8小时"],
                ["三重冲突+置信差异", "AI仲裁委员会", "24小时"]
            ], columns=["冲突类型", "处理通道", "时限"])
            st.dataframe(matrix_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("AI输出溯源验证")
        
        verify_df = pd.DataFrame([
            ["采购AI", "交付准时率", "98%", "ERP订单数据", "已验证"],
            ["法务AI", "关联诉讼", "1条", "裁判文书网", "已核实"],
            ["财务AI", "价格偏离度", "+12%", "历史采购记录", "需复核"]
        ], columns=["AI系统", "关键指标", "输出值", "数据源", "验证状态"])
        
        st.dataframe(verify_df.style.applymap(
            lambda x: "color: green" if x=="已验证" else "color: orange" if x=="已核实" else "color: red"), 
            use_container_width=True)
    
    # 仲裁会议标签页
    with tab2:
        st.subheader("仲裁会议进程")
        
        timeline_df = pd.DataFrame([
            {"阶段": "会前准备", "状态": "已完成", "耗时": 2, "负责人": "系统自动"},
            {"阶段": "证据调取", "状态": "进行中", "耗时": 1, "负责人": "内审部"},
            {"阶段": "多方听证", "状态": "待处理", "耗时": 3, "负责人": "仲裁主席"},
            {"阶段": "决议生成", "状态": "待处理", "耗时": 1, "负责人": "AI顾问"}
        ])
        
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("**多AI证据链分析**")
            st.code("""采购AI证据链：
✓ 10次准时交付记录
✓ 3项质量认证证书
✓ 产能利用率85%

法务AI风险链：
✗ 关联企业未决诉讼
✗ 合同模版版本过期
✓ 无行政处罚记录

财务AI成本链：
✓ 报价高于行业基准
✓ 付款条款风险中等
✓ 汇率风险可控""")
            
        with col2:
            st.markdown("**AI置信度评估**")
            st.metric("采购AI置信度", "92%", delta="高可信区间")
            st.metric("法务AI置信度", "78%", delta_color="inverse")
            st.metric("财务AI置信度", "85%", delta="高可信区间")
    
    # 系统连携标签页
    with tab3:
        st.subheader("系统连携拓扑")
        
        nodes = pd.DataFrame([
            {"节点": "链智审核心", "类型": "中枢系统", "x": 2, "y": 2},
            {"节点": "ERP", "类型": "业务系统", "x": 1, "y": 1},
            {"节点": "合同数据库", "类型": "法务系统", "x": 3, "y": 1},
            {"节点": "财务中台", "类型": "财务系统", "x": 2, "y": 0},
            {"节点": "舆情监控", "类型": "外部数据", "x": 4, "y": 2}
        ])
        
        edges = [
            {"来源": "链智审核心", "目标": "ERP", "类型": "实时数据"},
            {"来源": "链智审核心", "目标": "合同数据库", "类型": "API调用"},
            {"来源": "链智审核心", "目标": "财务中台", "类型": "双向同步"},
            {"来源": "链智审核心", "目标": "舆情监控", "类型": "数据抓取"}
        ]
        
        fig = px.scatter(nodes, x="x", y="y",
                        size=[30,20,20,20,20],
                        color="类型",
                        text="节点",
                        title="系统集成拓扑图")
        
        for edge in edges:
            source = nodes[nodes["节点"] == edge["来源"]].iloc[0]
            target = nodes[nodes["节点"] == edge["目标"]].iloc[0]
            fig.add_shape(
                type="line",
                x0=source["x"], y0=source["y"],
                x1=target["x"], y1=target["y"],
                line=dict(color="#BDBDBD", width=2)
            )
            
        fig.update_traces(marker=dict(size=100),
                         textfont=dict(size=14))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**实时数据流状态**")
        flow_df = pd.DataFrame([
            ["ERP→核心", "采购订单", "正常", "5ms"],
            ["法务→核心", "合同条款", "延迟", "320ms"],
            ["财务→核心", "成本数据", "正常", "8ms"],
            ["舆情→核心", "行业风险", "正常", "120ms"]
        ], columns=["通道", "数据类型", "状态", "延迟"])
        st.dataframe(flow_df.style.applymap(
            lambda x: "color: red" if x=="延迟" else None), 
            use_container_width=True)
    
    # 执行跟踪标签页
    with tab4:
        st.subheader("执行追踪矩阵")
        task_df = pd.DataFrame([
            ["合同修订", "法务部", "内审部", "风险<30"],
            ["付款调整", "财务部", "供应链部", "偏差<5%"],
            ["关系维护", "采购部", "客户成功部", "评分≥4"]
        ], columns=["任务", "执行方", "监督方", "验收标准"])
        
        st.dataframe(task_df.style.applymap(
            lambda x: "background-color: #e6f3ff" if x=="法务部" else ""), 
            use_container_width=True)
        
        st.button("模拟完成通知", help="点击发送完成通知邮件")

# 实施案例库页
elif page == "实施案例库":
    st.header("📚 实施案例库")
    
    case_filter = st.selectbox("筛选案例类型", ["全部", "三重冲突", "双重冲突", "单一冲突"])
    
    case_df = pd.DataFrame({
        "案例ID": ["C-2023-045", "C-2024-012", "C-2024-018"],
        "冲突类型": ["三重冲突", "双重冲突", "单一冲突"],
        "处置方式": ["有条件通过", "调整后通过", "自动处理"],
        "处理时长": [24, 8, 2],
        "保留结果": ["成功合作", "进行中", "已终止"]
    })
    
    if case_filter != "全部":
        case_df = case_df[case_df["冲突类型"] == case_filter]
    
    st.dataframe(case_df, use_container_width=True)
    
    with st.expander("案例趋势分析"):
        fig = px.line(case_df, x="案例ID", y="处理时长",
                     title="案例处理效率趋势")
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("演示系统说明：本系统使用模拟数据展示核心业务流程")
