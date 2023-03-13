import psycopg2

conn = psycopg2.connect(
    host="192.168.199.51",
    port=5432,
    database="metadb-test",
    user="sxwldba",
    password="sxwldba!"
)
# 开启游标
cur = conn.cursor()
# 需要复制数据的账号的id
new_user_id = 256
# 被复制的账号的id
goal_user_id = 1

# 拿到存在creator_id的所有表的表名
cur.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.COLUMNS  WHERE COLUMN_NAME = 'creator_id'")
# 获取结果集每一行
rows = cur.fetchall()
for row in rows:
    # 拿到数据表名
    table_name = row[0]
    cur.execute(f"select COLUMN_NAME from information_schema.COLUMNS where table_name = '{table_name}'")
    rows_name = cur.fetchall()
    # 拿到表中的字段名
    rows_name = [x[0] for x in rows_name]
    cur.execute(f"select * from {table_name} where creator_id = {goal_user_id}")
    rows = cur.fetchall()
    # 拿到需要复制的用户数据
    for row in rows:
        row_list = list(row)
        sql_dict = dict(zip(rows_name, row_list))
        cur.execute(f"select max(id) from {table_name}")
        max_id = cur.fetchall()[0][0]
        # 拿到最大的id值
        sql_dict['id'] = max_id + 1
        # 更换创建者id
        sql_dict['creator_id'] = new_user_id
        # 解决insert时列表未加''的问题
        for key in sql_dict:
            if isinstance(sql_dict[key], list):
                sql_dict[key] = str(sql_dict[key])
        keys = ', '.join(sql_dict.keys())
        values = ', '.join(['%s'] * len(sql_dict))
        sql = f"INSERT INTO {table_name}({keys}) VALUES ({values})"
        cur.execute(sql, tuple(sql_dict.values()))
conn.commit()
print('数据转移成功！！！')
conn.close()
