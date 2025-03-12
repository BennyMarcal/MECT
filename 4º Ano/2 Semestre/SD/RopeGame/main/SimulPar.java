package main;

/**
 *    Definition of simulation parameters for the Tug of War game.
 */
public final class SimulPar
{
   /**
    *   Maximum number of matches.
    */
    public static final int NUM_MATCHES = 1;

  /**
   *   Number of games in a match.
   */
   public static final int NUM_GAMES = 3;

   /**
    *   Maximum number of attempts per game.
    */
    public static final int MAX_TRIALS = 6;

  /**
   *   Number of teams.
   */
   public static final int NUM_TEAMS = 2;

  /**
   *   Number of units of length indicating a knockout victory.
   */
   public static final int KNOCKOUT_DISTANCE = 4;

  /**
   *   Number of members in each team.
   */
   public static final int TEAM_SIZE = 5;

  /**
   *   Number of members competing in each attempt.
   */
   public static final int COMPETING_MEMBERS_PER_TRIAL = 3;

  /**
   *   Maximum strength of each competitor.
   */
   public static final int MAX_STRENGTH = 10;

   /**
   *   Minimum strength of each competitor.
   */
   public static final int MIN_STRENGTH = 4;

  /**
   *   Team 1 trials.
   */
   public static final int TEAM1_TRIALS = 0;

   /**
   *   Team 2 trials.
   */
   public static final int TEAM2_TRIALS = 0;

    /**
   *   Team 1 games.
   */
   public static final int TEAM1_GAMES = 0;

   /**
   *   Team 2 games.
   */
   public static final int TEAM2_GAMES = 0;

   /**
   *   Length of the rope.
   */
   public static final int ROPE_LENGTH = 20;

   /**
   *   Length of the playing field.
   */
   public static final int FIELD_LENGTH = 30;

   private SimulPar ()
   { }
}
