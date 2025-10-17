from datetime import datetime
from myapp.utils.database_tools import execute_sql, package_execute


def date_record():
    time = datetime.now().strftime('%H')

    if time == '0':
        pendent = execute_sql(3, 2)[0][2]
        debris = execute_sql(3, 3)[0][2]
        resource = execute_sql(3, 1)[0][2]
        bubble = execute_sql(3, 5)[0][2]
        ab = execute_sql(3, 4)[0][2]
        print(pendent)
        execute_sql(sid=5, channel_id=1, name='pendent', content=pendent)
        execute_sql(sid=5, channel_id=2, name='debris', content=debris)
        execute_sql(sid=5, channel_id=3, name='resource', content=resource)
        execute_sql(sid=5, channel_id=4, name='bubble', content=bubble)
        execute_sql(sid=5, channel_id=5, name='ab', content=ab)
        print('数据已记录')
    else:
        print('当前时间不符合要求，未记录')
