import pymysql


def execute_sql(sid, channel_id, content):
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='zxcv1234',
        database='localhost_interface'
    )
    if sid == 1:
        filter_execute_statistics = f"select {content} from  translate_statistics where channel_id ={channel_id} order by time desc limit 5;"
        cursor = db.cursor()
        try:
            cursor.execute(filter_execute_statistics)
            result = cursor.fetchall()
            return result
        except pymysql.MySQLError as e:
            print(e, '查询失败')
        db.commit()
        db.close()
    elif sid == 2:
        filter_execute_statistics = f'SELECT  CAST(time AS DATE) AS date_only, COUNT(*)  FROM translate_statistics  GROUP BY date_only ORDER BY date_only DESC limit 5;'
        cursor = db.cursor()
        try:
            cursor.execute(filter_execute_statistics)
            result = cursor.fetchall()
            return result
        except pymysql.MySQLError as e:
            print(e, '查询失败')
        db.commit()
        db.close()


def package_execute(new_list, sid, cid, statement):
    """
    :param statement: sql语句
    :param cid:端id
    :param sid:执行的语句id
    :param new_list:导入表格
    :return:数据表
    """
    new = execute_sql(sid, cid, statement)
    for i in new:
        new_list.append(i[0])
    return new_list


if __name__ == '__main__':
    print(execute_sql(2, 2, 'quantity'))
