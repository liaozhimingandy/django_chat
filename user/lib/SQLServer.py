# coding=utf-8
import pymssql
from dbutils.persistent_db import PersistentDB
from pymssql import OperationalError
from pymssql._mssql import MSSQLDatabaseException


class SQLServer:
    def __init__(self, server, user, password, database):
        # 类的构造函数，初始化DBC连接信息
        self.server = server
        self.user = user
        self.password = password
        self.database = database
        self.pool = self.__get_connect()

    def __get_connect(self):
        # 得到数据库连接信息，返回conn.cursor()
        if not self.database:
            raise (NameError, "没有设置数据库信息")

        # 创建数据库连接池,明显提高速度
        try:
            # self.conn = pymssql.connect(server=self.server, user=self.user, password=self.password,
            #                             database=self.database, login_timeout=3, timeout=30, appname='alsoapp.com')
            pool = PersistentDB(creator=pymssql, user=self.user, password=self.password, database=self.database,
                                server=self.server, login_timeout=3, timeout=30, appname='alsoapp.com')
        except (MSSQLDatabaseException, OperationalError) as e:
            raise MSSQLDatabaseException("连接数据库失败")

        return pool

    def exec_query(self, sql):
        """
        执行查询语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)  # 执行查询语句
                result = cur.fetchall()  # fetchall()获取查询结果
                return result

    def exec_update(self, sql, value):
        """
        执行执行语句
        返回一个包含tuple的list，list是元素的记录行，tuple记录每行的字段数值
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, value)  # 执行更新语句
            # 提交事务
            conn.commit()

    def __del__(self):
        """对象销毁时触发"""
        pass
        # self.pool.close()
        # print('数据库连接管理器对象已销毁')


def main():
    msg = SQLServer(server="172.16.33.183", user="sa", password="Knt2020@lh", database="ESB_MSG-B")
    result = msg.exec_query(
        "SELECT TOP 1 * FROM MessageTagList")
    for item in result:
        print(item)


if __name__ == '__main__':
    main()
