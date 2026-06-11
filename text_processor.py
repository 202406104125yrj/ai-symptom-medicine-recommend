import jieba

def clean_text(text):
    """清洗输入文本：去除空格、特殊字符，统一为小写"""
    text = text.strip()
    text = text.replace("，", " ").replace("。", " ").replace("、", " ")
    text = text.replace("！", " ").replace("？", " ")
    return text.lower()

def extract_keywords(text, symptom_list):
    """
    从用户输入中提取症状关键词
    基础版：字符串匹配；进阶版：jieba分词匹配
    """
    cleaned_text = clean_text(text)
    keywords = []
    
    # 进阶版：使用jieba分词（推荐，准确率更高）
    words = jieba.lcut(cleaned_text)
    for word in words:
        if word in symptom_list and word not in keywords:
            keywords.append(word)
    
    # 基础版：直接字符串包含匹配（不用jieba时取消注释下面代码，注释上面）
    # for symptom in symptom_list:
    #     if symptom in cleaned_text and symptom not in keywords:
    #         keywords.append(symptom)
    
    return keywords

def get_all_symptoms(knowledge_base):
    """从知识库中提取所有症状关键词"""
    all_symptoms = []
    for disease in knowledge_base.values():
        all_symptoms.extend(disease["symptoms"])
    return list(set(all_symptoms))