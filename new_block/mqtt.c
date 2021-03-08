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


int main(int argc, char *argv[])
{
	int rc;
	struct mosquitto_message *msg;

	mosquitto_lib_init();

	rc = mosquitto_subscribe_simple(
			&msg, 1, true,
			"irc/#", 0,
			"test.mosquitto.org", 1883,
			NULL, 60, true,
			NULL, NULL,
			NULL, NULL);

	if(rc){
		printf("Error: %s\n", mosquitto_strerror(rc));
		mosquitto_lib_cleanup();
		return rc;
	}

	printf("%s %s\n", msg->topic, (char *)msg->payload);
	mosquitto_message_free(&msg);

	mosquitto_lib_cleanup();

	return 0;
}
#include <pyblock.h>
#include <sys/types.h>
#include <sys/un.h>
#include <sys/socket.h>
#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <signal.h>
#include <unistd.h>
#include <sys/poll.h>
#include <mosquitto.h>
#define FALSE 0
double get_run_time();


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

rc = mosquitto_subscribe_simple(
			&msg, 1, true,
			block.str, 0,
			"localhost", 1883,
			NULL, 60, true,
			NULL, NULL,
			NULL, NULL);
	/*
	if(rc){
		printf("Error: %s\n", mosquitto_strerror(rc));
		mosquitto_lib_cleanup();
		return rc;
	}*/

	printf("%s %s\n", msg->topic, (char *)msg->payload);
	mosquitto_message_free(&msg);

	

  double *y;

  struct {
    double val[block->nin];
  }values;
  

         
         for(i=0;i<block->nout;i++){
    			y = (double *)block->y[i];
    			y[0] = values.val[i];

  		 }
     }        
  }
}

static void endC(python_block *block)
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
	int rc;

 
  double *y;
  
  pthread_t thrd;

  mosq = mosquitto_new(NULL, true, NULL);
	if(mosq == NULL){
		fprintf(stderr, "Error: Out of memory.\n");
		return 1;
	}
	
  	/* Connect to test.mosquitto.org on port 1883, with a keepalive of 60 seconds.
	 * This call makes the socket connection only, it does not complete the MQTT
	 * CONNECT/CONNACK flow, you should use mosquitto_loop_start() or
	 * mosquitto_loop_forever() for processing net traffic. */
	rc = mosquitto_connect(mosq, "test.mosquitto.org", 1883, 60);
	if(rc != MOSQ_ERR_SUCCESS){
		mosquitto_destroy(mosq);
		fprintf(stderr, "Error: %s\n", mosquitto_strerror(rc));
		return 1;
	}

	/* Run the network loop in a background thread, this call returns quickly. */
	rc = mosquitto_loop_start(mosq);
	if(rc != MOSQ_ERR_SUCCESS){
		mosquitto_destroy(mosq);
		fprintf(stderr, "Error: %s\n", mosquitto_strerror(rc));
		return 1;
	}
  block->inPar[0]= mosq; 
}

static void inoutP(python_block *block)
{
  int i;
  double *y;
  
  	char payload[20];
	int temp;
	int rc;
  
  struct {
    double val[block->nin];
  }values;
  
  if(block->intPar[0]){
    for(i=0;i<block->nin;i++){
      u = (double *) block->u[i];
      values.val[i] = u[0];
    }
    
    	snprintf(payload, sizeof(payload), "%d", values.val[0]);

	/* Publish the message
	 * mosq - our client instance
	 * *mid = NULL - we don't want to know what the message id for this message is
	 * topic = "example/temperature" - the topic on which this message will be published
	 * payloadlen = strlen(payload) - the length of our payload in bytes
	 * payload - the actual payload
	 * qos = 2 - publish with QoS 2 for this example
	 * retain = false - do not use the retained message feature for this message
	 */
	rc = mosquitto_publish(mosq, NULL, block->str, strlen(payload), payload, 2, false);
	if(rc != MOSQ_ERR_SUCCESS){
		fprintf(stderr, "Error publishing: %s\n", mosquitto_strerror(rc));
	}
}
}

static void endS(python_block *block)
{

  mosquitto_lib_cleanup();
  
}

void mqtt_pub(int flag, python_block *block)
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
