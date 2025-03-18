import pandas as pd
import matplotlib.pyplot as plt

# 读取CSV文件
file_path = '2025_Problem_D_Data/Bus_Stops.csv'  # 替换为你的文件路径
data = pd.read_csv(file_path)

# 检查是否包含所需列
if {'X', 'Y', 'stop_name'}.issubset(data.columns):
    # 提取列
    x = data['X']
    y = data['Y']

    # 绘制图形
    plt.figure(figsize=(10, 8))
    plt.scatter(x, y, c='blue', marker='o', label='Stops')

    # 图形设置
    plt.title('2D Plane of Stops')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("CSV 文件中缺少所需的列：X, Y, stop_name")
