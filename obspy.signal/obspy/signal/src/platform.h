#ifndef PLATFORM_H
#define PLATFORM_H 1

#ifdef __cplusplus
extern "C" {
#endif
  
#if defined(__linux__) || defined(__linux)
  #include <values.h>
  #include <malloc.h>
  void rffti(int n, double* wsave);            // fftpack init function
  void rfftf(int n, double* r, double* wsave); // fftpack r fwd
#elif defined(__APPLE__) || defined(__FreeBSD__) || defined(__OpenBSD__) || defined(__NetBSD__)
  #include <limits.h>
  #include <sys/malloc.h>
#elif defined(_WIN32) || defined(_WIN64)
  // Windows 32 & 64
  #include <limits.h>
  #include <malloc.h>
#else
  #include <limits.h>
  #include <malloc.h>
#endif


#ifndef M_PI
  #define M_PI 3.14159265
#endif


#ifdef __cplusplus
}
#endif
 
#endif
