import time
import re
from openai import OpenAI
import os
from dotenv import load_dotenv

def choose(query, A, B, C, D, dropdown):
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
        {"role": "system", "content": "你是一个专业的选择题评估助手。你的任务是根据以下标准判断四个选项中哪一个是对的：\n1. 准确性：选项是否准确无误地回答了问题。\n2. 相关性：选项是否与问题紧密相关。\n3. 逻辑性：选项的解释是否合乎逻辑。\n\n你的选择只能是大写字母A、B、C、D中的一个。请按以下格式输出：(你的选项)：阐述你的理由（不少于20字）。\n\n例如：\n(A)：选项A最符合问题的要求，因为它准确地回答了问题，并且提供了合理的解释。"},
        {"role": "user", "content": f"问题是: {query}\n选项A: {A}\n选项B: {B}\n选项C: {C}\n选项D: {D}\n请根据上述标准评判并回答：" }
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

    return extract_mark(result)
    

def chat(query, dropdown):
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
            {"role": "system", "content": "你是一个专业的问答助手。你的任务是对以下问题作出回答。请确保答案满足以下要求：\n1. 答案必须超过20字。\n2. 回答要准确、简洁且具有逻辑性。\n3. 如果可能，请提供具体的例子或解释来支持你的回答。\n请按照以下格式输出：[答案内容]"},
            {"role": "user", "content": f"问题是: {query}\n请根据上述要求回答：" }
        ],
        temperature=0.3,
        stream=False,
    )
    time.sleep(1)
    
    result = completion.choices[0].message.content
    result = result.replace('\n', '')
    print(result)
    
    if dropdown == 'DEEPSEEK':
        return re.split(r'</think>\s*', result, maxsplit=1)[1]
    else:
        return result

def extract_mark(response):
    # 找到第一个字母
    letter_match = re.search(r'[A-Z]', response)
    if letter_match:
        letter = letter_match.group()
        print(letter)
        stop = 0
    else:
        letter = '-FFFF'
        print("未找到字母")
        stop = 1
    
    # 找到结构 ":" 或 "：" 并提取其后面的内容直到字符串结束
    reason_match = re.search(r'[：:]\s*(.*)', response)
    if reason_match:
        reason = reason_match.group(1)
        print(reason)
        stop = 0
    else:
        reason = "-FFFF"
        print("未找到内容")
        stop = 1
        
    
    return letter, reason, stop
