import pymysql


def execute_sql():
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='zxcv1234',
        database='localhost_interface'
    )
    filter_execute_statistics = "select * from  translate_statistics a inner join translate_channel" \
                                " b on a.channel_id =b.channel_id"
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
    execute_sql()
