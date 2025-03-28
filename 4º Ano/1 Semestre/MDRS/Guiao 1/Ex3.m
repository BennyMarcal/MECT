%Aula 2

%% 3.a)
pstates = zeros(1, 5);
states = [10^-6 10^-5 10^-4 10^-3 10^-2];
den = 1 + 8/600 + 8/600 * 5/100 + 8/600 * 5/100 * 2/20 + 8/600 * 5/100 * 2/20 * 1/5; 
pstates(1) = 1 / den;
pstates(2) = (8/600) / den;
pstates(3) = (8/600 * 5/100) / den;
pstates(4) = (8/600 * 5/100 * 2/20) / den;
pstates(5) = (8/600 * 5/100 * 2/20 * 1/5) / den;

fprintf('The probability of link being in state 10^-6 is: %.2e\n', pstates(1));
fprintf('The probability of link being in state 10^-5 is: %.2e\n', pstates(2));
fprintf('The probability of link being in state 10^-4 is: %.2e\n', pstates(3));
fprintf('The probability of link being in state 10^-3 is: %.2e\n', pstates(4));
fprintf('The probability of link being in state 10^-2 is: %.2e\n', pstates(5));

%% 3.b)
fprintf(['Pelas propriedades das cadeias de Markov, a probabilidade de um link estar num' ...
    'determinado estado é igual à percentagem de tempo médio que cada link fica ness estado\n']);

%% 3.c)
ber = sum(pstates .* states);
fprintf('The average ber of the link is: %.2e\n', ber);

%% 3.d)
tavg_states = zeros(1, 5);
tavg_states(1) = 1/8;
tavg_states(2) = 1/(600 + 5);
tavg_states(3) = 1/(100 + 2);
tavg_states(4) = 1/(20 + 1);
tavg_states(5) = 1/5;

fprintf('The average time duration that the link stays is state 10^-6 is: %.2f min\n', tavg_states(1)*60);
fprintf('The average time duration that the link stays is state 10^-5 is: %.2f min\n', tavg_states(2)*60);
fprintf('The average time duration that the link stays is state 10^-4 is: %.2f min\n', tavg_states(3)*60);
fprintf('The average time duration that the link stays is state 10^-3 is: %.2f min\n', tavg_states(4)*60);
fprintf('The average time duration that the link stays is state 10^-2 is: %.2f min\n', tavg_states(5)*60);

%% 3.e)
pstate_normal = sum(pstates(1:3));
pstate_interference = sum(pstates(4:5));
fprintf('The probabilty of the link being in the normal state is: %.6f\n', pstate_normal);
fprintf('The probabilty of the link being in the interference state is: %.2e\n', pstate_interference);

%% 3.f)
ber_normal = sum(pstates(1:3) .* states(1:3))/pstate_normal;
ber_interference = sum(pstates(4:5) .* states(4:5))/pstate_interference;
fprintf('The average ber of the link when is in the normal state is: %.2e\n', ber_normal);
fprintf('The average ber of the link when is in the interference state is: %.2e\n', ber_interference);

%% 3.g)
x = 64:1500;
bits = 8;
p_errs = zeros(5, length(x));

for i = 1 : 5
    p_errs(i, 1:length(x)) = 1 - (1 - states(i)).^(x.*bits);
end

error = p_errs(1, 1:length(x)).*pstates(1) + p_errs(2, 1:length(x)).*pstates(2) + p_errs(3, 1:length(x)).*pstates(3) + p_errs(4, 1:length(x)).*pstates(4) + p_errs(5, 1:length(x)).*pstates(5);

figure(1);
plot(x, error, 'b');
xlabel('B (Bytes)');
title('Prob. of at least one error');
grid on;

%% 3.h)
error_normal = (p_errs(1, 1:length(x)) .* pstates(1) + p_errs(2, 1:length(x)) .* pstates(2) + p_errs(3, 1:length(x)) .* pstates(3)) ./ (p_errs(1, 1:length(x)) .* pstates(1) + p_errs(2, 1:length(x)) .* pstates(2) + p_errs(3, 1:length(x)) .* pstates(3) + p_errs(4, 1:length(x)) .* pstates(4) + p_errs(5, 1:length(x)) .* pstates(5));

figure(2);
plot(x, error_normal, 'b');
xlabel('B (Bytes)');
title('Prob. of Normal State');
grid on;

%% 3.i)
p_nerrs = zeros(5, length(x));

for i = 1 : 5
    p_nerrs(i, 1:length(x)) = (1 - states(i)).^(x.*bits);
end

error_interfece = (p_nerrs(4, 1:length(x)) .* pstates(4) + p_nerrs(5, 1:length(x)) .* pstates(5)) ./ (p_nerrs(1, 1:length(x)) .* pstates(1) + p_nerrs(2, 1:length(x)) .* pstates(2) + p_nerrs(3, 1:length(x)) .* pstates(3) + p_nerrs(4, 1:length(x)) .* pstates(4) + p_nerrs(5, 1:length(x)) .* pstates(5));

figure(3);
semilogy(x, error_interfece, 'b');
xlabel('B (Bytes)');
title('Prob. of Intereference State');
grid on;