package aula1.Exercicio1;

import java.util.*;

public class StackFunc<T> {

    private Stack<T> stack;

    public StackFunc() {
        this.stack = new Stack<>();
    }

    public void push(T element) {
        stack.push(element);
    }

    public T pop() {
        return stack.pop();
    }

    public boolean isEmpty() {
        return stack.isEmpty();
    }
}
