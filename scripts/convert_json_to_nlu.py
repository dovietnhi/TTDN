# import json
# from collections import defaultdict

# # Đọc file JSON
# with open("chat_data.json", "r", encoding="utf-8") as f:
#     conversations = json.load(f)

# # Gom các câu người dùng theo intent
# intent_examples = defaultdict(set)

# for convo in conversations:
#     for msg in convo:
#         if msg.get("sender") == "user" and msg.get("intent"):
#             text = msg["text"].strip()
#             intent = msg["intent"].strip()
#             # Bỏ qua các tin kiểu '/intent' (chỉ là lệnh, không phải ví dụ thực)
#             if text.startswith("/"):
#                 continue
#             intent_examples[intent].add(text)

# # Ghi ra file nlu.yml
# with open("nlu.yml", "w", encoding="utf-8") as f:
#     f.write('version: "3.1"\n')
#     f.write('nlu:\n')
#     for intent, examples in intent_examples.items():
#         f.write(f"  - intent: {intent}\n")
#         f.write("    examples: |\n")
#         for ex in sorted(examples):
#             f.write(f"      - {ex}\n")
#         f.write("\n")

# print("✅ Đã tạo file nlu.yml thành công!")
