// ==========================================================
// KB_DIABET NEO4J KNOWLEDGE GRAPH INITIALIZATION SCRIPT (EXPANDED)
// Toàn diện 143 Nodes, 280+ Relationships chuẩn hóa
// Tích hợp: QĐ 5481/QĐ-BYT, Vinmec Clinical, NIN, ADA 2024 & FPT Long Châu
// ==========================================================

MERGE (:Source {id: 'SRC_BYT_5481', name: 'QĐ 5481/QĐ-BYT Bộ Y Tế (30/12/2020)', type: 'PDF_GUIDELINE', scope: 'Chuẩn quốc gia Việt Nam'});
MERGE (:Source {id: 'SRC_VINMEC', name: 'Hướng dẫn Lâm sàng Nội tiết Bệnh viện Vinmec', type: 'WEB_CLINICAL', scope: 'Chẩn đoán và biến chứng lâm sàng'});
MERGE (:Source {id: 'SRC_NIN', name: 'Bảng thành phần thực phẩm Viện Dinh Dưỡng Quốc Gia (NIN)', type: 'NUTRITION_TABLE', scope: 'Dinh dưỡng lâm sàng & Chỉ số GI/GL'});
MERGE (:Source {id: 'SRC_ADA_2024', name: 'Standards of Care in Diabetes - ADA 2024', type: 'INT_GUIDELINE', scope: 'Khuyến cáo tim thận quốc tế'});
MERGE (:Source {id: 'SRC_LONGCHAU', name: 'Hệ thống Nhà thuốc FPT Long Châu', type: 'PHARMACY_ECOMMERCE', scope: 'Danh mục thuốc thương mại & Thiết bị y tế'});
MERGE (:Disease {id: 'T2D', name: 'Đái tháo đường Type 2', icd10: 'E11', desc: 'Rối loạn chuyển hóa glucose mạn tính đặc trưng bởi sự đề kháng insulin và suy giảm tiết insulin tiến triển'});
MERGE (:Disease {id: 'PRE_DIABETES', name: 'Tiền đái tháo đường', icd10: 'R73.0', desc: 'Rối loạn đường huyết lúc đói (IFG) hoặc rối loạn dung nạp glucose (IGT), nguy cơ cao tiến triển T2D'});
MERGE (:Disease {id: 'T1D', name: 'Đái tháo đường Type 1', icd10: 'E10', desc: 'Phá hủy tế bào beta tụy qua trung gian tự miễn, dẫn đến thiếu hụt insulin tuyệt đối'});
MERGE (:Disease {id: 'GESTATIONAL_DIABETES', name: 'Đái tháo đường thai kỳ', icd10: 'O24.4', desc: 'Tình trạng rối loạn dung nạp đường huyết được phát hiện lần đầu trong thai kỳ'});
MERGE (:Disease {id: 'METABOLIC_SYNDROME', name: 'Hội chứng chuyển hóa', icd10: 'E88.81', desc: 'Tập hợp các yếu tố nguy cơ bao gồm béo phì trung tâm, tăng huyết áp, tăng triglycerid và giảm HDL-C'});
MERGE (:Symptom {id: 'SYM_POLYURIA', name: 'Đi tiểu nhiều lần (Polyuria)', category: 'Hội chứng 4 nhiều', desc: 'Thận tăng bài tiết nước tiểu để đào thải nồng độ glucose dư thừa qua ngưỡng lọc'});
MERGE (:Symptom {id: 'SYM_POLYDIPSIA', name: 'Thường xuyên khát nước (Polydipsia)', category: 'Hội chứng 4 nhiều', desc: 'Cơ thể kích hoạt trung tâm khát ở não do mất nước thẩm thấu'});
MERGE (:Symptom {id: 'SYM_POLYPHAGIA', name: 'Ăn nhiều / Nhanh đói (Polyphagia)', category: 'Hội chứng 4 nhiều', desc: 'Tế bào thiếu năng lượng do glucose không vào được bên trong tế bào'});
MERGE (:Symptom {id: 'SYM_WEIGHT_LOSS', name: 'Sụt cân bất thường (Weight Loss)', category: 'Hội chứng 4 nhiều', desc: 'Dị hóa lipid và protein cơ bắp để cung cấp năng lượng thay thế cho glucose'});
MERGE (:Symptom {id: 'SYM_FATIGUE', name: 'Mệt mỏi kéo dài (Fatigue)', category: 'Triệu chứng toàn thân', desc: 'Tế bào suy giảm chuyển hóa năng lượng ATP'});
MERGE (:Symptom {id: 'SYM_BLURRED_VISION', name: 'Nhìn mờ tạm thời (Blurred Vision)', category: 'Triệu chứng thị giác', desc: 'Tăng áp lực thẩm thấu làm thay đổi thể tích nước và hình dạng thủy tinh thể'});
MERGE (:Symptom {id: 'SYM_NUMBNESS', name: 'Tê bì, dị cảm châm chích bàn chân (Paresthesia)', category: 'Thần kinh ngoại biên', desc: 'Tổn thương sớm bao myelin và các sợi thần kinh cảm giác ngoại vi'});
MERGE (:Symptom {id: 'SYM_SLOW_HEALING', name: 'Vết thương chậm lành (Slow Wound Healing)', category: 'Tổn thương vi mạch', desc: 'Lưu thông máu kém và suy giảm chức năng thực bào của bạch cầu'});
MERGE (:Symptom {id: 'SYM_DRY_MOUTH', name: 'Khô miệng họng (Dry Mouth)', category: 'Mất nước', desc: 'Giảm bài tiết tuyến nước bọt do mất nước mạn tính'});
MERGE (:Symptom {id: 'SYM_RECURRENT_INFECTION', name: 'Nhiễm trùng nấm tái phát (Recurrent Infections)', category: 'Miễn dịch', desc: 'Môi trường đường huyết cao tạo điều kiện thuận lợi cho nấm Candida và vi khuẩn phát triển'});
MERGE (:Biomarker {id: 'HBA1C', name: 'Chỉ số HbA1c (Hemoglobin A1c)', unit: '%', normal: '< 5.7', prediabetic: '5.7 - 6.4', diabetic: '>= 6.5', target: '< 7.0'});
MERGE (:Biomarker {id: 'FPG', name: 'Glucose huyết tương lúc đói (FPG)', unit: 'mg/dL', normal: '70 - 99', prediabetic: '100 - 125', diabetic: '>= 126', target: '80 - 130'});
MERGE (:Biomarker {id: 'OGTT_2H', name: 'Nghiệm pháp dung nạp glucose đường uống 2h (OGTT 75g)', unit: 'mg/dL', normal: '< 140', prediabetic: '140 - 199', diabetic: '>= 200', target: '< 140'});
MERGE (:Biomarker {id: 'RPG', name: 'Glucose huyết tương bất kỳ (RPG)', unit: 'mg/dL', normal: '< 140', prediabetic: '140 - 199', diabetic: '>= 200', target: '< 180'});
MERGE (:Biomarker {id: 'EGFR', name: 'Độ lọc cầu thận ước tính (eGFR CKD-EPI)', unit: 'mL/min/1.73m2', normal: '>= 90', prediabetic: '60 - 89', diabetic: '< 60', target: '>= 60'});
MERGE (:Biomarker {id: 'CREATININE', name: 'Creatinine huyết thanh', unit: 'mg/dL', normal: '0.7 - 1.2', prediabetic: '1.3 - 1.5', diabetic: '>= 1.5', target: '< 1.2'});
MERGE (:Biomarker {id: 'UACR', name: 'Tỷ số Albumin / Creatinine niệu (UACR)', unit: 'mg/g', normal: '< 30', prediabetic: '30 - 299', diabetic: '>= 300', target: '< 30'});
MERGE (:Biomarker {id: 'BMI', name: 'Chỉ số khối cơ thể (BMI)', unit: 'kg/m2', normal: '18.5 - 22.9', prediabetic: '23.0 - 24.9', diabetic: '>= 25.0', target: '18.5 - 22.9'});
MERGE (:Biomarker {id: 'WAIST', name: 'Chu vi vòng eo', unit: 'cm', normal: '< 90 (Nam) / < 80 (Nữ)', prediabetic: '90 (Nam) / 80 (Nữ)', diabetic: '>= 90 (Nam) / >= 80 (Nữ)', target: '< 90 / < 80'});
MERGE (:Biomarker {id: 'BP_SYS', name: 'Huyết áp tâm thu', unit: 'mmHg', normal: '< 120', prediabetic: '120 - 129', diabetic: '>= 130', target: '< 130'});
MERGE (:Biomarker {id: 'BP_DIA', name: 'Huyết áp tâm trương', unit: 'mmHg', normal: '< 80', prediabetic: '80 - 84', diabetic: '>= 85', target: '< 80'});
MERGE (:Biomarker {id: 'LIPID_LDL', name: 'Cholesterol LDL-C (Xấu)', unit: 'mg/dL', normal: '< 100', prediabetic: '100 - 129', diabetic: '>= 130', target: '< 70'});
MERGE (:Biomarker {id: 'LIPID_HDL', name: 'Cholesterol HDL-C (Tốt)', unit: 'mg/dL', normal: '> 50', prediabetic: '40 - 50', diabetic: '< 40', target: '> 40 (Nam) / > 50 (Nữ)'});
MERGE (:Biomarker {id: 'LIPID_TRIGLYCERIDE', name: 'Triglyceride huyết thanh', unit: 'mg/dL', normal: '< 150', prediabetic: '150 - 199', diabetic: '>= 200', target: '< 150'});
MERGE (:Complication {id: 'CKD', name: 'Bệnh thận mạn do đái tháo đường (Diabetic Kidney Disease)', icd10: 'N18', risk: 'Xơ hóa cầu thận tiến triển dẫn đến suy thận giai đoạn cuối'});
MERGE (:Complication {id: 'ASCVD', name: 'Bệnh lý tim mạch do xơ vữa (ASCVD)', icd10: 'I25', risk: 'Nhồi máu cơ tim cấp, đột quỵ thiếu máu cục bộ não'});
MERGE (:Complication {id: 'HEART_FAILURE', name: 'Suy tim sung huyết (Heart Failure - HFrEF/HFpEF)', icd10: 'I50', risk: 'Khó thở khi gắng sức, phù phổi, giảm phân suất tống máu'});
MERGE (:Complication {id: 'DIABETIC_RETINOPATHY', name: 'Bệnh võng mạc đái tháo đường', icd10: 'E11.3', risk: 'Xuất huyết dịch kính, bong võng mạc, nguy cơ mù lòa vĩnh viễn'});
MERGE (:Complication {id: 'DIABETIC_NEUROPATHY', name: 'Bệnh thần kinh ngoại biên đái tháo đường', icd10: 'E11.4', risk: 'Mất cảm giác bảo vệ đau nhiệt, dị cảm đối xứng kiểu mang bít tất'});
MERGE (:Complication {id: 'DIABETIC_FOOT_ULCER', name: 'Loét bàn chân đái tháo đường (Diabetic Foot Ulcer)', icd10: 'E11.7', risk: 'Hoại tử mô sâu nhiễm khuẩn kết hợp bệnh mạch máu ngoại biên, nguy cơ cắt cụt chi'});
MERGE (:Complication {id: 'PAD', name: 'Bệnh động mạch ngoại biên chi dưới (PAD)', icd10: 'I73.9', risk: 'Đau cách hồi, thiếu máu nuôi dưỡng bàn chân'});
MERGE (:Complication {id: 'DIABETIC_GASTROPARESIS', name: 'Liệt dạ dày do đái tháo đường', icd10: 'K31.84', risk: 'Chậm làm rỗng dạ dày, buồn nôn, chướng bụng, đường huyết dao động khó lường'});
MERGE (:Comorbidity {id: 'HYPERTENSION', name: 'Tăng huyết áp đồng mắc', icd10: 'I10', target: '< 130/80 mmHg'});
MERGE (:Comorbidity {id: 'DYSLIPIDEMIA', name: 'Rối loạn lipid máu hỗn hợp', icd10: 'E78', target: 'LDL-C < 70 mg/dL'});
MERGE (:Comorbidity {id: 'NAFLD', name: 'Gan nhiễm mỡ liên quan rối loạn chuyển hóa (MASLD/NAFLD)', icd10: 'K76.0', target: 'Kiểm soát cân nặng và enzyme men gan ALT/AST'});
MERGE (:RiskFactor {id: 'OBESITY', name: 'Béo phì / Thừa cân theo chuẩn IDI & WPRO', threshold: 'BMI >= 23.0 kg/m2'});
MERGE (:RiskFactor {id: 'FAMILY_HISTORY', name: 'Tiền sử gia đình trực hệ mắc đái tháo đường', threshold: 'Bố mẹ hoặc anh chị em ruột mắc T2D'});
MERGE (:RiskFactor {id: 'SMOKING', name: 'Hút thuốc lá chủ động / thụ động', threshold: 'Làm tổn thương nặng thêm nội mô mạch máu'});
MERGE (:RiskFactor {id: 'PHYSICAL_INACTIVITY', name: 'Lối sống tĩnh tại ít vận động thể lực', threshold: '< 150 phút hoạt động thể lực mỗi tuần'});
MERGE (:AdverseEffect {id: 'LACTIC_ACIDOSIS', name: 'Nhiễm toan Acid Lactic cấp tính', severity: 'FATAL', mortality: '50%', detail: 'Cồn rượu bia / Suy thận nặng eGFR < 30 mL/phút'});
MERGE (:AdverseEffect {id: 'HYPOGLYCEMIA_MILD', name: 'Hạ đường huyết mức độ nhẹ - trung bình (< 70 mg/dL)', severity: 'MODERATE', mortality: '0.1%', detail: 'Quy tắc 15-15 bổ sung 15g đường nhanh'});
MERGE (:AdverseEffect {id: 'HYPOGLYCEMIA_SEVERE', name: 'Hạ đường huyết mức độ nặng', severity: 'SEVERE', mortality: '5%', detail: 'Cần người khác trợ giúp, co giật hoặc hôn mê sâu'});
MERGE (:AdverseEffect {id: 'DKA', name: 'Nhiễm toan Ceton đái tháo đường (Diabetic Ketoacidosis)', severity: 'CRITICAL', mortality: '5-10%', detail: 'Thở nhanh sâu Kussmaul, mùi hơi thở táo thối ceton'});
MERGE (:AdverseEffect {id: 'EUG_DKA', name: 'Nhiễm toan Ceton đường huyết bình thường (Euglycemic DKA)', severity: 'HIGH', mortality: '2-5%', detail: 'Tác dụng không mong muốn của thuốc SGLT2i khi thiếu insulin'});
MERGE (:AdverseEffect {id: 'HHS', name: 'Hội chứng tăng áp lực thẩm thấu do tăng đường huyết', severity: 'CRITICAL', mortality: '10-20%', detail: 'Đường huyết > 600 mg/dL, áp lực thẩm thấu máu > 320 mOsm/kg'});
MERGE (:AdverseEffect {id: 'UTI', name: 'Nhiễm khuẩn đường tiết niệu & nấm sinh dục', severity: 'MODERATE', mortality: '< 0.01%', detail: 'Tăng nồng độ đường trong nước tiểu nuôi dưỡng vi khuẩn'});
MERGE (:AdverseEffect {id: 'GI_UPSET', name: 'Rối loạn tiêu hóa (Buồn nôn, tiêu chảy, đầy bụng)', severity: 'MILD', mortality: '0%', detail: 'Thường gặp khi bắt đầu dùng Metformin hoặc GLP-1 RA'});
MERGE (:AdverseEffect {id: 'WEIGHT_GAIN', name: 'Tăng cân ngoài ý muốn', severity: 'MILD_MODERATE', mortality: '0%', detail: 'Tác dụng đồng hóa của Sulfonylurea hoặc Insulin'});
MERGE (:AdverseEffect {id: 'PERIPHERAL_EDEMA', name: 'Phù ngoại biên (Giữ nước)', severity: 'MODERATE', mortality: '0%', detail: 'Tăng giữ muối nước do cơ chế Thiazolidinediones'});
MERGE (:AdverseEffect {id: 'FOURNIER_GANGRENE', name: 'Hoại thư sinh dục hoại tử Fournier', severity: 'RARE_FATAL', mortality: '20-30%', detail: 'Cảnh báo FDA và Bộ Y Tế cho nhóm thuốc SGLT2i'});
MERGE (:AdverseEffect {id: 'PANCREATITIS_ACUTE', name: 'Viêm tụy cấp', severity: 'SEVERE', mortality: '5%', detail: 'Cảnh báo thận trọng hiếm gặp của DPP-4i hoặc GLP-1 RA'});
MERGE (:Drug {id: 'METFORMIN', name: 'Metformin Hydrochloride', class: 'Biguanide', line: 'First-line (Thuốc đầu tay bắt buộc nếu không chống chỉ định)'});
MERGE (:Drug {id: 'GLICLAZIDE', name: 'Gliclazide MR', class: 'Sulfonylurea thế hệ 2', line: 'Add-on kích thích tiết insulin'});
MERGE (:Drug {id: 'GLIMEPIRIDE', name: 'Glimepiride', class: 'Sulfonylurea thế hệ 3', line: 'Add-on kích thích tiết insulin 1 lần/ngày'});
MERGE (:Drug {id: 'GLIBENCLAMIDE', name: 'Glibenclamide', class: 'Sulfonylurea thế hệ 2 cũ', line: 'Hạn chế dùng do nguy cơ hạ đường huyết kéo dài'});
MERGE (:Drug {id: 'DAPAGLIFLOZIN', name: 'Dapagliflozin', class: 'SGLT-2 Inhibitor', line: 'Bảo vệ tim mạch & Làm chậm suy thận mạn'});
MERGE (:Drug {id: 'EMPAGLIFLOZIN', name: 'Empagliflozin', class: 'SGLT-2 Inhibitor', line: 'Giảm tử vong tim mạch & Bảo vệ thận'});
MERGE (:Drug {id: 'CANAGLIFLOZIN', name: 'Canagliflozin', class: 'SGLT-2 Inhibitor', line: 'Bảo vệ tim thận & Giảm biến cố CKD'});
MERGE (:Drug {id: 'SITAGLIPTIN', name: 'Sitagliptin', class: 'DPP-4 Inhibitor', line: 'Add-on dung nạp tốt, an toàn ít hạ đường huyết'});
MERGE (:Drug {id: 'VILDAGLIPTIN', name: 'Vildagliptin', class: 'DPP-4 Inhibitor', line: 'Add-on tăng tiết insulin theo glucose máu'});
MERGE (:Drug {id: 'LINAGLIPTIN', name: 'Linagliptin', class: 'DPP-4 Inhibitor (Thải qua gan mật)', line: 'An toàn cho mọi mức độ suy thận không cần chỉnh liều'});
MERGE (:Drug {id: 'SAXAGLIPTIN', name: 'Saxagliptin', class: 'DPP-4 Inhibitor', line: 'Thận trọng tiền sử suy tim'});
MERGE (:Drug {id: 'SEMAGLUTIDE', name: 'Semaglutide', class: 'GLP-1 Receptor Agonist', line: 'Bảo vệ tim mạch vượt trội & Giảm cân mạnh'});
MERGE (:Drug {id: 'LIRAGLUTIDE', name: 'Liraglutide', class: 'GLP-1 Receptor Agonist', line: 'Bảo vệ tim mạch & Giảm biến cố xơ vữa'});
MERGE (:Drug {id: 'DULAGLUTIDE', name: 'Dulaglutide', class: 'GLP-1 Receptor Agonist', line: 'Tiêm 1 lần/tuần bảo vệ tim mạch'});
MERGE (:Drug {id: 'PIOGLITAZONE', name: 'Pioglitazone', class: 'Thiazolidinedione (TZD)', line: 'Tăng nhạy cảm insulin ngoại vi, giảm đề kháng gan'});
MERGE (:Drug {id: 'ACARBOSE', name: 'Acarbose', class: 'Alpha-glucosidase Inhibitor', line: 'Làm chậm hấp thu glucose tinh bột tại ruột non'});
MERGE (:Drug {id: 'INSULIN_GLARGINE', name: 'Insulin Glargine (Lantus / Toujeo)', class: 'Basal Insulin Analogue', line: 'Kiểm soát đường huyết nền 24h ổn định không đỉnh'});
MERGE (:Drug {id: 'INSULIN_ASPART', name: 'Insulin Aspart (NovoRapid)', class: 'Rapid-acting Insulin Analogue', line: 'Kiểm soát đường huyết đỉnh sau bữa ăn'});
MERGE (:Food {id: 'FOOD_COM_TRANG', name: 'Cơm trắng (Gạo tẻ)', gi: 83, category: 'Tinh bột nhanh', advice: 'Tăng vọt đường huyết sau ăn, cần hạn chế khẩu phần và ăn kèm nhiều rau xanh'});
MERGE (:Food {id: 'FOOD_XOI_NEP', name: 'Xôi nếp các loại', gi: 90, category: 'Tinh bột nếp cực nhanh', advice: 'Mật độ năng lượng và amylopectin rất cao, tránh ăn bữa sáng liên tục'});
MERGE (:Food {id: 'FOOD_BANH_MI_TRANG', name: 'Bánh mì trắng', gi: 85, category: 'Bột mì tinh luyện', advice: 'Hấp thu glucose nhanh chóng, không có chất xơ cám'});
MERGE (:Food {id: 'FOOD_BANH_CHUNG', name: 'Bánh chưng / Bánh tét', gi: 85, category: 'Nếp bão hòa mỡ', advice: 'Năng lượng cực cao kết hợp mỡ động vật thịt ba chỉ, hạn chế ngày lễ Tết'});
MERGE (:Food {id: 'FOOD_PHO_BO', name: 'Phở bò nước béo', gi: 72, category: 'Món nước nhiều dầu mỡ', advice: 'Bánh phở GI cao kết hợp nước dùng nhiều mỡ bão hòa và muối Natri'});
MERGE (:Food {id: 'FOOD_BUN_BO_HUE', name: 'Bún bò Huế nước béo', gi: 75, category: 'Món nước đậm vị', advice: 'Nhiều gia vị muối và mỡ bò, dễ tăng vọt đường huyết và huyết áp'});
MERGE (:Food {id: 'FOOD_BANH_CUON', name: 'Bánh cuốn chả quế', gi: 78, category: 'Bột gạo hấp', advice: 'Lượng tinh bột cao dễ gây no nhanh và tăng đường sau 1 giờ'});
MERGE (:Food {id: 'FOOD_BANH_MI_THIT', name: 'Bánh mì kẹp thịt pate', gi: 76, category: 'Thức ăn nhanh đường phố', advice: 'Bột mì tinh luyện kết hợp pate gan béo mỡ động vật'});
MERGE (:Food {id: 'FOOD_TRA_SUA', name: 'Trà sữa trân châu có đường', gi: 88, category: 'Đường lỏng fructose', advice: 'Cấm kỵ tuyệt đối: đường siro lỏng và bột béo công nghiệp chuyển hóa xấu'});
MERGE (:Food {id: 'FOOD_NUOC_NGOT', name: 'Nước ngọt có gas / Tăng lực', gi: 95, category: 'Đường đơn hấp thu tức thì', advice: 'Chỉ sử dụng 100-150ml khi cấp cứu hạ đường huyết nặng theo Quy tắc 15-15'});
MERGE (:Food {id: 'FOOD_CHE_NGOT', name: 'Chè ngọt nước cốt dừa', gi: 82, category: 'Đồ ngọt truyền thống', advice: 'Lượng đường tinh luyện và chất béo bão hòa từ dừa rất cao'});
MERGE (:Food {id: 'FOOD_DUA_HAU', name: 'Dưa hấu đỏ', gi: 76, category: 'Trái cây ngọt nhanh', advice: 'Chỉ số GI cao, chỉ nên ăn 1-2 miếng nhỏ sau bữa chính cách 2 tiếng'});
MERGE (:Food {id: 'FOOD_CHAO_LONG', name: 'Cháo lòng heo / Cháo hoa', gi: 80, category: 'Cháo ninh nhừ', advice: 'Tinh bột hồ hóa phân giải đường tức thì, nội tạng nhiều cholesterol'});
MERGE (:Food {id: 'FOOD_COM_GAO_LUC', name: 'Cơm gạo lứt (Đỏ/Đen)', gi: 55, category: 'Ngũ cốc nguyên cám', advice: 'Giàu chất xơ hòa tan beta-glucan và vitamin B, giúp đường huyết ổn định'});
MERGE (:Food {id: 'FOOD_KHOAI_LANG', name: 'Khoai lang luộc cả vỏ', gi: 48, category: 'Củ giàu chất xơ', advice: 'Lựa chọn tinh bột thay thế tuyệt vời cho bữa sáng, tạo cảm giác no lâu'});
MERGE (:Food {id: 'FOOD_BUN_MOC_RAU', name: 'Bún mọc nhiều rau xanh', gi: 50, category: 'Món nước thanh đạm', advice: 'Nước dùng trong ít béo, kèm nhiều rau sống xà lách, giá đỗ làm chậm hấp thu đường'});
MERGE (:Food {id: 'FOOD_BANH_MI_DEN', name: 'Bánh mì lúa mạch đen nguyên cám', gi: 48, category: 'Ngũ cốc nguyên hạt', advice: 'Hạn chế tăng đường huyết đỉnh sau ăn nhờ tỷ lệ xơ thô cao'});
MERGE (:Food {id: 'FOOD_YEN_MACH', name: 'Yến mạch nguyên hạt nấu', gi: 52, category: 'Ngũ cốc chất lượng cao', advice: 'Hạ mỡ máu LDL-C và kiểm soát đường huyết đói rất tốt'});
MERGE (:Food {id: 'FOOD_NGO_LUOC', name: 'Ngô (bắp) nếp luộc', gi: 52, category: 'Ngũ cốc thô', advice: 'Ăn 1/2 bắp cho bữa phụ giúp chống hạ đường huyết êm dịu'});
MERGE (:Food {id: 'FOOD_BONG_CAI_XANH', name: 'Bông cải xanh (Súp lơ) luộc', gi: 15, category: 'Rau họ cải', advice: 'Giàu sulforaphane chống viêm nội mô mạch máu và chất xơ tuyệt hảo'});
MERGE (:Food {id: 'FOOD_RAU_MUONG', name: 'Rau muống luộc / xào tỏi', gi: 10, category: 'Rau lá xanh Việt Nam', advice: 'Ăn một đĩa rau luộc trước bữa ăn chính để phủ một lớp màng chất xơ ở ruột'});
MERGE (:Food {id: 'FOOD_DAU_BAP', name: 'Đậu bắp hấp / luộc', gi: 20, category: 'Rau nhớt bảo vệ', advice: 'Chất nhầy tự nhiên làm chậm tốc độ tiêu hóa tinh bột tại tá tràng'});
MERGE (:Food {id: 'FOOD_KHO_QUA', name: 'Mướp đắng (Khổ qua) xào trứng / hấp', gi: 15, category: 'Rau dược liệu', advice: 'Chứa Charantin có tác dụng hỗ trợ hạ glucose tương tự insulin nội sinh'});
MERGE (:Food {id: 'FOOD_CA_HAP', name: 'Cá lóc / Cá hồi hấp hành gừng', gi: 0, category: 'Đạm lành mạnh Omega-3', advice: 'Không chứa carbohydrate, cung cấp đạm dễ tiêu và bảo vệ tim mạch'});
MERGE (:Food {id: 'FOOD_UC_GA', name: 'Ức gà hấp / áp chảo ít dầu', gi: 0, category: 'Đạm nạc chất lượng', advice: 'Cung cấp năng lượng duy trì cơ bắp cho người bệnh đái tháo đường'});
MERGE (:Food {id: 'FOOD_DAU_PHU', name: 'Đậu phụ luộc / hấp', gi: 15, category: 'Đạm thực vật', advice: 'Giàu Isoflavone, không chứa cholesterol xấu'});
MERGE (:Food {id: 'FOOD_BUOI', name: 'Bưởi da xanh / Năm roi', gi: 25, category: 'Trái cây múi giàu Vitamin C', advice: 'Ăn 2-3 múi mỗi ngày giúp tăng cường đề kháng mà không tăng đường'});
MERGE (:Food {id: 'FOOD_TAO_XANH', name: 'Táo xanh tươi cả vỏ', gi: 36, category: 'Trái cây giàu Pectin', advice: 'Chất xơ Pectin làm sạch đường ruột và ổn định chuyển hóa'});
MERGE (:Food {id: 'FOOD_TRA_XANH_MATCHA', name: 'Trà xanh nguyên chất / Ô long', gi: 0, category: 'Đồ uống chống oxy hóa', advice: 'Chứa hợp chất EGCG bảo vệ tế bào beta tụy và tăng độ nhạy insulin'});
MERGE (:ClinicalProtocol {id: 'PROTOCOL_FITT', name: 'Phác đồ vận động thể lực FITT chuẩn ADA & Bộ Y Tế', desc: '150 phút aerobic cường độ trung bình/tuần kết hợp 2-3 buổi tập kháng lực, không ngưng quá 2 ngày'});
MERGE (:ClinicalProtocol {id: 'PROTOCOL_RULE_15', name: 'Quy tắc cấp cứu 15-15 hạ đường huyết', desc: 'Bổ sung ngay 15g carbohydrate tác dụng nhanh (3 viên đường / 150ml nước ngọt), nghỉ ngơi và đo lại sau 15 phút'});
MERGE (:ClinicalProtocol {id: 'PROTOCOL_FOOT_CARE', name: 'Quy trình kiểm tra & chăm sóc bàn chân hằng ngày', desc: 'Rửa chân nước ấm, lau khô kỹ các kẽ ngón, quan sát vết nứt hoặc chai sần, mang tất đệm mềm, không đi chân đất'});
MERGE (:ClinicalProtocol {id: 'PROTOCOL_PLATE_METHOD', name: 'Mô hình đĩa thức ăn chuẩn NIN & Harvard', desc: '1/2 đĩa là rau củ quả không chứa tinh bột; 1/4 đĩa là protein nạc lành mạnh; 1/4 đĩa là tinh bột chuyển hóa chậm'});
MERGE (:ClinicalProtocol {id: 'PROTOCOL_SMBG', name: 'Quy trình tự theo dõi đường huyết mao mạch (SMBG)', desc: 'Đo đường huyết lúc đói sáng sớm, trước bữa ăn và 2 giờ sau ăn để theo dõi hiệu quả điều trị'});
MERGE (p:PharmacyProduct {id: 'lc_dia_01'})
            SET p.brand_name = 'Glucophage XR 500mg',
                p.active_ingredient = 'Metformin hydrochloride 500mg',
                p.drug_class = 'Biguanide (Thuốc hạ đường huyết đầu tay)',
                p.manufacturer = 'Merck Sante (Pháp)',
                p.packaging = 'Hộp 2 vỉ x 15 viên phóng thích kéo dài',
                p.box_price_vnd = 126000,
                p.unit_price_vnd = 4200,
                p.is_prescription_rx = true,
                p.indication = 'Điều trị đái tháo đường Type 2, giảm thiểu kích ứng tiêu hóa nhờ cơ chế phóng thích kéo dài XR',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/glucophage-xr-500mg-merck-h-30v-14249.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_02'})
            SET p.brand_name = 'Glucophage 850mg',
                p.active_ingredient = 'Metformin hydrochloride 850mg',
                p.drug_class = 'Biguanide',
                p.manufacturer = 'Merck Sante (Pháp)',
                p.packaging = 'Hộp 10 vỉ x 10 viên bao phim',
                p.box_price_vnd = 450000,
                p.unit_price_vnd = 4500,
                p.is_prescription_rx = true,
                p.indication = 'Điều trị đái tháo đường Type 2 đơn trị liệu hoặc phối hợp thuốc khác',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/glucophage-850mg-merck-h-100v-14248.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_03'})
            SET p.brand_name = 'Glucophage 1000mg',
                p.active_ingredient = 'Metformin hydrochloride 1000mg',
                p.drug_class = 'Biguanide',
                p.manufacturer = 'Merck Sante (Pháp)',
                p.packaging = 'Hộp 8 vỉ x 15 viên bao phim',
                p.box_price_vnd = 612000,
                p.unit_price_vnd = 5100,
                p.is_prescription_rx = true,
                p.indication = 'Duy trì kiểm soát đường huyết liều cao cho bệnh nhân dung nạp tốt',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/glucophage-1000mg-merck-14247.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_04'})
            SET p.brand_name = 'Glucophage XR 750mg',
                p.active_ingredient = 'Metformin hydrochloride 750mg',
                p.drug_class = 'Biguanide',
                p.manufacturer = 'Merck Sante (Pháp)',
                p.packaging = 'Hộp 2 vỉ x 15 viên phóng thích kéo dài',
                p.box_price_vnd = 174000,
                p.unit_price_vnd = 5800,
                p.is_prescription_rx = true,
                p.indication = 'Phóng thích kéo dài tiện lợi dùng 1 lần vào buổi tối',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/glucophage-xr-750mg-merck-h-30v-14250.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_05'})
            SET p.brand_name = 'Glucophage XR 1000mg',
                p.active_ingredient = 'Metformin hydrochloride 1000mg',
                p.drug_class = 'Biguanide',
                p.manufacturer = 'Merck Sante (Pháp)',
                p.packaging = 'Hộp 4 vỉ x 15 viên phóng thích kéo dài',
                p.box_price_vnd = 432000,
                p.unit_price_vnd = 7200,
                p.is_prescription_rx = true,
                p.indication = 'Liều tối ưu phóng thích kéo dài giúp kiểm soát HbA1c ổn định 24h',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/glucophage-xr-1000mg-merck-h-60v-14251.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_06'})
            SET p.brand_name = 'Diamicron MR 30mg',
                p.active_ingredient = 'Gliclazide 30mg phóng thích có kiểm soát',
                p.drug_class = 'Sulfonylurea thế hệ 2',
                p.manufacturer = 'Les Laboratoires Servier (Pháp)',
                p.packaging = 'Hộp 2 vỉ x 30 viên',
                p.box_price_vnd = 204000,
                p.unit_price_vnd = 3400,
                p.is_prescription_rx = true,
                p.indication = 'Kích thích tế bào beta đảo tụy tiết insulin, dùng khi Metformin chưa đạt mục tiêu',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/diamicron-mr-30mg-servier-h-60v-15065.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_07'})
            SET p.brand_name = 'Diamicron MR 60mg',
                p.active_ingredient = 'Gliclazide 60mg',
                p.drug_class = 'Sulfonylurea thế hệ 2',
                p.manufacturer = 'Les Laboratoires Servier (Pháp)',
                p.packaging = 'Hộp 2 vỉ x 15 viên',
                p.box_price_vnd = 186000,
                p.unit_price_vnd = 6200,
                p.is_prescription_rx = true,
                p.indication = 'Phối hợp điều trị bậc 2 hạ đường huyết Type 2',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/diamicron-mr-60mg-servier-h-30v-15066.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_08'})
            SET p.brand_name = 'Amaryl 2mg',
                p.active_ingredient = 'Glimepiride 2mg',
                p.drug_class = 'Sulfonylurea thế hệ 3',
                p.manufacturer = 'Sanofi (Đức / Ý)',
                p.packaging = 'Hộp 3 vỉ x 10 viên',
                p.box_price_vnd = 165000,
                p.unit_price_vnd = 5500,
                p.is_prescription_rx = true,
                p.indication = 'Kích thích tiết insulin mạnh mẽ, dùng 1 lần duy nhất trong ngày trước bữa sáng',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/amaryl-2mg-sanofi-h-30v-15070.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_09'})
            SET p.brand_name = 'Forxiga 10mg',
                p.active_ingredient = 'Dapagliflozin 10mg',
                p.drug_class = 'Ức chế SGLT2 (SGLT2 inhibitor)',
                p.manufacturer = 'AstraZeneca (Thụy Điển)',
                p.packaging = 'Hộp 2 vỉ x 14 viên',
                p.box_price_vnd = 602000,
                p.unit_price_vnd = 21500,
                p.is_prescription_rx = true,
                p.indication = 'Thải đường qua nước tiểu, đặc biệt bảo vệ suy tim và làm chậm suy thận mạn',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/forxiga-10mg-astrazeneca-28v-16301.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_10'})
            SET p.brand_name = 'Jardiance 10mg',
                p.active_ingredient = 'Empagliflozin 10mg',
                p.drug_class = 'Ức chế SGLT2 (SGLT2 inhibitor)',
                p.manufacturer = 'Boehringer Ingelheim (Đức)',
                p.packaging = 'Hộp 3 vỉ x 10 viên',
                p.box_price_vnd = 690000,
                p.unit_price_vnd = 23000,
                p.is_prescription_rx = true,
                p.indication = 'Hạ đường huyết kèm giảm tử vong do biến cố tim mạch ở bệnh nhân Type 2',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/jardiance-10mg-boehringer-h-30v-16302.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_11'})
            SET p.brand_name = 'Jardiance 25mg',
                p.active_ingredient = 'Empagliflozin 25mg',
                p.drug_class = 'Ức chế SGLT2 (SGLT2 inhibitor)',
                p.manufacturer = 'Boehringer Ingelheim (Đức)',
                p.packaging = 'Hộp 3 vỉ x 10 viên',
                p.box_price_vnd = 810000,
                p.unit_price_vnd = 27000,
                p.is_prescription_rx = true,
                p.indication = 'Liều tăng cường bảo vệ tim thận tối đa cho bệnh nhân nguy cơ tim mạch rất cao',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/jardiance-25mg-boehringer-h-30v-16303.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_12'})
            SET p.brand_name = 'Januvia 50mg',
                p.active_ingredient = 'Sitagliptin 50mg',
                p.drug_class = 'Ức chế DPP-4 (DPP-4 inhibitor)',
                p.manufacturer = 'MSD (Mỹ / Ý)',
                p.packaging = 'Hộp 2 vỉ x 14 viên',
                p.box_price_vnd = 509600,
                p.unit_price_vnd = 18200,
                p.is_prescription_rx = true,
                p.indication = 'Tăng tiết insulin phụ thuộc nồng độ glucose máu, an toàn cho người già ít hạ đường huyết',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/januvia-50mg-msd-28v-16298.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_13'})
            SET p.brand_name = 'Januvia 100mg',
                p.active_ingredient = 'Sitagliptin 100mg',
                p.drug_class = 'Ức chế DPP-4 (DPP-4 inhibitor)',
                p.manufacturer = 'MSD (Mỹ / Ý)',
                p.packaging = 'Hộp 2 vỉ x 14 viên',
                p.box_price_vnd = 588000,
                p.unit_price_vnd = 21000,
                p.is_prescription_rx = true,
                p.indication = 'Liều tiêu chuẩn 1 lần mỗi ngày cho kiểm soát đường huyết êm dịu',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/januvia-100mg-msd-28v-16299.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_14'})
            SET p.brand_name = 'Galvus Met 50mg/850mg',
                p.active_ingredient = 'Vildagliptin 50mg + Metformin HCl 850mg',
                p.drug_class = 'Viên phối hợp cố định DPP-4 + Biguanide',
                p.manufacturer = 'Novartis (Thụy Sĩ)',
                p.packaging = 'Hộp 6 vỉ x 10 viên',
                p.box_price_vnd = 690000,
                p.unit_price_vnd = 11500,
                p.is_prescription_rx = true,
                p.indication = 'Phối hợp 2 cơ chế hiệp đồng tác dụng: tăng tiết incretin và giảm đề kháng insulin',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/galvus-met-50-850-novartis-60v-16295.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_15'})
            SET p.brand_name = 'Trajenta 5mg',
                p.active_ingredient = 'Linagliptin 5mg',
                p.drug_class = 'Ức chế DPP-4 (Thải trừ qua gan/mật)',
                p.manufacturer = 'Boehringer Ingelheim (Đức)',
                p.packaging = 'Hộp 3 vỉ x 10 viên',
                p.box_price_vnd = 615000,
                p.unit_price_vnd = 20500,
                p.is_prescription_rx = true,
                p.indication = 'An toàn vượt trội trên bệnh nhân suy giảm chức năng thận, không cần chỉnh liều ở mọi giai đoạn CKD',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/trajenta-5mg-boehringer-h-30v-16297.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_16'})
            SET p.brand_name = 'Actos 15mg',
                p.active_ingredient = 'Pioglitazone 15mg',
                p.drug_class = 'Thiazolidinedione (TZD)',
                p.manufacturer = 'Takeda (Nhật Bản)',
                p.packaging = 'Hộp 3 vỉ x 10 viên',
                p.box_price_vnd = 420000,
                p.unit_price_vnd = 14000,
                p.is_prescription_rx = true,
                p.indication = 'Tăng nhạy cảm insulin tế bào cơ và mỡ, hạ gan nhiễm mỡ nhưng chống chỉ định suy tim',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/actos-15mg-takeda-h-30v-16310.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_17'})
            SET p.brand_name = 'Glucobay 50mg',
                p.active_ingredient = 'Acarbose 50mg',
                p.drug_class = 'Ức chế Alpha-glucosidase',
                p.manufacturer = 'Bayer (Đức)',
                p.packaging = 'Hộp 3 vỉ x 10 viên',
                p.box_price_vnd = 138000,
                p.unit_price_vnd = 4600,
                p.is_prescription_rx = true,
                p.indication = 'Làm chậm phân giải carbohydrate tại ruột non, kiểm soát đường huyết sau ăn hiệu quả',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/glucobay-50mg-bayer-h-30v-16315.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_18'})
            SET p.brand_name = 'Bút tiêm Lantus Solostar 100 U/ml',
                p.active_ingredient = 'Insulin Glargine 100 U/ml',
                p.drug_class = 'Insulin Analogue tác dụng kéo dài (Nền)',
                p.manufacturer = 'Sanofi-Aventis (Đức)',
                p.packaging = 'Hộp 5 bút tiêm x 3ml',
                p.box_price_vnd = 1225000,
                p.unit_price_vnd = 245000,
                p.is_prescription_rx = true,
                p.indication = 'Cung cấp insulin nền 24h ổn định không có đỉnh nhọn, hạn chế hạ đường huyết đêm',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/lantus-solostar-100u-ml-sanofi-h-5-but-16280.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_19'})
            SET p.brand_name = 'Bút tiêm Toujeo Solostar 300 U/ml',
                p.active_ingredient = 'Insulin Glargine nồng độ cao 300 U/ml',
                p.drug_class = 'Insulin Nền siêu kéo dài (lên đến 36h)',
                p.manufacturer = 'Sanofi (Đức)',
                p.packaging = 'Hộp 3 bút tiêm x 1.5ml',
                p.box_price_vnd = 1020000,
                p.unit_price_vnd = 340000,
                p.is_prescription_rx = true,
                p.indication = 'Duy trì đường huyết nền kéo dài với dao động cực thấp và giảm thiểu nguy cơ hạ đường huyết',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/toujeo-solostar-300u-ml-sanofi-16281.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_20'})
            SET p.brand_name = 'Bút tiêm NovoRapid FlexPen 100 U/ml',
                p.active_ingredient = 'Insulin Aspart 100 U/ml',
                p.drug_class = 'Insulin Analogue tác dụng nhanh (Bữa ăn)',
                p.manufacturer = 'Novo Nordisk (Đan Mạch)',
                p.packaging = 'Hộp 5 bút tiêm x 3ml',
                p.box_price_vnd = 1150000,
                p.unit_price_vnd = 230000,
                p.is_prescription_rx = true,
                p.indication = 'Kiểm soát đỉnh đường huyết ngay sau ăn, tiêm ngay trước hoặc sau khi ăn',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/novorapid-flexpen-100u-ml-novo-nordisk-16282.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_21'})
            SET p.brand_name = 'Bút tiêm Mixtard 30 FlexPen 100 IU/ml',
                p.active_ingredient = 'Insulin Hỗn Hợp Premix (30% nhanh + 70% trung bình)',
                p.drug_class = 'Insulin Premixed hỗn hợp',
                p.manufacturer = 'Novo Nordisk (Đan Mạch)',
                p.packaging = 'Hộp 5 bút tiêm x 3ml',
                p.box_price_vnd = 975000,
                p.unit_price_vnd = 195000,
                p.is_prescription_rx = true,
                p.indication = 'Tiêm 2 lần/ngày trước bữa ăn sáng và tối cho bệnh nhân cần phác đồ phối hợp đơn giản',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/mixtard-30-flexpen-novo-nordisk-16283.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_22'})
            SET p.brand_name = 'Bút tiêm Victoza 6mg/ml',
                p.active_ingredient = 'Liraglutide 6mg/ml',
                p.drug_class = 'Đồng vận thụ thể GLP-1 (GLP-1 RA)',
                p.manufacturer = 'Novo Nordisk (Đan Mạch)',
                p.packaging = 'Hộp 2 bút tiêm x 3ml',
                p.box_price_vnd = 2700000,
                p.unit_price_vnd = 1350000,
                p.is_prescription_rx = true,
                p.indication = 'Bảo vệ tim mạch rõ rệt, giảm cân nặng hiệu quả, tiêm dưới da 1 lần mỗi ngày',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuoc/victoza-6mg-ml-novo-nordisk-16290.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_23'})
            SET p.brand_name = 'Máy Đo Đường Huyết Accu-Chek Guide',
                p.active_ingredient = 'Thiết bị y tế theo dõi đường huyết cá nhân',
                p.drug_class = 'Dụng cụ chẩn đoán & Theo dõi tại nhà',
                p.manufacturer = 'Roche Diabetes Care (Đức)',
                p.packaging = 'Bộ gồm 1 máy, 1 bút lấy máu FastClix, 10 que thử, 6 kim',
                p.box_price_vnd = 1450000,
                p.unit_price_vnd = 1450000,
                p.is_prescription_rx = false,
                p.indication = 'Độ chính xác chuẩn 10/10 theo ISO 15197:2013, kết nối Bluetooth với điện thoại thông minh',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thiet-bi-y-te/may-do-duong-huyet-accu-chek-guide-roche-bo-16400.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_24'})
            SET p.brand_name = 'Máy Đo Đường Huyết Accu-Chek Instant',
                p.active_ingredient = 'Thiết bị y tế đo đường huyết nhanh',
                p.drug_class = 'Dụng cụ chẩn đoán & Theo dõi tại nhà',
                p.manufacturer = 'Roche Diabetes Care (Đức)',
                p.packaging = 'Bộ máy kèm bút lấy máu Softclix và 10 que',
                p.box_price_vnd = 890000,
                p.unit_price_vnd = 890000,
                p.is_prescription_rx = false,
                p.indication = 'Màn hình có vạch chỉ thị màu mục tiêu đường huyết trực quan, dễ sử dụng cho người cao tuổi',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thiet-bi-y-te/may-do-duong-huyet-accu-chek-instant-roche-16402.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_25'})
            SET p.brand_name = 'Que Thử Đường Huyết Accu-Chek Instant (Hộp 50 que)',
                p.active_ingredient = 'Que thử men điện hóa GDH-FAD',
                p.drug_class = 'Vật tư tiêu hao y tế',
                p.manufacturer = 'Roche (Đức)',
                p.packaging = 'Hộp 50 que thử',
                p.box_price_vnd = 440000,
                p.unit_price_vnd = 8800,
                p.is_prescription_rx = false,
                p.indication = 'Dùng kèm máy đo đường huyết Accu-Chek Instant, hút máu cực nhanh chỉ 0.6 µL',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thiet-bi-y-te/que-thu-duong-huyet-accu-chek-instant-50-que-16401.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_26'})
            SET p.brand_name = 'Kim Lấy Máu Accu-Chek Softclix (Hộp 100 kim)',
                p.active_ingredient = 'Kim lấy máu tiệt trùng không gây đau',
                p.drug_class = 'Vật tư tiêu hao y tế',
                p.manufacturer = 'Roche (Đức)',
                p.packaging = 'Hộp 100 kim',
                p.box_price_vnd = 180000,
                p.unit_price_vnd = 1800,
                p.is_prescription_rx = false,
                p.indication = 'Đầu kim vát 3 góc với công nghệ giảm đau Clixmotion, tương thích bút Softclix',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thiet-bi-y-te/kim-lay-mau-accu-chek-softclix-100-kim-16405.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_27'})
            SET p.brand_name = 'Máy Đo Đường Huyết Contour Plus',
                p.active_ingredient = 'Thiết bị đo đường huyết độ nhạy cao',
                p.drug_class = 'Dụng cụ chẩn đoán & Theo dõi tại nhà',
                p.manufacturer = 'Ascensia Diabetes Care (Thụy Sĩ)',
                p.packaging = 'Hộp máy Contour Plus + bút + 5 kim',
                p.box_price_vnd = 950000,
                p.unit_price_vnd = 950000,
                p.is_prescription_rx = false,
                p.indication = 'Công nghệ Second-Chance cho phép chấm thêm máu trong 30 giây nếu thiếu giọt máu',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thiet-bi-y-te/may-do-duong-huyet-contour-plus-ascensia-16410.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_28'})
            SET p.brand_name = 'Que Thử Đường Huyết Contour Plus (Hộp 50 que)',
                p.active_ingredient = 'Que thử men FAD-GDH',
                p.drug_class = 'Vật tư tiêu hao y tế',
                p.manufacturer = 'Ascensia (Thụy Sĩ)',
                p.packaging = 'Hộp 50 que thử',
                p.box_price_vnd = 430000,
                p.unit_price_vnd = 8600,
                p.is_prescription_rx = false,
                p.indication = 'Dùng kèm máy Contour Plus, độ bền cao và không bị ảnh hưởng bởi oxy trong máu',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thiet-bi-y-te/que-thu-contour-plus-50-que-16411.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_29'})
            SET p.brand_name = 'Sữa Dinh Dưỡng Y Học Glucerna 850g',
                p.active_ingredient = 'Hệ bột đường giải phóng chậm Fibersol + MUFA/PUFA',
                p.drug_class = 'Dinh dưỡng y học đặc trị đái tháo đường',
                p.manufacturer = 'Abbott Nutrition (Mỹ / Hà Lan)',
                p.packaging = 'Lon thiếc 850g',
                p.box_price_vnd = 820000,
                p.unit_price_vnd = 820000,
                p.is_prescription_rx = false,
                p.indication = 'Thay thế bữa ăn phụ hoặc bữa ăn chính khi bận rộn, chỉ số GI thấp giúp ổn định đường huyết',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/sua-bot-glucerna-850g-abbott-16500.html';
