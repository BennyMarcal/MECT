package Entities;

import sharedRegions.*;
import main.*;

public class Referee extends Thread
{
    private int refereeState;

    private final ContestantsBench contestantsBench;
    private final Playground playground;
    private final RefereeSite refereeSite;

    public Referee(String name, int refereeID, RefereeSite refereeSite, Playground playground, ContestantsBench contestantsBench){
        super(name);
        refereeState = RefereeStates.MATCH_START;
        this.refereeSite = refereeSite;
        this.contestantsBench = contestantsBench;
        this.playground = playground;
    }

    /**
     *   Set referee state.
     *
     *     @param state new referee state
     */
    public void setRefereeState (int state)
    {
        refereeState = state;
    }

    /**
     *   Get referee state.
     *
     *     @return referee state
     */
    public int getRefereeState ()
    {
        return refereeState;
    }

    @Override

    public void run() {

        while(playground.isMatchEnded() == false) {
            refereeSite.announceNewGame();
            refereeSite.callTrial();
            refereeSite.startTrial();
            while(!refereeSite.assertTrialDecision().equals("END_OF_A_GAME")){
                refereeSite.callTrial();
                refereeSite.startTrial();
            }
            refereeSite.declareGameWinner();
        }
        refereeSite.declareMatchWinner();
    }
}
