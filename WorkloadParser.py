import sys
import requests
import threading
import time


class WorkloadParser:
    def __init__(self, command_list, ip, port):
        """
        """
        self.commandList = command_list  # (transId, cmd, args)
        self.ip = ip
        self.port = port
        self.host = f'http://{self.ip}:{self.port}/stock-trade'
        self.accessToken = None  # userid: token

    def run(self):
        for (transId, cmd, args) in self.commandList:
            try:
                self.makeCommand(transId, cmd, args)
            except Exception as e:
                print(f'Error submitting transaction {transId} with command {cmd} and params {args}')
                print(e)

    def getToken(self, userId):
        """
        if a token is not saved, create account, login and get token to save
        """
        if self.accessToken is None:
            payload = {'username': userId, 'password': userId, 'email': f'{userId}@gmail.com', 'securityCode': userId}
            r = requests.post(f'{self.host}/users/sign-up', json=payload)

            # signup successful. Login and get token
            if r.status_code in [200, 500]:  # TODO fix 500 to new error
                payload = {'username': userId, 'password': userId}
                r = requests.post(f'{self.host}/users/login', json=payload)
                self.accessToken = r.json()['access_token']

        return self.accessToken

    def makeCommand(self, transId, cmd, args):
        print(f'Transaction: {transId} Command: {cmd} Arguments: {args}')

        if (cmd == 'ADD'):
            self.addRequest(transId, args)
        elif (cmd == 'QUOTE'):
            self.quoteRequest(transId, args)
        elif (cmd == 'BUY'):
            self.buyRequest(transId, args)
        elif (cmd == 'COMMIT_BUY'):
            self.commitBuyRequest(transId, args)
        elif (cmd == 'CANCEL_BUY'):
            self.cancelBuyRequest(transId, args)
        elif (cmd == 'SELL'):
            self.sellRequest(transId, args)
        elif (cmd == 'COMMIT_SELL'):
            self.commitSellRequest(transId, args)
        elif (cmd == 'CANCEL_SELL'):
            self.cancelSellRequest(transId, args)
        elif (cmd == 'SET_BUY_AMOUNT'):
            self.setBuyAmountRequest(transId, args)
        elif (cmd == 'CANCEL_SET_BUY'):
            self.cancelSetBuyRequest(transId, args)
        elif (cmd == 'SET_BUY_TRIGGER'):
            self.setBuyTriggerRequest(transId, args)
        elif (cmd == 'SET_SELL_AMOUNT'):
            self.setSellAmountRequest(transId, args)
        elif (cmd == 'SET_SELL_TRIGGER'):
            self.setSellTriggerRequest(transId, args)
        elif (cmd == 'CANCEL_SET_SELL'):
            self.cancelSetSellRequest(transId, args)
        elif (cmd == 'DUMPLOG'):
            self.dumplogRequest(transId, args)
        elif (cmd == 'DISPLAY_SUMMARY'):
            self.displaySummaryRequest(transId, args)
        else:
            print(f'Invalid user command: {cmd}')

    def addRequest(self, transId, args):
        """
        Add the given amount of money to the user's account
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'name': args[0], 'balance': float(args[1])}
        r = requests.post(f'{self.host}/accounts/add', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def quoteRequest(self, transId, args):
        """
        Get the current quote for the stock for the specified user
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId}
        r = requests.get(f'{self.host}/quote/{args[1]}', params=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def buyRequest(self, transId, args):
        """
        Buy the dollar amount of the stock for the specified user at the current price.
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'type': 'BUY', 'stockCode': args[1], 'cashAmount': float(args[2])}
        r = requests.post(f'{self.host}/order/simple', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def commitBuyRequest(self, transId, args):
        """
        Commits the most recently executed BUY command
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId}
        r = requests.post(f'{self.host}/buy/commit', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelBuyRequest(self, transId, args):
        """
        Cancels the most recently executed BUY Command
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId}
        r = requests.post(f'{self.host}/buy/cancel', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def sellRequest(self, transId, args):
        """
        Sell the specified dollar mount of the stock currently held by the specified user at the current price.
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'type': 'SELL', 'stockCode': args[1], 'cashAmount': float(args[2])}
        r = requests.post(f'{self.host}/order/simple', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def commitSellRequest(self, transId, args):
        """
        Commits the most recently executed SELL command
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId}
        r = requests.post(f'{self.host}/sell/commit', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelSellRequest(self, transId, args):
        """
        Cancels the most recently executed SELL Command
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId}
        r = requests.post(f'{self.host}/sell/cancel', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setBuyAmountRequest(self, transId, args):
        """
        Sets a defined amount of the given stock when the current stock price is less than or equal to the BUY_TRIGGER
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'type': 'BUY_AT', 'stockCode': args[1], 'stockAmount': float(args[2])}
        r = requests.post(f'{self.host}/order/limit', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelSetBuyRequest(self, transId, args):
        """
        Cancels a SET_BUY command issued for the given stock
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId}
        r = requests.post(f'{self.host}/setBuy/cancel/{args[1]}', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setBuyTriggerRequest(self, transId, args):
        """
        Sets the trigger point based on the current stock price when any SET_BUY will execute
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'type': 'BUY_AT', 'stockCode': args[1], 'unitPrice': float(args[2])}
        r = requests.post(f'{self.host}/setBuy/trigger', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setSellAmountRequest(self, transId, args):
        """
        Sets a defined amount of the specified stock to sell when the current stock price is equal or greater than the sell trigger point
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'type': 'SELL_AT', 'stockCode': args[1], 'stockAmount': float(args[2])}
        r = requests.post(f'{self.host}/order/limit', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def setSellTriggerRequest(self, transId, args):
        """
        Sets the stock price trigger point for executing any SET_SELL triggers associated with the given stock and user
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'type': 'SELL_AT', 'stockCode': args[1], 'unitPrice': float(args[2])}
        r = requests.post(f'{self.host}/setSell/trigger', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def cancelSetSellRequest(self, transId, args):
        """
        Cancels the SET_SELL associated with the given stock and user
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId}
        r = requests.post(f'{self.host}/setSell/cancel/{args[1]}', json=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')

    def dumplogRequest(self, transId, args):
        """
        (1) Print out to the specified file the complete set of transactions that have occurred in the system (admin privileges needed)
          or
        (2) Print out the history of the users transactions to the user specified file
        """

        if len(args) == 1:  # dumplog for all users. needs admin privileges
            filename = args[0]
            header_payload = {'authorization': self.getToken('sysadmin')}  # TODO: determine what the admin credentials will be
            payload = {'transactionId': transId, 'filename': filename, 'username': ''}
            r = requests.post(f'{self.host}/logs/dumplog', json=payload, headers=header_payload, stream=True)
        else:  # dumplog for a single user
            filename = args[1]
            access_token = self.getToken(args[0])
            header_payload = {'authorization': access_token}
            payload = {'transactionId': transId, 'username': args[0], 'filename': filename}
            r = requests.post(f'{self.host}/logs/user/dumplog', json=payload, headers=header_payload, stream=True)
        print(f'Response {r.status_code} at url {r.url}')

        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

    def displaySummaryRequest(self, transId, args):
        """
        Provides a summary to the client of the given user's transaction history and the current status of their accounts as well as any set buy or sell triggers and their parameters
        """
        access_token = self.getToken(args[0])
        header_payload = {'authorization': access_token}
        payload = {'transactionId': transId, 'userId': args[0]}
        r = requests.get(f'{self.host}/accounts/displaySummary', params=payload, headers=header_payload)
        print(f'Response {r.status_code} at url {r.url}')


def parseWorkloadFile(filename):
    """
    Return a dictionary where keys are the userIds and the value is the (transactionId, command, arguments) for each command for the user.
    DUMPLOG commands are separated and under the key 'DUMPLOG' so they can be run at the end
    """

    user_commands = {}
    with open(filename, 'r') as f:
        for line in f:
            split_line = line.rstrip().split(' ')
            user_command = split_line[1].split(',')

            transId = split_line[0][1:-1]
            cmd = user_command[0]
            args = user_command[1:]  # all commands have at least 1 param

            if cmd == 'DUMPLOG':
                if 'DUMPLOG' in user_commands:
                    user_commands['DUMPLOG'].append((transId, cmd, args))
                else:
                    user_commands['DUMPLOG'] = [(transId, cmd, args)]
            else:
                if args[0] in user_commands:
                    user_commands[args[0]].append((transId, cmd, args))
                else:
                    user_commands[args[0]] = [(transId, cmd, args)]

    return user_commands


def runThread(user_commands, ip, port):
    parser = WorkloadParser(user_commands, ip, port)
    parser.run()


def callWorkloadParser(args):
    if len(args) < 4:
        print(f'Please provide an input file, ip address and port')
        return

    filename = args[1]
    ip = args[2]
    port = args[3]

    # user_commands  will be a dict of the commands with the key being the user name
    user_commands = parseWorkloadFile(filename)

    # one thread per user
    for user in user_commands:
        if user == 'DUMPLOG':
            continue

        t = threading.Thread(target=runThread, args=(user_commands[user], ip, port,))
        t.start()

    while threading.active_count() > 1:
        time.sleep(5)
    time.sleep(5)

    # run dumplogs last
    if 'DUMPLOG' in user_commands:
        # append the number of users to each log file name
        num_users = len(user_commands.keys()) - 1
        for (transId, cmd, args) in user_commands['DUMPLOG']:
            args[-1] = f'{args[-1]}_{num_users}Users'

        runThread(user_commands['DUMPLOG'], ip, port)


if __name__ == '__main__':
    callWorkloadParser(sys.argv)
