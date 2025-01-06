import pymysql


def execute_sql(sid=None, channel_id=None, content=None, name=None, record_pag_url=None, record_png_url=None):
    db = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='zxcv1234',
        database='localhost_interface'
    )
    if sid in (1, 2, 3):
        if sid == 1:
            filter_execute_statistics = f"select {content} from  translate_statistics where channel_id ={channel_id} order by time desc;"
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
            filter_execute_statistics = f'SELECT  CAST(time AS DATE) AS date_only, COUNT(*)  FROM translate_statistics  GROUP BY date_only ORDER BY date_only DESC limit 6;'
            cursor = db.cursor()
            try:
                cursor.execute(filter_execute_statistics)
                result = cursor.fetchall()
                return result
            except pymysql.MySQLError as e:
                print(e, '查询失败')
            db.commit()
            db.close()
        elif sid == 3:
            filter_execute_statistics = f'SELECT * from myapp_resource_record WHERE record_id = {channel_id}'
            cursor = db.cursor()
            try:
                cursor.execute(filter_execute_statistics)
                result = cursor.fetchall()
                return result
            except pymysql.MySQLError as e:
                print(e, '查询失败')
            db.commit()
            db.close()
    elif sid == 4:
        cursor = db.cursor()
        update_execute_statistics = 'UPDATE myapp_resource_record SET record_number = %s,record_name ' \
                                    '= %s, record_png_url = %s ,record_pag_url= %s  WHERE record_id = %s'
        value = (content, name, record_png_url, record_pag_url, channel_id,)
        try:
            cursor.execute(update_execute_statistics, value)
            # result = cursor.fetchall()
            db.commit()
        except pymysql.MySQLError as e:
            print(e, '更新失败')
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
    execute_sql(sid=4, channel_id=1, content=1144, name='新增坐骑lea ')
