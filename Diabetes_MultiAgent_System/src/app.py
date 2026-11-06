#!/usr/bin/env python3
"""
app.py
======
HỆ THỐNG TRỢ LÝ TƯ VẤN ĐÁI THÁO ĐƯỜNG (DiaAgent Demo)
Giao diện Hội thoại Thông minh (Chatbot-First Interactive Consultation):
- Khởi động an toàn: Hệ thống ở trạng thái chờ, CHỈ phân tích khi người dùng nhấn nút hoặc gửi yêu cầu.
- Tương tác tự nhiên: Tiếp nhận triệu chứng, khai thác thể trạng và tự động tính chỉ số BMI.
- Phân luồng logic lâm sàng chặt chẽ:
  * Khi thiếu xét nghiệm: Chỉ phân tầng nguy cơ sơ bộ, hướng dẫn xét nghiệm cần làm, tuyệt đối không kết luận bệnh và không kê thuốc điều trị.
  * Khi đủ xét nghiệm: Đối chiếu tiêu chuẩn Bộ Y Tế (QĐ 5481/QĐ-BYT), đưa ra nhận định giai đoạn và hướng dẫn phác đồ thuốc + giá Long Châu.
- Thiết kế tối giản, tinh tế, sử dụng hoàn toàn Native Streamlit Containers, không dùng HTML lồng dòng tránh lỗi hiển thị.
"""

