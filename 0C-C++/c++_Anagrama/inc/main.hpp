#ifndef __main_hpp__
#define __main_hpp__

//#include <thread>

// BEGIN PERROR
/** En caso de necesitar deshabilitar las api strerrorname_np() y  strerrordesc_np() 
 * debemos descomentar las siguentes lineas: */
/* FIXME
#ifdef _GNU_SOURCE 
  #undef _GNU_SOURCE   
#endif 
*/
#include <cstdio>     /* for printf */
#include <cstdlib>    /* for exit */
#include <iostream>
#include <cstring>

#ifdef _GNU_SOURCE 
  #define mstrerrorname_np(Errno) strerrorname_np(Errno)
  #define mstrerrordesc_np(Errno) strerrordesc_np(Errno)
  #define mbasename(Argv0) basename(Argv0)
#else
  #ifndef mstrerrorname_np
    static inline char* fn_mstrerrorname_np(int errnum)
    {
      static char rval[32];
      snprintf(rval, sizeof(rval)-1,"N%04d",errnum);
      return rval;
    }
    #define mstrerrorname_np(Errno) fn_mstrerrorname_np(Errno)
  #endif
  #ifndef mstrerrordesc_np
    #define mstrerrordesc_np(Errno) strerror(Errno)
  #endif
  #ifndef mbasename
    static inline const char* fn_basename(const char* arg0)
    {
      const char *cp = std::strrchr(arg0, '/');
      return (cp ? cp+1 : arg0);
    }
    #define mbasename(Argv0) fn_basename(Argv0)
  #endif

#endif


#if (VERSION == 0)

#elif (VERSION == 1)

#elif (VERSION == 3)

#elif (VERSION == 4)

#elif (VERSION == 5)

#elif (VERSION == 6)

#elif (VERSION == 7)

#elif (VERSION == 8)

#elif (VERSION == 9)

#elif (VERSION == 10)

#else 

#endif
  



#endif /*#ifndef __main_hpp__ */
