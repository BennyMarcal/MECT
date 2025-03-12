package aula1.Exercicio1;

import java.util.Scanner;

public class PalindromeMain {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        while (true) {
            try {
                System.out.print("Enter a string (or type 'E' to end): ");
                String input = scanner.nextLine();

                if (input.equalsIgnoreCase("E")) {
                    break;
                }

                if (isPalindrome(input)) {
                    System.out.println("The entered string is a palindrome.");
                } else {
                    System.out.println("The entered string is not a palindrome.");
                }
            } catch (Exception e) {
                System.out.println("An error occurred: " + e.getMessage());
                scanner.nextLine(); // Consume the invalid input to avoid an infinite loop
            }
        }

        scanner.close();
    }

    private static boolean isPalindrome(String str) {
        String cleanedString = str.replaceAll("[^a-zA-Z]", "").toLowerCase();

        FIFOFunc<Character> queue = new FIFOFunc<>();
        StackFunc<Character> stack = new StackFunc<>();

        for (char c : cleanedString.toCharArray()) {
            queue.offer(c);
            stack.push(c);
        }

        while (!queue.isEmpty() && !stack.isEmpty()) {
            if (!queue.poll().equals(stack.pop())) {
                return false;
            }
        }

        return true;
    }
}
