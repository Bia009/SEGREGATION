import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


class Segre:

    def __init__(self, tpopu, simiTS, n_neigh):

        self.size = 2601  # Tamanho do tabuleiro
        self.tpopu = tpopu  # Tamanho da população
        self.simiTS = simiTS  # Valor de similares na vizinhança
        self.n_neigh = n_neigh  # Quantidade de vizinhos(Amplitude)
        self.mean_similarity = []  # Media da similaridade

        # Montagem do tabuleiro
        self.city = np.random.choice([-1, 1], size=self.tpopu)  # Para iniciar aleatoriamente
        self.houses = np.zeros(shape=(self.size - self.tpopu))  # Cria um numero de casa vazias
        self.city = np.concatenate([self.city, self.houses])  # juntando vetores
        np.random.shuffle(self.city)  # Embaralha as casas no tabuleiro

        self.city = np.reshape(self.city, newshape=(int(self.size // np.sqrt(self.size)), int(self.size // np.sqrt(
            self.size))))  # Tabuleiro(transformando em matriz quadrada)

    # Executa um passo da simulação, calculando o a satisfação de cada casa e executando as mudanças de posição
    def runn(self):  # Retorna se existe casas insatisfeitas(unhappy)
        unhappy = False
        for index, value in np.ndenumerate(self.city):
            state = self.city[index[0], index[1]]  # -1, 1 ou 0
            if state != 0:
                neighborhood = self.city[index[0] - self.n_neigh:index[0] + self.n_neigh,
                               index[1] - self.n_neigh:index[1] + self.n_neigh]  # Procurar por vizinhos semelhantes
                nbsize = np.size(np.where(neighborhood != 0)[0])  # Número de vizinhos
                n_empty = np.size(np.where(neighborhood == 0)[0])  #
                if nbsize != n_empty + 1:
                    nsimilar = np.size(np.where(neighborhood == state)[0]) - 1.
                    similar_ratio = nsimilar / (nbsize - 1)  # similarR = similar/total de vizinhos
                    if (similar_ratio < self.simiTS):  # Quanto maior simiTS mais insatisfeitos # Teste para saber se a casa está satisfeita ou não
                        unhappy = True
                        empty_houses = list(zip(np.where(self.city == 0)[0], np.where(self.city == 0)[
                            1]))  # Lista as casas vazias no mapa e muda para uma casa aleatória trocando o seu estado
                        random_house = random.choice(empty_houses)
                        self.city[random_house] = state
                        self.city[index[0], index[1]] = 0  # Transforma a casa anterior em vazia
        return unhappy

    def get_similarAV(self):  # Tira a media da similaridade de todos.

        count = 0
        similarity_ratio = 0
        for index, value in np.ndenumerate(self.city):
            race = self.city[index[0], index[1]]
            if race != 0:
                neighborhood = self.city[index[0] - self.n_neigh:index[0] + self.n_neigh,
                               index[1] - self.n_neigh:index[1] + self.n_neigh]
                nbsize = np.size(np.where(neighborhood != 0)[0])
                n_empty = np.size(np.where(neighborhood == 0)[0])
                if nbsize != n_empty + 1:
                    nsimilar = np.size(np.where(neighborhood == race)[0]) - 1
                    similarity_ratio += (nsimilar / (nbsize - 1.))
                    count += 1
        return similarity_ratio / count

    def start(self):  # Transforma a matriz em tabuleiro de cores e cria o grafico.

        self.mean_similarity.append(Bianca.get_similarAV())
        plt.style.use("ggplot")
        plt.figure(figsize=(8, 4))

        self.cmap = ListedColormap(['red', 'white', 'royalblue'])
        plt.subplot(121)
        plt.axis('off')
        plt.pcolor(self.city, cmap=self.cmap, edgecolors='w', linewidths=1)
        plt.subplot(122)
        plt.xlabel("Iterations")
        plt.ylim([0.4, 1])
        plt.title("Mean Similarity Ratio", fontsize=15)
        plt.text(1, 0.95, "Similarity Ratio: %.4f" % self.get_similarAV(), fontsize=10)

    def Simul(self):

        while self.runn():  # Loop enquanto tiver uma casa insatisfeita
            plt.clf()
            self.mean_similarity.append(self.get_similarAV())
            # plt.figure(figsize=(8, 4))

            plt.subplot(121)
            plt.axis('off')
            plt.pcolor(self.city, cmap=self.cmap, edgecolors='w', linewidths=1)

            plt.subplot(122)
            plt.xlabel("Iterations")
            plt.ylim([0.4, 1])
            plt.title("Mean Similarity Ratio", fontsize=15)
            plt.plot(range(1, len(self.mean_similarity) + 1), self.mean_similarity)
            plt.text(1, 0.95, "Similarity Ratio: %.4f" % self.get_similarAV(), fontsize=10)
            plt.pause(0.001)


Bianca = Segre(2500, 0.7, 2)
Bianca.start()

Bianca.Simul()