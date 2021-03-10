# Seng-468-workloads

All the workload files are saved in the `WorkloadFiles/` directory.

`WorkloadParser.py` takes a workload file as input and submits the user actions to the application via HTTP calls.

To run:  
`python3 WorkloadParser.py <workloadfile> <debug flag> <host port> <host IP 1> <host IP 2> ... <host IP n>`

The debug flag should be one of `true` or `false`. This controls if the transaction print statements are outputted.  
note that the parser can still be run with a single host
