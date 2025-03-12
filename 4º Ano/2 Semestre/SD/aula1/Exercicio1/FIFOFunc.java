package aula1.Exercicio1;

import java.util.*;

public class FIFOFunc<T> {

    private Queue<T> queue;

    public FIFOFunc() {
        this.queue = new LinkedList<>();
    }

    public void offer(T element) {
        queue.offer(element);
    }

    public T poll() {
        return queue.poll();
    }

    public boolean isEmpty() {
        return queue.isEmpty();
    }
}
