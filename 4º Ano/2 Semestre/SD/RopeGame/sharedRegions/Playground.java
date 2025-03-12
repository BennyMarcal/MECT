package sharedRegions;

import Entities.*;
import sharedRegions.*;

public class Playground
{
    private boolean matchEnded;

    
    public synchronized boolean isMatchEnded() {
        return matchEnded;
    }

    private final Contestant [] team1;
    private final Contestant [] team2;


    private final GeneralRepos repos;

    public Playground (Contestant [] team1, Contestant [] team2, GeneralRepos repos)
    {
        this.repos = repos;
        this.team1 = team1;
        this.team2 = team2;
    }


    public synchronized void followCoachAdvice()
    {
    }

    public synchronized void getReady()
    {
    }

    public synchronized void pullTheRope()
    {
    }

    public synchronized void amDone()
    {
    }

    
}