import java.util.*;

public class b1_1 {
    public static void main(String[] args) {
        double num1, num2, resultado = 0;
        String operador;
        Scanner scanner = new Scanner(System.in);

        while (true) {
            try {
                System.out.print("Please insert a basic Mathematic operation: ");
                String input = scanner.nextLine();

                // Usando regex para dividir a entrada em números e operador
                String[] partes = input.split("\\s*([-+*/])\\s*");

                // Analisando os números
                num1 = Double.parseDouble(partes[0]);
                operador = input.replaceAll(".*?([-+*/]).*", "$1"); // Extraindo o operador
                num2 = Double.parseDouble(partes[1]);

                // Realizando a operação
                switch (operador) {
                    case "+":
                        resultado = num1 + num2;
                        break;
                    case "-":
                        resultado = num1 - num2;
                        break;
                    case "*":
                        resultado = num1 * num2;
                        break;
                    case "/":
                        if (num2 != 0) {
                            resultado = num1 / num2;
                        } else {
                            System.err.println("It's impossible to divide by zero, please try again!");
                            continue;
                        }
                        break;
                    default:
                        System.err.println("Invalid operator. Please try again using valid operators: +, -, *, /");
                        continue;
                }

                // Exibindo o resultado
                System.out.println("Result: " + resultado);

            } catch (NumberFormatException e) {
                System.err.println("Invalid Input. Please try again using valid numbers and operators!.");
            } catch (ArrayIndexOutOfBoundsException e) {
                System.err.println("Incorrect number of inputs, use this method <num> <op> <num>. Try again!");
            }
        }
    }
}
