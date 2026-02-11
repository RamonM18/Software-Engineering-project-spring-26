import java.sql.*;


public class PlayerDatabase 
{
    // Connection details
    private static final String URL = "jdbc:postgresql://localhost:5432/photon";
    private static final String USER = "student";
    private static final String PASSWORD = "";
    
    // Method to connect to database
    private Connection connect() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
    
    // Method to get codename by player ID
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
    
    // Test it
    public static void main(String[] args) {
        PlayerDatabase db = new PlayerDatabase();
        String name = db.getCodename(1);  // Should return "Opus"
        System.out.println("Codename: " + name);
    }

    
}