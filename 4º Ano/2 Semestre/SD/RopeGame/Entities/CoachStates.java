package Entities;
/**
 *    Definition of the internal states of the referee during his life cycle.
 */
public final class CoachStates
{
    /**
     *   Initial state, the coach receives a sign of start from the referee, callTrial(), to choose the next team to play
     */
    public static final int WAIT_FOR_REFEREE = 0;
    /**
     *   The coach sends a followCoachAdvice() to the players to assemble the team
     */
    public static final int ASSEMBLE = 1;

    /**
     *   The coach waits for the end of the game, assertTrialDecision()
     */
    public static final int WATCH = 2;

    private CoachStates ()
    { }
}