/////////////////////////////////////////////////////////////////////
//
// RT-DAC/USB board - I/O procedures
//
//  Copyright (c) by InTeCo/2K, 2004
//  All Rights Reserved
//
//  Version    Date     Description
//    1.5   2005.06.18  New USBOpen function: dynamic buffer allocation (required by OpenWatcom)
//    1.4   2004.10.07  New functions
//                        CommandSend
//    1.3   2004.09.14  Support of 1.12 logic
//                      Changed function name from CommandDummy_0111 to CommandDummy
//                      New functions:  
//                        CommandSend
//                        CommandRead
//                        CommandSend_0112
//                        CommandRead_0112
//    1.2   2004.07.18  Removed unbuffered/buffered commands
//    1.1   2004.01.28  Buffered I/O operations
//    1.0   2004.01.24  First RT-DAC/USB API release
//
//
/////////////////////////////////////////////////////////////////////

#include "string.h"
#include "rtdacusb.h"

// Handle to the FTDI USB device
static FT_HANDLE ftHandle;


// USBOpen/USBClose counter
static int USBCounter = 0;

// Last operation error code
static int LastErrorCode;


// Binary data send to the RT-DAC/USB device
unsigned char BinaryBufferToSend[ BINARY_BUFFER_SIZE ];
// Binary data read from the RT-DAC/USB device
unsigned char BinaryBufferToRead[ BINARY_BUFFER_SIZE ];

// Dummy command - aplied to leave the JTAG mode
int CommandDummy( void ) {
  unsigned char AuxBuffer[ 2 ];
  AuxBuffer[0] = COMMAND_DUMMY;
  return Send( 1, AuxBuffer ); 
}

/////////////////////////////////////////////////////////////////
//
// Return pointers to binary buffers 
//
unsigned char *GetBufferToSend( void ) {
  return BinaryBufferToSend;
}
unsigned char *GetBufferToRead( void ) {
  return BinaryBufferToRead;
}


/////////////////////////////////////////////////////////////////
//
// Universal Send/Read functions 
//
int CommandSend( RTDACUSBBufferType *RTDACUSBBufferToSend ) {
  switch( RTDACUSBBufferToSend->LogicVersion ) {
    case 0x111:   // Logic 1.11
	  return( CommandSend_0111( RTDACUSBBufferToSend ) );
    case 0x112:   // Logic 1.12
	  return( CommandSend_0112( RTDACUSBBufferToSend ) );
	default:
	  return( -99 );
  }
}

int CommandRead( RTDACUSBBufferType *RTDACUSBBufferToRead ) {
  switch( RTDACUSBBufferToRead->LogicVersion ) {
    case 0x111:   // Logic 1.11
	  return( CommandRead_0111( RTDACUSBBufferToRead ) );
    case 0x112:   // Logic 1.12
	  return( CommandRead_0112( RTDACUSBBufferToRead ) );
	default: 
	  return( -99 );
  }
}

