from environs import Env
import psycopg2


env = Env()
env.read_env()


def conn_cur():
    conn = psycopg2.connect(
        database=env("DATABASE"),
        host=env("HOST"),
        user=env("USER"),
        password=env("PASSWORD"),
    )

    cur = conn.cursor()

    return conn, cur


def end_conn_cur(conn, cur) -> None:
    conn.commit()
    cur.close()
    conn.close()