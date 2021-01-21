import sys


class WorkloadParser:
    def __init__(self, command_list):
        """
        TODO: set up HTTP stuff
        """
        self.commandList = command_list  # (cmd, args)

    def run(self):
        for (cmd, args) in self.commandList:
            try:
                self.makeCommand(cmd, args)
            except:
                print(f'Error submitting command {cmd} with params {args}')

    def makeCommand(self, cmd, args):
        print(f'Command: {cmd}: {args}')

        if (cmd == 'ADD'):
            self.addRequest(args)
        elif (cmd == 'QUOTE'):
            self.quoteRequest(args)
        elif (cmd == 'BUY'):
            self.buyRequest(args)
        elif (cmd == 'COMMIT_BUY'):
            self.commitBuyRequest(args)
        elif (cmd == 'CANCEL_BUY'):
            self.cancelBuyRequest(args)
        elif (cmd == 'SELL'):
            self.sellRequest(args)
        elif (cmd == 'COMMIT_SELL'):
            self.commitSellRequest(args)
        elif (cmd == 'CANCEL_SELL'):
            self.cancelSellRequest(args)
        elif (cmd == 'SET_BUY_AMOUNT'):
            self.setBuyAmountRequest(args)
        elif (cmd == 'CANCEL_SET_BUY'):
            self.cancelSetBuyRequest(args)
        elif (cmd == 'SET_BUY_TRIGGER'):
            self.setBuyTriggerRequest(args)
        elif (cmd == 'SET_SELL_AMOUNT'):
            self.setSellAmountRequest(args)
        elif (cmd == 'SET_SELL_TRIGGER'):
            self.setSellTriggerRequest(args)
        elif (cmd == 'CANCEL_SET_SELL'):
            self.cancelSetSellRequest(args)
        elif (cmd == 'DUMPLOG'):
            self.dumplogRequest(args)
        elif (cmd == 'DISPLAY_SUMMARY'):
            self.displaySummaryRequest(args)
        else:
            print(f'Invalid user command: {cmd}')

    def addRequest(self, args):
        """
        ADD userid,amount --> put?
        """
        pass

    def quoteRequest(self, args):
        """
        QUOTE userid,StockSymbol --> get
        """
        pass

    def buyRequest(self, args):
        """
        BUY userid,StockSymbol,amount --> post
        """
        pass

    def commitBuyRequest(self, args):
        """
        COMMIT_BUY userid --> post
        """
        pass

    def cancelBuyRequest(self, args):
        """
        CANCEL_BUY userid --> post
        """
        pass

    def sellRequest(self, args):
        """
        SELL userid,StockSymbol,amount --> post
        """
        pass

    def commitSellRequest(self, args):
        """
        COMMIT_SELL userid --> post
        """
        pass

    def cancelSellRequest(self, args):
        """
        CANCEL_SELL userid --> post
        """
        pass

    def setBuyAmountRequest(self, args):
        """
        SET_BUY_AMOUNT userid,StockSymbol,amount --> post
        """
        pass

    def cancelSetBuyRequest(self, args):
        """
        CANCEL_SET_BUY userid,StockSymbol --> post
        """
        pass

    def setBuyTriggerRequest(self, args):
        """
        SET_BUY_TRIGGER userid,StockSymbol,amount --> post
        """
        pass

    def setSellAmountRequest(self, args):
        """
        SET_SELL_AMOUNT userid,StockSymbol,amount --> post
        """
        pass

    def setSellTriggerRequest(self, args):
        """
        SET_SELL_TRIGGER userid,StockSymbol,amount --> post
        """
        pass

    def cancelSetSellRequest(self, args):
        """
        CANCEL_SET_SELL userid,StockSymbol --> post
        """
        pass

    def dumplogRequest(self, args):
        """
        DUMPLOG userid,filename --> get
        DUMPLOG filename --> get
        """
        pass

    def displaySummaryRequest(self, args):
        """
        DISPLAY_SUMMARY userid --> get
        """
        pass


def parseWorkloadFile(filename):
    command_list = []
    with open(filename, 'r') as f:
        for line in f:
            split_line = line.split(' ')
            user_command = split_line[1].split(',')

            cmd = user_command[0]
            args = user_command[1:]  # all commands have at least 1 param

            command_list.append((cmd, args))

    return command_list


def callWorkloadParser(args):
    """
    TODO: implement multithreading, error handling
    """
    if len(args) < 2:
        print(f'Please provide an input file')
        return
    filename = args[1]

    command_list = parseWorkloadFile(filename)
    # print(command_list)

    parser = WorkloadParser(command_list)
    parser.run()


if __name__ == '__main__':
    callWorkloadParser(sys.argv)
