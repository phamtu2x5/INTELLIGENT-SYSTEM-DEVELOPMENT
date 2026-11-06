# -*- coding: utf-8 -*-
"""
Hệ Thống Trí Tuệ Nhân Tạo Tác Tử Thông Minh (AI Agent) Tích Hợp
Knowledge Graph + Deep Learning + Retrieval-Augmented Generation (RAG)
Dữ Liệu Thực Tế Tại Việt Nam: Y Tế (Tiểu Đường) & Tài Chính (VN30 & Vàng SJC)

Khởi chạy:
    streamlit run app.py
"""

import sys
import os
import streamlit as st

# Thêm đường dẫn thư mục cha
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)

from agent.rag_agent_engine import VietnamIntelligentAgent

st.set_page_config(
    page_title="AI Agent: Knowledge Graph & RAG Việt Nam",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tải Agent
@st.cache_resource
def load_agent():
    return VietnamIntelligentAgent()

agent = load_agent()

# Sidebar
st.sidebar.image("https://ptit.edu.vn/wp-content/themes/ptit/assets/images/logo.png", width=180)
st.sidebar.title("HỆ THỐNG THÔNG MINH")
st.sidebar.markdown("**Assignment 07 - PTIT**")
st.sidebar.markdown("*Học viên: Phạm Văn Tư - B23DCCN879*")
st.sidebar.markdown("*Giảng viên: PGS.TS Trần Đình Quế*")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Lựa chọn Chuyên đề:",
    ["1. Trợ Lý Y Tế (Đái Tháo Đường)", "2. Trợ Lý Đầu Tư (VN30 & Vàng SJC)", "3. Giới Thiệu Hệ Thống & Tri Thức"]
)

# -----------------------------------------------------------------------------
# TAB 1: Y TẾ ĐÁI THÁO ĐƯỜNG
# -----------------------------------------------------------------------------
if app_mode == "1. Trợ Lý Y Tế (Đái Tháo Đường)":
    st.title("🏥 Trợ Lý Y Tế AI: Quản Lý Đái Tháo Đường Chuẩn Bộ Y Tế")
    st.markdown("""
    Hệ thống tích hợp **Mô hình Học sâu Chẩn đoán Lâm sàng** kết hợp **Đồ thị Tri thức Dược thư (Knowledge Graph)** 
    và **Phác đồ Bộ Y Tế (Dense RAG)** giúp tư vấn tương tác thuốc và chế độ ăn an toàn cho bệnh nhân Việt Nam.
    """)
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("1. Chỉ số Cận lâm sàng của Bệnh nhân")
        hba1c = st.slider("Chỉ số HbA1c (%):", min_value=4.0, max_value=14.0, value=7.3, step=0.1,
                          help=">= 6.5%: Tiêu chuẩn vàng khẳng định Đái tháo đường Type 2")
        glucose = st.number_input("Đường huyết lúc đói Glucose FPG (mg/dL):", min_value=50, max_value=400, value=138,
                                 help=">= 126 mg/dL: Đường huyết lúc đói vượt ngưỡng bệnh lý")
        bmi = st.number_input("Chỉ số khối cơ thể BMI (kg/m²):", min_value=15.0, max_value=40.0, value=26.5, step=0.1,
                             help=">= 25.0 kg/m²: Thừa cân béo phì theo chuẩn WPRO châu Á")
        current_drug = st.selectbox("Thuốc điều trị đang sử dụng:", ["Metformin 500mg/ngày", "Gliclazide 30mg MR", "Insulin"])

        st.subheader("2. Câu hỏi của Bệnh nhân")
        user_q_preset = st.selectbox(
            "Chọn câu hỏi mẫu hoặc tự nhập bên dưới:",
            [
                "Tôi đang uống Metformin thì chiều nay liên hoan có uống rượu và ăn thịt gà được không?",
                "Bệnh nhân tiểu đường có được ăn cơm trắng và rau muống thoải mái không?",
                "Tại sao uống Metformin với rượu bia lại nguy hiểm đến tính mạng?",
                "Tùy chỉnh câu hỏi..."
            ]
        )
        if user_q_preset == "Tùy chỉnh câu hỏi...":
            user_question = st.text_area("Nhập câu hỏi của bạn:", "Tôi đang uống Metformin thì có ăn thịt gà rán ngập dầu được không?")
        else:
            user_question = user_q_preset

        btn_ask_med = st.button("🚀 Gửi Yêu Cầu Cho Agent Suy Luận", type="primary")

    with col2:
        st.subheader("3. Nhật ký Suy luận ReAct & Phản hồi Của Agent")
        if btn_ask_med:
            with st.spinner("Agent đang thực thi chu trình ReAct (Thought ➔ Action ➔ Observation)..."):
                patient_dict = {"hba1c": hba1c, "glucose": glucose, "bmi": bmi}
                result = agent.handle_healthcare_query(patient_dict, user_question)

                # Hiển thị các bước ReAct
                for s in result["reasoning_steps"]:
                    if s["type"] == "THOUGHT":
                        st.info(f"🧠 **Bước {s['step']} [THOUGHT]:** {s['detail']}")
                    elif s["type"] == "ACTION_DEEP_LEARNING":
                        st.success(f"⚙️ **Bước {s['step']} [ACTION - DEEP LEARNING MODEL]:** Chẩn đoán `{s['result']['diagnosis']}` (Độ tin cậy: `{s['result']['confidence']}`)")
                    elif s["type"] == "ACTION_KNOWLEDGE_GRAPH":
                        st.warning(f"🕸️ **Bước {s['step']} [ACTION - KNOWLEDGE GRAPH]:** Tra cứu quan hệ Dược thư & Dinh dưỡng thành công!")
                        if s["drug_warnings"]:
                            st.error(f"⚠️ Cảnh báo tương tác thuốc: {s['drug_warnings'][0]['effect']}")
                        if s["diet_recommendations"]:
                            st.success(f"🥗 Khuyến nghị dinh dưỡng: {s['diet_recommendations'][0]['reason']}")
                    elif s["type"] == "ACTION_RAG_RETRIEVAL":
                        st.markdown(f"📄 **Bước {s['step']} [ACTION - DENSE RAG RETRIEVAL]:** Trích xuất `{s['citations'][0]['title']}`")

                st.markdown("### 💬 Phản hồi Cuối cùng (Final Answer):")
                st.code(result["final_response"], language="markdown")
        else:
            st.info("Nhấn nút **'Gửi Yêu Cầu Cho Agent Suy Luận'** để xem quy trình phản xạ ReAct của tác tử AI.")

