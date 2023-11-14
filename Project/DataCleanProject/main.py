# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import numpy as np
from Levenshtein import distance


def DetectAndFixingAddress():
    # Load data from CSV file
    df = pd.read_csv('building_V1.csv')

    # Detect Building_ID -> Address
    e0_violations = df.groupby('Building_ID')['Address'].nunique()

    # building_address_counts = df.groupby('Building_ID')['Address'].nunique().reset_index()
    # violations = building_address_counts[building_address_counts['Address'] > 1]

    e0_violations = e0_violations[e0_violations > 1]

    # print violations
    print("违反 e0: Building_ID → Address 的情况：")
    print(e0_violations)

    # 执行SQL类似的操作
    violation_pairs = pd.merge(df, df, on='Building_ID', suffixes=('_1', '_2'))
    violation_pairs = violation_pairs[(violation_pairs['Address_1'] != violation_pairs['Address_2'])]

    # 打印违规的元组对
    print("违反 e0: Building_ID → Address 元组对：")
    print(violation_pairs[['Building_ID', 'Address_1', 'Address_2']])

    # 修复违规
    # 以频率为例，为每个Address选择出现最频繁的Building_ID
    # frequent_ids = df.groupby('Address')['Building_ID'].agg(lambda x: x.value_counts().idxmax())
    # print(violations)
    # df['Building_ID'] = df['Address'].map(frequent_ids)

    # 将修复后的数据保存回CSV文件
    # df.to_csv('fixed_data.csv', index=False)


def DetectAndFixingState():
    # 读取数据
    df = pd.read_csv('building_V3.csv')

    # e1: Zip → State
    # 检测违反 e1 约束的情况
    e1_violations = df.groupby('Zip')['State'].nunique()
    e1_violations = e1_violations[e1_violations > 1]

    # 打印每个Zip违反的Stat
    # e数量
    # print("违反 e1:Zip → State 的情况：")
    # print(e1_violations)

    # 获取违反约束的 Zip 码列表
    violating_zips = e1_violations.index.tolist()

    # 打印违反 e1:Zip → State 的情况
    print("违反 e1:Zip → State 的情况：")
    print(e1_violations)

    # 筛选出违反约束的数据
    violating_data = df[df['Zip'].isin(violating_zips)]

    # 对违反约束的数据按 'Zip' 和 'State' 进行分组统计
    violating_distribution = violating_data.groupby(['Zip', 'State']).size().reset_index(name='Count')

    # 输出违反约束的 ZIP 码及其对应的 State 分布
    print(violating_distribution.to_string(index=False))

    # 计算每个州的出现频率
    state_counts = df['State'].value_counts(normalize=True)

    # 将出现频率转换为权重（这里可以加入任何逻辑来调整权重）
    weights = state_counts / state_counts.sum()

    print("=========================", weights)

    # 找出权重最大的State
    state_with_max_weight = weights.idxmax()

    # 对于Zip为空的记录，设置权重最大的State
    df.loc[df['Zip'].isnull(), 'State'] = state_with_max_weight

    # 对每个邮政编码内的数据进行排序，根据Count降序，权重升序（因为在并列情况下，权重越大越好）
    # 这将使得同一邮政编码下，计数最高且权重最大的州排在最前
    violating_distribution['weight'] = violating_distribution['State'].map(weights)
    sorted_violations = violating_distribution.sort_values(by=['Zip', 'Count', 'weight'],
                                                           ascending=[True, False, False])

    # 删除计数较小的州，只保留每个邮政编码下计数最大的州（如果并列，则选择权重最大的）
    max_states = sorted_violations.drop_duplicates(subset=['Zip'])

    print("违反 e1:Zip → State 的情况，以及选择的州：")
    print(max_states)

    # 接下来，我们找到每个邮政编码最大计数的州
    # max_states = violating_distribution.loc[violating_distribution.groupby(['Zip'])['Count'].idxmax()]

    print("++++++++++++++",max_states)

    # 创建一个从邮政编码到选择的州的映射
    state_map = max_states.set_index('Zip')['State'].to_dict()
    print("======================",state_map)

    # 在映射之前，我们首先保留原来Zip为空的State值
    mask = df['Zip'].notnull() & df['Zip'].apply(str).str.strip().ne('')

    # 使用映射更新State列
    df.loc[mask, 'State'] = df.loc[mask, 'Zip'].map(state_map)

    # df['State'] = df['Zip'].map(state_map)

    df.to_csv('building_V4.csv', index=False)

    # 如果您也想看到具体的违反数据行
    # if not e1_violations.empty:
    #    print("违反 'Zip → State' 约束的数据行:")
    #    print(e1_violations.to_string(index=False))

    # 找出每个 Zip 中出现频率最高的 State
    # frequent_states = df.groupby('Zip')['State'].agg(lambda x: x.value_counts().idxmax()).reset_index()

    # 根据频率最高的 State 更新违规数据
    # for index, row in frequent_states.iterrows():
    #    zip_code = row['Zip']
    #    most_frequent_state = row['State']
    #    print("Zip:",zip_code," Most_frequent_state:",most_frequent_state)

    # 修复违规
    # 以频率为例，为每个Address选择出现最频繁的Building_ID
    # frequent_ids = df.groupby('Address')['Building_ID'].agg(lambda x: x.value_counts().idxmax())
    # print(violations)
    # df['Building_ID'] = df['Address'].map(frequent_ids)

    # 将修复后的数据保存回CSV文件
    # df.to_csv('fixed_data.csv', index=False)


