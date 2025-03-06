import pandas as pd
import time
from model_ask import choose

def process_file(file_path, dropdown, socketio, filename, answer_path):
    df = pd.read_excel(file_path, header=0)  # header=0 表示第一行为列名

    if '问题' not in df.columns:
        df['问题'] = None
    if '选项A' not in df.columns:
        df['选项A'] = None
    if '选项B' not in df.columns:
        df['选项B'] = None
    if '选项C' not in df.columns:
        df['选项C'] = None
    if '选项D' not in df.columns:
        df['选项D'] = None
    if '模型答案' not in df.columns:
        df['模型答案'] = None
    if '标准答案' not in df.columns:
        df['标准答案'] = None
    if '结果' not in df.columns:
        df['结果'] = None
    if '理由' not in df.columns:
        df['理由'] = None

    print(dropdown)
    
    total_questions = len(df)
    stop_1 = 0
    for index, row in df.iterrows():
        if pd.notna(row['问题']) and pd.notna(row['选项A']) and pd.notna(row['选项B']) and pd.notna(row['选项C']) and pd.notna(row['选项D']) and pd.isna(row['模型答案']) and pd.isna(row['理由']):  
            question = row['问题']
            A = row['选项A']
            B = row['选项B']
            C = row['选项C']
            D = row['选项D']
            time.sleep(1)
            xuanxiang, liyou, stop = choose(question, A, B, C, D, dropdown)
            print("")
            
            if stop == 1:
                stop_1 = 1

            df.at[index, '模型答案'] = xuanxiang
            df.at[index, '理由'] = liyou
            
            # 更新进度
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
    
    if stop_1 == 1:  # 如果有停止标志，则发送停止信号
        socketio.emit('status', {'message': '回答中有错误，请检查结果！(-FFFF)'})
    else:
        socketio.emit('status', {'message': '回答成功!'})