import datetime

def save_history(symptoms, special_people, result):
    """保存问诊历史到本地文件"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    special = special_people if special_people else "普通人群"
    
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write("="*50 + "\n")
        f.write(f"问诊时间：{timestamp}\n")
        f.write(f"用户症状：{symptoms}\n")
        f.write(f"人群类型：{special}\n")
        f.write(f"诊断结果：{result}\n")
        f.write("="*50 + "\n\n")

def show_history():
    """显示所有问诊历史"""
    try:
        with open("history.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if not content:
                return "暂无问诊历史记录。"
            return content
    except FileNotFoundError:
        return "暂无问诊历史记录。"