def DetectAndFixingCity():
    # 读取数据
    df = pd.read_csv('building_V4.csv')

    # e2: Zip → City
    # 检测违反 e2 约束的情况
    e2_violations = df.groupby('Zip')['City'].nunique()
    e2_violations = e2_violations[e2_violations > 1]

    # 打印每个Zip违反的City数量
    print("违反 e2:Zip → City 的情况：")
    print(e2_violations)

    # 筛选出违反约束的数据
    violating_zips = e2_violations.index.tolist()
    violating_data = df[df['Zip'].isin(violating_zips)]

    # 对违反约束的数据按 'Zip' 和 'City' 进行分组统计
    violating_distribution = violating_data.groupby(['Zip', 'City']).size().reset_index(name='Count')

    # 计算每个城市的出现频率
    city_counts = df['City'].value_counts(normalize=True)

    # 将出现频率转换为权重（这里可以加入任何逻辑来调整权重）
    weights = city_counts / city_counts.sum()

    # 找出权重最大的City
    city_with_max_weight = weights.idxmax()

    # 对于Zip为空的记录，设置权重最大的City
    df.loc[df['Zip'].isnull(), 'City'] = city_with_max_weight

    # 对每个邮政编码内的数据进行排序，根据Count降序，权重升序（因为在并列情况下，权重越大越好）
    violating_distribution['Weight'] = violating_distribution['City'].map(weights)
    sorted_violations = violating_distribution.sort_values(by=['Zip', 'Count', 'Weight'],
                                                           ascending=[True, False, False])

    # 删除计数较小的城市，只保留每个邮政编码下计数最大的城市（如果并列，则选择权重最大的）
    max_cities = sorted_violations.drop_duplicates(subset=['Zip'])

    print("违反 e2:Zip → City 的情况，以及选择的城市：")
    print(max_cities)

    # 创建一个从邮政编码到选择的城市的映射
    city_map = max_cities.set_index('Zip')['City'].to_dict()
    print(city_map)

    # 在映射之前，我们首先保留原来Zip为空的City值
    mask = df['Zip'].notnull() & df['Zip'].apply(str).str.strip().ne('')

    # 使用映射更新City列
    df.loc[mask, 'City'] = df.loc[mask, 'Zip'].map(city_map)

    # 更新原始数据框中的 'City' 列
    # df['City'] = df['Zip'].map(city_map)

    # 将修正后的数据框保存为新的 CSV 文件
    df.to_csv('building_V5.csv', index=False)

