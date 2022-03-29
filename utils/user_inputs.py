import math


class UserInputMethods:

    @staticmethod
    def get_scale_value(scale, digits):
        """
        Takes the time scale required (year, month, day) and checks if it is an integer and 'digits' long.
        @param scale: string
        @param digits: int
        @return: int
        """
        try:
            scale_input = int(input(f"Enter the {scale} you want: "))
            input_digits = int(math.log10(scale_input)) + 1
            if not isinstance(scale_input, int) or (input_digits != digits):
                raise TypeError
            else:
                return scale_input
        except:
            print("Incorrect format")

    def get_trade_data_variables(self):
        """
        Takes user input to assign values for all the required options.
        A valid output will be of form: [currency_pair, date, data_type, time_interval]
        @return: list or boolean
        """

        currency_pair = input("Enter trade pair: ").upper()
        variables = [currency_pair]

        year = self.get_scale_value('year', 4)
        month = self.get_scale_value('month', 2)
        ans = input("Do you want to input the day value? (Y/N) ").upper()
        if ans == "Y":
            day = self.get_scale_value('day', 2)
            date = [year, month, day]
        else:
            date = [year, month]
        variables.append(date)

        extra = input("Do you want to input values for data_type or time_interval? (Y/N) ").upper()
        if extra == "Y":
            try:
                trade_data = input("Enter data type [klines, aggTrades or trades]: ")
                type_options = ['klines', 'aggTrades', 'trades']
                if trade_data not in type_options:
                    raise Exception(f"{trade_data} option not found.")
                else:
                    variables.append(trade_data)
            except:
                print("Invalid input.")
            try:
                interval_input = input("Enter time interval: ")
                interval_options = ['1m', '3m', '5m', '15m', '30m', '1h', '2h',
                                    '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1mo']
                if interval_input not in interval_options:
                    raise Exception(f"{interval_input} option not found.")
                else:
                    variables.append(interval_input)
            except:
                print("Invalid input.")
        else:
            trade_data = "klines"
            variables.append(trade_data)
            interval = "5m"
            variables.append(interval)

        print("Variables chosen:")
        for var in variables:
            print(var)
        try:
            check = input("Is this correct? (Y/N) ").upper()
            if check == "N":
                return False
            elif check == "Y":
                return variables
        except:
            print("Invalid answer")
