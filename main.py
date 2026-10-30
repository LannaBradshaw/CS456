import os, signal, subprocess, sys


ROOT = os.path.dirname(__file__)
monitor = subprocess.Popen(
    [sys.executable, os.path.join(ROOT, "monitor.py")],
    start_new_session=True,
)

try:
    monitor.wait()
except KeyboardInterrupt:
    os.killpg(monitor.pid, signal.SIGTERM)
    monitor.wait()
