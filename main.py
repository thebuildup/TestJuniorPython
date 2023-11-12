import random
import matplotlib.pyplot as plt
import networkx as nx

class CityGrid:
    def __init__(self, N, M, obstruction_prob=0.3):
        # Инициализация городской сетки
        self.N = N
        self.M = M
        self.obstructed = [[random.random() < obstruction_prob for _ in range(M)] for _ in range(N)]
        self.towers = []

    def place_tower(self, row, col, R, cost):
        # Размещение башни в указанных координатах с заданным радиусом и стоимостью
        self.towers.append((row, col, R, cost))

    def visualize_tower_coverage(self):
        # Визуализация городской сетки с башнями и их зонами покрытия
        plt.figure()
        plt.imshow(self.obstructed, cmap='gray', origin='lower')

        for i, tower in enumerate(self.towers):
            row, col, R, cost = tower
            plt.scatter(col, row, c='red', marker='x')
            coverage = plt.Circle((col, row), R, color='blue', alpha=0.3)
            plt.gca().add_patch(coverage)
            plt.text(col, row, f"{i}\nR: {R}\nCost: {cost}", color='white', ha='center', va='center')

        plt.title('Город с зоной покрытия башен')
        plt.show()

    def place_towers_optimally(self, R):
        # Размещение башен оптимальным образом с заданным радиусом
        for row in range(self.N):
            for col in range(self.M):
                if not self.obstructed[row][col]:
                    # Предполагаем, что стоимость случайна для демонстрационных целей
                    cost = random.randint(5, 20)
                    self.place_tower(row, col, R, cost)
                    self.update_obstructed_blocks(row, col, R)

    def update_obstructed_blocks(self, row, col, R):
        # Обновление прегражденных блоков вокруг размещенной башни
        for i in range(max(0, row - R), min(self.N, row + R + 1)):
            for j in range(max(0, col - R), min(self.M, col + R + 1)):
                if (row - i)**2 + (col - j)**2 <= R**2:
                    self.obstructed[i][j] = True

    def find_reliable_path(self, start_tower, end_tower):
        # Реализация алгоритма поиска наиболее надежного пути
        G = nx.Graph()

        for tower in self.towers:
            G.add_node(tower)

        for i, tower1 in enumerate(self.towers):
            for j, tower2 in enumerate(self.towers):
                if i < j:
                    distance = self.calculate_distance(tower1, tower2)
                    reliability = 1 / (distance + 1)  # Простая метрика надежности
                    G.add_edge(tower1, tower2, weight=reliability)

        path = nx.shortest_path(G, source=start_tower, target=end_tower, weight='weight')
        return path

    def calculate_distance(self, tower1, tower2):
        row1, col1, _ , _ = tower1
        row2, col2, _ , _ = tower2
        return ((row1 - row2)**2 + (col1 - col2)**2)**0.5

# Пример использования
city = CityGrid(N=10, M=10)
city.place_towers_optimally(R=3)
city.visualize_tower_coverage()

# Выбор двух башен для поиска надежного пути
start_tower = city.towers[0]
end_tower = city.towers[1]

# Нахождение наиболее надежного пути
reliable_path = city.find_reliable_path(start_tower, end_tower)
print("Наиболее надежный путь:", reliable_path)
