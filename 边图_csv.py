import csv
import matplotlib.pyplot as plt

# 读取边列表CSV文件
def read_edge_csv(edge_file):
    edge_list = []  # 存储边信息，(osmid, {'方向': direction, '几何形状': geometry, '起始节点': start, '终止节点': end, '其他信息': [...]})

    with open(edge_file, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            osmid = row['osmid']
            direction = int(row['方向'])  # 转换为整数
            start_node = row['起始节点']
            end_node = row['终止节点']
            geometry = row['几何形状']

            # 解析几何形状（转换为经纬度点的列表）
            points = geometry.split('; ')  # 假设每个点用分号分隔
            geometry_points = [(float(p.split(',')[0][1:]), float(p.split(',')[1][:-1])) for p in points]  # 去除括号并分割经纬度

            start_x, start_y = geometry_points[0]
            end_x, end_y = geometry_points[-1]

            edge_list.append((osmid,
                              {'方向': direction,
                               '几何形状': geometry_points,
                               '起始节点': (start_x, start_y),
                               '终止节点': (end_x, end_y),
                               '其他信息': []}))

    return edge_list

# 绘制网络图并标出节点
def plot_network_with_edges(edge_list):
    fig, ax = plt.subplots(figsize=(100, 100))

    # 绘制边（通过连接起始节点和终止节点的几何形状）
    for osmid, edge_info in edge_list:
        geometry_points = edge_info['几何形状']
        lons, lats = zip(*geometry_points)  # 解压经纬度点
        ax.plot(lons, lats, color='blue', linewidth=1)  # 绘制路径（边）

        # 标出起始和终止节点
        start_x, start_y = edge_info['起始节点']
        end_x, end_y = edge_info['终止节点']

        # 标出起始节点
        ax.scatter(start_x, start_y, color='green', s=5, zorder=5)  # 用绿色标出起始节点
        # ax.text(start_x, start_y, f"Start", fontsize=12, ha='right', color='green')

        # 标出终止节点
        ax.scatter(end_x, end_y, color='red', s=5, zorder=5)  # 用红色标出终止节点
        # ax.text(end_x, end_y, f"End", fontsize=12, ha='right', color='red')

    ax.set_title("Network Visualization")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.show()

# 主程序
edge_file = 'edge_list.csv'  # 你已经生成的边列表CSV文件路径

# 读取边数据
edge_list = read_edge_csv(edge_file)

# 可视化网络图（只使用边数据）
plot_network_with_edges(edge_list)
