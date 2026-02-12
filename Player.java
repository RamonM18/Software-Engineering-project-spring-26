
public class Player
{
    private static int nextPlayerNum = 1;
    private int playerNum;
    private String playerName;
    private int score = 0;
    private boolean isRedTeam;

    public Player(String playerName, boolean isRedTeam)
    {
        this.playerNum = nextPlayerNum;
        nextPlayerNum++;
        this.playerName = playerName;
        this.score = 0;
        this.isRedTeam = isRedTeam;
    }

    public Player(Player p)
    {
        this.playerNum = p.playerNum;
        this.playerName = p.playerName;
        this.score = p.score;
        this.isRedTeam = p.isRedTeam;
    }

    public String getPlayerName()
    {
        return playerName;
    }

    public int getPlayerNum()
    {
        return playerNum;
    }

    public int getScore()
    {
        return score;
    }

    public boolean getTeam()
    {
        return isRedTeam;
    }

    public void setPlayerName(String playerName)
    {
        this.playerName = playerName;
    }

    public void setScore(int score)
    {
        this.score = score;
    }

    public void setPlayerNum(int playerNum)
    {
        this.playerNum = playerNum;
    }

    public void setTeam(boolean isRedTeam)
    {
        this.isRedTeam = isRedTeam;
    }

    public String getPlayer()
    {
        String result = "";
        String teamName = "";

        if (isRedTeam)
        {
            teamName = "Red";
        }
        else {
            teamName = "Green";
        }

        result = "Player number: " + playerNum;
        result = result + ", Name: " + playerName;
        result = result + ", Score: " + score;
        result = result + ", Team: " + teamName;

        return result;


    }

    // Methods for adding score and subtracting
    public void addScore(int points)
    {
        this.score += points;
    }

    public void subtractScore(int points)
    {
        this.score -= points;
    }


    public static void main(String[] args) 
    {
        //Testing my code here
        Player p1 = new Player("Kyle", true);
        Player p2 = new Player("Ramon", false);

        System.out.println(p1.getPlayer());
        System.out.println(p2.getPlayer());

        p1.addScore(30);
        p2.subtractScore(10);

        System.out.println("\nResults\n");
        System.out.println(p1.getPlayer());
        System.out.println(p1.getPlayer());
    }
    
}