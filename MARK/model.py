import time
import re
from openai import OpenAI
import os
from dotenv import load_dotenv

def chat(query, answer, dropdown):
    load_dotenv()
    
    api_key = os.getenv(dropdown+'_KEY')
    base_url = os.getenv(dropdown+'_URL')
    model_name = os.getenv(dropdown+'_NAME')

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
        {"role": "system", "content": "你是一个专业的回答质量评估助手。你的任务是根据以下标准对提供的答案进行评分：\n1. 准确性：回答是否准确无误。\n2. 完整性：回答是否涵盖了问题的所有要点。\n3. 清晰度：回答是否表达清晰、易于理解。\n4. 相关性：回答是否与问题紧密相关。\n5. 逻辑性：回答是否有条理、逻辑清晰。\n\n评分采取5档制（1-5），5分表示非常优秀，1分表示非常差。请按照以下格式输出：(分数)：理由，不少于20字。\n\n例如：\n(5)：回答准确、完整、清晰且逻辑性强，完全符合问题要求。"},
        {"role": "user", "content": f"问题是: {query}\n回答是: {answer}\n请根据上述标准对这个回答进行评分并阐述理由。"}
        ],
        temperature=0.3,
        stream=False,
    )
    time.sleep(1)
    
    result = completion.choices[0].message.content
    result = result.replace('\n', '')
    print(result)
    
    if dropdown == 'DEEPSEEK':
        result = re.split(r'</think>\s*', result, maxsplit=1)[1]

    return extract_score_and_reason(result)

def extract_score_and_reason(response):
    # 找到第一个阿拉伯数字
    score_match = re.search(r'\d+', response)
    if score_match:
        score = int(score_match.group())
        print(score)
        stop = 0
    else:
        score = -9999
        print("未找到数字")
        stop = 1
    
    # 找到结构 ":" 或 "：" 并提取其后面的内容直到字符串结束
    reason_match = re.search(r'[：:]\s*(.*)', response)
    if reason_match:
        reason = reason_match.group(1)
        print(reason)
        stop = 0
    else:
        reason = "-9999"
        print("未找到内容")
        stop = 1
    
    return score, reason, stop
