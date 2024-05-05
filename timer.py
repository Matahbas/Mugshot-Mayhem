import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.best_time_line = self.read_best_time_from_file()
        self.best_time = self.best_time_line

    def read_best_time_from_file(self, filename='time.txt'):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                if lines:
                    return float(lines[-1].strip().split(': ')[1].split(' ')[0])
                else:
                    return float('inf')
        except FileNotFoundError:
            return float('inf')

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            self.elapsed_time += elapsed
            if elapsed < self.best_time:
                self.best_time = elapsed
            self.start_time = None

    def get_elapsed_time(self):
        if self.start_time is not None:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def write_elapsed_time_to_file(self, elapsed_time, filename='time.txt'):
        try:
            with open(filename, 'w') as file:
                file.write(f"Latest Game's Time: {elapsed_time:.2f} seconds\n")
                file.write(f"Best Time: {self.best_time:.2f} seconds\n")
        except Exception as e:
            print(f"An error occurred: {e}")