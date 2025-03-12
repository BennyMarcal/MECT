# Carregar pacotes necessários
install.packages("ggplot2")
install.packages("dplyr")
install.packages("tidyverse")
install.packages("emojifont")

library(ggplot2)
library(dplyr)
library(tidyverse)
library(emojifont)

# 1. Carregar e visualizar um conjunto de dados
data <- mtcars
print("Conjunto de dados mtcars:")
print(head(data))

# 2. Estatísticas descritivas
summary_stats <- summary(data)
print("Estatísticas descritivas:")
print(summary_stats)

# 3. Geração de gráficos simples

# Histograma do consumo de combustível (mpg)
ggplot(data, aes(x=mpg)) +
  geom_histogram(binwidth=2, fill="blue", color="black", alpha=0.7) +
  labs(title="Histograma do Consumo de Combustível (mpg)", x="Milhas por Galão", y="Frequência")

# Gráfico de dispersão (mpg vs hp)
ggplot(data, aes(x=hp, y=mpg)) +
  geom_point(color="red") +
  labs(title="Gráfico de Dispersão (mpg vs hp)", x="Potência (hp)", y="Milhas por Galão (mpg)")

# 4. Análise de regressão linear
modelo <- lm(mpg ~ hp, data=data)
print("Resumo do modelo de regressão:")
print(summary(modelo))

# 5. Função divertida: gráfico com emojis

# Função para criar um gráfico com emojis
plot_with_emojis <- function(data, x, y, emoji) {
  ggplot(data, aes_string(x=x, y=y)) +
    geom_point(color="transparent") +
    geom_text(aes(label=emoji), family="EmojiOne", size=6) +
    labs(title=paste("Gráfico de", x, "vs", y, "com Emojis"), x=x, y=y)
}

# Usar a função divertida
print("Gráfico com emojis:")
emoji_plot <- plot_with_emojis(data, "hp", "mpg", emoji("1f602"))
print(emoji_plot)

# Exibir os gráficos
dev.new()
hist_plot <- ggplot(data, aes(x=mpg)) +
  geom_histogram(binwidth=2, fill="blue", color="black", alpha=0.7) +
  labs(title="Histograma do Consumo de Combustível (mpg)", x="Milhas por Galão", y="Frequência")
print(hist_plot)

dev.new()
scatter_plot <- ggplot(data, aes(x=hp, y=mpg)) +
  geom_point(color="red") +
  labs(title="Gráfico de Dispersão (mpg vs hp)", x="Potência (hp)", y="Milhas por Galão (mpg)")
print(scatter_plot)

dev.new()
print(emoji_plot)
