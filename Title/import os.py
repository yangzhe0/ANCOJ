import os
import chardet

def extract_and_combine_html_content(folder_path, output_file):
    if not os.path.exists(folder_path):
        print("指定的文件夹不存在！")
        return

    html_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".html")]
    if not html_files:
        print("指定文件夹中没有HTML文件！")
        return

    combined_content = ""

    for file_path in html_files:
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                encoding = chardet.detect(raw_data)['encoding']
                file_content = raw_data.decode(encoding or 'utf-8', errors='replace')
                # 查找"Format."的位置并截取之后的内容
                format_start = file_content.find('Format.')
                if format_start != -1:
                    format_start += len('Format.')
                    lines = file_content[format_start:].strip().split('\n')
                    # 只在第一行添加两个空格
                    first_line = '  ' + lines[0] if lines else ''
                    remaining_lines = '\n'.join(lines[1:])
                    file_content = first_line + '\n' + remaining_lines

                    # 检测是否有超过四个连续的'-'，如果有，则截断内容
                    if '----' in file_content:
                        file_content = file_content.split('----')[0]

                    combined_content += f"### {os.path.splitext(os.path.basename(file_path))[0]}\n{file_content}\n\n"
                else:
                    print(f"No 'Format.' field found in file: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"An error occurred while processing file {os.path.basename(file_path)}: {e}")

    # 将合并后的内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as output:
        output.write(combined_content)

    print(f"All HTML content has been combined into '{output_file}'.")

# 使用示例
folder_path = './Data/J'  # 替换为你的HTML文件所在的文件夹路径
output_file = 'combined_html_content.md'  # 输出文件的路径和文件名
extract_and_combine_html_content(folder_path, output_file)
