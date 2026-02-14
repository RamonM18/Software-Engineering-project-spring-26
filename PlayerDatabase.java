import java.sql.*;


public class PlayerDatabase 
{
    //Connection details
    private static final String URL = "jdbc:postgresql://localhost:5432/photon";
    private static final String USER = "student";
    private static final String PASSWORD = "student";
    
    //Method to connect to database
    private Connection connect() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
    
    //Method to get codename by player ID
    public String getCodename(int playerId) {
        String codename = null;
        String sql = "SELECT codename FROM players WHERE id = ?";
        
        try (Connection conn = connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setInt(1, playerId);
            ResultSet rs = pstmt.executeQuery();
            
            if (rs.next()) {
                codename = rs.getString("codename");
            }
            
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
        
        return codename;
    }


    //adding player method
    public void addPlayer(int id, String codename)
    {
        //write if statement that is mod player 2 to figure out if they are even or odd. do if else, if 1 then even else 0 
        String sql = "INSERT INTO players (id, codename) VALUES (?, ?)";

        try(Connection conn = connect();
            PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setInt(1,id);
            pstmt.setString(2, codename);
            pstmt.executeUpdate();

            System.out.println("Player has been added!");

            } catch(SQLException e) {
                System.out.println(e.getMessage());
            }

    }
    //testing the addplayer method
    public static void main(String[] args) {
        PlayerDatabase db = new PlayerDatabase();

        //getting existing player info
        String name = db.getCodename(1);  // Should return "Opus"
        System.out.println("Codename: " + name);

        //manually testing to add player
        db.addPlayer(500,"Ramon");

        //print to show it was added
        String newName = db.getCodename(500);
        System.out.println("New Player: " + newName);
    }

    
}