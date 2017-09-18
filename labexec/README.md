# labexec
This is a convenience script which allows the user to execute commands/scripts, or distribute files over ssh to a list of hosts. It has Curtin University's Computer department labs hard coded as this was the programs intended use.

It will *"ping"* each host specified using ssh to ensure it is up, then notify the user if any hosts are down.

## Usage
~~~bash
python labaxec.py [-hL] [-lf targets] [-c command] [-s script] [-p src dst]
~~~

## Output

The program will log stdout and stderr in log files with timestamps as the names.

