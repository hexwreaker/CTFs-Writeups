FROM i386/debian:bookworm AS b0
RUN mkdir /app
WORKDIR  /app
RUN apt update
RUN apt install -y openssh-server gcc  sshpass build-essential libseccomp-dev strace gdb gdbserver
RUN adduser --disabled-password insecure_shell


FROM b0 AS b1
COPY insecure_shell.c /app
COPY Dockerfile /app
RUN gcc ./insecure_shell.c -o insecure_shell -lseccomp -m32 -fstack-protector


COPY sshd_config /etc/ssh/sshd_config
COPY start.sh /app/start.sh
COPY passwd.txt /app/passwd.txt
RUN chmod 600 /app/passwd.txt

RUN ssh-keygen -A
RUN chmod +x /app/start.sh
RUN mkdir /run/sshd

RUN ssh-keygen -q -N "" -t rsa -f /app/ssh_key
RUN cp /app/ssh_key.pub /root/.ssh/authorized_keys
RUN chown insecure_shell:insecure_shell /app/ssh_key

EXPOSE 4444
EXPOSE 3333
CMD ["/app/start.sh"]
