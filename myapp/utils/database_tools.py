import pymysql


def execute_sql(channel_id):
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='zxcv1234',
        database='localhost_interface'
    )
    filter_execute_statistics = f"select * from  translate_statistics where channel_id ={channel_id} order by time desc;"
    cursor = db.cursor()
    try:
        cursor.execute(filter_execute_statistics)
        result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(e, '查询失败')
    db.commit()
    db.close()


if __name__ == '__main__':
    print(execute_sql(2))
