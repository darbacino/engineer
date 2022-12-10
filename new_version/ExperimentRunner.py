from connect_setup import DevOperations

# from Plotter import Plotter


class ExperimentRunner:
    def __init__(self, reruns=1):
        """Run specific task on devices that are configured in config

        Args:
            reruns (int, optional): Set number of reruns of tasks. Defaults to 1.
        """
        self.__preparation = DevOperations()
        self.__experiment_strategies = []
        self.__experiment_reruns = reruns

    def addStrategy(self, __object):
        """Add experiment to execute

        Args:
            __object (class): Class created from template
        """
        self.__experiment_strategies.append(__object)

    def setReruns(self, num: int):
        """The number how much times it will rerun experiments

        Args:
            num (int): Number of reruns. Must be bigger thatn 0
        """
        if num > 0:
            self.__experiment_reruns = num
        else:
            print(
                f"Error in setReruns({num}) -- value '{num}' must be bigger than 0. Exit"
            )
            exit(1)

    def start(self):
        for _ in range(self.__experiment_reruns):
            self.__preparation.check_and_prepare_devices()

            for strategy in self.__experiment_strategies:
                strategy.start()

            self.__preparation.get_data_from_devices()