def DetectAndFixingLocation():
    # 读取数据
    df = pd.read_csv('building_V5.csv')

    # 检测违反 e4 约束的情况
    e4_violations = df.groupby(['Latitude', 'Longitude'])['Location'].nunique()
    e4_violations = e4_violations[e4_violations > 1]
    print("e4_violations:",e4_violations.to_string())

    # 获取违反约束的纬度和经度组合列表，确保不包括空值
    violating_coords  = e4_violations.index.tolist()
    # 筛选出违反约束的数据
    violating_data  = df.set_index(['Latitude', 'Longitude']).loc[violating_coords].reset_index()
    print("violating_data:",violating_data.to_string())

    # 对违反约束的数据按 'Latitude', 'Longitude' 和 'Location' 进行分组统计
    violating_distribution = violating_data .groupby(['Latitude', 'Longitude', 'Location']).size().reset_index(name='Count')

    # 假设我们没有外部系统来验证每对经纬度对应的准确位置，我们可以选择计数最多的 Location
    max_locations = violating_distribution.loc[violating_distribution.groupby(['Latitude', 'Longitude'])['Count'].idxmax()]

    print("max_locations:",max_locations.to_string())

    # 创建一个从纬度和经度到选择的位置的映射
    location_map_e4 = max_locations.set_index(['Latitude', 'Longitude'])['Location'].to_dict()
    print(location_map_e4)

    # 更新原始数据框中的 'Location' 列
    for (lat, long), location in location_map_e4.items():
        mask = (df['Latitude'] == lat) & (df['Longitude'] == long)
        df.loc[mask, 'Location'] = location

    # 对于纬度和经度为空的情况，如果您有默认值或者可以通过某种方式获取Location，可以在这里设置
    # 例如，您可以留空或设置为未知
    # df.loc[df['Latitude'].isnull() | df['Longitude'].isnull(), 'Location'] = 'Unknown'  # 或者您的默认值

    # 保存到新文件
    df.to_csv('building_V6.csv', index=False)

def DetectAndFixingLocation2():
    df = pd.read_csv('building_V6.csv')
    df['Location'] = df.apply(lambda row: f"({row['Latitude']}, {row['Longitude']})", axis=1)

    # 现在 'Location' 列将包含格式为 (Latitude, Longitude) 的元组
    # 接下来的步骤是处理任何数据完整性问题，例如重复的位置信息等
    # ...（这里可以加入任何需要的数据清洗步骤）

    # 保存修改后的DataFrame到CSV文件
    df.to_csv('building_V7.csv', index=False)

def DetectAndFixingAddressLocation():
    # 读取数据
    df = pd.read_csv('building_V8.csv')

    # e3: Address → Location
    # 首先定义 Location 为 Latitude 和 Longitude 的组合
    df['Location'] = list(zip(df['Latitude'], df['Longitude']))

    # 检测违反 e3 约束的情况
    e3_violations = df.groupby('Address')['Location'].nunique()
    e3_violations = e3_violations[e3_violations > 1]

    # 输出违反 e3 约束的情况
    print("violate e3: Address → Location data:")
    print(e3_violations)

    # 筛选出违反约束的地址
    violating_addresses = e3_violations.index.tolist()
    violating_data = df[df['Address'].isin(violating_addresses)]

    # 对违反约束的数据按 'Address' 和 'Location' 进行分组统计
    violating_distribution = violating_data.groupby(['Address', 'Location']).size().reset_index(name='Count')

    # 计算每个位置的出现频率
    location_counts = df['Location'].value_counts(normalize=True)

    # 将出现频率转换为权重（这里可以加入任何逻辑来调整权重）
    weights = location_counts / location_counts.sum()

    # 对每个地址内的数据进行排序，根据Count降序，权重升序
    violating_distribution['Weight'] = violating_distribution['Location'].apply(lambda x: weights.get(x, 0))
    sorted_violations = violating_distribution.sort_values(by=['Address', 'Count', 'Weight'],
                                                           ascending=[True, False, False])

    # 删除计数较小的位置，只保留每个地址下计数最大的位置（如果并列，则选择权重最大的）
    max_locations = sorted_violations.drop_duplicates(subset=['Address'])
    print(max_locations)

    # 创建一个从地址到选择的位置的映射
    location_map = max_locations.set_index('Address')['Location'].to_dict()
    print(location_map)

    # 更新DataFrame
    for address, location in location_map.items():
        df.loc[df['Address'] == address, ['Latitude', 'Longitude']] = location

    # 保存更正后的数据
    # df.to_csv('building_V9.csv', index=False)

