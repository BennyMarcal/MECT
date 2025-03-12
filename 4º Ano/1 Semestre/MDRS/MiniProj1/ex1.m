% Task 1: Simulator2 for different bit error rates and arrival rates

% Given Parameters
lambda_values = [1500, 1600, 1700, 1800, 1900];  % Arrival rates
num_runs = 20;    % Number of runs for each lambda
P = 100000;       % Stopping criterion
C = 10;           % Link bandwidth in Mbps
f = 10000;        % Queue size in Bytes

% Part 1.a: For b = 10^-6
b_1a = 1e-6;  % Bit error rate for 1.a

% Initializing result storage for Part 1.a
APD_results_1a = zeros(num_runs, length(lambda_values));
PL_results_1a = zeros(num_runs, length(lambda_values));

% Running simulations for 1.a
for i = 1:length(lambda_values)
    lambda = lambda_values(i);
    for run = 1:num_runs
        [PL, APD, ~, ~] = Simulator2(lambda, C, f, P, b_1a);
        APD_results_1a(run, i) = APD;
        PL_results_1a(run, i) = PL;
    end
end

% Calculate mean and 90% confidence interval for Part 1.a
mean_APD_1a = mean(APD_results_1a);
mean_PL_1a = mean(PL_results_1a);
std_APD_1a = std(APD_results_1a);
std_PL_1a = std(PL_results_1a);

% Confidence interval (90% confidence)
t_value = tinv(0.95, num_runs-1);
error_APD_1a = t_value * std_APD_1a / sqrt(num_runs);
error_PL_1a = t_value * std_PL_1a / sqrt(num_runs);

% Plot bar chart with error bars for APD (1.a)
figure;
bar(lambda_values, mean_APD_1a);
hold on;
errorbar(lambda_values, mean_APD_1a, error_APD_1a, '.');
title('Average Packet Delay with 90% CI (b = 10^{-6})');
xlabel('Arrival Rate (packets/sec)');
ylabel('Average Packet Delay (ms)');
hold off;

% Plot bar chart with error bars for PL (1.a)
figure;
bar(lambda_values, mean_PL_1a);
hold on;
errorbar(lambda_values, mean_PL_1a, error_PL_1a, '.');
title('Packet Loss with 90% CI (b = 10^{-6})');
xlabel('Arrival Rate (packets/sec)');
ylabel('Packet Loss (%)');
hold off;

% Part 1.b: For b = 10^-4
b_1b = 1e-4;  % Bit error rate for 1.b

% Initializing result storage for Part 1.b
APD_results_1b = zeros(num_runs, length(lambda_values));
PL_results_1b = zeros(num_runs, length(lambda_values));

% Running simulations for 1.b
for i = 1:length(lambda_values)
    lambda = lambda_values(i);
    for run = 1:num_runs
        [PL, APD, ~, ~] = Simulator2(lambda, C, f, P, b_1b);
        APD_results_1b(run, i) = APD;
        PL_results_1b(run, i) = PL;
    end
end

% Calculate mean and 90% confidence interval for Part 1.b
mean_APD_1b = mean(APD_results_1b);
mean_PL_1b = mean(PL_results_1b);
std_APD_1b = std(APD_results_1b);
std_PL_1b = std(PL_results_1b);

% Confidence interval (90% confidence)
error_APD_1b = t_value * std_APD_1b / sqrt(num_runs);
error_PL_1b = t_value * std_PL_1b / sqrt(num_runs);

% Plot bar chart with error bars for APD (1.b)
figure;
bar(lambda_values, mean_APD_1b);
hold on;
errorbar(lambda_values, mean_APD_1b, error_APD_1b, '.');
title('Average Packet Delay with 90% CI (b = 10^{-4})');
xlabel('Arrival Rate (packets/sec)');
ylabel('Average Packet Delay (ms)');
hold off;

% Plot bar chart with error bars for PL (1.b)
figure;
bar(lambda_values, mean_PL_1b);
hold on;
errorbar(lambda_values, mean_PL_1b, error_PL_1b, '.');
title('Packet Loss with 90% CI (b = 10^{-4})');
xlabel('Arrival Rate (packets/sec)');
ylabel('Packet Loss (%)');
hold off;

% Part 1.c: Theoretical packet loss due to bit error rate

% Theoretical packet loss calculation for b = 10^-6 and b = 10^-4
b_values = [1e-6, 1e-4];
L = 8 * mean([64, 110, 1518]);  % Average packet size in bits (mean size)

% Theoretical packet loss
PL_theory = 1 - (1 - b_values).^L;

% Display theoretical results
fprintf('Theoretical Packet Loss for b = 10^-6: %.5f%%\n', PL_theory(1) * 100);
fprintf('Theoretical Packet Loss for b = 10^-4: %.5f%%\n', PL_theory(2) * 100);

% Comparison of theoretical vs simulated packet loss
figure;
bar([mean_PL_1a', mean_PL_1b']);
hold on;
theory_PL_plot = [PL_theory(1) * 100, PL_theory(2) * 100];
plot(lambda_values, theory_PL_plot(1) * ones(size(lambda_values)), 'r--');
plot(lambda_values, theory_PL_plot(2) * ones(size(lambda_values)), 'g--');
legend('Simulated b = 10^{-6}', 'Simulated b = 10^{-4}', 'Theory b = 10^{-6}', 'Theory b = 10^{-4}');
title('Comparison of Simulated vs Theoretical Packet Loss');
xlabel('Arrival Rate (packets/sec)');
ylabel('Packet Loss (%)');
hold off;
