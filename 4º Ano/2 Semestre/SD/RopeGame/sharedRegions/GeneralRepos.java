package sharedRegions;

import Entities.*;
import main.*;

import java.io.*;
import java.util.*;

public class GeneralRepos {

    private final String logFileName;

    private int[] contestantStates;
    private int[] contestantStrengths;
    private int[] coachStates;
    private int refereeState;
    private int nGames;
    private int nTrial;
    private int mark;
    private int[][] participatingContestants;

    public GeneralRepos(String logFileName, int[] initialStrengths) {
        if (logFileName == null || logFileName.equals(""))
            this.logFileName = "logger";
        else
            this.logFileName = logFileName;

        contestantStates = new int[SimulPar.NUM_TEAMS * SimulPar.TEAM_SIZE];
        contestantStrengths = new int[SimulPar.NUM_TEAMS * SimulPar.TEAM_SIZE];
        for (int i = 0; i < SimulPar.NUM_TEAMS * SimulPar.TEAM_SIZE; i++) {
            contestantStates[i] = ContestantStates.SEAT_AT_BENCH;
            contestantStrengths[i] = initialStrengths[i];
        }

        coachStates = new int[SimulPar.NUM_TEAMS];
        for (int i = 0; i < SimulPar.NUM_TEAMS; i++) {
            coachStates[i] = CoachStates.WAIT_FOR_REFEREE;
        }

        participatingContestants = new int[SimulPar.NUM_TEAMS][SimulPar.COMPETING_MEMBERS_PER_TRIAL];
        for (int i = 0; i < SimulPar.NUM_TEAMS; i++) {
            for (int j = 0; j < SimulPar.COMPETING_MEMBERS_PER_TRIAL; j++) {
                participatingContestants[i][j] = -1;
            }
        }

        printTitle();
        printHeader();
    }

    public synchronized void setContestantState(int id, int state) {
        contestantStates[id] = state;
        printState();
    }

    public synchronized void setParticipatingContestants(int id, int[] participatingContestants) {
        this.participatingContestants[id] = participatingContestants;
    }

    public synchronized void setCoachState(int id, int state) {
        coachStates[id] = state;
        printState();
    }

    public synchronized void setRefereeState(int state) {
        this.refereeState = state;
        if (state == RefereeStates.START_OF_GAME) {
            nGames++;
            nTrial = 0;
            mark = 0;
            printGame();
            printHeader();
        }

        if (state == RefereeStates.WAIT_FOR_TRIAL_CONCLUSION) {
            nTrial++;
        }
        printState();
    }

    public synchronized void setMark(int mark) {
        this.mark = mark;
    }

    public synchronized void updateContestantsStrength(int id, int[] contestantsStrength) {
        for (int i = id * SimulPar.TEAM_SIZE; i < (id + 1) * SimulPar.TEAM_SIZE; i++) {
            contestantStrengths[i] = contestantsStrength[i % SimulPar.TEAM_SIZE];
        }
    }

    public synchronized void declareGameWinner(int id) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            if (nTrial == SimulPar.MAX_TRIALS) {
                writer.println(String.format("Game %d was won by team %d by points.", nGames, id + 1));
            } else {
                writer.println(String.format("Game %d was won by team %d by knockout in %d trials.", nGames, id + 1, nTrial));
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public synchronized void declareGameDraw() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            writer.println(String.format("Game %d was a draw.", nGames));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public synchronized void declareMatchWinner(int id, int pointsTeam1, int pointsTeam2) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            writer.println(String.format("Match was won by team %d (%d - %d).", id + 1, pointsTeam1, pointsTeam2));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public synchronized void declareMatchDraw(int pointsTeam1, int pointsTeam2) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            writer.println(String.format("Match was a draw (%d - %d).", pointsTeam1, pointsTeam2));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void printTitle() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            writer.println("                            Game of the Rope - Description of the internal state\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void printHeader() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            writer.println("Ref Coa 1 Cont 1 Cont 2 Cont 3 Cont 4 Cont 5 Coa 2 Cont 1 Cont 2 Cont 3 Cont 4 Cont 5         Trial       ");
            writer.println("Sta  Stat Sta SG Sta SG Sta SG Sta SG Sta SG  Stat Sta SG Sta SG Sta SG Sta SG Sta SG   3 2 1 . 1 2 3 NB PS");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void printGame() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            writer.println("Game " + nGames);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void printState() {
        try (PrintWriter writer = new PrintWriter(new FileWriter(logFileName, true))) {
            String states = String.format("%3d  %4d %3d %2d %3d %2d %3d %2d %3d %2d %3d %2d  %4d %3d %2d %3d %2d %3d %2d %3d %2d %3d %2d",
                    refereeState,
                    coachStates[0],
                    contestantStates[0], contestantStrengths[0],
                    contestantStates[1], contestantStrengths[1],
                    contestantStates[2], contestantStrengths[2],
                    contestantStates[3], contestantStrengths[3],
                    contestantStates[4], contestantStrengths[4],
                    coachStates[1],
                    contestantStates[5], contestantStrengths[5],
                    contestantStates[6], contestantStrengths[6],
                    contestantStates[7], contestantStrengths[7],
                    contestantStates[8], contestantStrengths[8],
                    contestantStates[9], contestantStrengths[9]
            );

            StringBuilder trialStatus = new StringBuilder();
            for (int teamID = 0; teamID < SimulPar.NUM_TEAMS; teamID++) {
                for (int i = 0; i < SimulPar.COMPETING_MEMBERS_PER_TRIAL; i++) {
                    int idToAppend = participatingContestants[teamID][i];
                    if (idToAppend != -1) {
                        trialStatus.append(String.format("%d ", idToAppend));
                    } else {
                        trialStatus.append("- ");
                    }
                }
                if (teamID == 0) trialStatus.append(". ");
            }

            if (nTrial > 0) {
                trialStatus.append(String.format("%d ", nTrial));
                trialStatus.append(mark);
            }

            writer.println(states + "   " + trialStatus);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
