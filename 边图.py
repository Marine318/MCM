import csv
from collections import defaultdict


# 读取第一个CSV文件并构建两个字典
def read_node_csv(node_file):
    node_list = []  # 存储节点信息，(osmid, {'经纬度': (x, y), '其他信息': [...]})
    node_dict_2 = defaultdict(list)  # (x, y) -> osmid

    with open(node_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            osmid = row['osmid']
            x = float(row['x'])
            y = float(row['y'])

            # 存储节点信息
            node_list.append((osmid, {'经纬度': (x, y), '其他信息': []}))  # 其他信息可以继续添加
            node_dict_2[(x, y)].append(osmid)

    return node_list, node_dict_2


# 读取第二个CSV文件并构建边字典
def read_edge_csv(edge_file, node_dict_2):
    edge_list = []  # 存储边信息，(osmid, {'方向': direction, '几何形状': geometry, '起始节点': start, '终止节点': end, '其他信息': [...]})
    reverse_edge_dict = defaultdict(list)  # (start_osmid, end_osmid) -> [(osmid, reversed, geometry)]

    with open(edge_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            osmid = row['osmid']
            reversed_flag = row['reversed']  # 获取原始的reversed列

            # 解析reversed的值
            if reversed_flag == 'FALSE':
                direction = 1  # 正向，标记为1
            elif reversed_flag == 'TRUE':
                direction = 2  # 反向，标记为2
            elif reversed_flag == '[False, True]':
                direction = 3  # 双向，标记为3
            else:
                # 如果遇到不符合的值，可以考虑抛出异常或者给一个默认值
                print(f"警告：无法识别的reversed值: {reversed_flag}")
                continue  # 跳过这条记录，或者你可以选择其他处理方式

            geometry = row['geometry']
            points = geometry[geometry.index('(') + 1:geometry.index(')')].split(',')
            start_x, start_y = map(float, points[0].strip().split())
            end_x, end_y = map(float, points[-1].strip().split())

            # 获取起始和终止节点的osmid
            start_osmid = None
            end_osmid = None
            if (start_x, start_y) in node_dict_2:
                start_osmid = node_dict_2[(start_x, start_y)][0]  # 取第一个osmid
            if (end_x, end_y) in node_dict_2:
                end_osmid = node_dict_2[(end_x, end_y)][0]  # 取第一个osmid

            if start_osmid and end_osmid:
                geometry_points = [(float(p.split()[0]), float(p.split()[1])) for p in points]  # 将geometry转换为元组列表
                edge_list.append((osmid,
                                  {'方向': direction, '几何形状': geometry_points, '起始节点': (start_x, start_y),
                                   '终止节点': (end_x, end_y), '其他信息': []}))
                reverse_edge_dict[(end_osmid, start_osmid)].append((osmid, direction, geometry))

    return edge_list, reverse_edge_dict


# 将点列表保存到CSV文件
def save_node_list_to_csv(node_list, filename):
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(['osmid', 'x', 'y', '其他信息'])
        for osmid, attributes in node_list:
            x, y = attributes['经纬度']
            other_info = ', '.join(map(str, attributes['其他信息']))  # 其他信息如果有多个，合并为字符串
            writer.writerow([osmid, x, y, other_info])


# 将边列表保存到CSV文件
def save_edge_list_to_csv(edge_list, filename, node_dict_2):
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(
            ['osmid', '方向', '起始节点', '起始节点标号', '终止节点', '终止节点标号', '几何形状', '其他信息'])
        for osmid, edge_info in edge_list:
            direction = edge_info['方向']
            start_x, start_y = edge_info['起始节点']
            end_x, end_y = edge_info['终止节点']

            # 获取起始节点和终止节点的标号 (osmid)
            start_osmid = node_dict_2[(start_x, start_y)][0]  # 假设每个坐标只对应一个节点
            end_osmid = node_dict_2[(end_x, end_y)][0]  # 假设每个坐标只对应一个节点

            # 格式化几何形状为字符串
            geometry = '; '.join([f"({x},{y})" for x, y in edge_info['几何形状']])
            other_info = ', '.join(map(str, edge_info['其他信息']))  # 其他信息如果有多个，合并为字符串

            # 保存数据到CSV
            writer.writerow(
                [osmid, direction, f"({start_x},{start_y})", start_osmid, f"({end_x},{end_y})", end_osmid, geometry,
                 other_info])


# 主程序
node_file = '2025_Problem_D_Data/删去重复值后的nodes_all.csv'  # 节点数据文件路径
edge_file = '2025_Problem_D_Data/edges_all.csv'  # 边数据文件路径

# 读取数据
node_list, node_dict_2 = read_node_csv(node_file)
edge_list, reverse_edge_dict = read_edge_csv(edge_file, node_dict_2)

# 保存到CSV文件
save_node_list_to_csv(node_list, 'node_list_1.csv')  # 保存点列表
save_edge_list_to_csv(edge_list, 'edge_list_1.csv',node_dict_2)  # 保存边列表
