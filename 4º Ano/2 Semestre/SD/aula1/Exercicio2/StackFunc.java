package aula1.Exercicio2;

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

    public int size() {
        return stack.size();
    }

    @Override
    public String toString() {
        return stack.toString();
    }
}

