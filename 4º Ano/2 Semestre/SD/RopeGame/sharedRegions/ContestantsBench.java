package sharedRegions;

import Entities.*;

public class ContestantsBench
{

    private final Contestant [] team1;
    private final Contestant [] team2;
    private final Coach coach1;
    private final Coach coach2;


    private final GeneralRepos repos;

    public ContestantsBench (Coach coach1, Coach coach2, Contestants [] team1, Contestants [] team2, GeneralRepos repos)
    {
        this.repos = repos;
        this.team1 = team1;
        this.team2 = team2;
        this.coach1 = coach1;
        this.coach2 = coach2;
    }


    public synchronized void callContestants()
    {
    }

    public synchronized void informReferee()
    {
    }

    public synchronized void reviewNotes()
    {
    }

    public synchronized void seatDown()
    {
    }

    public synchronized void followCoachAdvice()
    {
    }
    
    public synchronized void waitForCallContestants()
    {
    }
}