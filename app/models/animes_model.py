from . import conn_cur, end_conn_cur
from psycopg2 import errors

class AnimesTable:
    table_fields = ["id", "anime", "released_date", "seasons"]
    required_fields = ["anime", "released_date", "seasons"]

    @staticmethod
    def create_table() -> None:
        conn, cur = conn_cur()

        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS animes
                    (
                        id BIGSERIAL PRIMARY KEY,
                        anime VARCHAR(100) NOT NULL UNIQUE,
                        released_date DATE NOT NULL,
                        seasons INTEGER NOT NULL
                    )
            """
        )

        end_conn_cur(conn, cur)


    def missing_fields(self, data: dict):
        recieved_keys = data.keys()
        return [
            required
            for required in self.required_fields
            if required not in recieved_keys
        ]


    def check_fields(self, data: dict, field_list: list):
        recieved_keys = data.keys()

        return [recieved for recieved in recieved_keys if recieved not in field_list]


    def create_anime(self, data: dict) -> dict:
        conn, cur = conn_cur()
        self.create_table()
        
        check_fields = self.check_fields(data, ["anime", "released_date", "seasons"])

        if check_fields:
            raise KeyError(
                {
                    "available_keys": ["anime", "released_date", "seasons"],
                    "wrong_keys_sended": check_fields,
                }
            )

        missing_fields = self.missing_fields(data)

        if missing_fields:
            raise KeyError(
                {
                    "required_keys": self.required_fields,
                    "missing_keys": missing_fields,
                }
            )

        data["anime"] = data["anime"].title()

        cur.execute(
            """
                INSERT INTO animes
                    (anime, released_date, seasons)
                VALUES
                    (%(anime)s, %(released_date)s, %(seasons)s)
                RETURNING *
            """,
            data,
        )

        query = cur.fetchone()

        end_conn_cur(conn, cur)

        return dict(zip(self.table_fields, query))

        
    def list_anime(self) -> dict:
        conn, cur = conn_cur()

        try:
            cur.execute(
                """
                    SELECT * 
                        FROM animes;
                """
            )
        except errors.UndefinedTable as _:
            return {"data": []}
        query = cur.fetchall()
        end_conn_cur(conn, cur)

        arr_anime = []
        for elem in query:
            arr_anime.append(dict(id = elem[0], anime = elem[1], released_date = elem[2], seasons = elem[3]))

        return {"data": arr_anime}
    
    def filter_anime(self, id: int):
        conn, cur = conn_cur()

        try:
            cur.execute(
                """
                    SELECT *
                    FROM animes 
                        WHERE id = %(id)s
                """,
                {"id": id},
            )
        except errors.UndefinedTable as _:
            return {"error": "Not Found"}, 404

        query = cur.fetchone()

        end_conn_cur(conn, cur)

        return dict(zip(self.table_fields, query))
        

    def update_anime(self, data: dict, id: int):
        conn, cur = conn_cur()

        anime_filtered = self.filter_anime(id)

        check_fields = self.check_fields(data, ["anime", "released_date", "seasons"])

        if check_fields:
            raise KeyError(
                {
                    "available_keys": ["anime", "released_date", "seasons"],
                    "wrong_keys_sended": check_fields,
                }
            )

        data["id"] = id
        try:
            data["anime"]
        except KeyError:
            data["anime"] = anime_filtered["anime"]
        try:
            data["released_date"]
        except KeyError:
            data["released_date"] = anime_filtered["released_date"]
        try:
            data["seasons"]
        except KeyError:    
            data["seasons"] = anime_filtered["seasons"]
        
        data["anime"] = data["anime"].title()

        cur.execute(
            """
                UPDATE animes
                SET anime = %(anime)s, released_date = %(released_date)s, seasons = %(seasons)s
                    WHERE id = %(id)s
                RETURNING *
            """,
            data,
        )
    
        query = cur.fetchone()
        print(query)

        end_conn_cur(conn, cur)

        return dict(zip(self.table_fields, query))

    def delete_anime(self, id: int):
        conn, cur = conn_cur()
        try:
            cur.execute(
                """
                    DELETE FROM animes
                        WHERE id = %(id)s
                    RETURNING *
                """,
                {"id": id},
            )
        except errors.UndefinedTable as _:
            return {"error": "Not Found"}, 404
        if cur.fetchone():
            end_conn_cur(conn, cur)
            return "No content", 204
        else:
            return {"error": "Not Found"}, 404
      
            
        


        
