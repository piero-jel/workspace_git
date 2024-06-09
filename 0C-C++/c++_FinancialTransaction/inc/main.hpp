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
* \brief Financial Transaction.
* \details Financial Transaction se basa en un software que simule una transaccion financiera.
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

#include <Exception.hpp>
#include <RangesRegister.hpp>
#include <CardsRegister.hpp>

#include <iostream>
#include <format>
#include <forward_list>
#include <algorithm>
#include <string>
#include <sstream>
#include <memory>
#include <iomanip>  /* std::setfill, std::setw */

//#include <bits/stdc++.h>
#include <vector>
#include <list>
#include <set>
#include <tuple>
/* header c */

#include <cstdlib>

#include <unistd.h> 
/* getopt();
 * extern char *optarg; 
 * extern int optind, opterr, optopt; 
 */
                      
#include <libgen.h> 
/* 
  + char *dirname(char *path);
  + char *basename(char *path);
*/                      





/**
 * @brief Objeto para el manejo de las opciones
 * ingresada por linea de comando 'CLI'
 * 
 */
struct CliApp {
  enum Flag:uint8_t {
      IP      = 0x01
    , PORT    = 0x02
    , TIMEOUT = 0x04
    , FRANGE  = 0x08
    , FCARDS  = 0x10   
    , ALL     = 0x1F
    , NONE    = 0x00
  };
  /* BEGIN attributes */
  std::string app{};    /**<@brief apliction name */
  std::string ip{};     /**<@brief -i ip server */
  uint16_t port{};      /**<@brief -p port server, para almacenar el numero de puerto */
  uint32_t timeout{};   /**<@brief -t timeout receive */
  std::string frange{}; /**<@brief -r path/file range */
  std::string fcards{}; /**<@brief -c path/file cards */
  /* END   attributes */
  
  /* BEGIN methods */
  /**
   * @brief Construct a new Cli App object
   * @param[in] argc opcional numero de arguements
   * @param[in] argv opcional array de arguements
   * @param[in,out] ou opcional, FILE stream para el print
   * de info en caso de ser necesario. Por defecto es stdout.
   */
  CliApp(int argc=0,char* argv[]=nullptr,FILE* ou= stdout);

  /**
   * @brief Este metodo realiza el parsin e inicializa
   * todas las opciones de linea de comando de la aplicacion
   * @param[in] argc numero de arguements
   * @param[in] argv array de arguements
   * @param[in,out] ou opcional, FILE stream para el print
   * de info en caso de ser necesario. Por defecto es stdout.
   */
  void parser(int argc,char** argv,FILE* ou= stdout);

  /**
   * @brief Para el print del help
   * @param[in,out] ou opcional, FILE stream para el print
   * de info en caso de ser necesario. Por defecto es stdout.
   */
  void help(FILE* ou= stdout);

  /**
   * @brief Metodo para establecer el estado de un flag,
   * de esta forma podemos chequear que parametros se pasaron
   * y cuales nos. 
   * @param[in] flag a establecer \p Flags
   * @param[in] st estado para el flag
   */
  void flags(Flag flag,bool st);

  /**
   * @brief Metodo para obtener el estado de un flag o un grupo de flags
   * @param flag que se desea consultar \p Flags
   * @return true se paso el argumentos relacionado
   * @return false No se paso.
   */
  bool flags(Flag flag);
  /* END   methods */

  /**
   * @brief metodo para depuracion
   * @param[in,out] ou opcional, FILE stream para el print
   * de info en caso de ser necesario. Por defecto es stdout.
   */
  void print(FILE* ou=stdout);


  private:
    uint8_t __flag{};
};


/**
 * @brief este template nos permite leer desde un \p std::iftream (un archivo)
 * y realizar el parsing para llenar un contenedor.
 * El tipo \p C::value_type debe contener un constructor
 * que admite un buffer " \p char* " el cual tiene la linea para construir el
 * el elemento.
 *
 * @tparam C tipo de contenedor
 * @tparam LEN \b Opcional, parameto para establecer la longitud del buffer
 * de lectura del archivo. Valor por defecto \p LEN \b 1024
 *
 * @param[in] src pathname del archivo que se lee.
 * @param[out] container contenedo que se llenara, debe poseer el metodo
 * \p push_back() "Podemos definir un insert, pero para este debemos considerar
 * el orden del mismo, por defecto al inicio del contenedor"
 * @param[in] comm Opcional, caracter de comentario para poder descartar
 * una linea leida desde el archivo.
 \code
  // definimos un alias para el tipo de contendor a usar
  using CType = std::vector<Register>;
  // definimos el vector
  CType vct1;
  // check y si es success llamamamos al template
  if(argc > 1)
  {
    if(!ReadAndFillContainer<CType,2048>(argv[1],vct1))
    {
      //report error...
      std::cerr<<"error to process file<"<<argv[1]
               <<"> for fill container."<<std::endl
    }
  }
 \endcode
 */
template <typename C,int LEN=1024>
void ReadAndFillContainer(const std::string& pathname , C& container, char comm='#');


/**
 * @brief metodo para la verificacion del card number
 * 
 * @param[in] card_number numero de tarjeta
 * @param[in] frange path/file-rango
 * @param[in] fcards path/file-cards
 * @return std::tuple<bool,RangesRegister,CardsRegister>
 *  + bool true succes , false not found
 *  + RangesRegister localcizado (si bool es true de lo contrario empty)
 *  + CardsRegister localizado (si bool es true de lo contrario empty)
 */
std::tuple<bool,RangesRegister,CardsRegister>
  VerifyCardNumber(std::string card_number
                  ,std::string frange
                  ,std::string fcards);
/**
 * @brief Get the Card Number object
 * @param[in] msg mensage para la peticion
 * @param lmin longitud minima
 * @param lmax longitud maxima
 * @return std::string con el Numuro de tarjeta
 */
std::string GetCardNumber ( const std::string& msg
                          , uint8_t lmin = 13
                          , uint8_t lmax = 99
                          );

/**
 * @brief Get the Card Code object
 * @param[in] msg mensage para la peticion
 * @return std::string con el card code
 */
std::string GetCardCode(const std::string& msg,uint8_t len = 3);

/**
 * @brief Get the Amount object
 * 
 * @tparam N tipo de valor para el Amount, pode defecto int 32
 * @param[in] msg mensaje
 * @param len longitud maxima
 * @return N valor de amount ingresado
 */
template<typename N=int64_t>
N GetAmount(const std::string& msg,uint8_t len=12);

/**
 * @brief Get the Request object
 * @tparam N template type for amount, default int64_t
 * @param[in] sld saldo
 * @param[in] ncard numero de tarjeta
 * @param[in] ccard codigo de tarjeta
 * @return std::string con el request armado
 */
template<typename N=int64_t>
std::string GetRequest( N sld
                      , const std::string& ncard
                      , const std::string& ccard
                      );

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
