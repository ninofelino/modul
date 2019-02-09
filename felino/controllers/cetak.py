import subprocess
lpr =  subprocess.Popen("/usr/bin/lp", stdin=subprocess.PIPE)
lpr.stdin.writeln("================")
