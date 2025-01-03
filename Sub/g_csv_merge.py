import os
import pandas as pd

def merge_csv_files(folder_path, output_file):
    # 获取文件夹中的所有CSV文件
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return

    # 初始化一个空的DataFrame来存储合并后的数据
    merged_df = pd.DataFrame()
    total_fields = 0
    issue_details = []

    # 遍历每个CSV文件
    for csv_file in csv_files:
        try:
            file_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(file_path)

            # 添加文件名和行号列（确保类型一致）
            df['file_line'] = df.index + 2  # 行号从 2 开始
            df['file_line'] = df['file_line'].astype(str)  # 转换为字符串
            df['file_line'] = os.path.splitext(csv_file)[0] + '_' + df['file_line']

            # 确保所有DataFrame都有相同的列，缺失的列用NaN填充
            if not merged_df.empty:
                merged_df = pd.concat([merged_df, df], ignore_index=True, sort=False)
            else:
                merged_df = df
        except Exception as e:
            issue_details.append(f"File: {csv_file}, Error: {e}")
    
    # 更新列顺序，将 file_line 移动到第一列
    if 'file_line' in merged_df.columns:
        columns = ['file_line'] + [col for col in merged_df.columns if col != 'file_line']
        merged_df = merged_df[columns]

    # 将合并后的数据写入到输出文件中
    merged_df.to_csv(output_file, index=False)

    # 输出报告
    total_fields = len(merged_df.columns) if not merged_df.empty else 0
    print(f"Processed {len(csv_files)} files.")
    print(f"Merged fields: {total_fields}.")
    print(f"Encountered {len(issue_details)} issues.")
    if issue_details:
        print("Issues details:")
        for detail in issue_details:
            print(detail)

# 文件路径和输出路径
folder_path = './Result/final'
output_file = './Result/merged.csv'

merge_csv_files(folder_path, output_file)
