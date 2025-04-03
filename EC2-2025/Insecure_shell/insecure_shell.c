/**
* Build:
*
* gcc ./insecure_shell_compac.c -o insecure_shell -lseccomp -m32
*/

#include <seccomp.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdarg.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <limits.h>
#include <dirent.h>
#include <sys/types.h>
#include <pwd.h>

#define PORT 4444
#define MAX_BUF 64
#define S(x) SCMP_SYS(x)


int allowed_syscall[] = {
	/**
		Almost every syscalls used by the program except execve... 
	*/

	/* IO */
	S(write), S(read),

	/* Network */
	S(send), S(recv), S(sendto), S(recvfrom), S(connect), S(socket),
	S(bind), S(accept),

	/* File Operations : */
	S(statx), S(access), S(openat), S(open), S(mmap), S(mmap2), S(munmap),
	S(getdents64), S(close),

	/* User privileges : */
	S(getuid32), S(setgid32), S(setuid32), S(setresuid32),

	/* Others: */
	S(fork)
};

scmp_filter_ctx ctx;

/* graceful_exit cleans up our seccomp context before exiting */
void graceful_exit(int rc)
{
	seccomp_release(ctx);
	printf("Bye. %d\n", rc);
	exit(rc);
}

/* setup_seccomp initializes seccomp and loads our BPF program that filters
* syscalls into the kernel */
void setup_seccomp()
{
	int rc;
	int i;

	/* Initialize the seccomp filter state */
	if ((ctx = seccomp_init(SCMP_ACT_KILL)) == NULL) {
		graceful_exit(6);
	}

	if ((rc = seccomp_reset(ctx, SCMP_ACT_KILL)) != 0) {
		graceful_exit(7);
	}

	for (i=0; i<sizeof(allowed_syscall); i++) {
		if ((rc = seccomp_rule_add(ctx, SCMP_ACT_ALLOW, allowed_syscall[i], 0)) != 0) {
			graceful_exit(1);
		}
	}

	/* Load the BPF program for the current context into the kernel */
	if ((rc = seccomp_load(ctx)) != 0) {
		graceful_exit(1);
	}
}


/*
* Bind a new SSH Session to the current client socket
*/
void shell(int client_sock)
{
	char *newenviron[] = { NULL };
	char *newargv[] = {
		"ssh" ,"root@127.0.0.1","-t", "-t","-o", "StrictHostKeyChecking=accept-new",
		"-i", "/app/ssh_key",NULL, NULL,
	};

	dup2(client_sock, 0);
	dup2(client_sock, 1);

	execve("/usr/bin/ssh", newargv, newenviron);
}

/*
* Drop root privileges
*/
void drop_priv()
{
	if (getuid() == 0) {
		/* process is running as root, drop privileges */
		setgid(1000);
		setuid(1000);
	}
	if (setuid(0) == 0 || seteuid(0) == 0) {
		printf("[-] Failed to drop root privileges!\n");
		exit(-1); 
	}
}


/*
* FORMAT and send a string to a socket
*/
int send_str(int sock, char* str, ...)
{
	char buf[1024];
	int ret;
	va_list args;

	va_start(args, str);
	ret = vsnprintf(buf, sizeof(buf), str, args);
	va_end(args);
	if (ret > sizeof(buf)) {
		ret = sizeof(buf);
	}

	return send(sock, buf, ret,0);
}

/*
* Check for admin privileges
*/
int check_admin(int client_sock)
{
	FILE *fptr;
	fptr = fopen("passwd.txt", "r");
	char secret_buf[64];
	char input_buf[64];
	int ret;

	memset(secret_buf, 0, sizeof(secret_buf));
	memset(input_buf, 0, sizeof(input_buf));

	send_str(client_sock, ">> Admin Password ?\n");

	fgets(secret_buf, sizeof(secret_buf), fptr);
	fclose(fptr);

	ret = recv(client_sock, input_buf , sizeof(input_buf), 0);

	if (ret>0 && ret <= sizeof(input_buf)) {
		input_buf[ret-1] = 0;
	}

	if (strncmp(secret_buf, input_buf, sizeof(secret_buf))==0) {
		return 1;
	} else {

		explicit_bzero(secret_buf, sizeof(secret_buf));
		return 0;
	}
}


void readfile(int s)
{
	char filename[128];
	char buffer[256];
	int fd;
	int ret;
	char *f;
	struct stat fileInfo = {0};

	send_str(s, ">> Please provide filename: ");
	ret = recv(s, filename, sizeof(filename), 0);

	if (ret > 0 && ret <= sizeof(filename)) {
		filename[ret-1] = 0;
	}

	fd = open(filename, O_RDONLY);

	if (fd == -1) {
		snprintf(buffer, sizeof(buffer), "The file %s does not exist or you don't have enough privileges\n", filename);
		send_str(s, buffer);
		return;
	}

	if (fstat(fd, &fileInfo) == -1) {
		perror("Error getting the file size");
		exit(EXIT_FAILURE);
	}

	if (fileInfo.st_size == 0) {
		fprintf(stderr, "Error: File is empty, nothing to do\n");
			exit(EXIT_FAILURE);
	}

	char *map = mmap(0, fileInfo.st_size, PROT_READ, MAP_SHARED, fd, 0);
	if (map == MAP_FAILED)
	{
			close(fd);
			perror("Error mmapping the file");
			exit(EXIT_FAILURE);
	}

	ret = 0;
	while(ret < fileInfo.st_size) {
		if((ret+getpagesize()) < fileInfo.st_size) {
			send(s, map+ret, getpagesize(), 0);
			ret += getpagesize();
		} else {
			send(s, map+ret, fileInfo.st_size - ret, 0);
			ret = fileInfo.st_size;
		}
	}
};

