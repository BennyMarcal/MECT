%Aula 1

%% 1.a)
p = 0.6;
n = 4;
p_answer = p+(1-p)/n;
right_answer = p_answer * 100;
fprintf('Probabilidade de acertar a resposta é: %d%%\n', right_answer);

%% 1.b)
p = 0.7;
n = 5;
p_know = (p*n) / ( 1 + (n-1)*p );
know_answer = p_know * 100;
fprintf('Probabilidade de saber a resposta quando acerta é de: %.1f%%\n', know_answer);

%% 1.c)
x = linspace(0, 1, 100);

prob3 = 1*x + 1/3 * (1-x);
prob4 = 1*x + 1/4 * (1-x);
prob5 = 1*x + 1/5 * (1-x);

figure(1);
plot(100*x, 100*prob3, 'b', 100*x, 100*prob4, 'b--', 100*x, 100*prob5, 'b:');
yticks(0:20:100); %escala do y 
xticks(0:10:100); %escala do x
xlabel('p (%)');
legend('n= 3','n= 4','n= 5', 'location','northwest');
title('Probability of right answer (%)');
ylim([0, 100]);
grid on;

%% 1.d)
x = linspace(0, 1, 100);

know3 = (x*3)./(1 + (3-1)*x);
know4 = (x*4)./(1 + (4-1)*x);
know5 = (x*5)./(1 + (5-1)*x);

figure(2);
plot(100*x, 100*know3, 'b', 100*x, 100*know4, 'b--', 100*x, 100*know5, 'b:');
yticks(0:20:100);
xticks(0:10:100);
xlabel('p (%)');
legend('n=3','n=4','n=5', 'location','northwest');
title('Probability of knowing the answer (%)');
ylim([0, 100]);
grid on;