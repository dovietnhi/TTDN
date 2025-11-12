import os
import re
import subprocess
import matplotlib.pyplot as plt

# === 1. Đường dẫn và lệnh đánh giá ===
results_dir = "results"
log_path = os.path.join(results_dir, "evaluation.log")

os.makedirs(results_dir, exist_ok=True)

print("🚀 Đang chạy đánh giá mô hình hội thoại...")

# Chạy Rasa test core, ghi cả stdout và stderr vào log
with open(log_path, "w", encoding="utf-8") as f:
    subprocess.run(
        ["rasa", "test", "core", "--stories", "test_stories.yml", "--out", results_dir],
        stdout=f,
        stderr=subprocess.STDOUT,
        check=True
    )

# === 2. Đọc file log kết quả ===
if not os.path.exists(log_path):
    print("❌ Không tìm thấy file log. Kiểm tra lại quá trình đánh giá!")
    exit()

with open(log_path, "r", encoding="utf-8") as f:
    log_text = f.read()

# === 3. Debug log (xem nhanh 500 ký tự đầu/cuối) ===
print("==== Đầu file log ====")
print(log_text[:500])
print("==== Cuối file log ====")
print(log_text[-500:])

# === 4. Trích xuất số liệu bằng regex (không phân biệt hoa thường) ===
accuracy_list = re.findall(r"accuracy[: ]+([0-9.]+)", log_text, re.I)
precision_list = re.findall(r"precision[: ]+([0-9.]+)", log_text, re.I)
f1_list = re.findall(r"f1[- ]score[: ]+([0-9.]+)", log_text, re.I)
correct_list = re.findall(r"correct[: ]+(\d+)\s*/\s*(\d+)", log_text, re.I)

accuracy = float(accuracy_list[-1]) if accuracy_list else None
precision = float(precision_list[-1]) if precision_list else None
f1 = float(f1_list[-1]) if f1_list else None
correct = correct_list[-1] if correct_list else None

# === 5. In kết quả ra màn hình ===
print("\n📊 KẾT QUẢ ĐÁNH GIÁ HỘI THOẠI")
if correct:
    print(f"✅ Correct: {correct[0]} / {correct[1]}")
if accuracy is not None:
    print(f"🎯 Accuracy: {accuracy:.3f}")
if precision is not None:
    print(f"💡 Precision: {precision:.3f}")
if f1 is not None:
    print(f"🔥 F1-Score: {f1:.3f}")

# === 6. Vẽ biểu đồ ===
labels = []
values = []

if accuracy is not None:
    labels.append("Accuracy")
    values.append(accuracy)
if precision is not None:
    labels.append("Precision")
    values.append(precision)
if f1 is not None:
    labels.append("F1-score")
    values.append(f1)

if labels:
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color='skyblue')
    plt.ylim(0.0, 1.0)
    plt.title("📈 Hiệu suất mô hình hội thoại Rasa")
    plt.ylabel("Giá trị")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
else:
    print("⚠️ Không đủ dữ liệu để vẽ biểu đồ (thiếu tất cả các chỉ số).")

# === 7. In các hội thoại dự đoán sai ===
failed_path = os.path.join(results_dir, "failed_test_stories.yml")
if os.path.exists(failed_path):
    print("\n🚨 Các hội thoại mô hình dự đoán sai:")
    with open(failed_path, "r", encoding="utf-8") as f:
        for line in f:
            if "story:" in line or "action:" in line:
                print(line.strip())
else:
    print("\n✅ Không có hội thoại nào bị dự đoán sai!")

print("\n📁 Kiểm tra thêm chi tiết trong thư mục:", results_dir)