/////////////////////////////////////////////////////////////////
//
// Logic 1.11 funtions 
//
static void CreateBinaryBufferToSend_0111( RTDACUSBBufferType *RTDACUSBBufferToSend ) {
  BinaryBufferToSend[  0] = 0;  // Logic version - read only
  BinaryBufferToSend[  1] = 0;  // Logic version - read only
  BinaryBufferToSend[  2] = 0;  // Logic version - read only
  BinaryBufferToSend[  3] = 0;  // Application name - read only
  BinaryBufferToSend[  4] = 0;  // Application name - read only
  BinaryBufferToSend[  5] = 0;  // Application name - read only
  BinaryBufferToSend[  6] = 0;  // Application name - read only
  BinaryBufferToSend[  7] = 0;  // Application name - read only

  BinaryBufferToSend[  8] = RTDACUSBBufferToSend->CN1PinMode & 0x1F;  
  BinaryBufferToSend[  9] = RTDACUSBBufferToSend->CN1Direction & 0x7F;  
  BinaryBufferToSend[ 10] = (RTDACUSBBufferToSend->CN1Direction >>  7) & 0x7F;  
  BinaryBufferToSend[ 11] = (RTDACUSBBufferToSend->CN1Direction >> 14) & 0x7F;  
  BinaryBufferToSend[ 12] = (RTDACUSBBufferToSend->CN1Direction >> 21) & 0x1F;  
  BinaryBufferToSend[ 13] = RTDACUSBBufferToSend->CN1Output & 0x7F;  
  BinaryBufferToSend[ 14] = (RTDACUSBBufferToSend->CN1Output >>  7) & 0x7F;  
  BinaryBufferToSend[ 15] = (RTDACUSBBufferToSend->CN1Output >> 14) & 0x7F;  
  BinaryBufferToSend[ 16] = (RTDACUSBBufferToSend->CN1Output >> 21) & 0x1F;  
  BinaryBufferToSend[ 17] = 0;  // Digital inputs - read only  
  BinaryBufferToSend[ 18] = 0;  // Digital inputs - read only  
  BinaryBufferToSend[ 19] = 0;  // Digital inputs - read only  
  BinaryBufferToSend[ 20] = 0;  // Digital inputs - read only  

  BinaryBufferToSend[ 21] = RTDACUSBBufferToSend->PWM[0].Prescaler & 0x7F;  
  BinaryBufferToSend[ 22] = (RTDACUSBBufferToSend->PWM[0].Prescaler >>  7) & 0x7F;  
  BinaryBufferToSend[ 23] = ((RTDACUSBBufferToSend->PWM[0].Prescaler >> 14) & 0x03) |  
	                        (0x40*RTDACUSBBufferToSend->PWM[0].Mode);
  BinaryBufferToSend[ 24] = RTDACUSBBufferToSend->PWM[0].Width & 0x7F;  
  BinaryBufferToSend[ 25] = (RTDACUSBBufferToSend->PWM[0].Width >> 7) & 0x1F;  
  BinaryBufferToSend[ 26] = RTDACUSBBufferToSend->PWM[1].Prescaler & 0x7F;  
  BinaryBufferToSend[ 27] = (RTDACUSBBufferToSend->PWM[1].Prescaler >>  7) & 0x7F;  
  BinaryBufferToSend[ 28] = ((RTDACUSBBufferToSend->PWM[1].Prescaler >> 14) & 0x03) |  
	                        (0x40*RTDACUSBBufferToSend->PWM[1].Mode);
  BinaryBufferToSend[ 29] = RTDACUSBBufferToSend->PWM[1].Width & 0x7F;  
  BinaryBufferToSend[ 30] = (RTDACUSBBufferToSend->PWM[1].Width >> 7) & 0x1F;  
  BinaryBufferToSend[ 31] = RTDACUSBBufferToSend->PWM[2].Prescaler & 0x7F;  
  BinaryBufferToSend[ 32] = (RTDACUSBBufferToSend->PWM[2].Prescaler >>  7) & 0x7F;  
  BinaryBufferToSend[ 33] = ((RTDACUSBBufferToSend->PWM[2].Prescaler >> 14) & 0x03) |  
	                        (0x40*RTDACUSBBufferToSend->PWM[2].Mode);
  BinaryBufferToSend[ 34] = RTDACUSBBufferToSend->PWM[2].Width & 0x7F;  
  BinaryBufferToSend[ 35] = (RTDACUSBBufferToSend->PWM[2].Width >> 7) & 0x1F;  
  BinaryBufferToSend[ 36] = RTDACUSBBufferToSend->PWM[3].Prescaler & 0x7F;  
  BinaryBufferToSend[ 37] = (RTDACUSBBufferToSend->PWM[3].Prescaler >>  7) & 0x7F;  
  BinaryBufferToSend[ 38] = ((RTDACUSBBufferToSend->PWM[3].Prescaler >> 14) & 0x03) |  
	                        (0x40*RTDACUSBBufferToSend->PWM[3].Mode);
  BinaryBufferToSend[ 39] = RTDACUSBBufferToSend->PWM[3].Width & 0x7F;  
  BinaryBufferToSend[ 40] = (RTDACUSBBufferToSend->PWM[3].Width >> 7) & 0x1F;  

  BinaryBufferToSend[ 41] = 0x08*RTDACUSBBufferToSend->Encoder[3].Reset |
	                        0x04*RTDACUSBBufferToSend->Encoder[2].Reset |
							0x02*RTDACUSBBufferToSend->Encoder[1].Reset |
							0x01*RTDACUSBBufferToSend->Encoder[0].Reset;  
  BinaryBufferToSend[ 42] = 0x08*RTDACUSBBufferToSend->Encoder[3].IdxActive |
	                        0x04*RTDACUSBBufferToSend->Encoder[2].IdxActive |
							0x02*RTDACUSBBufferToSend->Encoder[1].IdxActive |
							0x01*RTDACUSBBufferToSend->Encoder[0].IdxActive;  
  BinaryBufferToSend[ 43] = 0x08*RTDACUSBBufferToSend->Encoder[3].IdxInvert |
	                        0x04*RTDACUSBBufferToSend->Encoder[2].IdxInvert |
							0x02*RTDACUSBBufferToSend->Encoder[1].IdxInvert |
							0x01*RTDACUSBBufferToSend->Encoder[0].IdxInvert;  
  BinaryBufferToSend[ 44] = 0;  // Encoder 0 counter - read only  
  BinaryBufferToSend[ 45] = 0;  // Encoder 0 counter - read only  
  BinaryBufferToSend[ 46] = 0;  // Encoder 0 counter - read only  
  BinaryBufferToSend[ 47] = 0;  // Encoder 0 counter - read only  
  BinaryBufferToSend[ 48] = 0;  // Encoder 0 counter - read only  
  BinaryBufferToSend[ 49] = 0;  // Encoder 1 counter - read only  
  BinaryBufferToSend[ 50] = 0;  // Encoder 1 counter - read only  
  BinaryBufferToSend[ 51] = 0;  // Encoder 1 counter - read only  
  BinaryBufferToSend[ 52] = 0;  // Encoder 1 counter - read only  
  BinaryBufferToSend[ 53] = 0;  // Encoder 1 counter - read only  
  BinaryBufferToSend[ 54] = 0;  // Encoder 2 counter - read only  
  BinaryBufferToSend[ 55] = 0;  // Encoder 2 counter - read only  
  BinaryBufferToSend[ 56] = 0;  // Encoder 2 counter - read only  
  BinaryBufferToSend[ 57] = 0;  // Encoder 2 counter - read only  
  BinaryBufferToSend[ 58] = 0;  // Encoder 2 counter - read only  
  BinaryBufferToSend[ 59] = 0;  // Encoder 3 counter - read only  
  BinaryBufferToSend[ 60] = 0;  // Encoder 3 counter - read only  
  BinaryBufferToSend[ 61] = 0;  // Encoder 3 counter - read only  
  BinaryBufferToSend[ 62] = 0;  // Encoder 3 counter - read only  
  BinaryBufferToSend[ 63] = 0;  // Encoder 3 counter - read only  

  BinaryBufferToSend[ 64] = 0x02*RTDACUSBBufferToSend->TmrCnt[1].Reset |
							0x01*RTDACUSBBufferToSend->TmrCnt[0].Reset;  
  BinaryBufferToSend[ 65] = 0x02*RTDACUSBBufferToSend->TmrCnt[1].Mode |
							0x01*RTDACUSBBufferToSend->TmrCnt[0].Mode;  
  BinaryBufferToSend[ 66] = 0;  // Tmr/Cnt 0 counter - read only  
  BinaryBufferToSend[ 67] = 0;  // Tmr/Cnt 0 counter - read only  
  BinaryBufferToSend[ 68] = 0;  // Tmr/Cnt 0 counter - read only  
  BinaryBufferToSend[ 69] = 0;  // Tmr/Cnt 0 counter - read only  
  BinaryBufferToSend[ 70] = 0;  // Tmr/Cnt 0 counter - read only  
  BinaryBufferToSend[ 71] = 0;  // Tmr/Cnt 1 counter - read only  
  BinaryBufferToSend[ 72] = 0;  // Tmr/Cnt 1 counter - read only  
  BinaryBufferToSend[ 73] = 0;  // Tmr/Cnt 1 counter - read only  
  BinaryBufferToSend[ 74] = 0;  // Tmr/Cnt 1 counter - read only  
  BinaryBufferToSend[ 75] = 0;  // Tmr/Cnt 1 counter - read only  

  BinaryBufferToSend[ 76] = 0x40*RTDACUSBBufferToSend->Generator[0].InfiniteGeneration |
	                        0x20*RTDACUSBBufferToSend->Generator[0].InvertStart |
	                        0x10*RTDACUSBBufferToSend->Generator[0].InvertGate |
	                        0x08*RTDACUSBBufferToSend->Generator[0].SwStart |
	                        0x04*RTDACUSBBufferToSend->Generator[0].SwGate |
	                        0x02*RTDACUSBBufferToSend->Generator[0].SwHwGateStartFlag |
							0x01*RTDACUSBBufferToSend->Generator[0].Enable; 
  BinaryBufferToSend[ 77] = 0x04*RTDACUSBBufferToSend->Generator[0].TerminateLevel |
	                        0x02*RTDACUSBBufferToSend->Generator[0].InitLevel |
							0x01*RTDACUSBBufferToSend->Generator[0].St1Level; 
  BinaryBufferToSend[ 78] =  RTDACUSBBufferToSend->Generator[0].St1Len & 0x7F;  
  BinaryBufferToSend[ 79] = (RTDACUSBBufferToSend->Generator[0].St1Len >>  7) & 0x7F;  
  BinaryBufferToSend[ 80] = (RTDACUSBBufferToSend->Generator[0].St1Len >> 14) & 0x7F; 
  BinaryBufferToSend[ 81] = (RTDACUSBBufferToSend->Generator[0].St1Len >> 21) & 0x7F; 
  BinaryBufferToSend[ 82] = (RTDACUSBBufferToSend->Generator[0].St1Len >> 28) & 0x0F; 
  BinaryBufferToSend[ 83] =  RTDACUSBBufferToSend->Generator[0].St2Len & 0x7F;  
  BinaryBufferToSend[ 84] = (RTDACUSBBufferToSend->Generator[0].St2Len >>  7) & 0x7F;  
  BinaryBufferToSend[ 85] = (RTDACUSBBufferToSend->Generator[0].St2Len >> 14) & 0x7F; 
  BinaryBufferToSend[ 86] = (RTDACUSBBufferToSend->Generator[0].St2Len >> 21) & 0x7F; 
  BinaryBufferToSend[ 87] = (RTDACUSBBufferToSend->Generator[0].St2Len >> 28) & 0x0F; 
  BinaryBufferToSend[ 88] =  RTDACUSBBufferToSend->Generator[0].NoOfPeriods & 0x7F;  
  BinaryBufferToSend[ 89] = (RTDACUSBBufferToSend->Generator[0].NoOfPeriods >>  7) & 0x7F;  
  BinaryBufferToSend[ 90] = (RTDACUSBBufferToSend->Generator[0].NoOfPeriods >> 14) & 0x7F; 
  BinaryBufferToSend[ 91] = (RTDACUSBBufferToSend->Generator[0].NoOfPeriods >> 21) & 0x7F; 
  BinaryBufferToSend[ 92] = (RTDACUSBBufferToSend->Generator[0].NoOfPeriods >> 28) & 0x0F; 

  BinaryBufferToSend[ 93] = (((RTDACUSBBufferToSend->AD[ 1].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 0].Gain) & 0x07 );
  BinaryBufferToSend[ 94] = (((RTDACUSBBufferToSend->AD[ 3].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 2].Gain) & 0x07 );
  BinaryBufferToSend[ 95] = (((RTDACUSBBufferToSend->AD[ 5].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 4].Gain) & 0x07 );
  BinaryBufferToSend[ 96] = (((RTDACUSBBufferToSend->AD[ 7].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 6].Gain) & 0x07 );
  BinaryBufferToSend[ 97] = (((RTDACUSBBufferToSend->AD[ 9].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 8].Gain) & 0x07 );
  BinaryBufferToSend[ 98] = (((RTDACUSBBufferToSend->AD[11].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[10].Gain) & 0x07 );
  BinaryBufferToSend[ 99] = (((RTDACUSBBufferToSend->AD[13].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[12].Gain) & 0x07 );
  BinaryBufferToSend[100] = (((RTDACUSBBufferToSend->AD[15].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[14].Gain) & 0x07 );
  BinaryBufferToSend[101] = 0;  // A/D  0 result - read only  
  BinaryBufferToSend[102] = 0;  // A/D  0 result - read only  
  BinaryBufferToSend[103] = 0;  // A/D  1 result - read only  
  BinaryBufferToSend[104] = 0;  // A/D  1 result - read only  
  BinaryBufferToSend[105] = 0;  // A/D  2 result - read only  
  BinaryBufferToSend[106] = 0;  // A/D  2 result - read only  
  BinaryBufferToSend[107] = 0;  // A/D  3 result - read only  
  BinaryBufferToSend[108] = 0;  // A/D  3 result - read only  
  BinaryBufferToSend[109] = 0;  // A/D  4 result - read only  
  BinaryBufferToSend[110] = 0;  // A/D  4 result - read only  
  BinaryBufferToSend[111] = 0;  // A/D  5 result - read only  
  BinaryBufferToSend[112] = 0;  // A/D  5 result - read only  
  BinaryBufferToSend[113] = 0;  // A/D  6 result - read only  
  BinaryBufferToSend[114] = 0;  // A/D  6 result - read only  
  BinaryBufferToSend[115] = 0;  // A/D  7 result - read only  
  BinaryBufferToSend[116] = 0;  // A/D  7 result - read only  
  BinaryBufferToSend[117] = 0;  // A/D  8 result - read only  
  BinaryBufferToSend[118] = 0;  // A/D  8 result - read only  
  BinaryBufferToSend[119] = 0;  // A/D  9 result - read only  
  BinaryBufferToSend[120] = 0;  // A/D  9 result - read only  
  BinaryBufferToSend[121] = 0;  // A/D 10 result - read only  
  BinaryBufferToSend[122] = 0;  // A/D 10 result - read only  
  BinaryBufferToSend[123] = 0;  // A/D 11 result - read only  
  BinaryBufferToSend[124] = 0;  // A/D 11 result - read only  
  BinaryBufferToSend[125] = 0;  // A/D 12 result - read only  
  BinaryBufferToSend[126] = 0;  // A/D 12 result - read only  
  BinaryBufferToSend[127] = 0;  // A/D 13 result - read only  
  BinaryBufferToSend[128] = 0;  // A/D 13 result - read only  
  BinaryBufferToSend[129] = 0;  // A/D 14 result - read only  
  BinaryBufferToSend[130] = 0;  // A/D 14 result - read only  
  BinaryBufferToSend[131] = 0;  // A/D 15 result - read only  
  BinaryBufferToSend[132] = 0;  // A/D 15 result - read only  

  BinaryBufferToSend[133] = (RTDACUSBBufferToSend->DA[0]) & 0x7F;
  BinaryBufferToSend[134] = (RTDACUSBBufferToSend->DA[0] >> 7) & 0x7F;
  BinaryBufferToSend[135] = (RTDACUSBBufferToSend->DA[1]) & 0x7F;
  BinaryBufferToSend[136] = (RTDACUSBBufferToSend->DA[1] >> 7) & 0x7F;
  BinaryBufferToSend[137] = (RTDACUSBBufferToSend->DA[2]) & 0x7F;
  BinaryBufferToSend[138] = (RTDACUSBBufferToSend->DA[2] >> 7) & 0x7F;
  BinaryBufferToSend[139] = (RTDACUSBBufferToSend->DA[3]) & 0x7F;
  BinaryBufferToSend[140] = (RTDACUSBBufferToSend->DA[3] >> 7) & 0x7F;

}

static void UnpackBinaryBuffer_0111( RTDACUSBBufferType *RTDACUSBBufferToRead ) {
  RTDACUSBBufferToRead->LogicVersion = ((int)(BinaryBufferToRead[1]) <<  8) +
	                                  ((int)(BinaryBufferToRead[0]) );  
  RTDACUSBBufferToRead->ApplicationName[5] = '\0';
  RTDACUSBBufferToRead->ApplicationName[4] = (char)(BinaryBufferToRead[3]);
  RTDACUSBBufferToRead->ApplicationName[3] = (char)(BinaryBufferToRead[4]);
  RTDACUSBBufferToRead->ApplicationName[2] = (char)(BinaryBufferToRead[5]);
  RTDACUSBBufferToRead->ApplicationName[1] = (char)(BinaryBufferToRead[6]);
  RTDACUSBBufferToRead->ApplicationName[0] = (char)(BinaryBufferToRead[7]);

  RTDACUSBBufferToRead->CN1PinMode = BinaryBufferToRead[8] & 0x1F;

  RTDACUSBBufferToRead->CN1Direction =  (int)(BinaryBufferToRead[9]) |
	                                  (((int)(BinaryBufferToRead[10])) <<  8) |
	                                  (((int)(BinaryBufferToRead[11])) << 16) |
	                                  (((int)(BinaryBufferToRead[12])) << 24);
  RTDACUSBBufferToRead->CN1Output    =  (int)(BinaryBufferToRead[13]) |
	                                  (((int)(BinaryBufferToRead[14])) <<  8) |
	                                  (((int)(BinaryBufferToRead[15])) << 16) |
	                                  (((int)(BinaryBufferToRead[16])) << 24);
  RTDACUSBBufferToRead->CN1Input     =  (int)(BinaryBufferToRead[17]) |
	                                  (((int)(BinaryBufferToRead[18])) <<  8) |
	                                  (((int)(BinaryBufferToRead[19])) << 16) |
	                                  (((int)(BinaryBufferToRead[20])) << 24);

  RTDACUSBBufferToRead->PWM[0].Prescaler = (int)(BinaryBufferToRead[21]) +
	                                    (((int)(BinaryBufferToRead[22])) << 8);
  RTDACUSBBufferToRead->PWM[0].Mode  = (int)(BinaryBufferToRead[23]);
  RTDACUSBBufferToRead->PWM[0].Width = (int)(BinaryBufferToRead[24]) +
	                                (((int)(BinaryBufferToRead[25])) << 8);
  RTDACUSBBufferToRead->PWM[1].Prescaler = (int)(BinaryBufferToRead[26]) +
	                                    (((int)(BinaryBufferToRead[27])) << 8);
  RTDACUSBBufferToRead->PWM[1].Mode  = (int)(BinaryBufferToRead[28]);
  RTDACUSBBufferToRead->PWM[1].Width = (int)(BinaryBufferToRead[29]) +
	                                (((int)(BinaryBufferToRead[30])) << 8);
  RTDACUSBBufferToRead->PWM[2].Prescaler = (int)(BinaryBufferToRead[31]) +
	                                    (((int)(BinaryBufferToRead[32])) << 8);
  RTDACUSBBufferToRead->PWM[2].Mode  = (int)(BinaryBufferToRead[33]);
  RTDACUSBBufferToRead->PWM[2].Width = (int)(BinaryBufferToRead[34]) +
	                                (((int)(BinaryBufferToRead[35])) << 8);
  RTDACUSBBufferToRead->PWM[3].Prescaler = (int)(BinaryBufferToRead[36]) +
	                                    (((int)(BinaryBufferToRead[37])) << 8);
  RTDACUSBBufferToRead->PWM[3].Mode  = (int)(BinaryBufferToRead[38]);
  RTDACUSBBufferToRead->PWM[3].Width = (int)(BinaryBufferToRead[39]) +
	                                (((int)(BinaryBufferToRead[40])) << 8);

  RTDACUSBBufferToRead->Encoder[0].Reset = (BinaryBufferToRead[41] >> 0) & 0x01;
  RTDACUSBBufferToRead->Encoder[1].Reset = (BinaryBufferToRead[41] >> 1) & 0x01;
  RTDACUSBBufferToRead->Encoder[2].Reset = (BinaryBufferToRead[41] >> 2) & 0x01;
  RTDACUSBBufferToRead->Encoder[3].Reset = (BinaryBufferToRead[41] >> 3) & 0x01;
  RTDACUSBBufferToRead->Encoder[0].IdxActive = (BinaryBufferToRead[42] >> 0) & 0x01;
  RTDACUSBBufferToRead->Encoder[1].IdxActive = (BinaryBufferToRead[42] >> 1) & 0x01;
  RTDACUSBBufferToRead->Encoder[2].IdxActive = (BinaryBufferToRead[42] >> 2) & 0x01;
  RTDACUSBBufferToRead->Encoder[3].IdxActive = (BinaryBufferToRead[42] >> 3) & 0x01;
  RTDACUSBBufferToRead->Encoder[0].IdxInvert = (BinaryBufferToRead[43] >> 0) & 0x01;
  RTDACUSBBufferToRead->Encoder[1].IdxInvert = (BinaryBufferToRead[43] >> 1) & 0x01;
  RTDACUSBBufferToRead->Encoder[2].IdxInvert = (BinaryBufferToRead[43] >> 2) & 0x01;
  RTDACUSBBufferToRead->Encoder[3].IdxInvert = (BinaryBufferToRead[43] >> 3) & 0x01;

  RTDACUSBBufferToRead->Encoder[0].Counter =  (int)(BinaryBufferToRead[44]) |
	                                       (((int)(BinaryBufferToRead[45])) <<  8) |
	                                       (((int)(BinaryBufferToRead[46])) << 16) |
	                                       (((int)(BinaryBufferToRead[47])) << 24);
  RTDACUSBBufferToRead->Encoder[1].Counter =  (int)(BinaryBufferToRead[49]) |
	                                       (((int)(BinaryBufferToRead[50])) <<  8) |
	                                       (((int)(BinaryBufferToRead[51])) << 16) |
	                                       (((int)(BinaryBufferToRead[52])) << 24);
  RTDACUSBBufferToRead->Encoder[2].Counter =  (int)(BinaryBufferToRead[54]) |
	                                       (((int)(BinaryBufferToRead[55])) <<  8) |
	                                       (((int)(BinaryBufferToRead[56])) << 16) |
	                                       (((int)(BinaryBufferToRead[57])) << 24);
  RTDACUSBBufferToRead->Encoder[3].Counter =  (int)(BinaryBufferToRead[59]) |
	                                       (((int)(BinaryBufferToRead[60])) <<  8) |
	                                       (((int)(BinaryBufferToRead[61])) << 16) |
	                                       (((int)(BinaryBufferToRead[62])) << 24);

  RTDACUSBBufferToRead->TmrCnt[0].Reset = (BinaryBufferToRead[64] >> 0) & 0x01;
  RTDACUSBBufferToRead->TmrCnt[1].Reset = (BinaryBufferToRead[64] >> 1) & 0x01;
  RTDACUSBBufferToRead->TmrCnt[0].Mode  = (BinaryBufferToRead[65] >> 0) & 0x01;
  RTDACUSBBufferToRead->TmrCnt[1].Mode  = (BinaryBufferToRead[65] >> 1) & 0x01;
  
  RTDACUSBBufferToRead->TmrCnt[0].Counter =  (int)(BinaryBufferToRead[66]) |
	                                      (((int)(BinaryBufferToRead[67])) <<  8) |
	                                      (((int)(BinaryBufferToRead[68])) << 16) |
	                                      (((int)(BinaryBufferToRead[69])) << 24);
  RTDACUSBBufferToRead->TmrCnt[1].Counter =  (int)(BinaryBufferToRead[71]) |
	                                      (((int)(BinaryBufferToRead[72])) <<  8) |
	                                      (((int)(BinaryBufferToRead[73])) << 16) |
	                                      (((int)(BinaryBufferToRead[74])) << 24);

  RTDACUSBBufferToRead->Generator[0].Enable             = (BinaryBufferToRead[76] >> 0) & 0x01;
  RTDACUSBBufferToRead->Generator[0].SwHwGateStartFlag  = (BinaryBufferToRead[76] >> 1) & 0x01;
  RTDACUSBBufferToRead->Generator[0].SwGate             = (BinaryBufferToRead[76] >> 2) & 0x01;
  RTDACUSBBufferToRead->Generator[0].SwStart            = (BinaryBufferToRead[76] >> 3) & 0x01;
  RTDACUSBBufferToRead->Generator[0].InvertGate         = (BinaryBufferToRead[76] >> 4) & 0x01;
  RTDACUSBBufferToRead->Generator[0].InvertStart        = (BinaryBufferToRead[76] >> 5) & 0x01;
  RTDACUSBBufferToRead->Generator[0].InfiniteGeneration = (BinaryBufferToRead[76] >> 6) & 0x01;
  RTDACUSBBufferToRead->Generator[0].St1Level           = (BinaryBufferToRead[77] >> 0) & 0x01;
  RTDACUSBBufferToRead->Generator[0].InitLevel          = (BinaryBufferToRead[77] >> 1) & 0x01;
  RTDACUSBBufferToRead->Generator[0].TerminateLevel     = (BinaryBufferToRead[77] >> 2) & 0x01;
  RTDACUSBBufferToRead->Generator[0].St1Len =  (int)(BinaryBufferToRead[78]) |
	                                         (((int)(BinaryBufferToRead[79])) <<  8) |
	                                         (((int)(BinaryBufferToRead[80])) << 16) |
	                                         (((int)(BinaryBufferToRead[81])) << 24);
  RTDACUSBBufferToRead->Generator[0].St2Len =  (int)(BinaryBufferToRead[83]) |
	                                         (((int)(BinaryBufferToRead[84])) <<  8) |
	                                         (((int)(BinaryBufferToRead[85])) << 16) |
	                                         (((int)(BinaryBufferToRead[86])) << 24);
  RTDACUSBBufferToRead->Generator[0].NoOfPeriods =  (int)(BinaryBufferToRead[88]) |
	                                              (((int)(BinaryBufferToRead[89])) <<  8) |
	                                              (((int)(BinaryBufferToRead[90])) << 16) |
	                                              (((int)(BinaryBufferToRead[91])) << 24);

  RTDACUSBBufferToRead->AD[ 0].Gain =  (int)(BinaryBufferToRead[ 93]) & 0x07;
  RTDACUSBBufferToRead->AD[ 1].Gain = ((int)(BinaryBufferToRead[ 93]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 2].Gain =  (int)(BinaryBufferToRead[ 94]) & 0x07;
  RTDACUSBBufferToRead->AD[ 3].Gain = ((int)(BinaryBufferToRead[ 94]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 4].Gain =  (int)(BinaryBufferToRead[ 95]) & 0x07;
  RTDACUSBBufferToRead->AD[ 5].Gain = ((int)(BinaryBufferToRead[ 95]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 6].Gain =  (int)(BinaryBufferToRead[ 96]) & 0x07;
  RTDACUSBBufferToRead->AD[ 7].Gain = ((int)(BinaryBufferToRead[ 96]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 8].Gain =  (int)(BinaryBufferToRead[ 97]) & 0x07;
  RTDACUSBBufferToRead->AD[ 9].Gain = ((int)(BinaryBufferToRead[ 97]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[10].Gain =  (int)(BinaryBufferToRead[ 98]) & 0x07;
  RTDACUSBBufferToRead->AD[11].Gain = ((int)(BinaryBufferToRead[ 98]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[12].Gain =  (int)(BinaryBufferToRead[ 99]) & 0x07;
  RTDACUSBBufferToRead->AD[13].Gain = ((int)(BinaryBufferToRead[ 99]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[14].Gain =  (int)(BinaryBufferToRead[100]) & 0x07;
  RTDACUSBBufferToRead->AD[15].Gain = ((int)(BinaryBufferToRead[100]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 0].Result =    (int)(BinaryBufferToRead[101]) |
	                                     (((int)(BinaryBufferToRead[102])) <<  8);
  RTDACUSBBufferToRead->AD[ 1].Result =    (int)(BinaryBufferToRead[103]) |
	                                     (((int)(BinaryBufferToRead[104])) <<  8);
  RTDACUSBBufferToRead->AD[ 2].Result =    (int)(BinaryBufferToRead[105]) |
	                                     (((int)(BinaryBufferToRead[106])) <<  8);
  RTDACUSBBufferToRead->AD[ 3].Result =    (int)(BinaryBufferToRead[107]) |
	                                     (((int)(BinaryBufferToRead[108])) <<  8);
  RTDACUSBBufferToRead->AD[ 4].Result =    (int)(BinaryBufferToRead[109]) |
	                                     (((int)(BinaryBufferToRead[110])) <<  8);
  RTDACUSBBufferToRead->AD[ 5].Result =    (int)(BinaryBufferToRead[111]) |
	                                     (((int)(BinaryBufferToRead[112])) <<  8);
  RTDACUSBBufferToRead->AD[ 6].Result =    (int)(BinaryBufferToRead[113]) |
	                                     (((int)(BinaryBufferToRead[114])) <<  8);
  RTDACUSBBufferToRead->AD[ 7].Result =    (int)(BinaryBufferToRead[115]) |
	                                     (((int)(BinaryBufferToRead[116])) <<  8);
  RTDACUSBBufferToRead->AD[ 8].Result =    (int)(BinaryBufferToRead[117]) |
	                                     (((int)(BinaryBufferToRead[118])) <<  8);
  RTDACUSBBufferToRead->AD[ 9].Result =    (int)(BinaryBufferToRead[119]) |
	                                     (((int)(BinaryBufferToRead[120])) <<  8);
  RTDACUSBBufferToRead->AD[10].Result =    (int)(BinaryBufferToRead[121]) |
	                                     (((int)(BinaryBufferToRead[122])) <<  8);
  RTDACUSBBufferToRead->AD[11].Result =    (int)(BinaryBufferToRead[123]) |
	                                     (((int)(BinaryBufferToRead[124])) <<  8);
  RTDACUSBBufferToRead->AD[12].Result =    (int)(BinaryBufferToRead[125]) |
	                                     (((int)(BinaryBufferToRead[126])) <<  8);
  RTDACUSBBufferToRead->AD[13].Result =    (int)(BinaryBufferToRead[127]) |
	                                     (((int)(BinaryBufferToRead[128])) <<  8);
  RTDACUSBBufferToRead->AD[14].Result =    (int)(BinaryBufferToRead[129]) |
	                                     (((int)(BinaryBufferToRead[130])) <<  8);
  RTDACUSBBufferToRead->AD[15].Result =    (int)(BinaryBufferToRead[131]) |
	                                     (((int)(BinaryBufferToRead[132])) <<  8);

  RTDACUSBBufferToRead->DA[0] =   (int)(BinaryBufferToRead[133]) |
	                            (((int)(BinaryBufferToRead[134])) <<  8);
  RTDACUSBBufferToRead->DA[1] =   (int)(BinaryBufferToRead[135]) |
	                            (((int)(BinaryBufferToRead[136])) <<  8);
  RTDACUSBBufferToRead->DA[2] =   (int)(BinaryBufferToRead[137]) |
	                            (((int)(BinaryBufferToRead[138])) <<  8);
  RTDACUSBBufferToRead->DA[3] =   (int)(BinaryBufferToRead[139]) |
	                            (((int)(BinaryBufferToRead[140])) <<  8);
}

int CommandSend_0111( RTDACUSBBufferType *RTDACUSBBufferToSend ) {
  int i;
  unsigned char AuxBuffer[ 512 ];
  CreateBinaryBufferToSend_0111( RTDACUSBBufferToSend );
  AuxBuffer[0] = COMMAND_SEND;
  for( i=0; i<=150; i++ )
    AuxBuffer[i+1] = BinaryBufferToSend[i] & 0x7F;
  return Send( 150, AuxBuffer ); 
}

int CommandRead_0111( RTDACUSBBufferType *RTDACUSBBufferToRead ) {
  int RecQueue, SendQueue, EventStatus;
  unsigned char AuxBuffer[ 5 ];
  static unsigned char AuxReciveBuff[ 67000 ];
  AuxBuffer[0] = COMMAND_READ;
  Send( 1, AuxBuffer );        // Send the command
  if( LastErrorCode != FT_OK )
    return( -5 );

  LastErrorCode = Receive( 150, BinaryBufferToRead );
  GetStatus( &RecQueue, &SendQueue, &EventStatus );
  if( RecQueue > 0 )
    LastErrorCode = Receive( RecQueue, AuxReciveBuff );
  UnpackBinaryBuffer_0111( RTDACUSBBufferToRead );
  return LastErrorCode;
}


/////////////////////////////////////////////////////////////////
//
// Logic 1.12 funtions 
//
static void CreateBinaryBufferToSend_0112( RTDACUSBBufferType *RTDACUSBBufferToSend ) {
  BinaryBufferToSend[  0] = 0;  // Logic version - read only
  BinaryBufferToSend[  1] = 0;  // Logic version - read only
  BinaryBufferToSend[  2] = 0;  // Logic version - read only
  BinaryBufferToSend[  3] = 0;  // Application name - read only
  BinaryBufferToSend[  4] = 0;  // Application name - read only
  BinaryBufferToSend[  5] = 0;  // Application name - read only
  BinaryBufferToSend[  6] = 0;  // Application name - read only
  BinaryBufferToSend[  7] = 0;  // Application name - read only

  BinaryBufferToSend[  8] = RTDACUSBBufferToSend->CN1PinMode & 0x03;  
  BinaryBufferToSend[  9] = RTDACUSBBufferToSend->CN1Direction & 0x7F;  
  BinaryBufferToSend[ 10] = (RTDACUSBBufferToSend->CN1Direction >>  7) & 0x7F;  
  BinaryBufferToSend[ 11] = (RTDACUSBBufferToSend->CN1Direction >> 14) & 0x7F;  
  BinaryBufferToSend[ 12] = (RTDACUSBBufferToSend->CN1Direction >> 21) & 0x1F;  
  BinaryBufferToSend[ 13] = RTDACUSBBufferToSend->CN1Output & 0x7F;  
  BinaryBufferToSend[ 14] = (RTDACUSBBufferToSend->CN1Output >>  7) & 0x7F;  
  BinaryBufferToSend[ 15] = (RTDACUSBBufferToSend->CN1Output >> 14) & 0x7F;  
  BinaryBufferToSend[ 16] = (RTDACUSBBufferToSend->CN1Output >> 21) & 0x1F;  
  BinaryBufferToSend[ 17] = 0;  // Digital inputs - read only  
  BinaryBufferToSend[ 18] = 0;  // Digital inputs - read only  
  BinaryBufferToSend[ 19] = 0;  // Digital inputs - read only  
  BinaryBufferToSend[ 20] = 0;  // Digital inputs - read only  

  BinaryBufferToSend[ 21] = RTDACUSBBufferToSend->PWM[0].Prescaler & 0x7F;  
  BinaryBufferToSend[ 22] = (RTDACUSBBufferToSend->PWM[0].Prescaler >>  7) & 0x7F;  
  BinaryBufferToSend[ 23] = ((RTDACUSBBufferToSend->PWM[0].Prescaler >> 14) & 0x03) |  
	                        (0x40*RTDACUSBBufferToSend->PWM[0].Mode);
  BinaryBufferToSend[ 24] = RTDACUSBBufferToSend->PWM[0].Width & 0x7F;  
  BinaryBufferToSend[ 25] = (RTDACUSBBufferToSend->PWM[0].Width >> 7) & 0x1F;  
  BinaryBufferToSend[ 26] = RTDACUSBBufferToSend->PWM[1].Prescaler & 0x7F;  
  BinaryBufferToSend[ 27] = (RTDACUSBBufferToSend->PWM[1].Prescaler >>  7) & 0x7F;  
  BinaryBufferToSend[ 28] = ((RTDACUSBBufferToSend->PWM[1].Prescaler >> 14) & 0x03) |  
	                        (0x40*RTDACUSBBufferToSend->PWM[1].Mode);
  BinaryBufferToSend[ 29] = RTDACUSBBufferToSend->PWM[1].Width & 0x7F;  
  BinaryBufferToSend[ 30] = (RTDACUSBBufferToSend->PWM[1].Width >> 7) & 0x1F;  

  BinaryBufferToSend[ 31] = 0x40*RTDACUSBBufferToSend->Encoder[ 6].Reset |
	                        0x20*RTDACUSBBufferToSend->Encoder[ 5].Reset |
	                        0x10*RTDACUSBBufferToSend->Encoder[ 4].Reset |
	                        0x08*RTDACUSBBufferToSend->Encoder[ 3].Reset |
	                        0x04*RTDACUSBBufferToSend->Encoder[ 2].Reset |
							0x02*RTDACUSBBufferToSend->Encoder[ 1].Reset |
							0x01*RTDACUSBBufferToSend->Encoder[ 0].Reset;  
  BinaryBufferToSend[ 32] = 0x10*RTDACUSBBufferToSend->Encoder[11].Reset |
	                        0x08*RTDACUSBBufferToSend->Encoder[10].Reset |
	                        0x04*RTDACUSBBufferToSend->Encoder[ 9].Reset |
							0x02*RTDACUSBBufferToSend->Encoder[ 8].Reset |
							0x01*RTDACUSBBufferToSend->Encoder[ 7].Reset;  


  BinaryBufferToSend[ 33] = 0;  // Encoder  0 counter - read only  
  BinaryBufferToSend[ 34] = 0;  // Encoder  0 counter - read only  
  BinaryBufferToSend[ 35] = 0;  // Encoder  0 counter - read only  
  BinaryBufferToSend[ 36] = 0;  // Encoder  0 counter - read only  
  BinaryBufferToSend[ 37] = 0;  // Encoder  1 counter - read only  
  BinaryBufferToSend[ 38] = 0;  // Encoder  1 counter - read only  
  BinaryBufferToSend[ 39] = 0;  // Encoder  1 counter - read only  
  BinaryBufferToSend[ 40] = 0;  // Encoder  1 counter - read only  
  BinaryBufferToSend[ 41] = 0;  // Encoder  2 counter - read only  
  BinaryBufferToSend[ 42] = 0;  // Encoder  2 counter - read only  
  BinaryBufferToSend[ 43] = 0;  // Encoder  2 counter - read only  
  BinaryBufferToSend[ 44] = 0;  // Encoder  2 counter - read only  
  BinaryBufferToSend[ 45] = 0;  // Encoder  3 counter - read only  
  BinaryBufferToSend[ 46] = 0;  // Encoder  3 counter - read only  
  BinaryBufferToSend[ 47] = 0;  // Encoder  3 counter - read only  
  BinaryBufferToSend[ 48] = 0;  // Encoder  3 counter - read only  
  BinaryBufferToSend[ 49] = 0;  // Encoder  4 counter - read only  
  BinaryBufferToSend[ 50] = 0;  // Encoder  4 counter - read only  
  BinaryBufferToSend[ 51] = 0;  // Encoder  4 counter - read only  
  BinaryBufferToSend[ 52] = 0;  // Encoder  4 counter - read only  
  BinaryBufferToSend[ 53] = 0;  // Encoder  5 counter - read only  
  BinaryBufferToSend[ 54] = 0;  // Encoder  5 counter - read only  
  BinaryBufferToSend[ 55] = 0;  // Encoder  5 counter - read only  
  BinaryBufferToSend[ 56] = 0;  // Encoder  5 counter - read only  
  BinaryBufferToSend[ 57] = 0;  // Encoder  6 counter - read only  
  BinaryBufferToSend[ 58] = 0;  // Encoder  6 counter - read only  
  BinaryBufferToSend[ 59] = 0;  // Encoder  6 counter - read only  
  BinaryBufferToSend[ 60] = 0;  // Encoder  6 counter - read only  
  BinaryBufferToSend[ 61] = 0;  // Encoder  7 counter - read only  
  BinaryBufferToSend[ 62] = 0;  // Encoder  7 counter - read only  
  BinaryBufferToSend[ 63] = 0;  // Encoder  7 counter - read only  
  BinaryBufferToSend[ 64] = 0;  // Encoder  7 counter - read only  
  BinaryBufferToSend[ 65] = 0;  // Encoder  8 counter - read only  
  BinaryBufferToSend[ 66] = 0;  // Encoder  8 counter - read only  
  BinaryBufferToSend[ 67] = 0;  // Encoder  8 counter - read only  
  BinaryBufferToSend[ 68] = 0;  // Encoder  8 counter - read only  
  BinaryBufferToSend[ 69] = 0;  // Encoder  9 counter - read only  
  BinaryBufferToSend[ 70] = 0;  // Encoder  9 counter - read only  
  BinaryBufferToSend[ 71] = 0;  // Encoder  9 counter - read only  
  BinaryBufferToSend[ 72] = 0;  // Encoder  9 counter - read only  
  BinaryBufferToSend[ 73] = 0;  // Encoder 10 counter - read only  
  BinaryBufferToSend[ 74] = 0;  // Encoder 10 counter - read only  
  BinaryBufferToSend[ 75] = 0;  // Encoder 10 counter - read only  
  BinaryBufferToSend[ 76] = 0;  // Encoder 10 counter - read only  
  BinaryBufferToSend[ 77] = 0;  // Encoder 11 counter - read only  
  BinaryBufferToSend[ 78] = 0;  // Encoder 11 counter - read only  
  BinaryBufferToSend[ 79] = 0;  // Encoder 11 counter - read only  
  BinaryBufferToSend[ 80] = 0;  // Encoder 11 counter - read only  

  BinaryBufferToSend[ 93] = (((RTDACUSBBufferToSend->AD[ 1].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 0].Gain) & 0x07 );
  BinaryBufferToSend[ 94] = (((RTDACUSBBufferToSend->AD[ 3].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 2].Gain) & 0x07 );
  BinaryBufferToSend[ 95] = (((RTDACUSBBufferToSend->AD[ 5].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 4].Gain) & 0x07 );
  BinaryBufferToSend[ 96] = (((RTDACUSBBufferToSend->AD[ 7].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 6].Gain) & 0x07 );
  BinaryBufferToSend[ 97] = (((RTDACUSBBufferToSend->AD[ 9].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[ 8].Gain) & 0x07 );
  BinaryBufferToSend[ 98] = (((RTDACUSBBufferToSend->AD[11].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[10].Gain) & 0x07 );
  BinaryBufferToSend[ 99] = (((RTDACUSBBufferToSend->AD[13].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[12].Gain) & 0x07 );
  BinaryBufferToSend[100] = (((RTDACUSBBufferToSend->AD[15].Gain) & 0x07) << 4 ) |
	                         ((RTDACUSBBufferToSend->AD[14].Gain) & 0x07 );
  BinaryBufferToSend[101] = 0;  // A/D  0 result - read only  
  BinaryBufferToSend[102] = 0;  // A/D  0 result - read only  
  BinaryBufferToSend[103] = 0;  // A/D  1 result - read only  
  BinaryBufferToSend[104] = 0;  // A/D  1 result - read only  
  BinaryBufferToSend[105] = 0;  // A/D  2 result - read only  
  BinaryBufferToSend[106] = 0;  // A/D  2 result - read only  
  BinaryBufferToSend[107] = 0;  // A/D  3 result - read only  
  BinaryBufferToSend[108] = 0;  // A/D  3 result - read only  
  BinaryBufferToSend[109] = 0;  // A/D  4 result - read only  
  BinaryBufferToSend[110] = 0;  // A/D  4 result - read only  
  BinaryBufferToSend[111] = 0;  // A/D  5 result - read only  
  BinaryBufferToSend[112] = 0;  // A/D  5 result - read only  
  BinaryBufferToSend[113] = 0;  // A/D  6 result - read only  
  BinaryBufferToSend[114] = 0;  // A/D  6 result - read only  
  BinaryBufferToSend[115] = 0;  // A/D  7 result - read only  
  BinaryBufferToSend[116] = 0;  // A/D  7 result - read only  
  BinaryBufferToSend[117] = 0;  // A/D  8 result - read only  
  BinaryBufferToSend[118] = 0;  // A/D  8 result - read only  
  BinaryBufferToSend[119] = 0;  // A/D  9 result - read only  
  BinaryBufferToSend[120] = 0;  // A/D  9 result - read only  
  BinaryBufferToSend[121] = 0;  // A/D 10 result - read only  
  BinaryBufferToSend[122] = 0;  // A/D 10 result - read only  
  BinaryBufferToSend[123] = 0;  // A/D 11 result - read only  
  BinaryBufferToSend[124] = 0;  // A/D 11 result - read only  
  BinaryBufferToSend[125] = 0;  // A/D 12 result - read only  
  BinaryBufferToSend[126] = 0;  // A/D 12 result - read only  
  BinaryBufferToSend[127] = 0;  // A/D 13 result - read only  
  BinaryBufferToSend[128] = 0;  // A/D 13 result - read only  
  BinaryBufferToSend[129] = 0;  // A/D 14 result - read only  
  BinaryBufferToSend[130] = 0;  // A/D 14 result - read only  
  BinaryBufferToSend[131] = 0;  // A/D 15 result - read only  
  BinaryBufferToSend[132] = 0;  // A/D 15 result - read only  

  BinaryBufferToSend[133] = (RTDACUSBBufferToSend->DA[0]) & 0x7F;
  BinaryBufferToSend[134] = (RTDACUSBBufferToSend->DA[0] >> 7) & 0x7F;
  BinaryBufferToSend[135] = (RTDACUSBBufferToSend->DA[1]) & 0x7F;
  BinaryBufferToSend[136] = (RTDACUSBBufferToSend->DA[1] >> 7) & 0x7F;
  BinaryBufferToSend[137] = (RTDACUSBBufferToSend->DA[2]) & 0x7F;
  BinaryBufferToSend[138] = (RTDACUSBBufferToSend->DA[2] >> 7) & 0x7F;
  BinaryBufferToSend[139] = (RTDACUSBBufferToSend->DA[3]) & 0x7F;
  BinaryBufferToSend[140] = (RTDACUSBBufferToSend->DA[3] >> 7) & 0x7F;

}

static void UnpackBinaryBuffer_0112( RTDACUSBBufferType *RTDACUSBBufferToRead ) {
  RTDACUSBBufferToRead->LogicVersion = ((int)(BinaryBufferToRead[1]) <<  8) +
	                                  ((int)(BinaryBufferToRead[0]) );  
  RTDACUSBBufferToRead->ApplicationName[5] = '\0';
  RTDACUSBBufferToRead->ApplicationName[4] = (char)(BinaryBufferToRead[3]);
  RTDACUSBBufferToRead->ApplicationName[3] = (char)(BinaryBufferToRead[4]);
  RTDACUSBBufferToRead->ApplicationName[2] = (char)(BinaryBufferToRead[5]);
  RTDACUSBBufferToRead->ApplicationName[1] = (char)(BinaryBufferToRead[6]);
  RTDACUSBBufferToRead->ApplicationName[0] = (char)(BinaryBufferToRead[7]);

  RTDACUSBBufferToRead->CN1PinMode = BinaryBufferToRead[8] & 0x03;

  RTDACUSBBufferToRead->CN1Direction =  (int)(BinaryBufferToRead[9]) |
	                                  (((int)(BinaryBufferToRead[10])) <<  8) |
	                                  (((int)(BinaryBufferToRead[11])) << 16) |
	                                  (((int)(BinaryBufferToRead[12])) << 24);
  RTDACUSBBufferToRead->CN1Output    =  (int)(BinaryBufferToRead[13]) |
	                                  (((int)(BinaryBufferToRead[14])) <<  8) |
	                                  (((int)(BinaryBufferToRead[15])) << 16) |
	                                  (((int)(BinaryBufferToRead[16])) << 24);
  RTDACUSBBufferToRead->CN1Input     =  (int)(BinaryBufferToRead[17]) |
	                                  (((int)(BinaryBufferToRead[18])) <<  8) |
	                                  (((int)(BinaryBufferToRead[19])) << 16) |
	                                  (((int)(BinaryBufferToRead[20])) << 24);

  RTDACUSBBufferToRead->PWM[0].Prescaler = (int)(BinaryBufferToRead[21]) +
	                                    (((int)(BinaryBufferToRead[22])) << 8);
  RTDACUSBBufferToRead->PWM[0].Mode  = (int)(BinaryBufferToRead[23]);
  RTDACUSBBufferToRead->PWM[0].Width = (int)(BinaryBufferToRead[24]) +
	                                (((int)(BinaryBufferToRead[25])) << 8);
  RTDACUSBBufferToRead->PWM[1].Prescaler = (int)(BinaryBufferToRead[26]) +
	                                    (((int)(BinaryBufferToRead[27])) << 8);
  RTDACUSBBufferToRead->PWM[1].Mode  = (int)(BinaryBufferToRead[28]);
  RTDACUSBBufferToRead->PWM[1].Width = (int)(BinaryBufferToRead[29]) +
	                                (((int)(BinaryBufferToRead[30])) << 8);

  RTDACUSBBufferToRead->Encoder[ 0].Reset = (BinaryBufferToRead[31] >> 0) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 1].Reset = (BinaryBufferToRead[31] >> 1) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 2].Reset = (BinaryBufferToRead[31] >> 2) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 3].Reset = (BinaryBufferToRead[31] >> 3) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 4].Reset = (BinaryBufferToRead[31] >> 4) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 5].Reset = (BinaryBufferToRead[31] >> 5) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 6].Reset = (BinaryBufferToRead[31] >> 6) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 7].Reset = (BinaryBufferToRead[31] >> 7) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 8].Reset = (BinaryBufferToRead[32] >> 0) & 0x01;
  RTDACUSBBufferToRead->Encoder[ 9].Reset = (BinaryBufferToRead[32] >> 1) & 0x01;
  RTDACUSBBufferToRead->Encoder[10].Reset = (BinaryBufferToRead[32] >> 2) & 0x01;
  RTDACUSBBufferToRead->Encoder[11].Reset = (BinaryBufferToRead[32] >> 3) & 0x01;

  RTDACUSBBufferToRead->Encoder[ 0].Counter =  (int)(BinaryBufferToRead[33]) |
	                                         (((int)(BinaryBufferToRead[34])) <<  8) |
	                                         (((int)(BinaryBufferToRead[35])) << 16) |
	                                         (((int)(BinaryBufferToRead[36])) << 24);
  RTDACUSBBufferToRead->Encoder[ 1].Counter =  (int)(BinaryBufferToRead[37]) |
	                                         (((int)(BinaryBufferToRead[38])) <<  8) |
	                                         (((int)(BinaryBufferToRead[39])) << 16) |
	                                         (((int)(BinaryBufferToRead[40])) << 24);
  RTDACUSBBufferToRead->Encoder[ 2].Counter =  (int)(BinaryBufferToRead[41]) |
	                                         (((int)(BinaryBufferToRead[42])) <<  8) |
	                                         (((int)(BinaryBufferToRead[43])) << 16) |
	                                         (((int)(BinaryBufferToRead[44])) << 24);
  RTDACUSBBufferToRead->Encoder[ 3].Counter =  (int)(BinaryBufferToRead[45]) |
	                                         (((int)(BinaryBufferToRead[46])) <<  8) |
	                                         (((int)(BinaryBufferToRead[47])) << 16) |
	                                         (((int)(BinaryBufferToRead[48])) << 24);
  RTDACUSBBufferToRead->Encoder[ 4].Counter =  (int)(BinaryBufferToRead[49]) |
	                                         (((int)(BinaryBufferToRead[50])) <<  8) |
	                                         (((int)(BinaryBufferToRead[51])) << 16) |
	                                         (((int)(BinaryBufferToRead[52])) << 24);
  RTDACUSBBufferToRead->Encoder[ 5].Counter =  (int)(BinaryBufferToRead[53]) |
	                                         (((int)(BinaryBufferToRead[54])) <<  8) |
	                                         (((int)(BinaryBufferToRead[55])) << 16) |
	                                         (((int)(BinaryBufferToRead[56])) << 24);
  RTDACUSBBufferToRead->Encoder[ 6].Counter =  (int)(BinaryBufferToRead[57]) |
	                                         (((int)(BinaryBufferToRead[58])) <<  8) |
	                                         (((int)(BinaryBufferToRead[59])) << 16) |
	                                         (((int)(BinaryBufferToRead[60])) << 24);
  RTDACUSBBufferToRead->Encoder[ 7].Counter =  (int)(BinaryBufferToRead[61]) |
	                                         (((int)(BinaryBufferToRead[62])) <<  8) |
	                                         (((int)(BinaryBufferToRead[63])) << 16) |
	                                         (((int)(BinaryBufferToRead[64])) << 24);
  RTDACUSBBufferToRead->Encoder[ 8].Counter =  (int)(BinaryBufferToRead[65]) |
	                                         (((int)(BinaryBufferToRead[66])) <<  8) |
	                                         (((int)(BinaryBufferToRead[67])) << 16) |
	                                         (((int)(BinaryBufferToRead[68])) << 24);
  RTDACUSBBufferToRead->Encoder[ 9].Counter =  (int)(BinaryBufferToRead[69]) |
	                                         (((int)(BinaryBufferToRead[70])) <<  8) |
	                                         (((int)(BinaryBufferToRead[71])) << 16) |
	                                         (((int)(BinaryBufferToRead[72])) << 24);
  RTDACUSBBufferToRead->Encoder[10].Counter =  (int)(BinaryBufferToRead[73]) |
	                                         (((int)(BinaryBufferToRead[74])) <<  8) |
	                                         (((int)(BinaryBufferToRead[75])) << 16) |
	                                         (((int)(BinaryBufferToRead[76])) << 24);
  RTDACUSBBufferToRead->Encoder[11].Counter =  (int)(BinaryBufferToRead[77]) |
	                                         (((int)(BinaryBufferToRead[78])) <<  8) |
	                                         (((int)(BinaryBufferToRead[79])) << 16) |
	                                         (((int)(BinaryBufferToRead[80])) << 24);

  RTDACUSBBufferToRead->AD[ 0].Gain =  (int)(BinaryBufferToRead[ 93]) & 0x07;
  RTDACUSBBufferToRead->AD[ 1].Gain = ((int)(BinaryBufferToRead[ 93]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 2].Gain =  (int)(BinaryBufferToRead[ 94]) & 0x07;
  RTDACUSBBufferToRead->AD[ 3].Gain = ((int)(BinaryBufferToRead[ 94]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 4].Gain =  (int)(BinaryBufferToRead[ 95]) & 0x07;
  RTDACUSBBufferToRead->AD[ 5].Gain = ((int)(BinaryBufferToRead[ 95]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 6].Gain =  (int)(BinaryBufferToRead[ 96]) & 0x07;
  RTDACUSBBufferToRead->AD[ 7].Gain = ((int)(BinaryBufferToRead[ 96]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 8].Gain =  (int)(BinaryBufferToRead[ 97]) & 0x07;
  RTDACUSBBufferToRead->AD[ 9].Gain = ((int)(BinaryBufferToRead[ 97]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[10].Gain =  (int)(BinaryBufferToRead[ 98]) & 0x07;
  RTDACUSBBufferToRead->AD[11].Gain = ((int)(BinaryBufferToRead[ 98]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[12].Gain =  (int)(BinaryBufferToRead[ 99]) & 0x07;
  RTDACUSBBufferToRead->AD[13].Gain = ((int)(BinaryBufferToRead[ 99]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[14].Gain =  (int)(BinaryBufferToRead[100]) & 0x07;
  RTDACUSBBufferToRead->AD[15].Gain = ((int)(BinaryBufferToRead[100]) >> 4) & 0x07;
  RTDACUSBBufferToRead->AD[ 0].Result =    (int)(BinaryBufferToRead[101]) |
	                                     (((int)(BinaryBufferToRead[102])) <<  8);
  RTDACUSBBufferToRead->AD[ 1].Result =    (int)(BinaryBufferToRead[103]) |
	                                     (((int)(BinaryBufferToRead[104])) <<  8);
  RTDACUSBBufferToRead->AD[ 2].Result =    (int)(BinaryBufferToRead[105]) |
	                                     (((int)(BinaryBufferToRead[106])) <<  8);
  RTDACUSBBufferToRead->AD[ 3].Result =    (int)(BinaryBufferToRead[107]) |
	                                     (((int)(BinaryBufferToRead[108])) <<  8);
  RTDACUSBBufferToRead->AD[ 4].Result =    (int)(BinaryBufferToRead[109]) |
	                                     (((int)(BinaryBufferToRead[110])) <<  8);
  RTDACUSBBufferToRead->AD[ 5].Result =    (int)(BinaryBufferToRead[111]) |
	                                     (((int)(BinaryBufferToRead[112])) <<  8);
  RTDACUSBBufferToRead->AD[ 6].Result =    (int)(BinaryBufferToRead[113]) |
	                                     (((int)(BinaryBufferToRead[114])) <<  8);
  RTDACUSBBufferToRead->AD[ 7].Result =    (int)(BinaryBufferToRead[115]) |
	                                     (((int)(BinaryBufferToRead[116])) <<  8);
  RTDACUSBBufferToRead->AD[ 8].Result =    (int)(BinaryBufferToRead[117]) |
	                                     (((int)(BinaryBufferToRead[118])) <<  8);
  RTDACUSBBufferToRead->AD[ 9].Result =    (int)(BinaryBufferToRead[119]) |
	                                     (((int)(BinaryBufferToRead[120])) <<  8);
  RTDACUSBBufferToRead->AD[10].Result =    (int)(BinaryBufferToRead[121]) |
	                                     (((int)(BinaryBufferToRead[122])) <<  8);
  RTDACUSBBufferToRead->AD[11].Result =    (int)(BinaryBufferToRead[123]) |
	                                     (((int)(BinaryBufferToRead[124])) <<  8);
  RTDACUSBBufferToRead->AD[12].Result =    (int)(BinaryBufferToRead[125]) |
	                                     (((int)(BinaryBufferToRead[126])) <<  8);
  RTDACUSBBufferToRead->AD[13].Result =    (int)(BinaryBufferToRead[127]) |
	                                     (((int)(BinaryBufferToRead[128])) <<  8);
  RTDACUSBBufferToRead->AD[14].Result =    (int)(BinaryBufferToRead[129]) |
	                                     (((int)(BinaryBufferToRead[130])) <<  8);
  RTDACUSBBufferToRead->AD[15].Result =    (int)(BinaryBufferToRead[131]) |
	                                     (((int)(BinaryBufferToRead[132])) <<  8);

  RTDACUSBBufferToRead->DA[0] =   (int)(BinaryBufferToRead[133]) |
	                            (((int)(BinaryBufferToRead[134])) <<  8);
  RTDACUSBBufferToRead->DA[1] =   (int)(BinaryBufferToRead[135]) |
	                            (((int)(BinaryBufferToRead[136])) <<  8);
  RTDACUSBBufferToRead->DA[2] =   (int)(BinaryBufferToRead[137]) |
	                            (((int)(BinaryBufferToRead[138])) <<  8);
  RTDACUSBBufferToRead->DA[3] =   (int)(BinaryBufferToRead[139]) |
	                            (((int)(BinaryBufferToRead[140])) <<  8);
}

int CommandSend_0112( RTDACUSBBufferType *RTDACUSBBufferToSend ) {
  int i;
  unsigned char AuxBuffer[ 512 ];
  CreateBinaryBufferToSend_0112( RTDACUSBBufferToSend );
  AuxBuffer[0] = COMMAND_SEND;
  for( i=0; i<=150; i++ )
    AuxBuffer[i+1] = BinaryBufferToSend[i] & 0x7F;
  return Send( 150, AuxBuffer ); 
}

int CommandRead_0112( RTDACUSBBufferType *RTDACUSBBufferToRead ) {
  int RecQueue, SendQueue, EventStatus;
  unsigned char AuxBuffer[ 5 ];
  static unsigned char AuxReciveBuff[ 67000 ];
  AuxBuffer[0] = COMMAND_READ;
  Send( 1, AuxBuffer );        // Send the command
  if( LastErrorCode != FT_OK )
    return( -5 );

  LastErrorCode = Receive( 150, BinaryBufferToRead );
  GetStatus( &RecQueue, &SendQueue, &EventStatus );
  if( RecQueue > 0 )
    LastErrorCode = Receive( RecQueue, AuxReciveBuff );
  UnpackBinaryBuffer_0112( RTDACUSBBufferToRead );
  return LastErrorCode;
}

///////////////////////////////////////////////////////////
//
// General USB I/O functions
//
int Receive( int NoOfBytes, unsigned char ToRead[] ) {
  DWORD BytesReceived;
  LastErrorCode = FT_Read( ftHandle, ToRead, NoOfBytes, &BytesReceived );
  return LastErrorCode;
}

int Send( int NoOfBytes, unsigned char ToSend[] ) {
  DWORD Written;
  LastErrorCode = FT_Write( ftHandle, (LPVOID)ToSend, NoOfBytes, &Written );
  return LastErrorCode;
}


int USBOpen( void ) {
  int RecQueue, SendQueue, EventStatus;
  if( USBCounter <= 0 ) {
	LastErrorCode = FT_Open( 0, &ftHandle );
	if( LastErrorCode != FT_OK ) 
	  return( -1 );
	LastErrorCode = FT_ResetDevice( ftHandle );
	if( LastErrorCode != FT_OK )
	  return( -2 );
	LastErrorCode = FT_SetLatencyTimer( ftHandle, 1 );
	if( LastErrorCode != FT_OK )
	  return( -3 );
	LastErrorCode = FT_SetUSBParameters( ftHandle, 0, 0 );
	if( LastErrorCode != FT_OK )
	  return( -4 );
	// Set event char to 0x3F, enable event char, disable error char
	LastErrorCode = FT_SetChars( ftHandle, 0x3F, 1, 0, 0 );
	if( LastErrorCode != FT_OK )
	  return( -5 );
    USBCounter = 1;
	// Switch from JTAG programming mode into operation mode
    CommandDummy( );
	// Flush receive queue
    GetStatus( &RecQueue, &SendQueue, &EventStatus );
	if( LastErrorCode != FT_OK )
	  return( -6 );
	else {
	  unsigned char *RxBuffer;
	  if( (RxBuffer = (unsigned char *)malloc(66000)) != NULL ) {
	    ReadReceiveQueue( RecQueue, RxBuffer );
	    free( RxBuffer );
	  }
	}
  } 
  else 
    USBCounter++;
  return USBCounter;
}

int USBClose( void ) {
  if( USBCounter <= 0 )
    USBCounter = 0;
  else {
    USBCounter--;
	if( USBCounter == 0 ) {
	LastErrorCode = FT_Close( ftHandle );
	if( LastErrorCode != FT_OK )
	  return( -1 );
	}
  }
  return USBCounter;
}

int USBLastError( char *Dsrp ) {
  if( Dsrp != NULL ) {
    switch( LastErrorCode ) {
      case FT_OK:                          strcpy( Dsrp, "FT_OK" );                          break;
      case FT_INVALID_HANDLE:              strcpy( Dsrp, "FT_INVALID_HANDLE" );              break;
      case FT_DEVICE_NOT_FOUND:            strcpy( Dsrp, "FT_DEVICE_NOT_FOUND" );            break;
      case FT_DEVICE_NOT_OPENED:           strcpy( Dsrp, "FT_DEVICE_NOT_OPENED" );           break;
      case FT_IO_ERROR:                    strcpy( Dsrp, "FT_IO_ERROR" );                    break;
      case FT_INSUFFICIENT_RESOURCES:      strcpy( Dsrp, "FT_INSUFFICIENT_RESOURCES" );      break;
      case FT_INVALID_PARAMETER:           strcpy( Dsrp, "FT_INVALID_PARAMETER" );           break;
      case FT_INVALID_BAUD_RATE:           strcpy( Dsrp, "FT_INVALID_BAUD_RATE" );           break;
      case FT_DEVICE_NOT_OPENED_FOR_ERASE: strcpy( Dsrp, "FT_DEVICE_NOT_OPENED_FOR_ERASE" ); break;
      case FT_DEVICE_NOT_OPENED_FOR_WRITE: strcpy( Dsrp, "FT_DEVICE_NOT_OPENED_FOR_WRITE" ); break;
      case FT_FAILED_TO_WRITE_DEVICE:      strcpy( Dsrp, "FT_FAILED_TO_WRITE_DEVICE" );      break;
      case FT_EEPROM_READ_FAILED:          strcpy( Dsrp, "FT_EEPROM_READ_FAILED" );          break;
      case FT_EEPROM_WRITE_FAILED:         strcpy( Dsrp, "FT_EEPROM_WRITE_FAILED" );         break;
      case FT_EEPROM_ERASE_FAILED:         strcpy( Dsrp, "FT_EEPROM_ERASE_FAILED" );         break;
      case FT_EEPROM_NOT_PRESENT:          strcpy( Dsrp, "FT_EEPROM_NOT_PRESENT" );          break;
      case FT_EEPROM_NOT_PROGRAMMED:       strcpy( Dsrp, "FT_EEPROM_NOT_PROGRAMMED" );       break;
      case FT_INVALID_ARGS:                strcpy( Dsrp, "FT_INVALID_ARGS" );                break;
      case FT_NOT_SUPPORTED:               strcpy( Dsrp, "FT_NOT_SUPPORTED" );               break;
      case FT_OTHER_ERROR:                 strcpy( Dsrp, "FT_OTHER_ERROR" );                 break;

      default :                            strcpy( Dsrp, "FT_UNKNOWN_ERROR" );               break;
	}
  }
  return( LastErrorCode );
}


int SetTimeouts( int RecTimeout, int SendTimeout ) {
  LastErrorCode = FT_SetTimeouts( ftHandle, (DWORD)RecTimeout, (DWORD)SendTimeout );
  return( LastErrorCode );
}

int FlushReceiveQueue( void ) {
  FT_Purge( ftHandle, FT_PURGE_RX );
  return( LastErrorCode );
}

int FlushSendQueue( void ) {
  FT_Purge( ftHandle, FT_PURGE_TX );
  return( LastErrorCode );
}

int ReadReceiveQueue( int NoOfBytes, unsigned char Buff[] ) {
  int RecQueue, SendQueue, EventStatus;
  GetStatus( &RecQueue, &SendQueue, &EventStatus );
  Receive( min(NoOfBytes, RecQueue), Buff );
  return( LastErrorCode );
}

int GetStatus( int *RecQueue, int *SendQueue, int *EventStatus ) {
  DWORD RQ, TQ, ES;
  LastErrorCode = FT_GetStatus( ftHandle, &RQ, &TQ, &ES );
  *RecQueue    = (int)RQ;
  *SendQueue   = (int)TQ;
  *EventStatus = (int)ES;
  return( LastErrorCode );
}

