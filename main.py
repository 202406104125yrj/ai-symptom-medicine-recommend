from text_processor import extract_keywords, get_all_symptoms
from recommender import generate_recommendation
from history_manager import save_history, show_history
from knowledge_base import MEDICINE_KNOWLEDGE

def print_welcome():
    """打印欢迎界面"""
    print("="*60)
    print("        AI症状智能用药推荐系统（课程实训版）")
    print("="*60)
    print("⚠️ 重要声明：本系统仅为人工智能课程实训项目")
    print("   不具备医疗诊断资质，不能替代专业医师诊断与治疗")
    print("   如有身体不适，请及时前往正规医院就诊")
    print("="*60)
    print("使用说明：")
    print("1. 输入您的身体症状（如：感冒发烧流鼻涕）")
    print("2. 选择是否为特殊人群（孕妇/哺乳期/18岁以下等）")
    print("3. 输入 'history' 查看问诊历史")
    print("4. 输入 'quit' 退出系统")
    print("="*60)

def main():
    print_welcome()
    all_symptoms = get_all_symptoms(MEDICINE_KNOWLEDGE)
    
    while True:
        # 获取用户输入
        user_input = input("\n请输入您的症状：").strip()
        
        # 特殊命令处理
        if user_input.lower() == "quit":
            print("感谢使用，祝您身体健康！")
            break
        if user_input.lower() == "history":
            print("\n📋 问诊历史记录：")
            print(show_history())
            continue
        if not user_input:
            print("请输入有效的症状描述！")
            continue
        
        # 获取特殊人群信息
        special_input = input("是否为特殊人群？（孕妇/哺乳期/18岁以下/肝肾功能不全/糖尿病患者/否）：").strip()
        special_people = None
        if special_input in SPECIAL_CONTRAINDICATIONS.keys():
            special_people = special_input
        
        # 提取关键词并生成推荐
        keywords = extract_keywords(user_input, all_symptoms)
        result = generate_recommendation(keywords, special_people)
        
        # 输出结果
        print("\n" + "-"*60)
        if result["status"] == "success":
            print(f"🔍 初步诊断：{result['disease']}（匹配度：{result['match_score']}%）")
            print("\n💊 推荐用药：")
            for i, med in enumerate(result["medicines"], 1):
                print(f"\n{i}. {med['name']}")
                print(f"   用法用量：{med['usage']}")
                print(f"   禁忌人群：{', '.join(med['contraindication'])}")
                print(f"   不良反应：{med['adverse_reaction']}")
            print(f"\n💡 温馨提示：{result['special_tips']}")
            
            # 保存历史记录
            save_history(user_input, special_people, f"诊断：{result['disease']}，推荐用药：{[m['name'] for m in result['medicines']]}")
        
        elif result["status"] == "no_medicine":
            print(result["message"])
            save_history(user_input, special_people, result["message"])
        
        else:
            print(result["message"])
        
        print("-"*60)

if __name__ == "__main__":
    main()