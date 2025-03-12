package Entities;
/**
 *    Definition of the internal states of the referee during his life cycle.
 */
public final class ContestantStates
{
    /**
     *   Initial state, the contestants are sat in the bench
     */
    public static final int SEAT_AT_BENCH = 0;

    /**
     *   The contestants will be in position to start the game, startTrial() given by referee
     */
    public static final int POSITION = 1;

    /**
     *   The contestants will play the game (will, in fact, be in silent for a random time) until the referee calls the end of the game, assertTrialDecision()
     */
    public static final int DO_YOUR_BEST = 2;
    
    private ContestantStates ()
    { }
}