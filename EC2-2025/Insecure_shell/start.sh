#!/bin/sh

/usr/sbin/sshd &
gdbserver :3333 /app/insecure_shell
# Don't hesitate to use gdb-server or strace (Already installed in the docker image)