/*
* Leave a note to be read by the administrator
*/
void leave_note(int s)
{
	int fd;
	char buffer[256];
	int ret;
	int size;

	fd = open("notes", O_WRONLY | O_CREAT);
	send_str(s, "Message size: \n");
	ret = recv(s, buffer, sizeof(buffer), 0);
	size = atoi(buffer);
	send_str(s, "Received size : %d\n", size);


	if(size > 256){
		// WIP: Implement chunck mode
	}
	else{
		ret = recv(s, buffer, size, 0);
		write(fd, buffer, ret);
		close(fd);
	}

	return;
};



void listfiles(int s)
{
	char dirname[128];
	char path[PATH_MAX + 1];
	char fpath[PATH_MAX + 1];

	int ret;
	struct stat fileInfo = {0};
	DIR *d;
	struct dirent *dirent;
	struct passwd * pInfo;
		
	send_str(s, ">> Please provide a dir: ");
	ret = recv(s, dirname, sizeof(dirname), 0);
	if(ret > 0 && ret <= sizeof(dirname))
		dirname[ret-1] = 0;

	d = opendir(dirname);
	
	if (d) {
		strcpy(path, dirname);
		strcat(path, "/");
		while ((dirent = readdir(d)) != NULL) {
			strcpy(fpath, path);
			strcat(fpath, dirent->d_name);
			if (stat(fpath, &fileInfo) == 0)
				{
					send_str(s, "%-20s (Owner: %d / perm %o)\n", dirent->d_name, fileInfo.st_uid, fileInfo.st_mode & 0777);
				}
		}
		closedir(d);
	}
	else {
		send_str(s, "[-] This dir does not exist\n");
	}
}

int handle_client(int client_sock)
{
	char buffer[MAX_BUF];
	char size;
	int ret;
	int exit = 0;
	if (check_admin(client_sock))
		{
			shell(client_sock);
		}
	else
		{
			send_str(client_sock, "[-] Ohh... You are not the admin...\n");
			setup_seccomp();
			drop_priv();
		}

	while (exit == 0)
	{
		send_str(client_sock, "[Guest Restricted Shell] >> ");
		ret = recv(client_sock, buffer, sizeof(buffer), 0);
		if (ret>0 && ret <= sizeof(buffer))
			buffer[ret-1] = 0;


		if (strncmp(buffer, "cat", sizeof(buffer)) == 0){
			readfile(client_sock);
		}
		if (strncmp(buffer, "ls", sizeof(buffer)) == 0){
			listfiles(client_sock);
		}
		if (strncmp(buffer, "leave_note", sizeof(buffer)) == 0){
			leave_note(client_sock);
		}
		if (strncmp(buffer, "exit", sizeof(buffer)) == 0){
			exit = 1;
		}
		
		if (strncmp(buffer, "whoami", sizeof(buffer)) == 0){
			send_str(client_sock, "Current user: %d\n", getuid());
		}
		if (strncmp(buffer, "help", sizeof(buffer)) == 0){
			send_str(client_sock, "- cat \n- ls\n- leave_note\n- whoami\n- exit\n");
		}


	}
	close(client_sock);
	return 0;
}
 
int main()
{
 
	int server_fd, new_socket;
	struct sockaddr_in address;
	int opt = 1;
	socklen_t addrlen = sizeof(address);
 
	// Creating socket file descriptor
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
		perror("socket failed");
		exit(EXIT_FAILURE);
	}
 
	if (setsockopt(server_fd, SOL_SOCKET,
								 SO_REUSEADDR | SO_REUSEPORT, &opt,
								 sizeof(opt))) {
		perror("setsockopt");
		exit(EXIT_FAILURE);
	}
	
	address.sin_family = AF_INET;
	address.sin_addr.s_addr = inet_addr("0.0.0.0");
	address.sin_port = htons(PORT);
 
	if (bind(server_fd, (struct sockaddr*)&address,
					 sizeof(address))    < 0) {
		perror("bind failed");
		exit(EXIT_FAILURE);
	}
 
	if (listen(server_fd, 3) < 0) {
		perror("listen");
		exit(EXIT_FAILURE);
	}
	
	while(1) {

		if ((new_socket = accept(server_fd, (struct sockaddr*)&address, &addrlen))  < 0) {
			perror("accept");
			exit(EXIT_FAILURE);
		}
 
		if(fork() == 0)
			handle_client(new_socket);
		else
			close(new_socket);
	}
 
 
}