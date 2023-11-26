class Jar:
    # Initialize size and capacity variables
    def __init__(self, capacity=12):
        self.capacity = capacity
        self.size = 0

    # Define what happens when you print the jar
    def __str__(self):
        if self.size > 0:
            return "🍪" * self.size
        else:
            return ""

    # Deposit behavior
    def deposit(self, n):
        self.validate(n)
        self.size = self.size + n
        if self.size > self.capacity:
            raise ValueError(f"Too many cookies! Jar only holds {self.capacity} cookies. Tried to fit {self.size}.")
        return self.size

    # Withdraw behavior
    def withdraw(self, n):
        self.validate(n)
        if n > self.size:
            raise ValueError(f"Tried to take {n} cookies. Jar only has {self.size} cookies left!")
        self.size = self.size - n
        return self.size

    # Validation checker
    def validate(self, n):
        try:
            n = int(n)
            if n < 0:
                raise ValueError("Value was not a positive integer")
        except ValueError:
            raise ValueError("Value was not a positive integer")

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, capacity):
        self.validate(capacity)
        self._capacity = capacity

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

def main():
    ...

if __name__ == "__main__":
    main()
