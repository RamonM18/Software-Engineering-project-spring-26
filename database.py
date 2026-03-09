import psycopg2
from psycopg2 import sql

class PlayerDatabase:
    # Handles all database operations for player data
    
    # Connection details
    CONNECTION_PARAMS = {
        'dbname': 'photon',
        #'user': 'student',
        #'password': 'student',
        #'host': 'localhost',
        #'port': '5432'
    }
    
    def connect(self):
        # Method to connect to database
        return psycopg2.connect(**self.CONNECTION_PARAMS)
    
    def get_codename(self, player_id):
        # Method to get codename by player ID
        codename = None
        sql = "SELECT codename FROM players WHERE id = %s"
        
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute(sql, (player_id,))
            result = cursor.fetchone()
            
            if result:
                codename = result[0]
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(str(e))
        
        return codename
    
    def add_player(self, player_id, codename):
        # Adding player method
        sql = "INSERT INTO players (id, codename) VALUES (%s, %s)"
        
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute(sql, (player_id, codename))
            conn.commit()
            
            print("Player has been added!")
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(str(e))


# Testing the methods
if __name__ == "__main__":
    db = PlayerDatabase()
    
    # Getting existing player info
    name = db.get_codename(1)  # Should return "Opus"
    print(f"Codename: {name}")
    
    # Manually testing to add player
    db.add_player(500, "Ramon")
    
    # Print to show it was added
    new_name = db.get_codename(500)
    print(f"New Player: {new_name}")
