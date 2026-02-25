import json
import os
from datetime import datetime
class ScoreManager:

    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.score: int = 0
        self.reaction_times: list[float] = []
        
        # Combo System: 
        self.current_combo: int = 0
        self.max_combo: int = 0
        
    @property
    def multiplier(self) -> float:
        """Tính hệ số nhân điểm dựa trên Combo hiện tại"""
        if self.current_combo >= 30: return 2.5
        if self.current_combo >= 20: return 2.0
        if self.current_combo >= 10: return 1.5
        if self.current_combo >= 5:  return 1.2
        return 1.0

    def register_hit(self, reaction_time_ms: float, ttl: float) -> int:
        self.current_combo += 1
        if self.current_combo > self.max_combo:
            self.max_combo = self.current_combo
            
        time_bonus = int(max(0, ttl - reaction_time_ms) / ttl * 50) if ttl > 0 else 0
        # points = 100 + time_bonus
        points = int((100 + time_bonus) * self.multiplier)
        self.score += points
        self.hits += 1
        self.reaction_times.append(reaction_time_ms)
        return points

    def register_miss(self) -> None:
        self.misses += 1
        self.current_combo = 0

    def reset(self) -> None:
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.reaction_times = []
        self.current_combo = 0
        self.max_combo = 0

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

    def save_session(self, mode: str = "basic") -> None:
        """Lưu kết quả ván chơi vào file JSON"""
        stats_file = "stats.json"
        data = []
        
        # Đọc dữ liệu cũ nếu có
        if os.path.exists(stats_file):
            try:
                with open(stats_file, "r") as f:
                    data = json.load(f)
            except Exception:
                pass
                
        # Tạo record mới
        session = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "mode": mode,
            "score": self.score,
            "hits": self.hits,
            "misses": self.misses,
            "accuracy": round(self.accuracy, 2),
            "avg_reaction": round(self.avg_reaction_time, 2),
            "best_reaction": round(self.best_reaction_time, 2),
            "max_combo": self.max_combo
        }
        data.append(session)
        
        # Ghi đè file
        try:
            with open(stats_file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception:
            pass