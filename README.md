# Minecraft Bedrock Server Checker

[Русская версия](README.ru.md)

A small async command-line tool that checks the status of many **Minecraft Bedrock / Pocket Edition** servers at once. For each server it shows online players, max slots and game version, sorted by online count. Built on [mcstatus](https://github.com/py-mine/mcstatus).

## Features

- Check any number of servers in parallel
- Shows online players, max slots and version
- Results sorted by player count
- Separate list of servers that did not respond, with the reason
- Input validation: bad ports, empty hosts and duplicates are skipped
- Default port 19132 if none is given
- Check as many lists as you want in one session

## Installation

```bash
git clone https://github.com/notevelin/bedrock-server-checker.git
cd bedrock-server-checker
pip install -r requirements.txt
```

## Usage

```bash
python check_servers.py
```

Enter servers one per line as `host` or `host:port`. Press Enter on an empty line to start the check. After the results you can enter another list; an empty list exits the program.

```
> play.example.com:19133
> mc.example.org
> 

Server                 Online    Max    Version
----------------------------------------------
play.example.com:19133    120    500     1.21.50
mc.example.org:19132       34    100     1.21.44

Did not respond:
  dead.example.net:19132: timeout (server did not answer)
```

## Requirements

- Python 3.10+
- `mcstatus`

## Notes

- Bedrock uses UDP (default port 19132). If a server never responds, make sure the address and port are correct and the server allows status queries.
- The timeout per server is 5 seconds (`TIMEOUT` in the script).

## Author

[notevelin](https://github.com/notevelin)

## License

MIT
