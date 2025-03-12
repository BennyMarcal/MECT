package sharedRegions;

import Entities.*;
import main.*;
/**
 * This class represents the shared region managed by the Referee.
 */


public class RefereeSite {

    // Variables to keep track of the current game and trial number
    private int currentGameNumber = 0;
    private int currentTrialNumber = 0;

    // The current state of the Referee
    private int refereeState;

    public RefereeSite() {
        refereeState = RefereeStates.MATCH_START;
    }

    public synchronized void announceNewGame(){
        
    }

    public synchronized void startGame() {
        currentGameNumber++;
        currentTrialNumber = 0; // Reset the trial number at the start of each game
        refereeState = RefereeStates.GAME_START;
        notifyAll(); // Notify any waiting threads that a new game is starting
    }

    public synchronized void startTrial() {
        currentTrialNumber++;
        refereeState = RefereeStates.TEAMS_READY;
        notifyAll(); // Notify any waiting threads that a new trial is starting
    }

    public synchronized void endTrial() {
        if (currentTrialNumber == SimulPar.NUM_TRIALS) {
            refereeState = RefereeStates.END_OF_GAME;
        } else {
            refereeState = RefereeStates.WAITING;
        }
        notifyAll(); // Notify any waiting threads that the trial has ended
    }

    public synchronized void endGame() {
        refereeState = RefereeStates.END_OF_GAME;
        // Logic for ending a game, such as updating scores or preparing for the next game
        notifyAll(); // Notify any waiting threads that the game has ended
    }

   
    public synchronized void endMatch() {
        refereeState = RefereeStates.END_OF_MATCH;
        notifyAll(); // Notify any waiting threads that the match has ended
    }
    
    public synchronized boolean isMatchEnded() {
        return refereeState == RefereeStates.END_OF_MATCH;
    }
    
    public synchronized boolean isGameEnded() {
        return currentTrialNumber == SimulPar.NUM_TRIALS;
    }
    
    // Methods to wait for a certain state to be reached
    public synchronized void waitForState(int state) {
        while (refereeState != state) {
            try {
                wait();  // Wait until the required state is set
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt(); // Preserve interrupt status
                throw new RuntimeException("Thread was interrupted", e);
            }
        }
    }
    
    // Getters for current game and trial numbers
    public synchronized int getCurrentGameNumber() {
        return currentGameNumber;
    }
    
    public synchronized int getCurrentTrialNumber() {
        return currentTrialNumber;
    }
    
    // Getters and setters for refereeState
    public synchronized int getRefereeState() {
        return refereeState;
    }
    
    public synchronized void setRefereeState(int state) {
        this.refereeState = state;
        notifyAll();  // Notify any threads waiting for a state change
    }

    public synchronized void announceMatch() {
        // Logic to handle match start
        notifyAll(); // Notify any waiting threads
    }

    public synchronized void callTrial() {
        // Logic to handle call for trial
        notifyAll(); // Notify any waiting threads
    }

    public synchronized void waitForTrialConclusion() {
        /** Wait for trial to conclude
        try {
            while (/* condition to wait for trial conclusion ) {
                wait();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt(); // Handle interrupted exception
        }*/
    }

    public synchronized String assertTrialDecision() {
        String aux = "Game End";
        // Logic to assert trial decision
        notifyAll(); // Notify any waiting threads
        return aux;
        
    }

    public synchronized void declareGameWinner() {
        // Logic to declare game winner
        notifyAll(); // Notify any waiting threads
    }

    public synchronized void declareMatchWinner() {
        // Logic to declare match winner
        notifyAll(); // Notify any waiting threads
    }
}    