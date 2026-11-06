import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['OMP_NUM_THREADS'] = '1'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys
import io
import time
import base64
import json
import nbformat as nbf

notebook_path = "src/dia_mas/notebooks/01_diabetes_model_training_and_optimization.ipynb"
print(f"Bắt đầu thực thi và render kết quả vào Notebook: {notebook_path}")

with open(notebook_path, "r", encoding="utf-8") as f:
    nb = nbf.read(f, as_version=4)

global_scope = {
    '__name__': '__main__',
    '__file__': os.path.abspath(notebook_path),
}

# Override display function to print text/dataframes cleanly
def custom_display(*args, **kwargs):
    for arg in args:
        if hasattr(arg, 'to_string'):
            print(arg.to_string())
        elif hasattr(arg, '_repr_html_'):
            # Pandas Styler or similar
            if hasattr(arg, 'data'):
                print(arg.data.to_string())
            else:
                print(str(arg))
        else:
            print(str(arg))

global_scope['display'] = custom_display

execution_count = 1
total_code_cells = sum(1 for c in nb.cells if c.cell_type == 'code')
current_code_idx = 0

start_total_time = time.time()

for idx, cell in enumerate(nb.cells):
    if cell.cell_type != 'code':
        continue
        
    current_code_idx += 1
    print(f"\n[{current_code_idx:02d}/{total_code_cells:02d}] Đang thực thi Cell {idx+1}...")
    
    # Capture stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    sys.stdout = captured_stdout
    sys.stderr = captured_stderr
    
    cell_start_time = time.time()
    try:
        exec(cell.source, global_scope)
    except Exception as e:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        print(f"❌ LỖI TẠI CELL {idx+1}: {e}")
        import traceback
        traceback.print_exc()
        raise e
        
    printed_out = captured_stdout.getvalue()
    printed_err = captured_stderr.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    
    cell_elapsed = time.time() - cell_start_time
    print(f"  ✓ Hoàn thành trong {cell_elapsed:.2f}s (Output: {len(printed_out)} chars)")
    
    # Construct cell outputs
    outputs = []
    if printed_out:
        outputs.append(nbf.v4.new_output(
            output_type='stream',
            name='stdout',
            text=printed_out
        ))
    if printed_err:
        outputs.append(nbf.v4.new_output(
            output_type='stream',
            name='stderr',
            text=printed_err
        ))
        
    # Capture any matplotlib figures
    for fig_num in plt.get_fignums():
        fig = plt.figure(fig_num)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', dpi=120)
        buf.seek(0)
        b64_data = base64.b64encode(buf.read()).decode('utf-8')
        outputs.append(nbf.v4.new_output(
            output_type='display_data',
            data={
                'image/png': b64_data,
                'text/plain': f"<Figure size {fig.get_size_inches()} with {len(fig.axes)} Axes>"
            }
        ))
    plt.close('all')
    
    cell.outputs = outputs
    cell.execution_count = execution_count
    execution_count += 1

total_elapsed = time.time() - start_total_time
print(f"\n==================================================================")
print(f"✓ TOÀN BỘ NOTEBOOK ĐÃ THỰC THI THÀNH CÔNG TRONG {total_elapsed:.2f} GIÂY!")
print(f"==================================================================")

# Write back executed notebook
with open(notebook_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"✓ Đã lưu Notebook có đầy đủ Output, Training Logs và Biểu Đồ tại:\n  -> {notebook_path}")
