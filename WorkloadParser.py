import sys
import requests
import json


class WorkloadParser:
    def __init__(self, command_list, ip, port):
        """
        """
        self.commandList = command_list  # (cmd, args)
        self.ip = ip
        self.port = port
        self.host = f'http://{self.ip}:{self.port}/stock-trade'
        self.accessTokens = {}  # userid: token

    def run(self):
        for (cmd, args) in self.commandList:
            try:
                self.makeCommand(cmd, args)
            except Exception as e:
                print(f'Error submitting command {cmd} with params {args}')
                print(e)

    def getToken(self, userId):
        """
        if a token is not saved, create account, login and get token to save
        """
        if userId not in self.accessTokens:
            payload = {'username': userId, 'password': userId, 'email': f'{userId}@gmail.com', 'securityCode': userId}
            r = requests.post(f'{self.host}/users/sign-up', json=payload)

            # signup successful. Login and get token
            if r.status_code in [200, 500]:  # TODO fix 500 to new error
                payload = {'username': userId, 'password': userId}
                r = requests.post(f'{self.host}/users/login', json=payload)
                self.accessTokens[userId] = r.json()['access_token']

        return self.accessTokens[userId]

    def makeCommand(self, cmd, args):
        print(f'Command: {cmd} Arguments: {args}')

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
        ADD userid,amount --> PUT
        url: /accounts/add
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'name': args[0], 'balance': float(args[1])}
        r = requests.post(f'{self.host}/accounts/add', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def quoteRequest(self, args):
        """
        QUOTE userid,StockSymbol --> GET
        url: /quote
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1]}
        r = requests.get(f'{self.host}/quote', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def buyRequest(self, args):
        """
        BUY userid,StockSymbol,amount --> POST
        url: /buy/create
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1], 'amount': float(args[2])}
        r = requests.post(f'{self.host}/buy/create', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def commitBuyRequest(self, args):
        """
        COMMIT_BUY userid --> POST
        url: /buy/commit
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0]}
        r = requests.post(f'{self.host}/buy/commit', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelBuyRequest(self, args):
        """
        CANCEL_BUY userid --> POST
        url: /buy/cancel
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0]}
        r = requests.post(f'{self.host}/buy/cancel', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def sellRequest(self, args):
        """
        SELL userid,StockSymbol,amount --> POST
        url: /sell/create
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1], 'amount': float(args[2])}
        r = requests.post(f'{self.host}/sell/create', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def commitSellRequest(self, args):
        """
        COMMIT_SELL userid --> POST
        url: /sell/commit
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0]}
        r = requests.post(f'{self.host}/sell/commit', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelSellRequest(self, args):
        """
        CANCEL_SELL userid --> POST
        url: /sell/cancel
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0]}
        r = requests.post(f'{self.host}/sell/cancel', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setBuyAmountRequest(self, args):
        """
        SET_BUY_AMOUNT userid,StockSymbol,amount --> POST
        url: /setBuy/amount
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1], 'amount': float(args[2])}
        r = requests.post(f'{self.host}/setBuy/amount', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelSetBuyRequest(self, args):
        """
        CANCEL_SET_BUY userid,StockSymbol --> POST
        url: /setBuy/cancel
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1]}
        r = requests.post(f'{self.host}/setBuy/cancel', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setBuyTriggerRequest(self, args):
        """
        SET_BUY_TRIGGER userid,StockSymbol,amount --> POST
        url: /setBuy/trigger
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1], 'amount': float(args[2])}
        r = requests.post(f'{self.host}/setBuy/trigger', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setSellAmountRequest(self, args):
        """
        SET_SELL_AMOUNT userid,StockSymbol,amount --> POST
        url: /setSell/amount
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1], 'amount': float(args[2])}
        r = requests.post(f'{self.host}/setSell/amount', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setSellTriggerRequest(self, args):
        """
        SET_SELL_TRIGGER userid,StockSymbol,amount --> POST
        url: /setSell/trigger
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1], 'amount': float(args[2])}
        r = requests.post(f'{self.host}/setSell/trigger', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelSetSellRequest(self, args):
        """
        CANCEL_SET_SELL userid,StockSymbol --> POST
        url: /setSell/cancel
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0], 'stockSymbol': args[1]}
        r = requests.post(f'{self.host}/setSell/cancel', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def dumplogRequest(self, args):
        """
        TODO: decide how we want to handle the distinction. Right now implementing as userId empty
        TODO: add authorization for system admin to dump all logs
        DUMPLOG userid,filename --> GET
        DUMPLOG filename --> GET
        url: /dumplog
        """

        if len(args) == 1:
            header_payload = {'authorization': 'sysadmin'}  # TODO: fix
            payload = {'userId': '', 'fileName': args[0]}
        else:
            access_token = self.getToken(args[0])
            header_payload = {'authorization': access_token}
            payload = {'userId': args[0], 'fileName': args[1]}
        r = requests.get(f'{self.host}/dumplog', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def displaySummaryRequest(self, args):
        """
        DISPLAY_SUMMARY userid --> GET
        url: /displaySummary
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'userId': args[0]}
        r = requests.get(f'{self.host}/displaySummary', json=payload)
        print(f'Response {r.status_code} at url {r.url}')


def parseWorkloadFile(filename):
    command_list = []
    with open(filename, 'r') as f:
        for line in f:
            split_line = line.rstrip().split(' ')
            user_command = split_line[1].split(',')

            cmd = user_command[0]
            args = user_command[1:]  # all commands have at least 1 param

            command_list.append((cmd, args))

    return command_list


def callWorkloadParser(args):
    """
    TODO: implement multithreading, error handling
    """

    if len(args) < 4:
        print(f'Please provide an input file, ip address and port')
        return

    filename = args[1]
    ip = args[2]
    port = args[3]

    command_list = parseWorkloadFile(filename)

    parser = WorkloadParser(command_list, ip, port)
    parser.run()


if __name__ == '__main__':
    callWorkloadParser(sys.argv)
