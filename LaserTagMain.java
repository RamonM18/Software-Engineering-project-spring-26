import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;

public class LaserTagMain {

    public static void main(String[] args) {
        // Create the main frame
        PlayerDatabase db = new PlayerDatabase();
        JFrame frame = new JFrame("Player Setup");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);
        frame.setLocationRelativeTo(null); // Center on screen

        // Display splash screen
        showSplashScreen(frame, "logo.jpg"); // Replace with JPEG filename

        // Ask for number of players
        int numPlayers = 0;
        while (numPlayers <= 0) {
            String input = JOptionPane.showInputDialog(frame, "Enter number of players:");
            if (input == null) { // User pressed cancel
                System.exit(0);
            }
            try {
                numPlayers = Integer.parseInt(input);
                if (numPlayers <= 0) {
                    JOptionPane.showMessageDialog(frame, "Number of players must be positive.");
                }
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(frame, "Invalid number. Try again.");
            }
        }

        // Create player list
        ArrayList<Player> players = new ArrayList<>();
        for (int i = 1; i <= numPlayers; i++) {
            //String name = null;
            int playerID = 0;
            while (playerID <= 0) {
                String input = JOptionPane.showInputDialog(frame, "Enter ID for Player " + i + ":");
                if (input == null) { // User pressed cancel
                    System.exit(0);
                }

                try {
                    playerID = Integer.parseInt(input);
                }
                catch (NumberFormatException e) {
                    JOptionPane.showMessageDialog(frame, "Invaild id");
                }
            }
            // For simplicity, assign all players to team 1 
            // players.add(new Player(playerID, 1));

            String codename = db.getCodename(playerID);

            if (codename == null) {
                // Player not found → ask for codename
                codename = JOptionPane.showInputDialog(frame, "Enter codename for new player:");
                if (codename == null) System.exit(0);

                db.addPlayer(playerID, codename);
            }

            // 🔹 Assign team (even = Red, odd = Green)
            int teamCode = (playerID % 2 == 0) ? 1 : 2;

            // 🔹 Create Player object
            Player player = new Player(codename, teamCode);
            players.add(player);
        }



        // Show all players
        StringBuilder sb = new StringBuilder("Players created:\n");
        for (Player p : players) {
            sb.append(p.getPlayerInfo()).append("\n");
        }
        JOptionPane.showMessageDialog(frame, sb.toString());

        frame.dispose(); // Close frame
    }

    // Method to display splash screen
    private static void showSplashScreen(JFrame frame, String imagePath) {
        JDialog splash = new JDialog(frame, "Splash", false);
        ImageIcon icon = new ImageIcon(imagePath);
        Image img = icon.getImage();
        Image scaledImage = img.getScaledInstance(800,600,Image.SCALE_SMOOTH);
        ImageIcon scaledIcon = new ImageIcon(scaledImage);
        JLabel label = new JLabel(scaledIcon);
        splash.getContentPane().add(label);
        splash.pack();
        splash.setLocationRelativeTo(null);

        // Display splash for 3 seconds
        //new Thread(() -> {
            splash.setVisible(true);
       // }).start();

        try {
            Thread.sleep(6000); // 6 seconds
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        splash.dispose();
    }
}