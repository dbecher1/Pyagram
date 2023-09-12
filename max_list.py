
class Max_List:
    def __init__(self, n:int) -> None:
        self.items = [None] * n
        for i in range(n):
            self.items[i] = 0

    def calculate_helper(self, n:int, val) -> None:
        length = len(self.items)
        for i in range(n, length):
            if val > self.items[i]:
                temp = self.items[i]
                self.items[i] = val
                self.calculate_helper(i, temp)

    def calculate(self, val) -> None:
        self.calculate_helper(0, val)

    def sum(self) -> int:
        sum = 0
        for i in self.items:
            sum += i
        return sum

if __name__ == '__main__':
    pass