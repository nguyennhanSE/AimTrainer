class ScoreManager:

    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.score: int = 0
        self.reaction_times: list[float] = []

    def register_hit(self, reaction_time_ms: float, ttl: float) -> int:
        time_bonus = int(max(0, ttl - reaction_time_ms) / ttl * 50) if ttl > 0 else 0
        points = 100 + time_bonus
        self.score += points
        self.hits += 1
        self.reaction_times.append(reaction_time_ms)
        return points

    def register_miss(self) -> None:
        self.misses += 1

    def reset(self) -> None:
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.reaction_times = []

    @property
    def accuracy(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return self.hits / total * 100

    @property
    def avg_reaction_time(self) -> float:
        if not self.reaction_times:
            return 0.0
        return sum(self.reaction_times) / len(self.reaction_times)

    @property
    def best_reaction_time(self) -> float:
        if not self.reaction_times:
            return 0.0
        return min(self.reaction_times)
