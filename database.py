import sqlite3
'''
В данном класе реализуется логика взаимодействия с БД
'''


class Database():
    # путь до бд
    path_to_db = "znakomstvaDB.db"

    def createDB(self):
        try:
            connection = sqlite3.connect(self.path_to_db)
            cursor = connection.cursor()
            # sex - это пол, может быть 0 или 1, где 0 это парень, 1 девушка
            # скрипты для создания базы данных
            create_table_sql = ''' 
                create table if not exists User(
                    id integer primary key autoincrement,
                    tgId integer not null,
                    tgUsername text null,
                    name text not null,
                    age integer not null,
                    photo blob not null,
                    is_activity integer null,
                    desc text null,
                    city text not null,
                    sex integer not null,
                    sex_search integer not null,
                    create_at text
                    );
               
            '''
            cursor.execute(create_table_sql)
            create_table_sql = '''
             create table if not exists LikeHistory(
                    id integer primary key autoincrement,
                    from_user integer not null,
                    to_user integer not null,
                    like integer not null,
                    is_match integer not null,
                    content string null,
                    create_at text,
                    foreign key (from_user) references User(id),
                    foreign key (to_user) references User(id)
                    );
            '''
            cursor.execute(create_table_sql)

            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            return ex
    # Проверка пользователяв бд

    def checkUserId(self,  userId: str):
        try:
            connection = sqlite3.connect(self.path_to_db)
            cursor = connection.cursor()
            select_sql = ''' Select * from User where tgId='''+userId
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            data = []
            for row in rows:
                data.push(row)
                print(row)
            return data
        except Exception as ex:
            return ex

    # сохранения новой анкеты юзера
    def saveUser(self, id, username, name, age, photo, city, content, sex, sex_search):
        try:
            connection = sqlite3.connect(self.path_to_db)
            cursor = connection.cursor()
            insert_sql = '''insert into User(tgId, tgUsername, name, age, photo, city, desc, sex, sex_search) values (?,?,?,?,?,?,?,?,?)'''
            cursor.execute(insert_sql, (id, username, name,
                           age, photo, city, content, sex, sex_search))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            return ex

    # Получаем рандомного пользователя из бд
    def getRandomUser(self, id):
        try:
            data = []
            while True:
                connection = sqlite3.connect(self.path_to_db)
                cursor = connection.cursor()
                select_sql = '''SELECT * FROM user ORDER BY RANDOM() LIMIT 1;'''
                cursor.execute(select_sql)
                data = cursor.fetchall()
                connection.commit()
                cursor.close()
                connection.close()
                if (data[0][1] != id):
                    return data[0]
        except Exception as ex:
            return ex

    # Сохраняем результат оценивания
    def saveAnswer(self, from_user, to_user, like):
        try:
            connection = sqlite3.connect(self.path_to_db)
            cursor = connection.cursor()
            save_sql = f'''Insert into LikeHistory(from_user,to_user,like ) values (?,?,?)'''
            cursor.execute(save_sql, (from_user, to_user, like))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            return False

    # Получаем id юзера в строке в таблице
    def getUserId(self, user_id):
        try:
            connection = sqlite3.connect(self.path_to_db)
            cursor = connection.cursor()
            save_sql = f''' select id from User where tgId={user_id}'''
            cursor.execute(save_sql)
            data = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            return data[0][0]
        except Exception as ex:
            return False