MERGE (p:PharmacyProduct {id: 'lc_dia_30'})
            SET p.brand_name = 'Sữa Dinh Dưỡng Glucerna Chai Pha Sẵn 220ml',
                p.active_ingredient = 'Dinh dưỡng cân đối chỉ số GI thấp dạng lỏng',
                p.drug_class = 'Dinh dưỡng y học dạng lỏng tiện lợi',
                p.manufacturer = 'Abbott Nutrition (Mỹ / Hà Lan)',
                p.packaging = 'Lốc 4 chai x 220ml',
                p.box_price_vnd = 208000,
                p.unit_price_vnd = 52000,
                p.is_prescription_rx = false,
                p.indication = 'Tiện lợi mang theo đi làm, bổ sung dinh dưỡng tức thì mà không gây biến động đường huyết',
                p.longchau_url = 'https://nhathuoclongchau.com.vn/thuc-pham-chuc-nang/sua-nuoc-glucerna-220ml-abbott-loc-4-chai-16501.html';

// RELATIONSHIPS

MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_POLYURIA'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'VERY_COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_POLYDIPSIA'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'VERY_COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_POLYPHAGIA'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_WEIGHT_LOSS'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_FATIGUE'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_BLURRED_VISION'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'OCCASIONAL'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_NUMBNESS'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_SLOW_HEALING'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_DRY_MOUTH'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'COMMON'}]->(s);
MATCH (d:Disease {id: 'T2D'}), (s:Symptom {id: 'SYM_RECURRENT_INFECTION'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'OCCASIONAL'}]->(s);
MATCH (d:Disease {id: 'PRE_DIABETES'}), (s:Symptom {id: 'SYM_FATIGUE'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'INSIDIOUS'}]->(s);
MATCH (d:Disease {id: 'PRE_DIABETES'}), (s:Symptom {id: 'SYM_NUMBNESS'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'INSIDIOUS'}]->(s);
MATCH (d:Disease {id: 'T1D'}), (s:Symptom {id: 'SYM_POLYURIA'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'ACUTE'}]->(s);
MATCH (d:Disease {id: 'T1D'}), (s:Symptom {id: 'SYM_POLYDIPSIA'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'ACUTE'}]->(s);
MATCH (d:Disease {id: 'T1D'}), (s:Symptom {id: 'SYM_WEIGHT_LOSS'})
            MERGE (d)-[:HAS_SYMPTOM {frequency: 'ACUTE'}]->(s);
