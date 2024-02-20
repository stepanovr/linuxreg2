#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUFSIZE 1024
#define PARAM_NUM 4

char* mem_access(void* p_addr, uint64_t value, int bits, int read);

/*
 * error - wrapper for perror
 */
void error(char *msg) {
  perror(msg);
  exit(1);
}


int main(int argc, char **argv) {
  int sockfd; /* socket */
  int portno; /* port to listen on */
  int clientlen; /* byte size of client's address */
  struct sockaddr_in serveraddr; /* server's addr */
  struct sockaddr_in clientaddr; /* client addr */
  char buf[BUFSIZE]; /* message buf */
  char *resp;
  char *hostaddrp; /* dotted decimal host addr string */
  int optval; /* flag value for setsockopt */
  int n; /* message byte size */
  char *token;
  int param_idx;
  uint64_t params[PARAM_NUM];

  if (geteuid() != 0)
    {
      printf("\n\nSuperuser access rights are required!!!\n\n\n\n");
      exit(-1);
    }

  /*
   * check command line arguments
   */
  if (argc != 4) {
    fprintf(stderr, "usage: %s <port> <pipe_down> <pipe_up>\n", argv[0]);
    exit(-1);
  }
  portno = atoi(argv[1]);

  /*
   * socket: create the parent socket
   */
  sockfd = socket(AF_INET, SOCK_DGRAM, 0);
  if (sockfd < 0)
    error("ERROR opening socket");

  /* setsockopt: Handy debugging trick that lets
   * us rerun the server immediately after we kill it;
   * otherwise we have to wait about 20 secs.
   * Eliminates "ERROR on binding: Address already in use" error.
   */
  optval = 1;
  setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR,
             (const void *)&optval , sizeof(int));

  /*
   * build the server's Internet address
   */
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  serveraddr.sin_port = htons((unsigned short)portno);

  /*
   * bind: associate the parent socket with a port
   */
  if (bind(sockfd, (struct sockaddr *) &serveraddr,
           sizeof(serveraddr)) < 0)
    error("ERROR on binding");

  /*
   * main loop: wait for a datagram, then echo it
   */
  clientlen = sizeof(clientaddr);
  while (1) {

    /*
     * recvfrom: receive a UDP datagram from a client
     */
    bzero(buf, BUFSIZE);
    n = recvfrom(sockfd, buf, BUFSIZE, 0,
                 (struct sockaddr *) &clientaddr, (unsigned int*)&clientlen);
    if (n < 0)
      error("ERROR in recvfrom");

    /*
     * gethostbyaddr: determine who sent the datagram
     */
    hostaddrp = inet_ntoa(clientaddr.sin_addr);
    if (hostaddrp == NULL)
      error("ERROR on inet_ntoa\n");
    printf("%s ", buf);

    token = strtok(buf, " ");
    param_idx = 0;
    memset(params, 0, sizeof(params[0])*PARAM_NUM);

    if(strcmp("-h", token) == 0)
    {
      printf("Test connection\n");
      resp = " "; 
    }
    else
    {
      while(token)
      {
        if(param_idx == 1)
        {
          params[param_idx] = strtoull(token, NULL, 10);
        }
        else
        {
          params[param_idx] = strtoull(token, NULL, 16);
        }

        param_idx++;

        if(param_idx >= PARAM_NUM)
        {
          break;
        }

        token = strtok(NULL, " ");
      }

      resp = mem_access((void*) params[0], params[2], params[1], param_idx != 3);
    }

    printf(" %s\n", resp);


    /*
     * sendto: echo the input back to the client
     */
    n = sendto(sockfd, resp, strlen(resp), 0,
               (struct sockaddr *) &clientaddr, clientlen);
    if (n < 0)
      error("ERROR in sendto");
  }
}


