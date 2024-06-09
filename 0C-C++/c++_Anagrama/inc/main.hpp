/** ******************************************************************************************************//**
* \addtogroup main
* @{ }// delete this
* \copyright
* Copyright 2024, Jesus Emanuel Luccioni
* All rights reserved.
* 
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
* 
*  1. Redistributions of source code must retain the above copyright notice,
*     this list of conditions and the following disclaimer.
* 
*  2. Redistributions in binary form must reproduce the above copyright notice,
*     this list of conditions and the following disclaimer in the documentation
*     and/or other materials provided with the distribution.
* 
*  3. Neither the name of the copyright holder nor the names of its
*     contributors may be used to endorse or promote products derived from this
*     software without specific prior written permission.
* 
* THIS SOURCE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
* ARISING IN ANY WAY OUT OF THE USE OF THIS SOURCE, EVEN IF ADVISED OF THE
* POSSIBILITY OF SUCH DAMAGE.
*
* \file main.hpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief Verificacion de palabras, \b Anagrama.
* \details Una palabra es \b Anagrama de otra si las dos tienen las mismas letras, con el mismo número de apariciones,
* pero en un orden diferente.
*
* \version 0.0.1.
* \date Sabado 8 de Junio de 2024.
* \pre pre, condiciones que deben cuplirse antes del llamado,
* \bug bug, depuracion example: Not all memory is freed when deleting an object
* of this class.
* \warning
* \note
* \par \b Change History:
* Author         Date                 Version     Brief
* JEL            2024.05.06           0.0.1       Version Inicial no release
*
* @} doxygen end group definition
* ********************************************************************************************************* */
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