MATCH (a {id: 'T2D'}), (b {id: 'HBA1C'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'HbA1c >= 6.5%', method: 'Chuẩn NGSP/DCCT theo QĐ 5481'}]->(b);
MATCH (a {id: 'T2D'}), (b {id: 'FPG'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'FPG >= 126 mg/dL', condition: 'Nhịn đói ít nhất 8 tiếng'}]->(b);
MATCH (a {id: 'T2D'}), (b {id: 'OGTT_2H'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'OGTT 2h >= 200 mg/dL', method: '75g Anhydrous Glucose'}]->(b);
MATCH (a {id: 'T2D'}), (b {id: 'RPG'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'RPG >= 200 mg/dL', condition: 'Đi kèm triệu chứng lâm sàng kinh điển'}]->(b);
MATCH (a {id: 'PRE_DIABETES'}), (b {id: 'HBA1C'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: '5.7% <= HbA1c <= 6.4%'}]->(b);
MATCH (a {id: 'PRE_DIABETES'}), (b {id: 'FPG'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: '100 mg/dL <= FPG <= 125 mg/dL'}]->(b);
MATCH (a {id: 'PRE_DIABETES'}), (b {id: 'OGTT_2H'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: '140 mg/dL <= OGTT 2h <= 199 mg/dL'}]->(b);
MATCH (a {id: 'CKD'}), (b {id: 'EGFR'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'eGFR < 60 mL/min/1.73m2 kéo dài > 3 tháng'}]->(b);
MATCH (a {id: 'CKD'}), (b {id: 'UACR'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'UACR >= 30 mg/g'}]->(b);
MATCH (a {id: 'CKD'}), (b {id: 'CREATININE'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'Creatinine tăng cao'}]->(b);
MATCH (a {id: 'HYPERTENSION'}), (b {id: 'BP_SYS'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'Huyết áp tâm thu >= 130 mmHg'}]->(b);
MATCH (a {id: 'HYPERTENSION'}), (b {id: 'BP_DIA'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'Huyết áp tâm trương >= 80 mmHg'}]->(b);
MATCH (a {id: 'DYSLIPIDEMIA'}), (b {id: 'LIPID_LDL'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'LDL-C >= 100 mg/dL'}]->(b);
MATCH (a {id: 'DYSLIPIDEMIA'}), (b {id: 'LIPID_TRIGLYCERIDE'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'Triglyceride >= 150 mg/dL'}]->(b);
MATCH (a {id: 'OBESITY'}), (b {id: 'BMI'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'BMI >= 23.0 kg/m2 (Chuẩn IDI/WPRO)'}]->(b);
MATCH (a {id: 'OBESITY'}), (b {id: 'WAIST'})
            MERGE (a)-[:DIAGNOSED_BY {threshold: 'Vòng eo >= 90cm (Nam) / >= 80cm (Nữ)'}]->(b);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'CKD'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Tổn thương màng đáy mao mạch cầu thận và tăng áp lực lọc'}]->(c);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'ASCVD'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Rối loạn nội mô mạch máu và oxy hóa hạt LDL xơ vữa'}]->(c);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'HEART_FAILURE'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Bệnh cơ tim đái tháo đường và quá tải thể tích mạn tính'}]->(c);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'DIABETIC_RETINOPATHY'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Tổn thương vi mạch võng mạc gây vi phình mạch và tân mạch xuất huyết'}]->(c);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'DIABETIC_NEUROPATHY'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Độc tính glucose tích tụ Sorbitol và tổn thương mạch nuôi dây thần kinh'}]->(c);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'DIABETIC_FOOT_ULCER'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Phối hợp mất cảm giác thần kinh và thiếu máu tưới nuôi dưỡng mô sâu'}]->(c);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'PAD'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Xơ cứng và hẹp tắc các động mạch vừa và lớn nuôi chi dưới'}]->(c);