import os
import sys
import streamlit as st

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from src.orchestrator import DiabetesMASOrchestrator
from src.core.state_schema import DiabetesMASState
from src.knowledge.neo4j_kg_service import neo4j_service
from src.knowledge.neo4j_graph_rag import graph_rag

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="DiaAgent Demo - Hệ Thống Trợ Lý Tư Vấn Đái Tháo Đường",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS giao diện tinh gọn, chuyên nghiệp
st.markdown("""
<style>
    header[data-testid="stHeader"] { height: 3rem; }
    .block-container {
        padding-top: 4.5rem !important;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1400px;
    }
    .app-header {
        border-bottom: 2px solid #0F172A;
        padding-top: 6px;
        padding-bottom: 12px;
        margin-bottom: 20px;
    }
    .app-title {
        font-size: 1.65rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0;
        letter-spacing: -0.3px;
    }
    .app-subtitle {
        font-size: 0.92rem;
        color: #475569;
        margin-top: 4px;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0F172A;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 6px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_orchestrator():
    return DiabetesMASOrchestrator()


orchestrator = get_orchestrator()

# Khởi tạo trạng thái hội thoại và trạng thái phân tích trong Session State
if "has_analyzed" not in st.session_state:
    st.session_state.has_analyzed = False

if "mas_state" not in st.session_state:
    st.session_state.mas_state = DiabetesMASState()

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = [
        {
            "role": "assistant",
            "content": (
                "Chào bạn, tôi là Trợ lý Sức khỏe DiaAgent. Bạn có thể nhập tình trạng sức khỏe, "
                "thể trạng (chiều cao, cân nặng), triệu chứng hoặc kết quả xét nghiệm vào ô bên dưới, "
                "sau đó nhấn 'Tiến hành Phân tích & Tư vấn' để nhận đánh giá y tế."
            )
        }
    ]


def execute_analysis(query_text: str):
    """Hàm xử lý phân tích dữ liệu qua orchestrator và kích hoạt hiển thị kết quả."""
    st.session_state.chat_messages.append({"role": "user", "content": query_text})
    with st.spinner("Đang kết nối Trợ lý DiaAgent..."):
        reply, updated_state = orchestrator.chat_turn(query_text, st.session_state.mas_state)
        st.session_state.chat_messages.append({"role": "assistant", "content": reply})
        st.session_state.mas_state = updated_state
        # Chỉ bật trạng thái đã phân tích lâm sàng nếu không phải lời chào xã giao
        if updated_state.metadata.get("last_intent") != "GREETING":
            st.session_state.has_analyzed = True
    st.rerun()


# Header ứng dụng chính thức
st.markdown("""
<div class="app-header">
    <div class="app-title">HỆ THỐNG TRỢ LÝ TƯ VẤN ĐÁI THÁO ĐƯỜNG (DiaAgent Demo)</div>
    <div class="app-subtitle">Tư vấn thông minh qua hội thoại: Sàng lọc nguy cơ lâm sàng, cá nhân hóa chế độ dinh dưỡng và tra cứu dược phẩm chính hãng</div>
</div>
""", unsafe_allow_html=True)

# Bố cục 2 cột cân đối: Cột 1 là Khung Hội Thoại & Nhập liệu, Cột 2 là Hồ Sơ Sức Khỏe & Kết Quả Chi Tiết
col_chat, col_summary = st.columns([1.1, 1.25], gap="large")

# -----------------------------------------------------------------------------
# CỘT 1: KHUNG HỘI THOẠI & ĐIỀU KHIỂN PHÂN TÍCH (CONVERSATION HUB)
# -----------------------------------------------------------------------------
with col_chat:
    st.markdown('<div class="section-title">1. Cuộc trò chuyện tư vấn trực tuyến</div>', unsafe_allow_html=True)

    # Nút chọn ca thử nghiệm mẫu và nút làm mới phiên tư vấn
    st.write("**Chọn ca mẫu để phân tích nhanh:**")
    q_col1, q_col2, q_col3 = st.columns([1, 1, 0.5])
    with q_col1:
        if st.button("Ca 1: Có triệu chứng (Chưa xét nghiệm)", use_container_width=True):
            st.session_state.mas_state = DiabetesMASState()
            sample_1 = "Tôi năm nay 55 tuổi, cao 1m65, nặng 74kg, dạo này hay khát nước liên tục, đêm đi tiểu 3 lần, người sụt 2kg. Tôi có bị tiểu đường không?"
            execute_analysis(sample_1)

    with q_col2:
        if st.button("Ca 2: Đã có xét nghiệm (HbA1c 7.8%)", use_container_width=True):
            st.session_state.mas_state = DiabetesMASState()
            sample_2 = "Tôi 55 tuổi, cao 1m65, nặng 74kg, vừa có kết quả xét nghiệm máu: đường huyết lúc đói 155 mg/dL và chỉ số HbA1c 7.8%. Xin tư vấn phác đồ và thuốc."
            execute_analysis(sample_2)

    with q_col3:
        if st.button("Làm mới", use_container_width=True):
            st.session_state.mas_state = DiabetesMASState()
            st.session_state.has_analyzed = False
            st.session_state.chat_messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Chào bạn, tôi là Trợ lý Sức khỏe DiaAgent. Bạn có thể nhập tình trạng sức khỏe, "
                        "thể trạng (chiều cao, cân nặng), triệu chứng hoặc kết quả xét nghiệm vào ô bên dưới "
                        "để nhận đánh giá y tế."
                    )
                }
            ]
            st.rerun()

    # Khung hiển thị cuộc trò chuyện trực tuyến
    chat_box = st.container(height=480)
    with chat_box:
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

    # DUY NHẤT 1 Ô NHẬP LIỆU CHUẨN CHATBOT (Không dùng text_area trùng lặp)
    chat_input_val = st.chat_input("Nhập thể trạng (chiều cao, cân nặng), triệu chứng hoặc kết quả xét nghiệm...")
    if chat_input_val and chat_input_val.strip():
        execute_analysis(chat_input_val.strip())

# -----------------------------------------------------------------------------
# CỘT 2: HỒ SƠ SỨC KHỎE TỔNG HỢP & PHÁC ĐỒ HÀNH ĐỘNG
# -----------------------------------------------------------------------------
with col_summary:
    st.markdown('<div class="section-title">2. Hồ sơ đánh giá sức khỏe & Khuyến nghị hành động</div>', unsafe_allow_html=True)

    # NẾU CHƯA NHẤN PHÂN TÍCH: Hiển thị màn hình chờ, TUYỆT ĐỐI không chạy phân tích trước
    if not st.session_state.has_analyzed:
        with st.container(border=True):
            st.markdown("### Trạng thái: Chờ thông tin phân tích")
            st.write(
                "Hệ thống hiện tại đang ở trạng thái sẵn sàng và chưa thực hiện lượt phân tích nào. "
                "Kết quả đánh giá nguy cơ, phác đồ điều trị và danh mục sản phẩm sẽ hiển thị tại đây sau khi bạn nhấn phân tích."
            )
            st.markdown(
                "**Hướng dẫn bắt đầu:**\n"
                "- Bấm chọn một trong hai **Ca thử nghiệm mẫu** ở cột bên trái để xem nhanh luồng xử lý.\n"
                "- Hoặc tự nhập mô tả tình trạng sức khỏe (chiều cao, cân nặng, triệu chứng hoặc xét nghiệm) "
                "rồi nhấn nút **Tiến hành Phân tích & Tư vấn**."
            )
    else:
        # NẾU ĐÃ NHẤN PHÂN TÍCH: Hiển thị đầy đủ thông tin chuyên môn
        state = st.session_state.mas_state
        p = state.patient_profile
        ml = state.ml_prediction
        rx = state.clinical_prescription
        nutri = state.nutrition_recommendation
        life = state.lifestyle_recommendation
        safety = state.safety_check

        is_sufficient = (p.data_completeness == "SUFFICIENT_LABS")
        status_label = "Đã có xét nghiệm xác định" if is_sufficient else "Giai đoạn sàng lọc nguy cơ (Chưa có xét nghiệm)"
        status_bg = "#E0F2FE" if is_sufficient else "#FEF3C7"
        status_color = "#0284C7" if is_sufficient else "#B45309"

        # 1. Thẻ Nhận định / Phân tầng nguy cơ (Native Streamlit Container, không rò rỉ mã HTML)
        with st.container(border=True):
            st.markdown(
                f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">'
                f'<span style="font-size:1.15rem; font-weight:700; color:#0F172A;">{rx.diagnosis}</span>'
                f'<span style="font-size:0.78rem; font-weight:600; color:{status_color}; background:{status_bg}; padding:3px 8px; border-radius:4px;">{status_label}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            c_met1, c_met2, c_met3 = st.columns(3)
            with c_met1:
                st.caption("Mức độ nguy cơ")
                st.markdown(f"**{ml.risk_tier}**")
            with c_met2:
                if is_sufficient:
                    st.caption("Xác suất dự báo ML (LightGBM)")
                    if ml.risk_probability is not None:
                        st.markdown(f"**{ml.risk_probability*100:.1f}%**")
                    else:
                        st.markdown("*Chưa xác định*")
                else:
                    st.caption("Mô hình Machine Learning")
                    st.markdown("**Không kích hoạt** *(Chưa có xét nghiệm máu)*")
            with c_met3:
                st.caption("Thể trạng BMI tự tính")
                if p.bmi:
                    st.markdown(f"**{p.bmi} kg/m²**")
                else:
                    st.markdown("*Chưa rõ chiều cao/cân nặng*")

            st.divider()

            if rx.primary_drug:
                st.markdown(f"**Thuốc khuyến nghị ban đầu:** `{rx.primary_drug}` ({rx.primary_dose})")
            else:
                st.warning("**Hướng dẫn điều trị:** Chưa chỉ định thuốc điều trị. Bệnh nhân cần đến cơ sở y tế làm xét nghiệm máu để có chẩn đoán xác định.")

            if rx.clinical_rationale:
                st.caption(f"Căn cứ lâm sàng: {rx.clinical_rationale}")

        # 2. Danh mục sản phẩm tham khảo tại FPT Long Châu
        if is_sufficient and rx.has_confirmed_diabetes:
            st.write(f"**Dược phẩm theo phác đồ tại FPT Long Châu** (Dự toán: ~{state.total_monthly_pharmacy_cost_vnd:,} VNĐ/tháng):")
        else:
            st.write("**Thiết bị y tế theo dõi cá nhân tại FPT Long Châu** (Tự theo dõi tại nhà):")

        for item in state.pharmacy_items:
            with st.container(border=True):
                p_c1, p_c2 = st.columns([3, 1])
                with p_c1:
                    st.markdown(f"**{item.brand_name}**")
                    rx_badge = "Thuốc kê đơn (Rx)" if item.is_prescription_rx else "Không kê đơn / Thiết bị"
                    badge_style = "color:#991B1B; background:#FEE2E2;" if item.is_prescription_rx else "color:#166534; background:#DCFCE7;"
                    st.markdown(
                        f"<span style='font-size:0.75rem; font-weight:600; padding:2px 6px; border-radius:4px; {badge_style}'>{rx_badge}</span> · Hoạt chất: *{item.active_ingredient}*",
                        unsafe_allow_html=True
                    )
                    st.caption(item.indication)
                with p_c2:
                    st.markdown(f"**{item.box_price_vnd:,} VNĐ**")
                    if item.monthly_cost_vnd > 0:
                        st.caption(f"~{item.monthly_cost_vnd:,} đ/tháng")
                    st.markdown(f"[Xem tại Long Châu ↗]({item.longchau_url})")

        # 3. Chế độ dinh dưỡng và lối sống
        with st.expander("Chế độ ăn uống (NIN) và vận động thể lực", expanded=False):
            st.write(f"- **Nhu cầu năng lượng:** ~{nutri.daily_calories} kcal/ngày (Nguyên tắc đĩa thức ăn: 1/2 rau xanh, 1/4 đạm nạc, 1/4 tinh bột chậm)")
            st.write(f"- **Bữa sáng:** {nutri.breakfast}")
            st.write(f"- **Bữa trưa:** {nutri.lunch}")
            st.write(f"- **Bữa tối:** {nutri.dinner}")
            st.write("**Gợi ý thay đổi món ăn:**")
            for s in nutri.healthy_swaps[:2]:
                st.write(f"  • Hạn chế: **{s['avoid']}** ➔ Thay bằng: **{s['swap_to']}**")
            st.write(f"- **Vận động thể chất:** {life.fitt_aerobic}")
            st.caption(f"Lưu ý an toàn: {life.hypoglycemia_protocol}")

# Khu vực thông tin kỹ thuật phục vụ báo cáo / kiểm chứng
st.markdown("---")
with st.expander("Thông tin kỹ thuật hệ thống (Mô hình học máy và rà soát dược lý ngầm)", expanded=False):
    if not st.session_state.has_analyzed:
        st.info("Chưa có lượt phân tích nào được thực thi. Sau khi bạn gửi yêu cầu phân tích, toàn bộ thông số mô hình ML, đóng góp SHAP và nhật ký phản biện đa Agent sẽ hiển thị tại đây.")
    else:
        state = st.session_state.mas_state
        p = state.patient_profile
        ml = state.ml_prediction
        safety = state.safety_check

        t_c1, t_c2 = st.columns(2)
        with t_c1:
            st.write(f"**Chế độ đánh giá:** {ml.mode}")
            st.write(f"**Công cụ áp dụng:** {ml.model_name}")
            st.write(f"**Mức độ dữ liệu đầu vào:** {p.data_completeness}")
            if not is_sufficient:
                st.info("Mô hình Machine Learning (LightGBM 13 đặc trưng) **không được kích hoạt** do người bệnh chưa có kết quả xét nghiệm sinh hóa máu (HbA1c/FPG). Hệ thống chỉ sử dụng bảng điểm sàng lọc lâm sàng không xâm lấn.")
            elif ml.top_shap_features:
                st.write("**Đóng góp yếu tố lâm sàng (SHAP):**")
                for f in ml.top_shap_features:
                    st.write(f"- {f['feature']} ({f['value']}): {f['impact']}")
        with t_c2:
            st.write(f"**Kiểm tra an toàn (Knowledge Graph):** {'ĐẠT' if safety.passed else 'CÓ VI PHẠM'}")
            st.write(f"**Số vòng lặp phản biện sửa đổi (Reflection):** {safety.revision_iteration}")
            st.write(f"**Căn cứ pháp lý:** Quyết định 5481/QĐ-BYT Bộ Y Tế & ADA 2024")
            st.write("**Nhật ký điều phối các Agent:**")
            for log in state.agent_execution_logs[-5:]:
                st.text(f"[{log.get('agent')}] {log.get('message')}")

    # Sơ đồ Embedding Đồ thị Tri thức (Node & Link Embeddings) - Hiển thị to rõ
    kg_emb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "knowledge_graph_node_embeddings.png")
    if os.path.exists(kg_emb_path):
        st.markdown("---")
        st.markdown("#### 🗺️ Sơ đồ Không gian Embedding Đồ thị Tri thức Mở rộng (Node & Link Embeddings)")
        st.caption("Biểu diễn trực quan không gian tiềm ẩn (Latent Embedding Space) 2D của **143 Node thực thể** và **271 Mối quan hệ liên kết lâm sàng** chuẩn hóa trong Đồ thị Tri thức Neo4j DiaAgent-MAS. Các thực thể cùng nhóm ngữ nghĩa tự động co cụm chặt chẽ (Dược chất & Biệt dược FPT Long Châu, Triệu chứng lâm sàng, Chỉ số xét nghiệm, Dinh dưỡng NIN, Biến chứng & Chống chỉ định).")
        st.image(kg_emb_path, caption="Không gian Vector Embedding 2D (Force-Directed Graph Layout & Semantic Priors) biểu diễn 143 Node và 271 Mối quan hệ trong Đồ thị Tri thức Neo4j", use_container_width=True)

    # 4. Cơ sở Dữ liệu Đồ thị Neo4j (Knowledge Graph Neo4j & GraphRAG link_DB)
    st.markdown("---")
    st.markdown("#### 🗄️ Cơ sở Dữ liệu Đồ thị Neo4j & GraphRAG (code RAG + link_DB)")
    
    neo_stats = neo4j_service.get_graph_stats()
    n_col1, n_col2 = st.columns([1, 1])
    with n_col1:
        if neo_stats.get("connected"):
            st.success(f"🟢 **Neo4j Database:** ĐÃ KẾT NỐI (`bolt://localhost:7687`)")
            st.write(f"- **Quy mô đồ thị trong DB:** **{neo_stats.get('nodes', 0)} Nodes** | **{neo_stats.get('relationships', 0)} Relationships**")
            st.write(f"- **Nhãn thực thể (12 Labels):** `{', '.join(neo_stats.get('labels', []))}`")
            st.markdown(f"👉 **Giao diện Neo4j Browser:** [Mở Neo4j Web UI (http://localhost:7474)](http://localhost:7474) *(Tài khoản: `neo4j` / Mật khẩu: `password123`)*")
            st.info("💡 **Mẹo xem toàn bộ đồ thị không bị giới hạn 25 node:** Trong Neo4j Browser, gõ câu lệnh sau vào thanh truy vấn rồi bấm nút **Run** (hoặc Ctrl+Enter):")
            st.code("MATCH (n)-[r]->(m) RETURN n, r, m", language="cypher")
        else:
            st.warning("🟡 Neo4j Server đang ở chế độ dự phòng. Hệ thống tự động chuyển sang In-memory Graph NetworkX.")
            st.caption("Bạn có thể khởi chạy Neo4j bằng lệnh: `docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password123 neo4j:5-community`")

    with n_col2:
        st.write("**Nguồn dữ liệu số hóa vào KB Đồ thị:**")
        st.write("1. 📄 **Tài liệu PDF:** Quyết định 5481/QĐ-BYT Bộ Y Tế (77 trang)")
        st.write("2. 🌐 **Web Y khoa:** Chuyên đề Đái tháo đường & Bàn chân Bệnh viện Vinmec")
        st.write("3. 💊 **Thương mại:** Dược phẩm FPT Long Châu & Dinh dưỡng Viện NIN")
        st.write("4. 🌍 **Chuẩn quốc tế:** Khuyến cáo ADA 2024 Standards of Care")
        st.write("**Ví dụ các câu lệnh Cypher khám phá:**")
        st.code("""// Xem cụm thuốc và sản phẩm Long Châu
MATCH (dr:Drug)-[r:DISPENSED_AS_PRODUCT]->(p:PharmacyProduct)
RETURN dr, r, p LIMIT 20

// Xem các cảnh báo chống chỉ định & nguy cơ
MATCH (dr:Drug)-[r:CONTRAINDICATED_IN|RISK_OF]->(target)
RETURN dr, r, target""", language="cypher")
