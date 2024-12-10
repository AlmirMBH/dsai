import csv
import matplotlib.pyplot as plt
from Runner import Runner
from NoRunners import NoRunners
"""
1) Has instance variable runners (a list of runners in the league)
2) Constructor sets this variable to an empty list
3) Method addRunner takes a runner as an argument and appends it to the runners list
4) Method getFastestRunner returns the name of the runner with the greatest pace
5) Method getBestLooser returns the name of the runner with the greatest pace who has never won in a competition.
6) Method SaveToCSV saves runners to a CSV file. Name of the file is given in the argument
7) Method LoadFromCSV loads runners from a CSV file. Name of the file is given in the argument
8) Method plotPaceInfo displays a scatter plot where each dot represents a runner with:
 - Age on the x axis
 - Weight on the y axis
 - The color of a dot represents the pace of the runner.
9) Method printRunners prints information for every runner in the league.
10) If there are no runners in the league, raise a custom exception 'NoRunners' with a message
    „There are no runners in the league!“
"""

class League:
    def __init__(self):
        self.runners = []


    def addRunner(self, runner):
        if not isinstance(runner, Runner):
            raise ValueError("Argument must be an instance of the Runner class.")
        self.runners.append(runner)


    def getFastestRunner(self):
        if not self.runners:
            raise NoRunners("There are no runners in the league!")
        fastest_runners = [runner for runner in self.runners if runner.best_place == 1]
        fastest_runner = max(fastest_runners, key=lambda runner: runner.pace)

        return fastest_runner.name


    def getBestLooser(self):
        if not self.runners:
            raise NoRunners("There are no runners in the league!")
        losers = [runner for runner in self.runners if runner.best_place > 1]
        if not losers:
            return None
        best_looser = max(losers, key=lambda runner: runner.pace)
        return best_looser.name


    def SaveToCSV(self, filename):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Weight", "BestPlace", "Pace", "Age"])
            for runner in self.runners:
                writer.writerow(runner.getList())


    def LoadFromCSV(self, filename):
        try:
            with open(filename, mode="r") as file:
                reader = csv.reader(file)
                next(reader)  # Skipping the header line
                self.runners = []
                for row in reader:
                    name, weight, best_place, pace, age = row
                    self.addRunner(Runner(name, float(weight), int(best_place), float(pace), int(age)))
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except Exception as exception:
            print(f"Error loading CSV file: {exception}")


    def plotPaceInfo(self):
        if not self.runners:
            raise NoRunners("There are no runners in the league!")

        ages = [runner.age for runner in self.runners]
        weights = [runner.weight for runner in self.runners]
        paces = [runner.pace for runner in self.runners]

        plt.scatter(ages, weights, c=paces, cmap="plasma") # bar can be styled with cmap="viridis" or "plasma", "inferno", "magma", "cividis"
        plt.xlabel("Age")
        plt.ylabel("Weight")
        plt.title("Runner Pace Info")
        plt.colorbar(label="Pace (m/s)")
        plt.show()


    def printRunners(self):
        if not self.runners:
            raise NoRunners("There are no runners in the league!")
        for runner in self.runners:
            print(runner)