MATCH (d:Disease {id: 'T2D'}), (c:Complication {id: 'DIABETIC_GASTROPARESIS'})
            MERGE (d)-[:CAUSES_COMPLICATION {mechanism: 'Tổn thương dây thần kinh phế vị chi phối nhu động dạ dày'}]->(c);
MATCH (a {id: 'HYPERTENSION'}), (b {id: 'ASCVD'})
            MERGE (a)-[:AGGRAVATES {impact: 'Gia tăng gấp 3 lần nguy cơ đột quỵ và nhồi máu cơ tim'}]->(b);
MATCH (a {id: 'HYPERTENSION'}), (b {id: 'CKD'})
            MERGE (a)-[:AGGRAVATES {impact: 'Đẩy nhanh tốc độ giảm eGFR và xuất hiện đạm niệu'}]->(b);
MATCH (a {id: 'DYSLIPIDEMIA'}), (b {id: 'ASCVD'})
            MERGE (a)-[:AGGRAVATES {impact: 'Tăng sinh và tích tụ mảng xơ vữa không ổn định'}]->(b);
MATCH (a {id: 'OBESITY'}), (b {id: 'T2D'})
            MERGE (a)-[:AGGRAVATES {impact: 'Gia tăng đề kháng insulin và viêm mạn tính hệ thống'}]->(b);
