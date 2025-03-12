import java.util.LinkedList;
import java.util.Queue;
import java.util.Stack;
import java.util.Scanner;

public class ArithmeticQueue {

    public static String add(String num1, String num2) {
        Stack<Integer> stack1 = new Stack<>();
        Stack<Integer> stack2 = new Stack<>();
        Stack<Integer> resultStack = new Stack<>();

        for (char c : num1.toCharArray()) stack1.push(Character.getNumericValue(c));
        for (char c : num2.toCharArray()) stack2.push(Character.getNumericValue(c));

        int carry = 0;
        while (!stack1.isEmpty() || !stack2.isEmpty() || carry != 0) {
            int sum = (stack1.isEmpty() ? 0 : stack1.pop()) + (stack2.isEmpty() ? 0 : stack2.pop()) + carry;
            resultStack.push(sum % 10);
            carry = sum / 10;
        }

        StringBuilder result = new StringBuilder();
        while (!resultStack.isEmpty()) result.append(resultStack.pop());
        return result.toString();
    }

    public static String multiply(String num1, String num2) {
        int len1 = num1.length(), len2 = num2.length();
        int[] result = new int[len1 + len2];

        for (int i = len1 - 1; i >= 0; i--) {
            for (int j = len2 - 1; j >= 0; j--) {
                int mul = (num1.charAt(i) - '0') * (num2.charAt(j) - '0');
                int sum = mul + result[i + j + 1];
                result[i + j + 1] = sum % 10;
                result[i + j] += sum / 10;
            }
        }

        StringBuilder resultStr = new StringBuilder();
        for (int num : result) {
            if (!(resultStr.length() == 0 && num == 0)) resultStr.append(num);
        }
        return resultStr.length() == 0 ? "0" : resultStr.toString();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Queue<String> operationsQueue = new LinkedList<>();

        while (true) {
            System.out.println("\nChoose an operation:");
            System.out.println("1. Addition");
            System.out.println("2. Multiplication");
            System.out.println("3. Process Queue");
            System.out.println("4. Exit");
            System.out.print("Option: ");

            String choice = scanner.nextLine();
            if (choice.equals("4")) {
                System.out.println("Exiting...");
                break;
            }

            if (choice.equals("3")) {
                while (!operationsQueue.isEmpty()) {
                    System.out.println(operationsQueue.poll());
                }
                continue;
            }

            System.out.print("Enter first number: ");
            String num1 = scanner.nextLine();
            System.out.print("Enter second number: ");
            String num2 = scanner.nextLine();

            if (!num1.matches("\\d+") || !num2.matches("\\d+")) {
                System.out.println("Error: Please enter only non-negative integers.");
                continue;
            }

            String result;
            if (choice.equals("1")) {
                result = "Result: " + add(num1, num2);
            } else if (choice.equals("2")) {
                result = "Result: " + multiply(num1, num2);
            } else {
                System.out.println("Invalid option.");
                continue;
            }
            
            operationsQueue.offer(result);
            System.out.println("Operation added to queue. Choose option 3 to process the queue.");
        }

        scanner.close();
    }
}
