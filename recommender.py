from knowledge_base import MEDICINE_KNOWLEDGE, SPECIAL_CONTRAINDICATIONS

def calculate_match_score(user_keywords, disease_symptoms):
    """计算用户症状与病症的匹配度得分"""
    match_count = 0
    for keyword in user_keywords:
        if keyword in disease_symptoms:
            match_count += 1
    return match_count / len(disease_symptoms) if len(disease_symptoms) > 0 else 0

def match_diseases(user_keywords):
    """匹配最可能的病症，按匹配度降序排列"""
    disease_scores = []
    for disease_name, disease_info in MEDICINE_KNOWLEDGE.items():
        score = calculate_match_score(user_keywords, disease_info["symptoms"])
        if score > 0:
            disease_scores.append((disease_name, score))
    
    # 按匹配度从高到低排序
    disease_scores.sort(key=lambda x: x[1], reverse=True)
    return disease_scores

def filter_medicines(medicines, special_people):
    """根据特殊人群过滤禁忌药品"""
    if not special_people or special_people not in SPECIAL_CONTRAINDICATIONS:
        return medicines
    
    forbidden_medicines = SPECIAL_CONTRAINDICATIONS[special_people]
    filtered = []
    for med in medicines:
        if med["name"] not in forbidden_medicines:
            filtered.append(med)
    return filtered

def generate_recommendation(user_keywords, special_people=None):
    """生成最终用药推荐结果"""
    # 匹配病症
    matched_diseases = match_diseases(user_keywords)
    
    if not matched_diseases:
        return {
            "status": "no_match",
            "message": "抱歉，未识别您描述的症状。\n⚠️ 重要提示：本系统仅为课程实训项目，不能替代专业医师诊断，建议您及时前往医院就诊。"
        }
    
    # 取匹配度最高的病症
    top_disease, top_score = matched_diseases[0]
    disease_info = MEDICINE_KNOWLEDGE[top_disease]
    
    # 过滤特殊人群禁忌药品
    available_medicines = filter_medicines(disease_info["medicines"], special_people)
    
    if not available_medicines:
        return {
            "status": "no_medicine",
            "disease": top_disease,
            "message": f"根据您的症状，初步判断为{top_disease}。\n⚠️ 由于您是{special_people}，系统中无适合您的非处方药品推荐，强烈建议您咨询专业医师。"
        }
    
    return {
        "status": "success",
        "disease": top_disease,
        "match_score": round(top_score * 100, 1),
        "medicines": available_medicines,
        "special_tips": disease_info["special_tips"]
    }