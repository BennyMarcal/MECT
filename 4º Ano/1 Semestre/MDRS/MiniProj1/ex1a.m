lambda_values = [1500, 1600, 1700, 1800, 1900];
num_runs = 20;
P = 100000;
C = 10;  % Mbps
f = 10000;  % Bytes
b = 1e-6;

APD_results = zeros(num_runs, length(lambda_values));
PL_results = zeros(num_runs, length(lambda_values));

for i = 1:length(lambda_values)
    lambda = lambda_values(i);
    for run = 1:num_runs
        [PL, APD, ~, ~] = Simulator2(lambda, C, f, P, b);
        APD_results(run, i) = APD;
        PL_results(run, i) = PL;
    end
end

% Compute mean and 90% confidence interval
mean_APD = mean(APD_results);
mean_PL = mean(PL_results);
std_APD = std(APD_results);
std_PL = std(PL_results);

% Confidence interval (90% confidence)
t_value = tinv(0.95, num_runs-1);
error_APD = t_value * std_APD / sqrt(num_runs);
error_PL = t_value * std_PL / sqrt(num_runs);

% Plot bar chart with error bars for APD
figure;
bar(lambda_values, mean_APD);
hold on;
errorbar(lambda_values, mean_APD, error_APD, '.');
title('Average Packet Delay with 90% CI');
xlabel('Arrival Rate (packets/sec)');
ylabel('Average Packet Delay (ms)');
hold off;

% Plot bar chart with error bars for PL
figure;
bar(lambda_values, mean_PL);
hold on;
errorbar(lambda_values, mean_PL, error_PL, '.');
title('Packet Loss with 90% CI');
xlabel('Arrival Rate (packets/sec)');
ylabel('Packet Loss (%)');
hold off;
