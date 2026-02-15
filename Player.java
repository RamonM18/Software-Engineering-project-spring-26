
public class Player
{
    private static int nextPlayerNum = 1;
    private int playerNum;
    private String playerName;
    private int score = 0;
    private int teamCode;


    public Player(String playerName, int teamCode)
    {
        this.playerNum = nextPlayerNum++;
        this.playerName = playerName;
        this.score = 0;
        this.teamCode = teamCode;
    }

    public Player(Player p)
    {
        this.playerNum = p.playerNum;
        this.playerName = p.playerName;
        this.score = p.score;
        this.teamCode = p.teamCode;
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

    public static int getNextPlayerNum()
    {
        return nextPlayerNum;
    }

    public String getTeam()
    {
        if (teamCode == 1) 
        {
            return "Red";
        }
        else if (teamCode == 2) 
        {
            return "Green";
        }
        else 
        {
            return "Unassigned";
        }
    }

    public void setScore(int score)
    {
        this.score = score;
    }

    public void setPlayerNum(int playerNum)
    {
        this.playerNum = playerNum;
    }

    public String getPlayerInfo()
    {
        return "Player Number: " + playerNum
        + ", Name: " + playerName
        + ", Score: " + score
        + ", Team: " + getTeam();

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
    
        
       
    }
    
}