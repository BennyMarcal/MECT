package aula1.Exercicio2;

import java.util.*;

public class TowerOfHanoi {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter the number of disks: ");
        int numberOfDisks = scanner.nextInt();

        solveTowersOfHanoi(numberOfDisks);

        scanner.close();
    }

    private static void solveTowersOfHanoi(int n) {
        TowerFunc source = new TowerFunc("Source");
        TowerFunc auxiliary = new TowerFunc("Auxiliary");
        TowerFunc destination = new TowerFunc("Destination");

        // Initializing source tower with disks
        for (int i = n; i > 0; i--) {
            source.pushDisk(i);
        }

        // Solving Towers of Hanoi
        hanoi(n, source, auxiliary, destination);

        // Printing movements
        System.out.println("Movements:");
        printMovements(source, destination, auxiliary);
    }

    private static void hanoi(int n, TowerFunc source, TowerFunc auxiliary, TowerFunc destination) {
        if (n > 0) {
            // Move n-1 disks from source to auxiliary using destination as the auxiliary tower
            hanoi(n - 1, source, destination, auxiliary);

            // Move the nth disk from source to destination
            moveDisk(source, destination);

            // Move n-1 disks from auxiliary to destination using source as the auxiliary tower
            hanoi(n - 1, auxiliary, source, destination);
        }
    }

    private static void moveDisk(TowerFunc source, TowerFunc destination) {
        int disk = source.popDisk();
        destination.pushDisk(disk);
        System.out.println("Move disk " + disk + " from " + source.getName() + " to " + destination.getName());
    }

    private static void printMovements(TowerFunc source, TowerFunc destination, TowerFunc auxiliary) {
        System.out.println(source);
        System.out.println(auxiliary);
        System.out.println(destination);
    }
}

