import os

def check_assignments(assignment_folder, criteria_file):
    # 读取检测点
    with open(criteria_file, 'r') as file:
        criteria = file.readlines()
        criteria = [line.strip().lower() for line in criteria]  # 去除空格并转换为小写

    # 准备结果列表
    results = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(assignment_folder):
        if filename.endswith('.txt'):
            student_name, student_id = filename.split('.')[0].split('(')
            student_id = student_id.rstrip(')')

            # 初始化分数
            score = 0

            # 读取文件内容
            with open(os.path.join(assignment_folder, filename), 'r') as file:
                content = file.read().lower()  # 转换为小写以忽略大小写差异

            # 检查每个检测点
            for criterion in criteria:
                if criterion in content:
                    score += 1  # 如果检测点在内容中，增加分数

            # 将结果添加到列表中
            results.append(f"{filename} {score}")

    # 将结果写入文件
    with open('results.txt', 'w') as result_file:
        for result in results:
            result_file.write(result + '\n')

# 使用示例
assignment_folder = 'path_to_assignment_folder'  # 替换为学生作业文件夹的路径
criteria_file = 'criteria.txt'  # 替换为你的检测点文件的路径
check_assignments(assignment_folder, criteria_file)
