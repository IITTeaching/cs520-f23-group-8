import pymysql
import csv
import re
import pymysql.cursors

def export_other():
    # 数据库连接配置
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'chenjy1234',
        'db': 'data_integration'
    }

    # 连接到数据库
    connection = pymysql.connect(**config)

    # Table names to export
    tables = ['building_community', 'building_street', 'community_service']

    # Create a cursor object
    cursor = connection.cursor()

    for table in tables:
        # SQL query to select data from the table
        query = f"SELECT * FROM {table}"

        # Execute the query
        cursor.execute(query)

        # Fetch all the records
        results = cursor.fetchall()

        # Specify the CSV file to write to
        csv_file_path = f'{table}.csv'

        # Open the CSV file for writing
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            # Create a csv writer object
            csv_writer = csv.writer(csvfile)

            # Write the header
            field_names = [i[0] for i in cursor.description]
            csv_writer.writerow(field_names)

            # Write the data
            for row in results:
                csv_writer.writerow(row)

        print(f'Data from {table} exported to {csv_file_path} successfully.')

    # Close the cursor and connection
    cursor.close()
    connection.close()

def export_building_energy():
    # 数据库连接配置
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'chenjy1234',
        'db': 'data_integration'
    }

    # 连接到数据库
    connection = pymysql.connect(**config)

    # 创建cursor以执行查询
    cursor = connection.cursor()

    # 执行你想导出的表的查询
    cursor.execute("SELECT * FROM building_energy")

    # 获取查询结果
    rows  = cursor.fetchall()

    # 指定将要保存CSV文件的路径
    csv_file_path = 'building_energy.csv'

    # 打开CSV文件，准备写入
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # 写入标题头（可选）
        field_names = [i[0] for i in cursor.description]
        csv_writer.writerow(field_names)

        # Identify index of 'Location' column based on the header
        location_index = field_names.index('Location')
        # 写入数据行
        for row in rows:
            modified_row = list(row)
            modified_row[-3] = modified_row[-3].replace('"', '')  # 假设Location是最后一列
            # Print original value for debugging
            # if row_as_list[location_index]:
            #    row_as_list[location_index] = row_as_list[location_index].replace('"', '')
            csv_writer.writerow(modified_row)

    # 关闭cursor和连接
    cursor.close()
    connection.close()

    print(f"数据已导出到 {csv_file_path}")

def export_building():
    # 数据库连接配置
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'chenjy1234',
        'db': 'data_integration'
    }

    # 连接到数据库
    connection = pymysql.connect(**config)

    # 创建cursor以执行查询
    cursor = connection.cursor()

    # 执行你想导出的表的查询
    cursor.execute("SELECT * FROM building")

    # 获取查询结果
    rows  = cursor.fetchall()

    # 指定将要保存CSV文件的路径
    csv_file_path = 'building.csv'

    # 打开CSV文件，准备写入
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # 写入标题头（可选）
        csv_writer.writerow([i[0] for i in cursor.description])

        # 写入数据行
        for row in rows:
            # 去除最后一列值中的双引号
            modified_row = list(row)
            modified_row[-1] = modified_row[-1].replace('"', '')  # 替换掉双引号
            csv_writer.writerow(modified_row)

    # 关闭cursor和连接
    cursor.close()
    connection.close()

    print(f"数据已导出到 {csv_file_path}")
def second_export_building():
    # 指定你的CSV文件路径
    csv_file_path = 'building.csv'
    temp_file_path = 'building_temp.csv'

    # 打开原始CSV文件和一个临时文件
    with open(csv_file_path, 'r', encoding='utf-8') as infile, \
            open(temp_file_path, 'w', newline='', encoding='utf-8') as outfile:
        # 读取原始文件内容
        filedata = infile.read()

        # 移除所有双引号
        filedata = filedata.replace('"', '')

        # 写入修改后的数据到临时文件
        outfile.write(filedata)

    # 替换原始文件
    import os
    os.remove(csv_file_path)  # 删除原始文件
    os.rename(temp_file_path, csv_file_path)  # 将临时文件重命名为原始文件名
