/*
COPYRIGHT (C) 2016  Roberto Bucher (roberto.bucher@supsi.ch)
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA.
*/

#include <pyblock.h>
#include <sys/types.h>
#include <sys/un.h>
#include <sys/socket.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <pthread.h>
#include <signal.h>
#include <unistd.h>
#include <sys/poll.h>
#include <mosquitto.h>
#include <assert.h>
#define FALSE 0
double get_run_time();

struct mosquitto *mosq1;


static void initS(python_block *block)
{
  mosquitto_lib_init();

  int ret;
  char mytopic[80];
  pthread_t thrd;

  signal(SIGPIPE, SIG_IGN);

  strcpy(mytopic,block->str);

}

static void inoutS(python_block *block)
{

int rc;
int i;
char tmp[15]="5.0";
double *y;
double *data;


struct mosquitto_message *msg;

	rc = mosquitto_subscribe_simple(
			&msg, 1, true,
			block->str, 0,
			"localhost", 1883,
			NULL, 60, true,
			NULL, NULL,
			NULL, NULL);
	
	
	if(rc){
		printf("Error: %s\n", mosquitto_strerror(rc));
		mosquitto_lib_cleanup();
		return rc;
	}
	sprintf(tmp, "%s", msg->payload);
    data= msg->payload;
    printf("Data: %s ---> %s \n",data, data[6]);
	mosquitto_message_free(&msg);

	

  

  struct {
    double val[block->nin];
  }values;
  
  values.val[0]=strtof(tmp,NULL);
  printf("Number: %s --> %f  ",tmp, strtof(tmp,NULL));
  
  if(rc==sizeof(values)){
	                for(i=0;i<block->nout;i++){
	                block->realPar[i] = values.val[i];
           }
  }
         
  for(i=0;i<block->nout;i++){
    			y = (double *)block->y[i];
    			y[0] = values.val[i];

  }
}

static void endS(python_block *block)
{
  
  mosquitto_lib_cleanup();
}

void mqtt_sub(int flag, python_block *block)
{
  if (flag==CG_OUT){          /* get input */
    inoutS(block);
  }
  else if (flag==CG_END){     /* termination */ 
    endS(block);
  }
  else if (flag ==CG_INIT){    /* initialisation */
    initS(block);
  }
}

  
static void initP(python_block *block)
{
  mosquitto_lib_init();
 
 	struct mosquitto *mosq;
 	//struct mosquitto *mosq1;
 	struct mosquitto **mosq2;
	int rc;
	intptr_t rc1;

 
  double *y;
  
  pthread_t thrd;
  char payload[20];

  mosq = mosquitto_new(NULL, true, NULL);
	if(mosq == NULL){
		fprintf(stderr, "Error: Out of memory.\n");
	}
	
  	/* Connect to test.mosquitto.org on port 1883, with a keepalive of 60 seconds.
	 * This call makes the socket connection only, it does not complete the MQTT
	 * CONNECT/CONNACK flow, you should use mosquitto_loop_start() or
	 * mosquitto_loop_forever() for processing net traffic. */
	rc = mosquitto_connect(mosq, "localhost", 1883, 60);
	if(rc != MOSQ_ERR_SUCCESS){
		mosquitto_destroy(mosq);
		fprintf(stderr, "Error: %s\n", mosquitto_strerror(rc));
	}

	/* Run the network loop in a background thread, this call returns quickly. */
	rc = mosquitto_loop_start(mosq);
	
	if(rc != MOSQ_ERR_SUCCESS){
		mosquitto_destroy(mosq);
		fprintf(stderr, "Error: %s\n", mosquitto_strerror(rc));
	}
	snprintf(payload, sizeof(payload), "%f", 45.0);
	
	printf("Important %s", "bat");
	mosq1=mosq;
	//block->realPar[0]= (intptr_t)mosq
	assert(mosq1== mosq);
	
	printf("Important %s", "bi");
	printf("Important %d %d \n", sizeof((intptr_t)&mosq), sizeof(block->realPar[0]));
	/*
	block->intPar[0] = ((intptr_t)&mosq);
	
	
	mosq2=(struct mosquitto **)((intptr_t)block->intPar[0]);
	
	
	assert(*mosq2== mosq);
	
	
	rc1= (intptr_t)mosq;
	assert((struct mosquitto *)rc1==mosq);
	
	assert(mosq1==mosq);*/
	
	rc = mosquitto_publish( mosq1, NULL, "paho", strlen(payload), payload, 2, false);
	if(rc != MOSQ_ERR_SUCCESS){
		fprintf(stderr, "Error publishing: %s\n", mosquitto_strerror(rc));
	}
  //printf("Important %d", mosq1);
  printf("%d %d", sizeof(block->realPar[0]), sizeof(mosq)); 
  block->intPar[0] = mosq;
  sleep(5);
}

static void inoutP(python_block *block)
{
  int i, ret;
  double *y;
  double *u;
  char payload[20];
  int temp;
	int rc;


  struct {
    double val[block->nin];
  }values;
  
  printf("Inputs: %d", block->intPar[0]);
  if(block->intPar[0]){
    for(i=0;i<block->nin;i++){
      u = (double *) block->u[i];
      values.val[i] = u[0];
    }
    }
    //ret = send(block->intPar[0],&values,sizeof(values),0);
    //if (ret<0) block->intPar[0]=0;

  //}
	printf("%f \n", values.val[0]);
    snprintf(payload, sizeof(payload), "%f", values.val[0]);
	printf("%s \n",payload);

	/* Publish the message
	 * mosq - our client instance	
	 * *mid = NULL - we don't want to know what the message id for this message is
	 * topic = "example/temperature" - the topic on which this message will be published
	 * payloadlen = strlen(payload) - the length of our payload in bytes
	 * payload - the actual payload
	 * qos = 2 - publish with QoS 2 for this example
	 * retain = false - do not use the retained message feature for this message
	 */
	
	//usleep(1000);
	rc = mosquitto_publish(mosq1, NULL, block->str, strlen(payload), payload, 2, false);
	if(rc != MOSQ_ERR_SUCCESS){
		//fprintf(stderr, "Error publishing: %s\n", mosquitto_strerror(rc));
	}

}

static void endP(python_block *block)
{

  mosquitto_lib_cleanup();
  
}

void mqtt_pub(int flag, python_block *block)
{
  if (flag==CG_OUT){          /* get input */
    inoutP(block);
  }
  else if (flag==CG_END){     /* termination */ 
    endP(block);
  }
  else if (flag ==CG_INIT){    /* initialisation */
    initP(block);
  }
}
