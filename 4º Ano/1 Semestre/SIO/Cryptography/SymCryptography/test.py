from time import sleep

x = 'hello benny'

h = [" ",'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
z = 0
t = ""

while t != x:
    for i in h:
        if t == x:
            break
        print(t + i, end='\r')  # Print the current state of 't' plus the current character 'i'
        if i == x[z]:
            t += i
            z += 1
            sleep(0.3)
            break
        sleep(0.1)
print()
