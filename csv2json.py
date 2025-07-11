import csv
import json

csv_path = './sample_labels.csv'  # 替换为你的 CSV 路径
train_json_path = './latex_ocr_train.json'
val_json_path = './latex_ocr_val.json'

def build_answer(disease_str):
    disease_list = disease_str.split("|")

    clean = lambda s: s.replace("_", " ").lower()
    disease_list = [clean(d) for d in disease_list]
    if len(disease_list) == 1:
        return f"This chest X-ray image shows {disease_list[0]}."
    else:
        return "This chest X-ray image shows " + ", ".join(disease_list[:-1]) + f", and {disease_list[-1]}."

# 读取 CSV，构造对话格式
conversations = []
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        image_path = f"sample/images/{row['Image Index']}"
        finding = row['Finding Labels']
        answer = build_answer(finding)
        conversations.append({
            "id": f"identity_{idx+1}",
            "conversations": [
                {"role": "user", "value": image_path},
                {"role": "assistant", "value": answer}
            ]
        })

# 动态划分训练集和验证集（80/20）
split_ratio = 0.8
split_index = int(len(conversations) * split_ratio)

train_conversations = conversations[:split_index]
val_conversations = conversations[split_index:]

# 保存 JSON 文件
with open(train_json_path, 'w', encoding='utf-8') as f:
    json.dump(train_conversations, f, ensure_ascii=False, indent=2)

with open(val_json_path, 'w', encoding='utf-8') as f:
    json.dump(val_conversations, f, ensure_ascii=False, indent=2)

print(f"✅ 已生成 {len(train_conversations)} 条训练数据，{len(val_conversations)} 条验证数据")
