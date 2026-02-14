import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;

public class Main {

    public static void main(String[] args) {
        // Create the main frame
        JFrame frame = new JFrame("Player Setup");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 400);
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
            String name = null;
            while (name == null || name.trim().isEmpty()) {
                name = JOptionPane.showInputDialog(frame, "Enter name for Player " + i + ":");
                if (name == null) { // User pressed cancel
                    System.exit(0);
                }
            }
            // For simplicity, assign all players to team 1 
            players.add(new Player(name, 1));
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
        JDialog splash = new JDialog(frame, "Splash", true);
        ImageIcon icon = new ImageIcon(imagePath);
        JLabel label = new JLabel(icon);
        splash.getContentPane().add(label);
        splash.pack();
        splash.setLocationRelativeTo(null);

        // Display splash for 3 seconds
        new Thread(() -> {
            splash.setVisible(true);
        }).start();

        try {
            Thread.sleep(3000); // 3 seconds
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        splash.dispose();
    }
}
