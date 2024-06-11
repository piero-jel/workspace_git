/** ******************************************************************************************************//**
* \addtogroup Exception
* @{
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
* \file Exception.hpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief Manejo de Exception
* \details Para el manejo de Exception de la misma forma que un print con formato

* \version 0.0.1.
* \date Viernes 7 de Junio de 2024.
* \pre pre, condiciones que deben cuplirse antes del llamado,
* \bug bug, depuracion example: Not all memory is freed when deleting an object
* of this class.
* \warning
* \note
* \par \b Change History:
* Author         Date                 Version     Brief
* JEL            2024.05.07          0.0.1       Version Inicial no release
*
* @} doxygen end group definition
* ********************************************************************************************************* */

#ifndef __Exception_hpp__
#define __Exception_hpp__ /**<@brief Definimos el Nombre del modulo */



/*
 * ======================[ BEGIN include header file ]=================================
 */
#include <cstdint>
#include <cstdarg>
#include <cstring>





/*
 * ======================[ END   include header file ]=================================
 */


/*
 * ========================[ BEGIN class interfaces ]==================================
 */
/**
* \class Exception
* \brief Clase para la notificacion de Exceptiones
*     
* Consturctores disponibles:    
*  \li \b Exception (const char* fmt, ...);     
*  \li \b Exception (const Exception& e); 
* 
*/
template <uint32_t LEN = 256>
class Exception : public std::exception
{
  static constexpr uint32_t _BUFF_LEN = LEN;   /**<@brief Longitud del buffer donde almacenarmeos el mensaje. */
  char _buff[LEN];                 /**<@brief buffer que almacenara el mensaje. */ 

  virtual void set(const Exception& e) noexcept
  {
    if(this == &e)
      return;  
    std::memcpy(this->_buff,e._buff,LEN);
  }

  virtual void set(const char* fmt,va_list args) noexcept
  {
    std::vsnprintf( this->_buff,LEN-1, fmt, args );
    /* cerramos la lista de argumentos */
    va_end( args );
  }

  public:
    /**
     * @brief Construct a new Exception object
     * @param[in] fmt CStyle string con el formato del print
     * @param ... : listado variadic de parametros relacionados a \p fmt
     */
    Exception(const char* fmt,...) noexcept
    {
      if(!fmt)
        return ;

      va_list args;
      va_start(args, fmt );
      this->set(fmt,args);  
    }

    /**
    * \brief constructor por copia
    * \param e : objeto a copiar
    * \return nothing
    * \note
    * \code
    * \endcode
    */
    Exception(const Exception& e) noexcept
    {
      this->set(e);
    }

    /**
    * \brief sobrecarga del operador de asignacion \b =
    * \param e : objeto a copiar.
    * \return La referenica del objeto copiado.
    * \note
    * \code
    * \endcode
    */
    Exception& operator= (const Exception& e)noexcept
    {
      this->set(e);
      return *this;
    }

    /**
    * \brief destructor
    * \return nothing
    * \note si no definimos esta y solo la declaramos vamos a tener
    * error a la hora de compilar.
    * <b> undefined reference to `vtable for Exception'</b>
    * \code
    * \endcode
    */
    virtual ~Exception()
    { }

    /**
    * \brief funcion miembro virtual, la cual obtiene
    * el mensaje de error para que se pueda imprimir
    * o escribir en un log
    * \return mensaje de error String Style-C
    *  \li \b const char*
    * \note
    * \code
    * //.. captura
    * catch(const Exception<>& e)
    * {
    *   std::cout<<"catch(const Exception& e):      "<<e.what();
    * }
    * \endcode
    */
    virtual const char* what(void) const noexcept
    { return (const char*) this->_buff; }     
};


#if ( IS_SAME >= 2017 )
  #ifdef NDEBUG
    #define EXCEPTION(Fmt, arg...)\
      Exception ( "[%s:%s():%ld] " Fmt\
                , __FILE__,__func__,(long int)__LINE__\
                , ##arg)
  #else
    #define EXCEPTION(Fmt, arg...) Exception(Fmt, ##arg)
  #endif
#else
  #ifdef NDEBUG
    #define EXCEPTION(Fmt, arg...)\
      Exception<> ( "[%s:%s():%ld] " Fmt\
                , __FILE__,__func__,(long int)__LINE__\
                , ##arg)
  #else
    #define EXCEPTION(Fmt, arg...) Exception<>(Fmt, ##arg)
  #endif
#endif

/*
 * ========================[ END   class interfaces ]==================================
 */
#endif /* #ifndef __Exception_hpp__ */
