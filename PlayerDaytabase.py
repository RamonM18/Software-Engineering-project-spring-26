import psycopg2
from psycopg2 import sql


class PlayerDatabase:
    # Connection details
    URL = "localhost"
    DATABASE = "photon"
    USER = "student"
    PASSWORD = "student"
    PORT = 5432

    # Method to connect to database
    def connect(self):
        return psycopg2.connect(
            host=self.URL,
            database=self.DATABASE,
            user=self.USER,
            password=self.PASSWORD,
            port=self.PORT
        )

    # Method to get codename by player ID
    def get_codename(self, player_id):
        codename = None
        query = "SELECT codename FROM players WHERE id = %s"

        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (player_id,))
                    result = cursor.fetchone()
                    if result:
                        codename = result[0]

        except Exception as e:
            print("Database error:", e)

        return codename

    # Adding player method
    def add_player(self, player_id, codename):
        query = "INSERT INTO players (id, codename) VALUES (%s, %s)"

        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (player_id, codename))
                    conn.commit()
                    print("Player has been added!")

        except Exception as e:
            print("Database error:", e)


# Testing
if __name__ == "__main__":
    db = PlayerDatabase()

    # Get existing player info
    name = db.get_codename(1)
    print("Codename:", name)

    # Manually test adding player
    db.add_player(500, "Ramon")

    # Verify insertion
    new_name = db.get_codename(500)
    print("New Player:", new_name)
