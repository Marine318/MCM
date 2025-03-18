import csv


# 读取第一个CSV文件并返回 u, v, osmid, length, width 的映射
def read_first_csv(file_path):
    u_v_length_width_dict = {}  # 用来存储 (u, v) -> (length, width)

    with open(file_path, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row['u']
            v = row['v']
            length = row['length']
            width = row['width']
            u_v_length_width_dict[(u, v)] = (length, width)  # 存储 (u, v) -> (length, width)

    return u_v_length_width_dict


# 读取第二个CSV文件并将length和width填到后面
def merge_csvs(edge_file, u_v_length_width_dict, output_file):
    with open(edge_file, mode='r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames + ['length', 'width']  # 添加length和width列

        with open(output_file, mode='w', newline='') as out_f:
            writer = csv.DictWriter(out_f, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                u = row['u']  # 第二个CSV文件中的起始节点标号
                v = row['v']  # 第二个CSV文件中的终止节点标号

                # 判断第一个CSV中的 (u, v) 是否存在
                if (u, v) in u_v_length_width_dict:
                    # 获取 (u, v) 对应的length和width
                    length, width = u_v_length_width_dict[(u, v)]
                    row['length'] = length
                    row['width'] = width
                else:
                    row['length'] = ''
                    row['width'] = ''

                writer.writerow(row)


# 主程序
first_csv_file = '2025_Problem_D_Data/edges_all.csv'  # 第一个CSV文件路径
second_csv_file = 'edge_list_1.csv'  # 第二个CSV文件路径
output_file = 'output.csv'  # 输出文件路径

# 读取第一个CSV文件的 (u, v) -> (length, width)
u_v_length_width_dict = read_first_csv(first_csv_file)

# 合并数据到第二个CSV文件
merge_csvs(second_csv_file, u_v_length_width_dict, output_file)
