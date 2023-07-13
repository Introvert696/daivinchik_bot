import sqlite3


class Database():
    path_to_db = "znakomstvaDB.db"

    def createDB(self):
        try:
            connection = sqlite3.connect(self.path_to_db)
            cursor = connection.cursor()
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
                    create_at text,
                    foreign key (from_user) references User(id),
                    foreign key (to_user) references User(id)
                    );
            '''
            cursor.execute(create_table_sql)
            create_table_sql = '''
             create table if not exists LikesOrder(
                    id integer primary key autoincrement,
                    from_user integer not null,
                    to_user  integer not null,
                    is_checked integer not null,
                    is_match integet not null,
                    create_at text,
                    foreign key (to_user) references User (id),
                    foreign key (from_user) references User (id)
                    );
            '''
            cursor.execute(create_table_sql)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as ex:
            return ex

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

    def saveUser(self, id, username, name, age, photo, city, content):
        try:
            connection = sqlite3.connect(self.path_to_db)
            cursor = connection.cursor()
            insert_sql = '''insert into User(tgId, tgUsername, name, age, photo, city, desc) values (?,?,?,?,?,?,?)'''
            cursor.execute(insert_sql, (id, username, name,
                           age, photo, city, content))
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
