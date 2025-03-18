import csv
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString

# 读取点数据并创建 GeoDataFrame
points = {}
osmid_count = 0  # 用于统计 osmid 的数量
with open('2025_Problem_D_Data/nodes_all.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        osmid = row['osmid']
        x = float(row['x'])
        y = float(row['y'])
        points[osmid] = Point(x, y)
        osmid_count += 1  # 每读一个 osmid，计数器加 1
    print(f"Loaded {osmid_count} points.")
    print(f"Type of points dictionary: {type(points)}")

# 读取路径数据并生成线数据
lines = []
path_count = 0  # 用于统计可视化路径的数量
with open('2025_Problem_D_Data/Edge_Names_With_Nodes.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        street_name = row['Street_Name']
        path_str = row['Nodes']

        # 解析路径数据（从字符串转换为列表）
        try:
            path_points = eval(path_str)  # 确保路径字符串能够正确解析
            # 检查路径数据是否是包含集合的列表
            if isinstance(path_points, list) and isinstance(path_points[0], set):
                # 如果是列表中的集合，提取集合并转换为列表
                path_points = [list(point_set) for point_set in path_points]
            else:
                print(f"Invalid path data format: {path_points}")
                continue
        except Exception as e:
            print(f"Error parsing path: {e}")
            continue

        # 提取路径的经纬度
        line_coords = []
        path_valid = True  # 标记路径是否有效

        # 检查路径中的所有点是否都存在于 points 字典中
        for osmid in path_points[0]:  # 只提取第一个集合的元素
            osmid_str = str(osmid)  # 强制将 osmid 转换为字符串（如果需要的话）
            point = points.get(osmid_str)  # 使用 get() 方法避免 KeyError
            if point:
                line_coords.append((point.x, point.y))
            else:
                print(f"Warning: osmid {osmid} not found in points")
                path_valid = False
                break  # 找到一个不存在的点，就跳过这条路径

        # 如果路径有效，则创建 LineString 并添加到 lines 列表
        if path_valid and len(line_coords) > 1:
            line = LineString(line_coords)
            lines.append(line)
            path_count += 1
            print(f"Added path: {line}")

print(f"Total valid paths added: {path_count}")

# 创建 GeoDataFrame 来保存线数据
gdf_lines = gpd.GeoDataFrame(geometry=lines)

# 创建 GeoDataFrame 来保存点数据
gdf_points = gpd.GeoDataFrame(geometry=list(points.values()))

# 可视化
fig, ax = plt.subplots(figsize=(10, 10))

# 绘制路径（线图层）
gdf_lines.plot(ax=ax, color='blue', linewidth=1)

# 绘制点（节点图层）
gdf_points.plot(ax=ax, color='red', markersize=2)

# 设置标题和标签
ax.set_title("Paths in Baltimore")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# 显示图像
plt.show()
