package Entities;

import sharedRegions.*;

public class Contestant extends Thread
{


    private final ContestantsBench contestantsBench;
    private final Playground playground;
    private final RefereeSite refereeSite;

    private int contestantsState;
    private final int strength;
    private final int team;
    private final int contestantId;
    private boolean matchOverFlag;


    /**
     *   Instantiation of a Contestants thread.
     *
     *     @param name thread name
     *     @param refereesite reference to the Referee Site
     *     @param playground reference to the Playground
     *     @param contestantsBench reference to the ContestantsBench
     */
    public Contestant(String name, int team, int contestantId, int strength, RefereeSite refereeSite, Playground playground, ContestantsBench contestantsBench)
    {
        super (name);
        this.contestantId = contestantId;
        contestantsState = ContestantStates.SEAT_AT_BENCH;
        this.team = team;
        this.playground = playground;
        this.contestantsBench = contestantsBench;
        this.refereeSite = refereeSite;
        this.strength = strength;
    }

    
    /**
     *   Get contestant id.
     *
     *     @return contestant id
     */


    public int getcontestantId ()
    {
        return contestantId;
    }

    /**
     *   Set Contestants state.
     *
     *     @param state new Contestants state
     */
    public void setContestantsState (int state)
    {
        contestantsState = state;
    }

    /**
     *   Get Contestants state.
     *
     *     @return Contestants state
     */
    public int getContestantsState ()
    {
        return contestantsState;
    }

    /**
     *   Get the Contestants strength
     *
     *     @return the Contestants's strength
     */

    public int getStrength ()
    {
        return strength;
    }

    /**
     *   Life cycle of the contestants.
     */
    @Override
    public synchronized void run (){
        while(true){
           contestantsBench.waitForCallContestants();
           if (matchOverFlag) 
           break;

           this.contestantsBench.followCoachAdvice();

           playground.getReady();;
           playground.pullTheRope();;
           playground.amDone();; 
           refereeSite.waitForTrialConclusion();
           contestantsBench.seatDown();;
        }
   }
}