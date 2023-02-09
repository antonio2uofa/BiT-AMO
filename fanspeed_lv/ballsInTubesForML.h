#include "extcode.h"
#pragma pack(push)
#pragma pack(1)

#ifdef __cplusplus
extern "C" {
#endif

/*!
 * BallsUsbIniDll
 */
int32_t __cdecl BallsUsbIniDll(void);
/*!
 * Balls_usb_open
 */
int32_t __cdecl Balls_usb_open(void);
/*!
 * Balls_usb_close
 */
int32_t __cdecl Balls_usb_close(void);
/*!
 * BallsDelayForMLDll
 */
void __cdecl BallsDelayForMLDll(uint32_t millisecondsToWait);
/*!
 * BallsOutputFanSpeedDll
 */
void __cdecl BallsOutputFanSpeedDll(float FANSPEED, int16_t TUBE);
/*!
 * BallsReadLevel_1Dll
 */
int32_t __cdecl BallsReadLevel_1Dll(int32_t *Ecode, uint32_t *SHOTTIME, 
	int16_t *TimeOut);
/*!
 * BallsReadLevel_2Dll
 */
int32_t __cdecl BallsReadLevel_2Dll(int32_t *Ecode, uint32_t *SHOTTIME, 
	int16_t *Timeout);
/*!
 * BallsReadLevel_3Dll
 */
void __cdecl BallsReadLevel_3Dll(int32_t *Ecode, uint32_t *SHOTTIME, 
	int16_t *Timeout);
/*!
 * BallsReadLevel_4Dll
 */
int32_t __cdecl BallsReadLevel_4Dll(int32_t *Ecode, uint32_t *SHOTTIME, 
	int16_t *Timeout);
/*!
 * BallsReadFanSpeedDll
 */
void __cdecl BallsReadFanSpeedDll(uint16_t FanSpeeds[], int32_t len);

MgErr __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

#ifdef __cplusplus
} // extern "C"
#endif

#pragma pack(pop)

