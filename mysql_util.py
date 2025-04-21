import pymysql
import traceback
import sys
from pathlib import Path

class MysqlUtil():
    def __init__(self):
        host = '127.0.0.1'
        user = 'root'
        password = '264301'
        database = 'users'
        self.connection = pymysql.connect(host=host, user=user, password=password, db=database)
        self.cursor = self.connection.cursor(pymysql.cursors.DictCursor)

    def insert(self, sql, params):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql, params)
            self.connection.commit()
        except Exception as e:
            print(f"Insert operation failed: {e}")
            self.connection.rollback()
        finally:
            self.connection.close()

    def fetchone(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
        except:
            traceback.print_exc()
            self.connection.rollback()
        finally:
            self.connection.close()
        return result

    def fetchall(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            results = self.cursor.fetchall()
        except:
            traceback.print_exc()
            self.connection.rollback()
        finally:
            self.connection.close()
        return results

    def execute(self, sql, params=None):
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
        except:
            traceback.print_exc()
            self.connection.rollback()
        finally:
            self.connection.close()

    def init_database(config):
        """通过Python执行SQL文件初始化数据库"""
        try:
            # 连接数据库（无需指定数据库名）
            connection = pymysql.connect(
                host=config['host'],
                user=config['user'],
                password=config['password'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            # 读取SQL文件内容
            sql_path = Path(__file__).parent.parent / 'sql' / 'books_table.sql'
            with open(sql_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()

            # 执行SQL语句
            with connection.cursor() as cursor:
                # 创建数据库（如果不存在）
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
                cursor.execute(f"USE {config['database']}")

                # 执行表创建语句（自动处理多语句）
                for statement in sql_script.split(';'):
                    if statement.strip():
                        cursor.execute(statement)

            connection.commit()
            return True

        except Exception as e:
            print(f"数据库初始化失败: {str(e)}")
            return False
        finally:
            if 'connection' in locals() and connection.open:
                connection.close()
