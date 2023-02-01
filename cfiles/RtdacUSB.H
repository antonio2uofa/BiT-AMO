/////////////////////////////////////////////////////////////////////
//
// RT-DAC/USB board - I/O procedures
// RTDACUSB.H
//
//  Copyright (c) by InTeCo/2K, 2001 - 2004
//  All Rights Reserved
//
/////////////////////////////////////////////////////////////////////

#include "ftd2xx.h"

#define NO_OF_PWM         ( 4)  /* Max number of PWMs */
#define NO_OF_ENCODER     (12)  /* Max number of encoders (with and without index signal) */
#define NO_OF_TMRCNT      ( 2)  /* Max number of timer/counters */
#define NO_OF_GENERATOR   ( 1)  /* Max number of generators */

#define NO_OF_AD          (16)
#define NO_OF_DA          ( 4)

#define BINARY_BUFFER_SIZE   (1024)

typedef struct {
  unsigned int Mode;
  unsigned int Prescaler;
  unsigned int Width;
} PWMType;

typedef struct {
  unsigned int Reset;
  unsigned int IdxActive;
  unsigned int IdxInvert;
  long int     Counter;
} EncoderType;

typedef struct {
  unsigned int Reset;
  unsigned int Mode;
  unsigned int Counter;
} TmrCntType;

typedef struct {
  unsigned int St1Len;
  unsigned int St2Len;
  unsigned int NoOfPeriods;
  int          Enable;
  int          SwHwGateStartFlag;
  int          SwGate;
  int          SwStart;
  int          InvertGate;
  int          InvertStart; 
  int          InfiniteGeneration;
  int          St1Level;
  int          InitLevel;
  int          TerminateLevel;
} GeneratorType;


typedef struct {
  unsigned int Gain;
  unsigned int Result;
} ADType;

typedef struct {
  unsigned int  LogicVersion;
  char          ApplicationName[6];
  unsigned int  CN1PinMode;
  unsigned int  CN1Direction;
  unsigned int  CN1Output;
  unsigned int  CN1Input;
  PWMType       PWM[ NO_OF_PWM ];
  EncoderType   Encoder[ NO_OF_ENCODER ];
  TmrCntType    TmrCnt[ NO_OF_TMRCNT ];
  GeneratorType Generator[ NO_OF_GENERATOR ];
  ADType        AD[ NO_OF_AD ];
  unsigned int  DA[ NO_OF_DA ];
} RTDACUSBBufferType;


#define COMMAND_DUMMY           (0x80)
#define COMMAND_SEND            (0x81)
#define COMMAND_READ            (0x82)
#define COMMAND_SEND_AND_READ   (0x83)


int  CommandDummy( void );

int  CommandSend( RTDACUSBBufferType *Buff );
int  CommandRead( RTDACUSBBufferType *Buff );

int  CommandSend_0111( RTDACUSBBufferType *Buff );
int  CommandRead_0111( RTDACUSBBufferType *Buff );

int  CommandSend_0112( RTDACUSBBufferType *Buff );
int  CommandRead_0112( RTDACUSBBufferType *Buff );

// Commands
#define CMD_MARKER         (0x80) /* Command marker */



int Receive( int NoOfBytes, unsigned char ToRead[] );
int Send( int NoOfBytes, unsigned char ToSend[] );


// Open and close USB device
int USBOpen( void );
int USBClose( void );

// Error code and description
int USBLastError( char *Dsrp );

// Timeout management function
int SetTimeouts( int RecTimeout, int SendTimeout );

// Flush queues
int FlushReceiveQueue( void );
int FlushSendQueue( void );
int ReadReceiveQueue( int NoOfBytes, unsigned char Buff[] );

int GetStatus( int *RecQueue, int *SendQueue, int *EventStatus );