def clean_location(location):
    try:
        # 假设 location 的格式为 "(lat, lon)"
        lat, lon = location.replace('(', '').replace(')', '').split(',')
        # 格式化为一个带有6位小数的字符串
        return f"({float(lat):.6f}, {float(lon):.6f})"
    except Exception as e:
        print(f"Error processing location: {location} - {e}")
        # 处理错误，返回原始字符串或考虑返回一个特殊值表示错误
        return location

def DetectAndFixingLocationCommunity():
    df = pd.read_csv('building_V8.csv')
    # 检测违反 e5 约束的情况
    e5_violations = df.groupby(['Location', 'Community_Number'])['Community_Name'].nunique()
    e5_violations = e5_violations[e5_violations > 1]

    # 获取违反 e5 约束的 Location 和 Community_Number 组合列表
    violating_locs = e5_violations.index.tolist()

    # 筛选出违反 e5 约束的数据
    violating_data = df.set_index(['Location', 'Community_Number']).loc[violating_locs].reset_index()

    # 对违反约束的数据按 'Location', 'Community_Number' 和 'Community_Name' 进行分组统计
    violating_distribution = violating_data.groupby(
        ['Location', 'Community_Number', 'Community_Name']).size().reset_index(name='Count')

    # 计算每个社区名称的出现频率
    community_name_counts = df['Community_Name'].value_counts(normalize=True)

    # 将出现频率转换为权重
    weights = community_name_counts / community_name_counts.sum()

    # 为每个违反约束的组合找出权重最大的 Community_Name
    def get_max_community_name(row, group_df):
        max_count = group_df['Count'].max()
        # 检查是否有多个 Community_Name 具有相同的最大计数
        if group_df[group_df['Count'] == max_count].shape[0] == 1:
            return group_df[group_df['Count'] == max_count]['Community_Name'].values[0]
        else:
            # 如果有多个具有最大计数的 Community_Name，则使用权重决定
            max_weight = group_df['Weight'].max()
            return group_df[group_df['Weight'] == max_weight]['Community_Name'].values[0]

    # 应用函数并创建映射
    community_name_map = {}
    for loc, group_df in violating_distribution.groupby(['Location', 'Community_Number']):
        group_df['Weight'] = group_df['Community_Name'].apply(lambda x: weights.get(x, 0))
        community_name_map[loc] = get_max_community_name(loc, group_df)

    # 更新原始数据框中的 'Community_Name' 列
    for (loc, comm_num), comm_name in community_name_map.items():
        mask = (df['Location'] == loc) & (df['Community_Number'] == comm_num)
        df.loc[mask, 'Community_Name'] = comm_name

    # 将修正后的数据框保存为新的 CSV 文件
    df.to_csv('building_V9.csv', index=False)


