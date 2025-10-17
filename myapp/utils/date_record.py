from datetime import datetime
from myapp.utils.database_tools import execute_sql, package_execute


def date_record():
    time = datetime.now().strftime('%H')
    date = datetime.now().strftime('%Y-%m-%d')
    if time == '0':
        pendent = execute_sql(3, 2)[0][2]
        debris = execute_sql(3, 3)[0][2]
        resource = execute_sql(3, 1)[0][2]
        bubble = execute_sql(3, 5)[0][2]
        ab = execute_sql(3, 4)[0][2]
        execute_sql(sid=5, channel_id=1, name='pendent', content=pendent, record_pag_url=date)
        execute_sql(sid=5, channel_id=2, name='debris', content=debris, record_pag_url=date)
        execute_sql(sid=5, channel_id=3, name='resource', content=resource, record_pag_url=date)
        execute_sql(sid=5, channel_id=4, name='bubble', content=bubble, record_pag_url=date)
        execute_sql(sid=5, channel_id=5, name='ab', content=ab, record_pag_url=date)
        print('数据已记录')
    else:
        print('当前时间不符合要求，未记录')


if __name__ == '__main__':
    date_record()
