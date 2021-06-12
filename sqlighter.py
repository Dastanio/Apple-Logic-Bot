import sqlite3


class SQlighter:
    
    def __init__(self, database):
        #Подключаемся к БД и сохраняем курсор соединение
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    
    def add_new_user(self, user_id):
        #Добавление нового пользователя
        with self.connection:
            if user_id not in self.get_users_id():
                return self.cursor.execute("INSERT INTO `users` (`user_id`, `apples`, `wins`, `defeats`, `giveups`) VALUES(?,?,?,?,?)", (user_id,0,0,0,0))
    
    def get_users_id(self):
        # Получаем список айдишников юзеров 
        with self.connection:
            user_id = self.cursor.execute("SELECT user_id FROM users")
            user_id_list = [x[0] for x in user_id]
            return user_id_list

    def update_column(self, user_id ,num, column):
        #Обновляем колонку с количеством яблок
        with self.connection:
            return self.cursor.execute(f"UPDATE users SET {column} = {num} WHERE user_id = {user_id}")

    def get_column(self, user_id, column):
        #Получаем количество яблок пользователя
        with self.connection:
            obj = self.cursor.execute(f"SELECT {column} FROM users WHERE user_id = {user_id}")
            return list(obj)[0][0]


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

database = SQlighter('sqlite.db')
