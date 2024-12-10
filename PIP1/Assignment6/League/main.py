from League import League
from Runner import Runner
from NoRunners import NoRunners

try:
    runner1 = Runner("Hussain Bolt", 70.5, 1, 5.27, 30)
    runner2 = Runner("Carl Lewis", 77.0, 2, 5.2, 33)
    runner3 = Runner("Amel Tuka", 73.0, 3, 5.1, 31)
    runner4 = Runner("Michael Johnson", 73.5, 3, 5.0, 32)

    league = League()
    league.addRunner(runner1)
    league.addRunner(runner2)
    league.addRunner(runner3)
    league.addRunner(runner4)

    league.printRunners()
    print(f"The Fastest Runner: {league.getFastestRunner()}")
    print(f"The Best Looser: {league.getBestLooser()}")

    # CSV
    league.SaveToCSV('runners.csv')
    league.LoadFromCSV('runners.csv')

    # Plot
    league.plotPaceInfo()

except NoRunners as exception:
    print(f"Error occurred: {exception}")
except ValueError as exception:
    print(f"ValueError occurred: {exception}")
except Exception as exception:
    print(f"Unexpected error occurred: {exception}")