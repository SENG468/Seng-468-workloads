import os
import sys

"""
Split workload files by users into separate workload files. The dumplog commands will be written to a separate file

Usage: python3 splitWorkloads.py <workload file> <number of splits>
"""


def splitWorkloads(filename, numSplits):

    # group commands by user
    user_commands = {}
    with open(filename, 'r') as f:
        for line in f:
            split_line = line.rstrip().split(' ')
            user_command = split_line[1].split(',')

            transId = split_line[0][1:-1]
            cmd = user_command[0]
            args = user_command[1:]

            if cmd == 'DUMPLOG':
                if 'DUMPLOG' in user_commands:
                    user_commands['DUMPLOG'].append(line)
                else:
                    user_commands['DUMPLOG'] = [line]
            else:
                if args[0] in user_commands:
                    user_commands[args[0]].append(line)
                else:
                    user_commands[args[0]] = [line]

    # create user file names
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    subpath = os.path.join(dirname, 'splitWorkloadFiles', basename, f'split-{numSplits}')
    os.makedirs(subpath, exist_ok=True)

    filenames = [os.path.join(subpath, f'file{i}') for i in range(0, numSplits)]
    filenames.append(os.path.join(subpath, 'dumplog'))

    # dump to files
    cnt = 0
    for user in user_commands:
        if user == 'DUMPLOG':
            fn = filenames[-1]
        else:
            fn = filenames[cnt % numSplits]
            cnt += 1

        with open(fn, 'a') as f:
            f.write(''.join(user_commands[user]))


if __name__ == "__main__":
    splitWorkloads(sys.argv[1], int(sys.argv[2]))
