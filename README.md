# Seng-468-workloads

All the workload files are saved in the `WorkloadFiles/` directory.

`WorkloadParser.py` takes a workload file as input and submits the user actions to the application via HTTP calls.

To run:  
`python3 WorkloadParser.py <workloadfile> <debug flag> <host port> <host IP 1> <host IP 2> ... <host IP n>`

The debug flag should be one of `true` or `false`. This controls if the transaction print statements are outputted.  
note that the parser can still be run with a single host

`splitWorkloads.py` takes a workload file and splits into smaller workload files, with each user assigned to a single smaller file (ie. all commands for a specific user will be in exactly 1 file). The dumplog commands will be placed into a separate file.

To run:
`python3 splitWorkloads.py <workloadfile> <numSplits>`

This will create numSplits+1 files (+1 is for the dumplog) in the same directory as the specified workload file.

Note: generated files are appended to in subsequent runs.
