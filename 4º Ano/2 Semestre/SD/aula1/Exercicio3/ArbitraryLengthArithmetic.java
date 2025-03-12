import java.math.BigInteger;
import java.util.Scanner;

public class ArbitraryLengthArithmetic {

    public static String add(String num1, String num2) {
        BigInteger bigNum1 = new BigInteger(num1);
        BigInteger bigNum2 = new BigInteger(num2);
        return bigNum1.add(bigNum2).toString();
    }

    public static String multiply(String num1, String num2) {
        BigInteger bigNum1 = new BigInteger(num1);
        BigInteger bigNum2 = new BigInteger(num2);
        return bigNum1.multiply(bigNum2).toString();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        while (true) {
            System.out.println("\nChoose an operation:");
            System.out.println("1. Addition");
            System.out.println("2. Multiplication");
            System.out.println("3. Exit");
            System.out.print("Option: ");
            
            String choice = scanner.nextLine();
            if (choice.equals("3")) {
                System.out.println("Exiting...");
                break;
            }
            
            System.out.print("Enter first number: ");
            String num1 = scanner.nextLine();
            System.out.print("Enter second number: ");
            String num2 = scanner.nextLine();
            
            if (!num1.matches("\\d+") || !num2.matches("\\d+")) {
                System.out.println("Error: Please enter only non-negative integers.");
                continue;
            }
            
            if (choice.equals("1")) {
                System.out.println("Result: " + add(num1, num2));
            } else if (choice.equals("2")) {
                System.out.println("Result: " + multiply(num1, num2));
            } else {
                System.out.println("Invalid option.");
            }
        }
        
        scanner.close();
    }
}
