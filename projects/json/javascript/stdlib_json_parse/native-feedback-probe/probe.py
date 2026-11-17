# gdb Python: one-shot breakpoint on every v8::internal::JsonParser<...> function entry in the pinned
# node binary; prints the demangled names entered while the given command line runs.
import gdb
import subprocess

names = {}
for line in subprocess.run(['nm', '-C', '/usr/local/bin/node'], capture_output=True, text=True).stdout.splitlines():
    parts = line.split(' ', 2)
    if len(parts) == 3 and parts[1] in ('t', 'T') and 'v8::internal::JsonParser<' in parts[2]:
        names.setdefault(int(parts[0], 16), parts[2])
gdb.execute('set pagination off')
gdb.execute('set confirm off')
gdb.execute('set startup-with-shell off')
gdb.execute('handle SIGSEGV SIGBUS SIGILL nostop noprint pass')
gdb.execute('starti', to_string=True)
# The pinned node binary is ELF EXEC (non-PIE), so nm addresses are load addresses.
assert open('/usr/local/bin/node', 'rb').read(18)[16] == 2
breakpoints = {}
for address in names:
    bp = gdb.Breakpoint(f'*{address:#x}', internal=True, temporary=True)
    bp.silent = True
    breakpoints[bp.number] = address
hit = set()


def on_stop(event):
    if isinstance(event, gdb.BreakpointEvent):
        for bp in event.breakpoints:
            if bp.number in breakpoints:
                hit.add(breakpoints[bp.number])


gdb.events.stop.connect(on_stop)
while True:
    try:
        gdb.execute('continue', to_string=True)
    except gdb.error:
        break
    if not gdb.selected_inferior().pid:
        break
print(f'SYMBOLS {len(names)}')
for address in sorted(hit):
    print('HIT', names[address])
