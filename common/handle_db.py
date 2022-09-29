import pymysql


class DbTrade:
    def __init__(self):
        # 创建一个连接对象
        self.conn = pymysql.connect(host="rm-3ns915h3g5jr67jbxbo.mysql.rds.aliyuncs.com",
                                    port=3306,
                                    user="ltpadmin",
                                    password="LTP@8888",
                                    charset="utf8",
                                    cursorclass=pymysql.cursors.DictCursor
                                    )
        # 创建一个游标
        self.cur = self.conn.cursor()

    def find_one(self, sql):
        """获取查询出来的第一条数据"""
        # 执行查询语句
        self.conn.commit()
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data

    def find_all(self, sql):
        """获取查询出来的所有数据"""
        self.conn.commit()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def find_count(self,sql):
        """返回查询数据的条数"""
        self.conn.commit()
        return self.cur.execute(sql)

    def close(self):
        """关闭游标，断开连接"""
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    db = DbTrade()
    sql= "select * from ltp_lat_monitor.t_lat_monitor tlm where id =1;"
    data = db.find_one(sql)
    print(data)