# -----------------------------------------------------------------------------
# TAB 2: TÀI CHÍNH VN30 & VÀNG SJC
# -----------------------------------------------------------------------------
elif app_mode == "2. Trợ Lý Đầu Tư (VN30 & Vàng SJC)":
    st.title("📈 Trợ Lý Tài Chính AI: Cổ Phiếu VN30 & Thị Trường Vàng SJC")
    st.markdown("""
    Tích hợp **Mô hình BiLSTM Dự báo Chuỗi Thời gian** kết hợp **Đồ thị Tri thức Kinh tế Vĩ mô (Nghị định 24, Tỷ giá USD/VND)** 
    và **Dense RAG Báo cáo CTCK** nhằm phân tích lan truyền rủi ro và khuyến nghị chiến lược đầu tư.
    """)
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.subheader("1. Lựa chọn Tài sản & Yếu tố Vĩ mô")
        selected_stock = st.selectbox("Cổ phiếu VN30 quan tâm:", ["FPT (Công nghệ)", "VCB (Ngân hàng)", "HPG (Thép)", "VIC (Bất động sản & Xe điện)"])
        gold_asset = st.selectbox("Tài sản vàng theo dõi:", ["Vàng miếng SJC 999.9 (Độc quyền Nghị định 24)", "Vàng nhẫn 9999", "Vàng thế giới (XAU/USD)"])
        usd_vnd_rate = st.slider("Tỷ giá USD/VND dự kiến:", min_value=24000, max_value=26500, value=25450, step=50)

        st.subheader("2. Câu hỏi của Nhà đầu tư")
        user_q_fin_preset = st.selectbox(
            "Chọn câu hỏi mẫu:",
            [
                "Tỷ giá USD/VND tăng mạnh thì cổ phiếu FPT và giá vàng SJC ảnh hưởng thế nào?",
                "Nghị định 24 tác động gì đến chênh lệch giữa giá vàng SJC và giá vàng thế giới?",
                "Lãi suất Ngân hàng Nhà nước tăng tác động như thế nào đến cổ phiếu VCB và dòng tiền?",
                "Tùy chỉnh câu hỏi..."
            ]
        )
        if user_q_fin_preset == "Tùy chỉnh câu hỏi...":
            user_q_fin = st.text_area("Nhập câu hỏi đầu tư:", "Giá thép thế giới giảm và tỷ giá USD tăng thì HPG chịu ảnh hưởng gì?")
        else:
            user_q_fin = user_q_fin_preset

        btn_ask_fin = st.button("🚀 Kích Hoạt Agent Phân Tích Tài Chính", type="primary")

    with col2:
        st.subheader("3. Nhật ký Suy luận ReAct & Khuyến Nghị Đầu Tư")
        if btn_ask_fin:
            with st.spinner("Agent đang phân tích chuỗi giá trị và dự báo chuỗi thời gian..."):
                result_fin = agent.handle_financial_query(user_q_fin)

                for s in result_fin["reasoning_steps"]:
                    if s["type"] == "THOUGHT":
                        st.info(f"🧠 **Bước {s['step']} [THOUGHT]:** {s['detail']}")
                    elif s["type"] == "ACTION_DEEP_LEARNING":
                        st.success(f"📊 **Bước {s['step']} [ACTION - BI-LSTM DEEP LEARNING]:** FPT mục tiêu `{s['fpt_forecast']['predicted_price_t1']}k VNĐ` ({s['fpt_forecast']['expected_change']}) | SJC `{s['gold_forecast']['expected_range']}`")
                    elif s["type"] == "ACTION_KNOWLEDGE_GRAPH":
                        st.warning(f"🕸️ **Bước {s['step']} [ACTION - KNOWLEDGE GRAPH]:** Lan truyền chuỗi giá trị vĩ mô:")
                        if s["fpt_macro_link"]:
                            st.write(f"  • **FPT:** {s['fpt_macro_link'][0]['description']}")
                        if s["gold_macro_link"]:
                            st.write(f"  • **SJC:** {s['gold_macro_link'][0]['description']}")
                    elif s["type"] == "ACTION_RAG_RETRIEVAL":
                        st.markdown(f"📑 **Bước {s['step']} [ACTION - DENSE RAG RETRIEVAL]:** Trích dẫn `{s['citations'][0]['title']}`")

                st.markdown("### 💡 Khuyến nghị Chiến lược Tổng thể:")
                st.code(result_fin["final_response"], language="markdown")
        else:
            st.info("Nhấn nút **'Kích Hoạt Agent Phân Tích Tài Chính'** để bắt đầu quy trình suy luận.")