def second_export_building_energy():
    # 指定你的CSV文件路径
    csv_file_path = 'building_energy.csv'
    temp_file_path = 'building_energy_temp.csv'

    # 打开原始CSV文件和一个临时文件
    with open(csv_file_path, 'r', encoding='utf-8') as infile, \
            open(temp_file_path, 'w', newline='', encoding='utf-8') as outfile:
        # 读取原始文件内容
        filedata = infile.read()

        # 移除所有双引号
        filedata = filedata.replace('"', '')

        # 写入修改后的数据到临时文件
        outfile.write(filedata)

    # 替换原始文件
    import os
    os.remove(csv_file_path)  # 删除原始文件
    os.rename(temp_file_path, csv_file_path)  # 将临时文件重命名为原始文件名

def second_export_other():
    import os
    # CSV文件列表
    tables = ['building_community.csv', 'building_street.csv', 'community_service.csv']
    for table in tables:
        # 指定CSV文件路径和临时文件路径
        csv_file_path = f'{table}'
        temp_file_path = f'temp_{table}'
        # 确保文件存在
        if not os.path.isfile(csv_file_path):
            print(f"File {csv_file_path} does not exist.")
            continue

        # 读取CSV文件内容，删除双引号，并写入临时文件
        with open(csv_file_path, 'r', encoding='utf-8') as infile, open(temp_file_path, 'w', newline='',
                                                                        encoding='utf-8') as outfile:
            filedata = infile.read()
            filedata = filedata.replace('"', '')  # 移除所有双引号
            outfile.write(filedata)  # 写入临时文件

        # 替换原始文件
        os.remove(csv_file_path)  # 删除原始文件
        os.rename(temp_file_path, csv_file_path)  # 将临时文件重命名为原始文件名

    print("Removed quotes from all CSV files.")


import random
import string

