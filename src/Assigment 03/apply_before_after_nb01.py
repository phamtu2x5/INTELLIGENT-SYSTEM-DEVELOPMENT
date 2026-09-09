import json
import os

NB_PATH = "src/Assigment 03/diabetes_large/notebooks/01_diabetes_large_ml_vs_dl_scratch.ipynb"
with open(NB_PATH, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Cell 32 Code
cell32_code = """# Xuất dữ liệu đối chuẩn ra file JSON (Đo lường đầy đủ cả Ngưỡng Mặc Định 0.50 và Ngưỡng Tối Ưu)
models_summary = []
m_configs = [
    ('Logistic Regression', 'ML Tuyến tính (Linear)', lr_params, lr_train_time, lr_probs, lr_auc, optimal_thresholds['Logistic Regression'], 'Cao (Hệ số hồi quy)'),
    ('Decision Tree', 'Cây quyết định đơn lẻ', f'{dt_nodes} nút', dt_train_time, dt_probs, dt_auc, optimal_thresholds['Decision Tree'], 'Rất cao (Luật rẽ nhánh)'),
    ('Random Forest', 'Ensemble 100 Cây', f'{rf_total_nodes:,} nút', rf_train_time, rf_probs, rf_auc, optimal_thresholds['Random Forest'], 'Trung bình (Feature Importance)'),
    ('Deeper DL Scratch', 'Mạng nơ-ron 3 lớp ẩn (14 → 64 → 32 → 16 → 1)', f'{dl_params:,} trọng số', dl_train_time, dl_probs, dl_auc, optimal_thresholds['Deeper DL Scratch'], 'Thấp (Mạng nơ-ron phi tuyến)')
]

def_confusion_matrices = []
opt_confusion_matrices = []
comparison_metrics_list = []

for name, m_type, n_params, t_train, te_probs, auc, opt_t, interp in m_configs:
    # 1. Ngưỡng mặc định 0.50
    p_def = (te_probs >= 0.50).astype(int)
    cm_def = confusion_matrix(y_test, p_def)
    def_confusion_matrices.append(cm_def)
    acc_def = accuracy_score(y_test, p_def)
    prec_def = precision_score(y_test, p_def, zero_division=0)
    rec_def = recall_score(y_test, p_def, zero_division=0)
    f1_def = f1_score(y_test, p_def, zero_division=0)
    fn_def = int(cm_def[1, 0])
    
    # 2. Ngưỡng tối ưu
    p_opt = (te_probs >= opt_t).astype(int)
    cm_opt = confusion_matrix(y_test, p_opt)
    opt_confusion_matrices.append(cm_opt)
    acc_opt = accuracy_score(y_test, p_opt)
    prec_opt = precision_score(y_test, p_opt, zero_division=0)
    rec_opt = recall_score(y_test, p_opt, zero_division=0)
    f1_opt = f1_score(y_test, p_opt, zero_division=0)
    fn_opt = int(cm_opt[1, 0])
    
    comparison_metrics_list.append({
        'name': name,
        'def': (acc_def, prec_def, rec_def, f1_def, fn_def),
        'opt': (acc_opt, prec_opt, rec_opt, f1_opt, fn_opt),
        'delta_fn': fn_def - fn_opt
    })
    
    models_summary.append({
        'Mô hình': name,
        'Loại mô hình': m_type,
        'Số tham số': str(n_params),
        'Thời gian Train (s)': f'{t_train:.3f}',
        'Ngưỡng tối ưu': f'{opt_t:.2f}',
        'Recall (0.50)': f'{rec_def*100:.2f}%',
        'Recall (Opt)': f'{rec_opt*100:.2f}%',
        'F1-Score (0.50)': f'{f1_def*100:.2f}%',
        'F1-Score (Opt)': f'{f1_opt*100:.2f}%',
        'Accuracy (Opt)': f'{acc_opt*100:.2f}%',
        'ROC-AUC': f'{auc:.4f}',
        'Số ca FN (0.50)': f'{fn_def:,} ca',
        'Số ca FN (Opt)': f'{fn_opt:,} ca',
        'FN cứu được': f'-{fn_def - fn_opt} ca',
        'Tính giải thích': interp
    })

with open(os.path.join(REPORTS_DIR, 'metrics_comparison_diabetes_large.json'), 'w', encoding='utf-8') as f:
    json.dump(models_summary, f, ensure_ascii=False, indent=4)

print(f"✅ Đã lưu kết quả đối chuẩn tinh chỉnh ngưỡng vào: {os.path.join(REPORTS_DIR, 'metrics_comparison_diabetes_large.json')}")
"""
nb["cells"][32]["source"] = [cell32_code]

# Cell 33 Code: Biểu đồ cột 2 Subplots (Before vs After)
cell33_code = """# Biểu đồ cột đối chuẩn đa chỉ số: SO SÁNH TRỰC TIẾP NGƯỠNG MẶC ĐỊNH 0.50 VS NGƯỠNG TỐI ƯU
fig, axes = plt.subplots(1, 2, figsize=(18, 6))

m_names = ['Logistic Reg', 'Decision Tree', 'Random Forest', 'Deeper DL']
x = np.arange(len(m_names))
w = 0.20

# Subplot 1: Recall và F1-Score (0.50 vs Tối ưu)
rec_defs = [m['def'][2]*100 for m in comparison_metrics_list]
rec_opts = [m['opt'][2]*100 for m in comparison_metrics_list]
f1_defs = [m['def'][3]*100 for m in comparison_metrics_list]
f1_opts = [m['opt'][3]*100 for m in comparison_metrics_list]

rects1 = axes[0].bar(x - 1.5*w, rec_defs, w, label='Recall (Ngưỡng 0.50)', color='#93c5fd', edgecolor='black', hatch='//')
rects2 = axes[0].bar(x - 0.5*w, rec_opts, w, label='Recall (Ngưỡng Tối ưu)', color='#1d4ed8', edgecolor='black')
rects3 = axes[0].bar(x + 0.5*w, f1_defs, w, label='F1-Score (Ngưỡng 0.50)', color='#fed7aa', edgecolor='black', hatch='//')
rects4 = axes[0].bar(x + 1.5*w, f1_opts, w, label='F1-Score (Ngưỡng Tối ưu)', color='#ea580c', edgecolor='black')

for rect in rects1 + rects2 + rects3 + rects4:
    h = rect.get_height()
    axes[0].annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                     xytext=(0, 3), textcoords="offset points", ha='center', fontsize=8, fontweight='bold')

axes[0].set_xticks(x)
axes[0].set_xticklabels(m_names, fontsize=11, fontweight='bold')
axes[0].set_ylabel('Phần trăm (%)', fontsize=11, fontweight='bold')
axes[0].set_ylim(0, 105)
axes[0].set_title('(A) So Sánh Độ Nhạy (Recall) & F1-Score Trước vs Sau Tinh Chỉnh', fontsize=12, fontweight='bold', pad=12)
axes[0].grid(True, linestyle='--', alpha=0.5, axis='y')
axes[0].legend(loc='lower right', framealpha=0.95, fontsize=9.5)

# Subplot 2: Số ca bỏ sót bệnh (False Negatives - FN): 0.50 vs Tối ưu
fn_defs = [m['def'][4] for m in comparison_metrics_list]
fn_opts = [m['opt'][4] for m in comparison_metrics_list]
w2 = 0.35

rects_fn1 = axes[1].bar(x - w2/2, fn_defs, w2, label='Số ca bỏ sót FN (Ngưỡng 0.50)', color='#ef4444', edgecolor='black', alpha=0.85)
rects_fn2 = axes[1].bar(x + w2/2, fn_opts, w2, label='Số ca bỏ sót FN (Ngưỡng Tối ưu)', color='#10b981', edgecolor='black', alpha=0.85)

for i in range(len(m_names)):
    axes[1].annotate(f'{fn_defs[i]:,}', (x[i] - w2/2, fn_defs[i] + 8), ha='center', fontsize=9, fontweight='bold')
    axes[1].annotate(f'{fn_opts[i]:,}', (x[i] + w2/2, fn_opts[i] + 8), ha='center', fontsize=9, fontweight='bold')
    # Vẽ delta giảm
    delta = fn_defs[i] - fn_opts[i]
    if delta > 0:
        axes[1].annotate(f'Giảm {delta} ca', (x[i], max(fn_defs[i], fn_opts[i]) + 35),
                         ha='center', fontsize=9, fontweight='bold', color='#047857',
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='#ecfdf5', edgecolor='#10b981', alpha=0.9))

axes[1].set_xticks(x)
axes[1].set_xticklabels(m_names, fontsize=11, fontweight='bold')
axes[1].set_ylabel('Số ca bệnh bị bỏ sót (False Negatives)', fontsize=11, fontweight='bold')
axes[1].set_ylim(0, max(fn_defs) + 80)
axes[1].set_title('(B) Đánh Giá Mức Độ Phát Hiện Ca Bệnh (Giảm False Negatives)', fontsize=12, fontweight='bold', pad=12)
axes[1].grid(True, linestyle='--', alpha=0.5, axis='y')
axes[1].legend(loc='lower right', framealpha=0.95, fontsize=9.5)

plt.tight_layout()
fig_cmp_path = os.path.join(FIGURES_DIR, 'fig06_diabetes_large_model_comparison.png')
plt.savefig(fig_cmp_path, dpi=300, bbox_inches='tight')
plt.show()
print(f"✅ Đã xuất biểu đồ đối chuẩn so sánh trước & sau tinh chỉnh vào: {fig_cmp_path}")
"""
nb["cells"][33]["source"] = [cell33_code]

# Cell 34 Code: Ma trận nhầm lẫn 2x4 (Hàng 1 Ngưỡng 0.50, Hàng 2 Ngưỡng Tối ưu)
cell34_code = """# Vẽ Ma trận nhầm lẫn chuẩn hóa: HÀNG 1 (NGƯỠNG 0.50) VS HÀNG 2 (NGƯỠNG TỐI ƯU)
fig, axes = plt.subplots(2, 4, figsize=(22, 10))
class_names = ['Âm tính (0)', 'Dương tính (1)']

for i in range(4):
    name = m_configs[i][0]
    opt_t = optimal_thresholds[name]
    
    # Hàng 1: Ngưỡng 0.50
    cm_def = def_confusion_matrices[i]
    cm_def_norm = cm_def.astype('float') / cm_def.sum(axis=1)[:, np.newaxis] * 100.0
    axes[0, i].imshow(cm_def_norm, interpolation='nearest', cmap=plt.cm.Reds, vmin=0, vmax=100)
    axes[0, i].set_title(f"{name} (Ngưỡng 0.50)\\n[Bỏ sót FN: {cm_def[1, 0]:,} ca]", fontsize=11, fontweight='bold', pad=8)
    
    # Hàng 2: Ngưỡng tối ưu
    cm_opt = opt_confusion_matrices[i]
    cm_opt_norm = cm_opt.astype('float') / cm_opt.sum(axis=1)[:, np.newaxis] * 100.0
    axes[1, i].imshow(cm_opt_norm, interpolation='nearest', cmap=plt.cm.Blues, vmin=0, vmax=100)
    axes[1, i].set_title(f"{name} (Tối ưu t={opt_t:.2f})\\n[Bỏ sót FN: {cm_opt[1, 0]:,} ca | Giảm -{cm_def[1, 0] - cm_opt[1, 0]} ca]", fontsize=11, fontweight='bold', pad=8)

for r in range(2):
    for c in range(4):
        ax = axes[r, c]
        ax.set_xticks([0, 1])
        ax.set_xticklabels(class_names, fontsize=9)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(class_names, fontsize=9)
        
        cm_data = def_confusion_matrices[c] if r == 0 else opt_confusion_matrices[c]
        cm_pct = cm_data.astype('float') / cm_data.sum(axis=1)[:, np.newaxis] * 100.0
        thresh = cm_pct.max() / 2.0
        for ro in range(2):
            for co in range(2):
                cnt = cm_data[ro, co]
                pct = cm_pct[ro, co]
                ax.text(co, ro, f"{cnt:,}\\n({pct:.1f}%)",
                        ha="center", va="center",
                        color="white" if pct > thresh else "black",
                        fontsize=10, fontweight='bold')
        if c == 0:
            ax.set_ylabel(f"{'HÀNG 1: NGƯỠNG 0.50' if r == 0 else 'HÀNG 2: NGƯỠNG TỐI ƯU'}\\n\\nNhãn thực tế", fontsize=10, fontweight='bold')
        ax.set_xlabel('Nhãn dự đoán', fontsize=10, fontweight='bold')

plt.suptitle("ĐỐI CHUẨN MA TRẬN NHẦM LẪN (CONFUSION MATRICES): NGƯỠNG MẶC ĐỊNH 0.50 VS NGƯỠNG TỐI ƯU", fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
fig_cfm_path = os.path.join(FIGURES_DIR, 'fig07_diabetes_large_confusion_matrices.png')
plt.savefig(fig_cfm_path, dpi=300, bbox_inches='tight')
plt.show()
print(f"✅ Đã xuất 8 ma trận nhầm lẫn so sánh trực tiếp trước & sau vào: {fig_cfm_path}")
"""
nb["cells"][34]["source"] = [cell34_code]

with open(NB_PATH, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Đã cập nhật code trước và sau tinh chỉnh cho cells 32, 33, 34!")
