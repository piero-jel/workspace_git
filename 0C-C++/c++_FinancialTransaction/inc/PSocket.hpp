/** ******************************************************************************************************//**
* \addtogroup PSocket
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
* \file PSocket.hpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief Posix Socket Stream Implementation.
* \details Posix Socket Stream Implementation.
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
* JEL            2024.05.08          0.0.1       Version Inicial no release
*
* @} doxygen end group definition
* ********************************************************************************************************* */

#ifndef __PSocket_hpp__
#define __PSocket_hpp__ /**<@brief Definimos el Nombre del modulo */



/*
 * ======================[ BEGIN include header file ]=================================
 */
#include <cstdint>
#include <string>

/*
 * ======================[ END   include header file ]=================================
 */

/*
 * ========================[ BEGIN class interfaces ]==================================
 */
namespace PSocket {

  struct Byteint 
  {  
    union {
      char b[4];
      uint32_t ui;
    } _byteint;

    uint8_t _len{};
    
    /**
    * @brief Construct a new Byteint object
    * 
    * @param[in] l bytes
    */
    Byteint(uint8_t l=4);
    

    /**
    * @brief metodos asociados al calculo de la longitud a colocaren el header
    * para el envio
    * 
    * @param[in] num longitud del mensaje
    * @param[in,out] buf buffer donde se coloca los bytes de header
    * @return char* 
    */
    char* number2binary(uint32_t num);
    
    /**
    * @brief metodos asociados al calculo de la longitud proveniente en el header
    * para la recepccion
    * 
    * @param[in] byte bytes recibido desde el header
    * @return uint32_t 
    */
    uint32_t binary2number(char* byte); 
  };


  /**
  * @brief enumeracion para la definicion del formato
  */
  enum FmtLen : uint8_t {
      FMTNONE = 0x00 /**<@brief sin formato para longitud */
    , FMT2B   = 0x02 /**<@brief formato de la longitud en 2 bytes SHORT */
    , FMT4B   = 0x04 /**<@brief formato de la longitud en 4 bytes LONG */
  };

  /**
  * @brief definicion de la Clase Base Abstracta  \b StreamSocket
  * 
  */
  class Stream {
    protected:
      using addrinfo_t = struct addrinfo;    
      char _ip[16];
      char _port[8];
      Byteint _byteint{};
      int _fd{};     
      
    public:
      /**
      * @brief Construct a new Stream Socket Srv object
      * 
      * @param[in] ip Optional, CStyle string with ip for stream socket server
      * @param[in] port Optional, number port
      * @param[in] fmtlen Optional, formato length
      */
      Stream( const char* ip=nullptr
            , uint16_t port=0
            , FmtLen fmtlen=FmtLen::FMT4B);

      /**
       * @brief Construct a new Stream Server object
       * 
       * @param[in] ip CStyle string with ip for stream socket server
       * @param[in] port CStyle string with port for stream socket server
       * @param[in] fmtlen formato length
       */
      Stream( const char* ip, const char* port
            , FmtLen fmtlen=FmtLen::FMT4B);
      
      /**
      * @brief destructor por defecto
      */
      virtual ~Stream();


      /**
      * @brief metodo para establecer la conexion
      * @param[in,out] info buffer opcinal donde colocara la info
      * \param[in] linfo longitud del buffer
      * @return estado si \b thr es false
      *  + 0 success
      *  + !=0 failure, errno
      */
      virtual int Connect(char* info=nullptr, int linfo=0) = 0;

      /**
      * @brief Metodo para desconectar un socket
      * @return 
      *  + 0 success
      *  + !=0 failure, errno
      */
      virtual int Disconnect(void) = 0;

      /**
      * @brief metodo para el envio de mensaja mediante un socket
      * Mensaje del tipo CStyle String.
      * @param[in] msg mensaje que se desea enviar
      * @param[in] len longitud del mensaje que se desea enviar
      * por defecto este es '-1', con lo que envia el mensja completo
      * @return cantidad de bytes del mensjae enviado
      */
      virtual uint32_t Send(const char* msg, uint32_t len=0);

      /**
      * @brief metodo para el envio de mensaja mediante un socket
      * Mensaje de tipo std::string 
      * @param[in] msg mensaje que se desea enviar
      * @param[in] len longitud del mensaje que se desea enviar
      * por defecto este es '-1', con lo que envia el mensja completo
      * @return cantidad de bytes del mensjae enviado
      */
      virtual uint32_t Send(const std::string& msg, uint32_t len=0);

      /**
      * @brief metodo para recibir un mensaje mediante un socket
      * @param[out] buf buffer donde se colocara el mensaje recibido
      * @param[in] len longitud del bufer \p buf
      * \param[in] reentry Opcional, para indicar si es una reentrada por
      * bytes pendientes ( \p len < byte_recv ) segund length in header.
      * @return cantidad de bytes recibidos sin leer
      */
      virtual uint32_t Recv(char* buf, uint32_t len, bool reentry=false);

      /**
       * @brief metodo para recibir un mensaje mediante un socket
       * @param[out] rcv string donde colocaremos el dato recibido
       * @param[in] len  cantidad de bytes a leer y colocar en \p rcv
       * \param[in] reentry Opcional, para indicar si es una reentrada por
       * bytes pendientes ( \p len < byte_recv ) segund length in header.
       * @return uint32_t 
       */
      virtual uint32_t Recv(std::string& rcv, uint32_t len=0, bool reentry=false);


