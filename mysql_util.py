import pymysql
import traceback
import sys

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