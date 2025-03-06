import pandas as pd
import time
from model_ask import chat

def process_file(file_path, dropdown, socketio, filename, answer_path):  
    df = pd.read_excel(file_path, header=0)  # header=0 表示第一行为列名

    if '问题' not in df.columns:
        df['问题'] = None
    if '模型答案(文字题)' not in df.columns:
        df['模型答案(文字题)'] = None
    if '标准答案(文字题)' not in df.columns:
        df['标准答案(文字题)'] = None 
    if '选项A' not in df.columns:
        df['选项A'] = None

    print(dropdown)
    
    total_questions = len(df)
    for index, row in df.iterrows():
        if pd.notna(row['问题']) and pd.isna(row['模型答案(文字题)']) and pd.isna(row['选项A']):  
            question = row['问题']
            time.sleep(1)
            response = chat(question, dropdown)
            print("")
            
            df.at[index, '模型答案(文字题)'] = response
            
            progress = (index + 1) / total_questions * 100
            socketio.emit('progress', {'filename': filename, 'progress': progress})
        else:
            if index == 0:
                error_message = f"文件格式！您所选择的操作与您的文件格式不匹配。"
            else:
                error_message = f"文件格式: 第 {index + 1} 行数据不完整。"
            
            socketio.emit('error', {'message': error_message})
            raise ValueError(error_message)  # 抛出异常以停止程序

    df.to_excel(answer_path, sheet_name='数据', index=False)
    
    socketio.emit('status', {'message': '回答成功!'})