def DetectAndFixingLocationCommunity2():
    df = pd.read_csv('building_V10.csv')
    # 检测违反 e5 约束的情况
    e5_violations = df.groupby(['Location', 'Community_Number'])['Community_Name'].nunique()
    e5_violations = e5_violations[e5_violations > 1]

    # 获取违反 e5 约束的 Location 和 Community_Number 组合列表
    violating_locs = e5_violations.index.tolist()

    # 筛选出违反 e5 约束的数据
    violating_data = df.set_index(['Location', 'Community_Number']).loc[violating_locs].reset_index()

    # 对违反约束的数据按 'Location', 'Community_Number' 和 'Community_Name' 进行分组统计
    violating_distribution = violating_data.groupby(
        ['Location', 'Community_Number', 'Community_Name']).size().reset_index(name='Count')

    # 计算每个社区名称的出现频率
    community_name_counts = df['Community_Name'].value_counts(normalize=True)

    # 将出现频率转换为权重
    weights = community_name_counts / community_name_counts.sum()

    # 为每个违反约束的组合找出权重最大的 Community_Name
    def get_max_community_name(row, group_df):
        max_count = group_df['Count'].max()
        # 检查是否有多个 Community_Name 具有相同的最大计数
        if group_df[group_df['Count'] == max_count].shape[0] == 1:
            return group_df[group_df['Count'] == max_count]['Community_Name'].values[0]
        else:
            # 如果有多个具有最大计数的 Community_Name，则使用权重决定
            max_weight = group_df['Weight'].max()
            return group_df[group_df['Weight'] == max_weight]['Community_Name'].values[0]

    # 应用函数并创建映射
    community_name_map = {}
    for loc, group_df in violating_distribution.groupby(['Location', 'Community_Number']):
        group_df['Weight'] = group_df['Community_Name'].apply(lambda x: weights.get(x, 0))
        community_name_map[loc] = get_max_community_name(loc, group_df)

    # 更新原始数据框中的 'Community_Name' 列
    for (loc, comm_num), comm_name in community_name_map.items():
        mask = (df['Location'] == loc) & (df['Community_Number'] == comm_num)
        df.loc[mask, 'Community_Name'] = comm_name

    # 将修正后的数据框保存为新的 CSV 文件
    df.to_csv('building_V11.csv', index=False)



def calculate_weighted_edit_distance(row1, row2, weights):
    w_distance = 0
    for key in weights:
        w_distance += weights[key] * distance(str(row1[key]), str(row2[key]))
    return w_distance


def ZipStateCityDataFusion():
    threshold_beta = 5  # 这是一个示例阈值
    weights = {'City': 1.5, 'State': 1.0, 'Zip': 2.0}

    df = pd.read_csv('building-V2.csv')
    medcond_data = df.to_dict('records')
    # 初始化一个列表来存储重复项
    duplicates = []

    # 计算加权编辑距离
    for i, row1 in enumerate(medcond_data):
        for j, row2 in enumerate(medcond_data):
            if i >= j:  # 避免重复比较
                continue
            weighted_distance = calculate_weighted_edit_distance(row1, row2, weights)
            if weighted_distance < threshold_beta:
                duplicates.append((i, j))  # 存储索引而不是记录，以避免重复数据
    print(duplicates)

    # 获取唯一的索引
    unique_indices = list(set(idx for pair in duplicates for idx in pair))
    # 筛选出重复的行
    duplicate_rows = df.loc[unique_indices]

    # 计算 state 列的分布
    state_distribution = duplicate_rows['State'].value_counts()
    print(state_distribution)

    # 通过选择更常见的州(state)值来解决冲突

    for i, j in duplicates:
        state1 = duplicate_rows.loc[i, 'State']
        state2 = duplicate_rows.loc[j, 'State']
        if state_distribution[state1] >= state_distribution[state2]:
            preferred_state = state1
        else:
            preferred_state = state2
        # 更新重复项的 state 值
        duplicate_rows.at[i, 'State'] = preferred_state
        duplicate_rows.at[j, 'State'] = preferred_state

    # 将融合后的数据保存到CSV文件
    duplicate_rows.to_csv('building_V3.csv', index=False)


# 函数来计算频率并返回一个权重映射
def calculate_weights(df, column_name):
    counts = df[column_name].value_counts(normalize=True)
    weights = counts / counts.sum()
    return weights


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(distance('IL', 'HA'))  # 应输出 3


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # ZipStateCityDataFusion();
    # DetectAndFixingAddress()
    # DetectAndFixingState()
    # DetectAndFixingCity()
    # DetectAndFixingLocation()
    # DetectAndFixingLocation2()
    # DetectAndFixingAddressLocation()
    # DetectAndFixingLocationCommunity()
    DetectAndFixingLocationCommunity2();

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
