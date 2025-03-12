package Entities;

import sharedRegions.ContestantsBench;
import sharedRegions.Playground;
import sharedRegions.RefereeSite;

public class Coach extends Thread
{

    private int coachState;

    private final ContestantsBench contestantsBench;
    private final Playground playground;
    private final RefereeSite refereeSite;

    private final int team;


    /**
     *   Instantiation of a Coach thread.
     *
     *     @param name thread name
     *     @param refereesite reference
     *     @param playground reference
     *     @param contestantsBench reference
     */
    public Coach(String name, int team, RefereeSite refereeSite, Playground playground, ContestantsBench contestantsBench)
    {
        super (name);
        coachState = CoachStates.WAIT_FOR_REFEREE;
        this.playground = playground;
        this.contestantsBench = contestantsBench;
        this.refereeSite = refereeSite;
        this.team = team;
    }

    /**
     *   Get team
     *
     *     @return team
     */


    public int getteam ()
    {
        return team;
    }

    /**
     *   Set Coach state.
     *
     *     @param state new Coach state
     */
    public void setCoachState (int state)
    {
        coachState = state;
    }

    /**
     *   Get Coach state.
     *
     *     @return Coach state
     */
    public int getCoachState ()
    {
        return coachState;
    }

    /**
     *   Life cycle of the coach.
     */
    @Override
    public synchronized void run ()
    {
        while (playground.isMatchEnded() == false)
        {
            contestantsBench.callContestants();
            contestantsBench.informReferee();
            contestantsBench.reviewNotes();
        }
    }
}