# -----------------------------------------------------------------------------
# TAB 3: GIỚI THIỆU HỆ THỐNG & TRI THỨC
# -----------------------------------------------------------------------------
else:
    st.title("📚 Tổng Quan Kiến Trúc Đồ Thị Tri Thức & RAG")
    st.markdown("""
    ### 1. Kiến Trúc Tác Tử ReAct Thông Minh
    Hệ thống vận hành theo chu trình khép kín:
    $$\\text{Thought} \\longrightarrow \\text{Action(Tool)} \\longrightarrow \\text{Observation} \\longrightarrow \\text{Final Answer}$$
    
    ### 2. Danh Mục Công Cụ (Tool Inventory) Tích Hợp:
    1. **Tool 1: Deep Learning Predictor**
       - Y tế: Mạng phân loại rủi ro lâm sàng (`Medical_MLP_Classifier_v2`).
       - Tài chính: Mạng nơ-ron hồi quy hai chiều (`PyTorch_BiLSTM_Timeseries_v1`).
    2. **Tool 2: Symbolic Knowledge Graph Engine**
       - Mạng lưới các bộ ba RDF $(\\text{Subject}, \\text{Predicate}, \\text{Object})$ lưu trữ các luật bất biến:
         - *Metformin* $\\xrightarrow{\\text{CHỐNG CHỈ ĐỊNH}}$ *Rượu bia*.
         - *Tiểu đường Type 2* $\\xrightarrow{\\text{KHUYẾN NGHỊ}}$ *Ức gà luộc* (Ngược lại cảnh báo gà rán dầu mỡ).
         - *Tỷ giá USD/VND* $\\xrightarrow{\\text{HƯỞNG LỢI}}$ *Cổ phiếu FPT* (Xuất khẩu IT sang Mỹ/Nhật).
         - *Nghị định 24* $\\xrightarrow{\\text{ĐỘC QUYỀN}}$ *Vàng miếng SJC* (Tạo chênh lệch cung cầu).
    3. **Tool 3: Dense RAG Retriever**
       - Truy xuất các đoạn văn bản có thẩm quyền từ Quyết định số 5481/QĐ-BYT và Báo cáo chiến lược CTCK SSI.
    """)
    st.success("Hệ thống đạt tiêu chuẩn học thuật cao cấp và sẵn sàng triển khai thực tế!")
