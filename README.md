# mcp-receiver
Open source implementation of receiver plugin for mocopi motion tracking system.

## Install
install dependency with pip command.
```
pip install -r requirements.txt
```

## Usage
Execute test application by following command.
```
python3 -m mcp_receiver
```
This command listens on port 12351, receiving packets from mocopi mobile app (and BVHSender), and then send VMC Protocol packets to localhost:39540.