      /**
      * @brief metodo de recepccion con timeout.
      * @param[out] rcv string donde se concatena el dato recibido
      * @param[in] timeout tiempo de espera en milisegundos
      * @param[in] len opcional, cantidad de bytes maximos a recibir      
      * @param[in] reentry opcional, si es reentry solo toma datos desde
      * el socket sin leer primero la longitud del header.
      * @return uint32_tcantidad de bytes pendiente para ser leidos      
      */
      virtual uint32_t Recv ( std::string& rcv
                            , double timeout
                            , uint32_t len = 0
                            , bool reentry=false);


      /**
      * @brief metodo de recepccion con timeout.
      * @param[out] buf buffer donde se colocara los datos recibido
      * @param[in] len longitud del buffer \p buf
      * @param[in] timeout tiempo de espera en milisegundos
      * @param[in] reentry opcional, si es reentry solo toma datos desde
      * el socket sin leer primero la longitud del header.
      * @return uint32_t cantidad de bytes pendiente para ser leidos.      
      */
      virtual uint32_t Recv( char* buf            
            , uint32_t len
            , double timeout            
            , bool reentry=false);
      
      /**
       * @brief metodo para establecer el timeout de recepcion
       * @param[in] timeout timeout en segundos
       */
      void RecvTimeout(double timeout);
  };




  /**
  * @brief definicion de la clase concreta \b StreamSocketSrv
  * 
  */
  class StreamServer: public Stream
  {
    protected:
      int _fdsrv{};      
      int _backlog{};
      
    public:
      /**
      * @brief Construct a new Stream Socket Srv object
      * 
      * @param[in] ip Optional, CStyle string with ip (IPv4) for stream socket server
      * @param[in] port Optional, number port
      * @param[in] fmtlen Optional, formato length
      */
      StreamServer( const char* ip=nullptr
                  , uint16_t port=0
                  , FmtLen fmtlen=FmtLen::FMT4B);

      /**
       * @brief Construct a new Stream Server object
       * @param[in] ip CStyle string with ip (IPv4) for stream socket server
       * @param[in] port CStyle string with port for stream socket server
       * @param[in] fmtlen formato length
       */
      StreamServer( const char* ip
                  , const char* port
                  , FmtLen fmtlen=FmtLen::FMT4B);

      /**
      * @brief destructor por defecto
      */
      virtual ~StreamServer();

      /**
      * @brief Operador de asignacion por copia
      * @param[in] obj objeto que se copiara 
      * @return this objetc
      */
      virtual StreamServer& operator=(const StreamServer& obj);

      /**
      * @brief Operacion de asingacion por movimiento
      * @param[in] obj objeto que se movera
      * @return this objetc
      */
      virtual StreamServer& operator=(StreamServer&& obj) ;


      /**
      * @brief metodo para establecer la conexion
      * \param[out] info Opcional, buffer donde podemos colocar
      * la info de la conexion
      * \param[in] linfo Opcional, longitud del buffer \p info .
      * @return estado de la coonexion
      *  + 0 \b success
      *  + !=0 \b failure, errno
      */
      virtual int Connect(char* info=nullptr, int linfo=0) override;

      /**
      * @brief Metodo para desconectar un socket
      * @return estado de la descoonexion
      *  + 0 success
      *  + !=0 failure, errno
      */
      virtual int Disconnect(void)override;


      /**
      * @brief funcion expropiativa que acepta una conexion, cuando 
      * esta se  concreta sigue el thread de ejeccion.
      * 
      * @param[out] info Opcional, buffer opcional donde podemos colocar 
      * la info de la conexion.
      * @param[in] linfo Opcional, longitud del buffer \p info .
      * @return estado de la accion
      *  + 0 success
      *  + !=0 failure, errno
      */
      virtual int Accept(char* info=nullptr, int linfo=0);
  };


  /**
  * @brief definicion de la clase concreta \b StreamClient
  * 
  */
  class StreamClient: public Stream
  {    
    public:
      /**
      * @brief Construct a new Stream Socket Client object
      * @param[in] ip Optional, CStyle string with ip (IPv4) for stream socket Client
      * @param[in] port Optional, number port
      * @param[in] fmtlen Optional, formato length
      */
      StreamClient( const char* ip=nullptr
                  , uint16_t port=0
                  , FmtLen fmtlen=FmtLen::FMT4B);

      /**
       * @brief Construct a new Stream Client object
       * 
       * @param[in] ip CStyle string with ip (IPv4) for stream socket Client
       * @param[in] port CStyle string with port for stream socket Client
       * @param[in] fmtlen formato length
       */
      StreamClient( const char* ip, const char* port
                  , FmtLen fmtlen=FmtLen::FMT4B);

      /**
      * @brief destructor por defecto
      */
      virtual ~StreamClient();

      /**
      * @brief Operador de asignacion por copia
      * @param[in] obj objecto que se copiara 
      * @return this object
      */
      virtual StreamClient& operator=(const StreamClient& obj);
      
      /**
      * @brief Operacion de asingacion por movimiento
      * @param[in] obj objecto que se movera
      * @return this object
      */
      virtual StreamClient& operator=(StreamClient&& obj) ;

      /**
      * @brief metodo para establecer la conexion
      * \param[out] info Opcional, buffer opcional donde podemos colocara
      * la info de la conexion.
      * \param[in] linfo Opcional, longitud del buffer \p info .
      * @return estado de la accion
      *  + 0 success
      *  + !=0 failure, errno
      */
      virtual int Connect(char* info=nullptr, int linfo=0) override;

      /**
      * @brief Metodo para desconectar un socket
      * @return estado de la accion
      *  + 0 success
      *  + !=0 failure, errno
      */
      virtual int Disconnect(void)override;

  };
};

/*
 * ========================[ END   class interfaces ]==================================
 */
#endif /* #ifndef __PSocket_hpp__ */
