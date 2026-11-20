"""Custom HashTable and recursive Tower of Hanoi solver."""


class HashTable:
    """Hash table using separate chaining with buckets."""

    def __init__(self, size: int = 16) -> None:
        if size <= 0:
            raise ValueError("HashTable size must be positive")
        self.size = size
        self.buckets: list[list[tuple[str, object]]] = [[] for _ in range(size)]

    def _hash(self, key: str) -> int:
        return sum((idx + 1) * ord(ch) for idx, ch in enumerate(key)) % self.size

    def put(self, key: str, value: object) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key: str, default: object = None) -> object:
        idx = self._hash(key)
        for k, v in self.buckets[idx]:
            if k == key:
                return v
        return default

    def delete(self, key: str) -> bool:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return True
        return False


def solve_hanoi(n: int, source: str = "A", auxiliary: str = "B", target: str = "C") -> list[tuple[str, str]]:
    """Return sequence of (from_rod, to_rod) moves for n disks."""
    if n < 0:
        raise ValueError("Disk count cannot be negative")
    if n == 0:
        return []
    moves = solve_hanoi(n - 1, source, target, auxiliary)
    moves.append((source, target))
    moves.extend(solve_hanoi(n - 1, auxiliary, source, target))
    return moves
