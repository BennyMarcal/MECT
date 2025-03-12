package aula1.Exercicio2;

public class TowerFunc {

    private StackFunc<Integer> stack;
    private String name;

    public TowerFunc(String name) {
        this.stack = new StackFunc<>();
        this.name = name;
    }

    public void pushDisk(int disk) {
        stack.push(disk);
    }

    public int popDisk() {
        return stack.pop();
    }

    public boolean isEmpty() {
        return stack.isEmpty();
    }

    public int size() {
        return stack.size();
    }

    public String getName() {
        return name;
    }

    @Override
    public String toString() {
        return name + " Tower: " + stack;
    }
}