MATCH (a {id: 'OBESITY'}), (b {id: 'NAFLD'})
            MERGE (a)-[:AGGRAVATES {impact: 'Tích tụ mỡ nội tạng xâm lấn và thoái hóa nhu mô gan'}]->(b);
MATCH (a {id: 'SMOKING'}), (b {id: 'ASCVD'})
            MERGE (a)-[:AGGRAVATES {impact: 'Làm co thắt mạch vành và hoại tử tế bào nội mạc'}]->(b);
MATCH (a {id: 'SMOKING'}), (b {id: 'PAD'})
            MERGE (a)-[:AGGRAVATES {impact: 'Tăng nguy cơ hoại tử chi dưới và cắt cụt chi gấp 4 lần'}]->(b);
MATCH (a {id: 'PHYSICAL_INACTIVITY'}), (b {id: 'T2D'})
            MERGE (a)-[:AGGRAVATES {impact: 'Giảm vận chuyển kênh GLUT4 lên màng tế bào cơ vân'}]->(b);
MATCH (dr:Drug {id: 'METFORMIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 1, guideline: "QĐ 5481/QĐ-BYT"}]->(d);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'GLIMEPIRIDE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'GLIBENCLAMIDE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 3}]->(d);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 1, condition: "Kèm suy tim hoặc bệnh thận mạn"}]->(d);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 1, condition: "Kèm bệnh tim mạch hoặc suy tim"}]->(d);
MATCH (dr:Drug {id: 'CANAGLIFLOZIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'SITAGLIPTIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'VILDAGLIPTIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'LINAGLIPTIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'SAXAGLIPTIN'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 3}]->(d);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 1, condition: "Kèm béo phì hoặc bệnh tim mạch xơ vữa"}]->(d);
MATCH (dr:Drug {id: 'LIRAGLUTIDE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 1, condition: "Kèm bệnh tim mạch xơ vữa"}]->(d);
MATCH (dr:Drug {id: 'DULAGLUTIDE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'PIOGLITAZONE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2}]->(d);
MATCH (dr:Drug {id: 'ACARBOSE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 3}]->(d);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 2, condition: "Thất bại thuốc uống hoặc HbA1c > 9.0%"}]->(d);
MATCH (dr:Drug {id: 'INSULIN_ASPART'}), (d:Disease {id: 'T2D'})
            MERGE (dr)-[:TREATS {priority: 3, condition: "Phác đồ Basal-Bolus hoặc ăn nhiều carb"}]->(d);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (d:Disease {id: 'T1D'})
            MERGE (dr)-[:TREATS {priority: 1, condition: "Liệu pháp bắt buộc suốt đời"}]->(d);
MATCH (dr:Drug {id: 'INSULIN_ASPART'}), (d:Disease {id: 'T1D'})
            MERGE (dr)-[:TREATS {priority: 1, condition: "Liệu pháp bắt buộc trước bữa ăn"}]->(d);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (c {id: 'CKD'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'DAPA-CKD: Giảm 39% nguy cơ suy thận tiến triển'}]->(c);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (c {id: 'HEART_FAILURE'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'DAPA-HF: Giảm 26% tử vong tim mạch và tái nhập viện'}]->(c);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (c {id: 'ASCVD'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'Làm giảm gánh nặng tim mạch toàn diện'}]->(c);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (c {id: 'CKD'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'EMPA-KIDNEY: Làm chậm rõ rệt suy giảm chức năng lọc'}]->(c);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (c {id: 'HEART_FAILURE'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'EMPEROR-Reduced & Preserved: Bảo vệ phân suất tống máu'}]->(c);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (c {id: 'ASCVD'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'EMPA-REG OUTCOME: Giảm 38% tử vong do biến cố tim mạch'}]->(c);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (c {id: 'ASCVD'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'SUSTAIN-6: Giảm 26% biến cố tim mạch chính MACE'}]->(c);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (c {id: 'CKD'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'FLOW trial: Bảo vệ thận độc lập'}]->(c);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (c {id: 'OBESITY'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'STEP trial: Giảm trung bình 15% trọng lượng cơ thể'}]->(c);
MATCH (dr:Drug {id: 'LIRAGLUTIDE'}), (c {id: 'ASCVD'})
            MERGE (dr)-[:HIGHLY_RECOMMENDED_FOR {evidence: 'LEADER trial: Giảm 13% biến cố tim mạch lớn'}]->(c);
MATCH (dr:Drug {id: 'METFORMIN'}), (c {id: 'CKD'})
            MERGE (dr)-[:CONTRAINDICATED_IN {condition: 'eGFR < 30 mL/min/1.73m2', severity: 'ABSOLUTE', reason: 'Tích tụ nguy cơ nhiễm toan acid lactic tử vong'}]->(c);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (c {id: 'CKD'})
            MERGE (dr)-[:CONTRAINDICATED_IN {condition: 'eGFR < 20 mL/min/1.73m2 để khởi đầu điều trị', severity: 'ABSOLUTE'}]->(c);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (c {id: 'CKD'})
            MERGE (dr)-[:CONTRAINDICATED_IN {condition: 'eGFR < 20 mL/min/1.73m2 để khởi đầu điều trị', severity: 'ABSOLUTE'}]->(c);
MATCH (dr:Drug {id: 'PIOGLITAZONE'}), (c {id: 'HEART_FAILURE'})
            MERGE (dr)-[:CONTRAINDICATED_IN {condition: 'Suy tim mức độ NYHA II - IV', severity: 'ABSOLUTE', reason: 'Gây giữ nước và làm trầm trọng suy tim'}]->(c);
MATCH (dr:Drug {id: 'SAXAGLIPTIN'}), (c {id: 'HEART_FAILURE'})
            MERGE (dr)-[:CONTRAINDICATED_IN {condition: 'Bệnh nhân có tiền sử hoặc nguy cơ suy tim cao (SAVOR-TIMI 53)', severity: 'RELATIVE'}]->(c);
MATCH (dr:Drug {id: 'METFORMIN'}), (c {id: 'CKD'})
            MERGE (dr)-[:CAUTION_IN {condition: '30 <= eGFR < 45 mL/min', instruction: 'Giảm 50% liều dùng (tối đa 1000 mg/ngày), kiểm tra eGFR mỗi 3 tháng'}]->(c);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (c {id: 'CKD'})
            MERGE (dr)-[:CAUTION_IN {condition: 'eGFR < 45 mL/min', instruction: 'Cần giảm liều và cảnh báo nguy cơ hạ đường huyết kéo dài'}]->(c);
MATCH (dr:Drug {id: 'GLIMEPIRIDE'}), (c {id: 'CKD'})
            MERGE (dr)-[:CAUTION_IN {condition: 'Suy giảm chức năng thận', instruction: 'Khởi đầu với liều thấp 1mg/ngày'}]->(c);
MATCH (dr:Drug {id: 'LINAGLIPTIN'}), (c {id: 'CKD'})
            MERGE (dr)-[:CAUTION_IN {instruction: 'Thải trừ 95% qua gan mật, an toàn tuyệt đối không cần chỉnh liều ở mọi giai đoạn CKD'}]->(c);
MATCH (dr:Drug {id: 'METFORMIN'}), (a:AdverseEffect {id: 'LACTIC_ACIDOSIS'})
            MERGE (dr)-[:RISK_OF {trigger: 'Uống rượu bia / Sử dụng cồn / Thiếu oxy mô cấp', severity: 'FATAL'}]->(a);
MATCH (dr:Drug {id: 'METFORMIN'}), (a:AdverseEffect {id: 'GI_UPSET'})
            MERGE (dr)-[:RISK_OF {frequency: '20-30% bệnh nhân trong 2-4 tuần đầu'}]->(a);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (a:AdverseEffect {id: 'HYPOGLYCEMIA_MILD'})
            MERGE (dr)-[:RISK_OF {trigger: 'Bỏ bữa ăn, lao động thể lực quá mức, hoặc người cao tuổi'}]->(a);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (a:AdverseEffect {id: 'WEIGHT_GAIN'})
            MERGE (dr)-[:RISK_OF {cause: 'Tác dụng đồng hóa của việc tăng tiết insulin'}]->(a);
MATCH (dr:Drug {id: 'GLIMEPIRIDE'}), (a:AdverseEffect {id: 'HYPOGLYCEMIA_MILD'})
            MERGE (dr)-[:RISK_OF {trigger: 'Bỏ bữa ăn hoặc dùng quá liều'}]->(a);
MATCH (dr:Drug {id: 'GLIBENCLAMIDE'}), (a:AdverseEffect {id: 'HYPOGLYCEMIA_SEVERE'})
            MERGE (dr)-[:RISK_OF {severity: 'HIGH_RISK_OF_FATAL_HYPO'}]->(a);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (a:AdverseEffect {id: 'UTI'})
            MERGE (dr)-[:RISK_OF {prevention: 'Uống đủ nước (1.5 - 2L/ngày), vệ sinh sạch sẽ bộ phận sinh dục'}]->(a);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (a:AdverseEffect {id: 'EUG_DKA'})
            MERGE (dr)-[:RISK_OF {trigger: 'Thiếu hụt insulin tương đối hoặc nhịn ăn kéo dài'}]->(a);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (a:AdverseEffect {id: 'FOURNIER_GANGRENE'})
            MERGE (dr)-[:RISK_OF {severity: 'RARE_WARNING'}]->(a);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (a:AdverseEffect {id: 'UTI'})
            MERGE (dr)-[:RISK_OF {prevention: 'Uống nhiều nước'}]->(a);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (a:AdverseEffect {id: 'EUG_DKA'})
            MERGE (dr)-[:RISK_OF {trigger: 'Thiếu insulin'}]->(a);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (a:AdverseEffect {id: 'GI_UPSET'})
            MERGE (dr)-[:RISK_OF {frequency: 'Buồn nôn nhẹ khi tăng liều, thường tự hết sau vài tuần'}]->(a);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (a:AdverseEffect {id: 'PANCREATITIS_ACUTE'})
            MERGE (dr)-[:RISK_OF {warning: 'Ngừng thuốc vĩnh viễn nếu nghi ngờ viêm tụy'}]->(a);
MATCH (dr:Drug {id: 'LIRAGLUTIDE'}), (a:AdverseEffect {id: 'GI_UPSET'})
            MERGE (dr)-[:RISK_OF {frequency: 'Thường gặp giai đoạn đầu'}]->(a);
MATCH (dr:Drug {id: 'PIOGLITAZONE'}), (a:AdverseEffect {id: 'PERIPHERAL_EDEMA'})
            MERGE (dr)-[:RISK_OF {cause: 'Giữ muối nước ở ống thận'}]->(a);
MATCH (dr:Drug {id: 'PIOGLITAZONE'}), (a:AdverseEffect {id: 'WEIGHT_GAIN'})
            MERGE (dr)-[:RISK_OF {cause: 'Tăng sinh mô mỡ dưới da'}]->(a);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (a:AdverseEffect {id: 'HYPOGLYCEMIA_MILD'})
            MERGE (dr)-[:RISK_OF {trigger: 'Tiêm quá liều hoặc ăn không đủ lượng carb'}]->(a);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (a:AdverseEffect {id: 'HYPOGLYCEMIA_SEVERE'})
            MERGE (dr)-[:RISK_OF {trigger: 'Bỏ bữa ăn chính sau khi tiêm'}]->(a);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (a:AdverseEffect {id: 'WEIGHT_GAIN'})
            MERGE (dr)-[:RISK_OF {cause: 'Tích tụ mỡ do insulin đồng hóa'}]->(a);
MATCH (dr:Drug {id: 'INSULIN_ASPART'}), (a:AdverseEffect {id: 'HYPOGLYCEMIA_MILD'})
            MERGE (dr)-[:RISK_OF {trigger: 'Tiêm nhưng ăn muộn quá 15 phút'}]->(a);
MATCH (dr:Drug {id: 'METFORMIN'}), (b:Biomarker {id: 'EGFR'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'METFORMIN'}), (b:Biomarker {id: 'CREATININE'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'METFORMIN'}), (b:Biomarker {id: 'HBA1C'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (b:Biomarker {id: 'FPG'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (b:Biomarker {id: 'HBA1C'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (b:Biomarker {id: 'EGFR'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (b:Biomarker {id: 'BP_SYS'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (b:Biomarker {id: 'HBA1C'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (b:Biomarker {id: 'EGFR'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (b:Biomarker {id: 'HBA1C'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (b:Biomarker {id: 'BMI'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'SEMAGLUTIDE'}), (b:Biomarker {id: 'HBA1C'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (b:Biomarker {id: 'FPG'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (dr:Drug {id: 'INSULIN_ASPART'}), (b:Biomarker {id: 'FPG'})
            MERGE (dr)-[:MONITORED_BY]->(b);
MATCH (orig:Food {id: 'FOOD_COM_TRANG'}), (rep:Food {id: 'FOOD_COM_GAO_LUC'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Chỉ số GI thấp hơn 28 đơn vị, hàm lượng chất xơ cao gấp 3 lần'}]->(rep);
MATCH (orig:Food {id: 'FOOD_COM_TRANG'}), (rep:Food {id: 'FOOD_KHOAI_LANG'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Chỉ số GI thấp hơn 35 đơn vị, tạo cảm giác no lâu cho bữa chính'}]->(rep);
MATCH (orig:Food {id: 'FOOD_XOI_NEP'}), (rep:Food {id: 'FOOD_YEN_MACH'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Thay thế nếp dẻo bằng ngũ cốc thô giàu chất xơ hòa tan beta-glucan'}]->(rep);
MATCH (orig:Food {id: 'FOOD_XOI_NEP'}), (rep:Food {id: 'FOOD_NGO_LUOC'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Ngô luộc GI thấp hơn 38 đơn vị so với xôi nếp béo'}]->(rep);
MATCH (orig:Food {id: 'FOOD_BANH_MI_TRANG'}), (rep:Food {id: 'FOOD_BANH_MI_DEN'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Bánh mì đen nguyên cám GI 48 so với bánh mì trắng GI 85'}]->(rep);
MATCH (orig:Food {id: 'FOOD_BANH_CHUNG'}), (rep:Food {id: 'FOOD_COM_GAO_LUC'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Cắt giảm chất béo động vật bão hòa và tinh bột nếp'}]->(rep);
MATCH (orig:Food {id: 'FOOD_PHO_BO'}), (rep:Food {id: 'FOOD_BUN_MOC_RAU'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Bún mọc nước thanh kết hợp nhiều rau xanh giúp giảm 22 đơn vị GI'}]->(rep);
MATCH (orig:Food {id: 'FOOD_BUN_BO_HUE'}), (rep:Food {id: 'FOOD_BUN_MOC_RAU'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Giảm lượng mỡ bò và muối bão hòa gây biến chứng tim thận'}]->(rep);
MATCH (orig:Food {id: 'FOOD_BANH_CUON'}), (rep:Food {id: 'FOOD_BANH_MI_DEN'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Bánh mì đen nguyên cám giàu dinh dưỡng và ít gây nhũ hóa đường ruột'}]->(rep);
MATCH (orig:Food {id: 'FOOD_BANH_MI_THIT'}), (rep:Food {id: 'FOOD_BANH_MI_DEN'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Bánh mì đen kẹp ức gà nạc thay thế cho pate mỡ động vật'}]->(rep);
MATCH (orig:Food {id: 'FOOD_TRA_SUA'}), (rep:Food {id: 'FOOD_TRA_XANH_MATCHA'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Trà xanh tự nhiên không đường bổ sung EGCG chống oxy hóa'}]->(rep);
MATCH (orig:Food {id: 'FOOD_NUOC_NGOT'}), (rep:Food {id: 'FOOD_TRA_XANH_MATCHA'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Nước lọc hoặc trà xanh nguyên chất không chứa calo rỗng'}]->(rep);
MATCH (orig:Food {id: 'FOOD_CHE_NGOT'}), (rep:Food {id: 'FOOD_BUOI'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Bưởi tươi ngọt nhẹ giàu vitamin thay thế cho chè đường ngọt'}]->(rep);
MATCH (orig:Food {id: 'FOOD_DUA_HAU'}), (rep:Food {id: 'FOOD_TAO_XANH'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Táo xanh chỉ số GI 36 so với dưa hấu GI 76'}]->(rep);
MATCH (orig:Food {id: 'FOOD_CHAO_LONG'}), (rep:Food {id: 'FOOD_CA_HAP'})
            MERGE (orig)-[:CAN_BE_REPLACED_BY {reason: 'Cá hồi hấp cung cấp protein lành mạnh không làm tăng vọt đường huyết'}]->(rep);
MATCH (a {id: 'T2D'}), (p:ClinicalProtocol {id: 'PROTOCOL_FITT'})
            MERGE (a)-[:RECOMMENDED_LIFESTYLE]->(p);
MATCH (a {id: 'T2D'}), (p:ClinicalProtocol {id: 'PROTOCOL_PLATE_METHOD'})
            MERGE (a)-[:RECOMMENDED_LIFESTYLE]->(p);
MATCH (a {id: 'T2D'}), (p:ClinicalProtocol {id: 'PROTOCOL_SMBG'})
            MERGE (a)-[:RECOMMENDED_LIFESTYLE]->(p);
MATCH (a {id: 'PRE_DIABETES'}), (p:ClinicalProtocol {id: 'PROTOCOL_FITT'})
            MERGE (a)-[:RECOMMENDED_LIFESTYLE]->(p);
MATCH (a {id: 'PRE_DIABETES'}), (p:ClinicalProtocol {id: 'PROTOCOL_PLATE_METHOD'})
            MERGE (a)-[:RECOMMENDED_LIFESTYLE]->(p);
MATCH (a {id: 'HYPOGLYCEMIA_MILD'}), (p:ClinicalProtocol {id: 'PROTOCOL_RULE_15'})
            MERGE (a)-[:TREATED_BY_PROTOCOL]->(p);
MATCH (a {id: 'DIABETIC_FOOT_ULCER'}), (p:ClinicalProtocol {id: 'PROTOCOL_FOOT_CARE'})
            MERGE (a)-[:TREATED_BY_PROTOCOL]->(p);
MATCH (dr:Drug {id: 'METFORMIN'}), (p:PharmacyProduct {id: 'lc_dia_01'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'METFORMIN'}), (p:PharmacyProduct {id: 'lc_dia_02'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'METFORMIN'}), (p:PharmacyProduct {id: 'lc_dia_03'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'METFORMIN'}), (p:PharmacyProduct {id: 'lc_dia_04'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'METFORMIN'}), (p:PharmacyProduct {id: 'lc_dia_05'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (p:PharmacyProduct {id: 'lc_dia_06'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'GLICLAZIDE'}), (p:PharmacyProduct {id: 'lc_dia_07'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'GLIMEPIRIDE'}), (p:PharmacyProduct {id: 'lc_dia_08'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'DAPAGLIFLOZIN'}), (p:PharmacyProduct {id: 'lc_dia_09'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (p:PharmacyProduct {id: 'lc_dia_10'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'EMPAGLIFLOZIN'}), (p:PharmacyProduct {id: 'lc_dia_11'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'SITAGLIPTIN'}), (p:PharmacyProduct {id: 'lc_dia_12'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'SITAGLIPTIN'}), (p:PharmacyProduct {id: 'lc_dia_13'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'VILDAGLIPTIN'}), (p:PharmacyProduct {id: 'lc_dia_14'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'LINAGLIPTIN'}), (p:PharmacyProduct {id: 'lc_dia_15'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'PIOGLITAZONE'}), (p:PharmacyProduct {id: 'lc_dia_16'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'ACARBOSE'}), (p:PharmacyProduct {id: 'lc_dia_17'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (p:PharmacyProduct {id: 'lc_dia_18'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'INSULIN_GLARGINE'}), (p:PharmacyProduct {id: 'lc_dia_19'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'INSULIN_ASPART'}), (p:PharmacyProduct {id: 'lc_dia_20'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (dr:Drug {id: 'LIRAGLUTIDE'}), (p:PharmacyProduct {id: 'lc_dia_22'})
            MERGE (dr)-[:DISPENSED_AS_PRODUCT]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_23'})
            MERGE (d)-[:RECOMMENDED_DEVICE_FOR]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_24'})
            MERGE (d)-[:RECOMMENDED_DEVICE_FOR]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_25'})
            MERGE (d)-[:RECOMMENDED_DEVICE_FOR]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_26'})
            MERGE (d)-[:RECOMMENDED_DEVICE_FOR]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_27'})
            MERGE (d)-[:RECOMMENDED_DEVICE_FOR]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_28'})
            MERGE (d)-[:RECOMMENDED_DEVICE_FOR]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_29'})
            MERGE (d)-[:NUTRITIONAL_SUPPORT_FOR]->(p);
MATCH (d:Disease {id: 'T2D'}), (p:PharmacyProduct {id: 'lc_dia_30'})
            MERGE (d)-[:NUTRITIONAL_SUPPORT_FOR]->(p);
MATCH (n {id: 'T2D'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'PRE_DIABETES'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'T1D'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'GESTATIONAL_DIABETES'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'METABOLIC_SYNDROME'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'HBA1C'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FPG'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'OGTT_2H'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'RPG'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'EGFR'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'CREATININE'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'UACR'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'BMI'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'CKD'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'ASCVD'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'HEART_FAILURE'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DIABETIC_RETINOPATHY'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DIABETIC_NEUROPATHY'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'HYPERTENSION'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DYSLIPIDEMIA'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'OBESITY'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'METFORMIN'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'GLICLAZIDE'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'GLIMEPIRIDE'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'GLIBENCLAMIDE'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DAPAGLIFLOZIN'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'EMPAGLIFLOZIN'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'SITAGLIPTIN'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'VILDAGLIPTIN'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'LINAGLIPTIN'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'INSULIN_GLARGINE'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'INSULIN_ASPART'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'LACTIC_ACIDOSIS'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'HYPOGLYCEMIA_MILD'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'HYPOGLYCEMIA_SEVERE'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DKA'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'HHS'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'PROTOCOL_FITT'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'PROTOCOL_RULE_15'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'PROTOCOL_SMBG'}), (s:Source {id: 'SRC_BYT_5481'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'SYM_NUMBNESS'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'SYM_SLOW_HEALING'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'SYM_BLURRED_VISION'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DIABETIC_FOOT_ULCER'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DIABETIC_NEUROPATHY'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'PAD'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DIABETIC_GASTROPARESIS'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'PROTOCOL_FOOT_CARE'}), (s:Source {id: 'SRC_VINMEC'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_COM_TRANG'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_COM_GAO_LUC'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_KHOAI_LANG'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_PHO_BO'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_BUN_MOC_RAU'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_BANH_MI_TRANG'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_BANH_MI_DEN'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_YEN_MACH'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_BONG_CAI_XANH'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_RAU_MUONG'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_DAU_BAP'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_KHO_QUA'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_CA_HAP'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_UC_GA'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_BUOI'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'FOOD_TAO_XANH'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'PROTOCOL_PLATE_METHOD'}), (s:Source {id: 'SRC_NIN'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'EUG_DKA'}), (s:Source {id: 'SRC_ADA_2024'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'SEMAGLUTIDE'}), (s:Source {id: 'SRC_ADA_2024'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'LIRAGLUTIDE'}), (s:Source {id: 'SRC_ADA_2024'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'DULAGLUTIDE'}), (s:Source {id: 'SRC_ADA_2024'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (n {id: 'CANAGLIFLOZIN'}), (s:Source {id: 'SRC_ADA_2024'})
            MERGE (n)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_01'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_02'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_03'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_04'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_05'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_06'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_07'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_08'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_09'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_10'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_11'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_12'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_13'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_14'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_15'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_16'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_17'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_18'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_19'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_20'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_21'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_22'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_23'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_24'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_25'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_26'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_27'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_28'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_29'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
MATCH (p:PharmacyProduct {id: 'lc_dia_30'}), (s:Source {id: 'SRC_LONGCHAU'})
            MERGE (p)-[:CITED_FROM]->(s);