def random_string(length=10):
    """Generate a random string of fixed length."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def random_number(min_value, max_value, precision=0):
    """Generate a random number within a range."""
    return round(random.uniform(min_value, max_value), precision)

def  insert_community_data():
    # 数据库连接配置
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'chenjy1234',
        'db': 'data_integration'
    }

    # 连接到数据库
    connection = pymysql.connect(**config)

    try:
        # 创建cursor以执行查询，使用DictCursor
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 执行你想导出的表的查询
            cursor.execute("SELECT * from building A,building_energy B WHERE A.Building_ID = B.ID ORDER BY A.Building_ID DESC")

            # 获取查询结果
            rows = cursor.fetchall()
            for row in rows:
                insert_statement = """
                        INSERT INTO building_community (
                            Building_ID, Community_ID, Community_Name, Description, Zip, State, Country, Area,
                            Population, EmploymentRate, CrimeRate, Amenities, PublicTransportAccess,
                            QualityOfLifeIndex, HealthCareIndex, CostOfLivingIndex, PollutionIndex, ClimateIndex
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        """
                # 用实际值替换占位符（这里只是示例）
                data = (
                    row['Building_ID'],
                    row['Community_Number'],
                    row['Community_Name'],
                    'Description here',
                    row['Zip'],
                    row['State'],
                    'USA',
                    f"{random_number(1, 100, 1)} sq mi",
                    random_number(1000, 50000),
                    random_number(0.5, 1.0, 2),
                    random_number(0, 0.5, 2),
                    random_string(20),
                    random.choice(["Good", "Average", "Poor"]),
                    random_number(50, 100),
                    random_number(50, 100),
                    random_number(50, 100),
                    random_number(0, 100),
                    random_number(0, 100)
                )

                # 执行INSERT语句
                if row['Community_Number']:
                    cursor.execute(insert_statement, data)
            connection.commit()
                # print(row['Building_ID'],row['Zip'],row['State'],row['City'],row['Community_Number'],row['Community_Name'])  # Now you can access by column name
    finally:
        # 关闭数据库连接
        connection.close()

def random_phone_number():
    """Generate a random phone number."""
    return f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"

def random_hours():
    """Generate random operating hours."""
    days = ['Mon-Fri', 'Sat', 'Sun']
    hours = [f"{random.randint(6, 9)}AM - {random.randint(5, 11)}PM", "Closed"]
    return ', '.join(f"{day} {random.choice(hours)}" for day in days)

def random_website():
    """Generate a random website URL."""
    domain = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
    return f"http://{domain}.com"

def  insert_community_Service():
    # Database connection configuration
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'chenjy1234',
        'db': 'data_integration'
    }

    # Establish a database connection
    connection = pymysql.connect(**config)

    try:
        # Create a cursor to execute queries using DictCursor
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Execute the query to export data from the building table
            cursor.execute(
                "SELECT * from building A,building_energy B WHERE A.Building_ID = B.ID ORDER BY A.Building_ID DESC")

            service_id = 1004  # Start the Service_ID from 1000
            # Fetch the result of the query
            rows = cursor.fetchall()
            for row in rows:
                # Generate random data for each row
                random_service_data = {
                    'ServiceName': random_string(20),
                    'ServiceType': random.choice(['Healthcare', 'Education', 'Recreation', 'Social']),
                    'ProviderName': random_string(15),
                    'Address': f"{random.randint(100, 9999)} {random_string(15)} St.",
                    'Contact': random_phone_number(),
                    'OperatingHours': random_hours(),
                    'Capacity': random.randint(1, 100),
                    'Specialties': random_string(30),
                    'InsuranceAccepted': random.choice(['Yes', 'No']),
                    'QualityRating': random.randint(1, 5),
                    'Accessibility': random.choice(['Good', 'Average', 'Poor']),
                    'EmergencyServices': random.choice(['Yes', 'No']),
                    'AverageWaitTime': f"{random.randint(10, 120)} minutes",
                    'PatientSatisfactionScore': random.randint(1, 10),
                    'Accreditation': random.choice(['Accredited', 'Not Accredited']),
                    'Website': random_website()
                }

                insert_statement = """
                        INSERT INTO community_service  (
                             Service_ID, Community_ID, ServiceName, ServiceType, ProviderName, Address, Contact, 
                             OperatingHours, Capacity, Specialties, InsuranceAccepted, QualityRating, Accessibility, 
                             EmergencyServices, AverageWaitTime, PatientSatisfactionScore, Accreditation, Website
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                        """

                # Execute the INSERT statement if Community_Number is not null
                if row['Community_Number']:
                    data = (
                        service_id,
                        row['Community_Number'],
                        random_service_data['ServiceName'],
                        random_service_data['ServiceType'],
                        random_service_data['ProviderName'],
                        random_service_data['Address'],
                        random_service_data['Contact'],
                        random_service_data['OperatingHours'],
                        random_service_data['Capacity'],
                        random_service_data['Specialties'],
                        random_service_data['InsuranceAccepted'],
                        random_service_data['QualityRating'],
                        random_service_data['Accessibility'],
                        random_service_data['EmergencyServices'],
                        random_service_data['AverageWaitTime'],
                        random_service_data['PatientSatisfactionScore'],
                        random_service_data['Accreditation'],
                        random_service_data['Website']
                    )
                    cursor.execute(insert_statement, data)
                    service_id += 1  # Increment the Service_ID for the next entry

            # Commit the transaction
            connection.commit()
    finally:
        # Close the database connection
        connection.close()


if __name__ == '__main__':
    # export_building()
    # second_export_building()
    # export_building_energy();
    # second_export_building_energy();
    # export_other()
    # second_export_other()
    # insert_community_data()
    insert_community_Service()
