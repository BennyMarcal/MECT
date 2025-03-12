package Entities;
/**
 *    Definition of the internal states of the referee during his life cycle.
 */
public final class RefereeStates
{
    /**
     *   Initial state, the referee is ready to start the match and can only be changed to the next state by starting the life cycle by announceNewGame()
     */
    public static final int MATCH_START = 0;
    /**
     *   The referee can now start the game.
     */
    public static final int START_OF_GAME = 1;
    /**
     *   The referee receives a signal from both teams that they are ready to start the game, informReferee()
     */
    public static final int TEAMS_READY = 2;
    /**
     *   The referee is waiting for the signal of end game, amDone() 
     */
    public static final int WAIT_FOR_TRIAL_CONCLUSION = 3;
    /**
     *  Second last state, the referee is presenting the report of end of game
     */
    public static final int END_OF_GAME = 4;
    /**
     *  Final state, the referee is presenting the report of end of match  
     */
    public static final int END_OF_MATCH = 5;

    private RefereeStates ()
    { }
}