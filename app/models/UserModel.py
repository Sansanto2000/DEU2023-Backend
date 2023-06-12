from database.db import get_connection
from .entities.User import User

class UserModel():
    _table_name = "clismo_user"
    
    @classmethod
    def get_users(self):
        try:
            connection = get_connection()
            users = []        
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT id, username, password, gender, weight, height, age FROM {self._table_name} ORDER BY username ASC")
                resultset = cursor.fetchall()
                for row in resultset:
                    user=User(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    users.append(user)
            connection.close()
        except Exception as ex:
            raise Exception(ex)