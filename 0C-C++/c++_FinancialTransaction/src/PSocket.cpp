/** ******************************************************************************************************//**
* \addtogroup PSocket
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
* THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
* ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
* POSSIBILITY OF SUCH DAMAGE.
*
* \file PSocket.cpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief Posix Socket Stream Implementation.
* \details Posix Socket Stream Implementation.
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
/*
 * ===========================[ BEGIN include header file ]======================================
 */

#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h> /* close() */


/* htonl() and  */
#include <netinet/in.h>
#include <arpa/inet.h>
#include <cstring>

#include <utility>
#include <memory>

#include <PSocket.hpp> /**<@brief Definimos el Nombre del modulo */
#include <Exception.hpp>
/*
 * ===========================[ END   include header file ]======================================
 */


/*
 * ===========================[ BEGIN defines labels/macros ]====================================
 */

#include <errno.h>  /* errno(3)  */
  
#ifdef _GNU_SOURCE 
  #define mstrerrorname_np(Errno) strerrorname_np(Errno)
  #define mstrerrordesc_np(Errno) strerrordesc_np(Errno)
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
#endif

#ifdef NDEBUG
  #define INFO()  fprintf(stdout,"%s\n",__PRETTY_FUNCTION__)
#else  
  #define INFO()
#endif

/*
 * ===========================[ END   defines labels/macros ]====================================
 */

/*
 * =============================[ BEGIN class interfaces ]=======================================
 */
namespace PSocket {

Byteint::Byteint(uint8_t l):_byteint{},_len(l)
{ }

/**
 * @brief metodos asociados al calculo de la longitud a colocaren el header
 * para el envio
 * 
 * @param[in] num longitud del mensaje
 * @param[in,out] buf buffer donde se coloca los bytes de header
 * @return char* 
 */
char* Byteint::number2binary(uint32_t num)
{
  std::memset(this->_byteint.b,0,sizeof(this->_byteint.b));
  uint8_t i=this->_len;
  while( i > 0 )
  {
    this->_byteint.b[--i] = num%0x100;
    num /= 0x100;
    //i--;    
  }
  return this->_byteint.b;
}

/**
 * @brief metodos asociados al calculo de la longitud proveniente en el header
 * para la recepccion
 * 
 * @param[in] byte bytes recibido desde el header
 * @return uint32_t 
 */
uint32_t Byteint::binary2number(char* byte)
{
  this->_byteint.ui = 0;
  uint8_t i=0;
  while( i < this->_len)
  {
    this->_byteint.ui |= byte[i++];
    if(i != this->_len)
    {
      this->_byteint.ui <<= 8;
    }
  }
  return this->_byteint.ui;
}


/**
* @brief Construct a new Stream Socket Srv object
* 
* @param[in] ip Optional, CStyle string with ip for stream socket server
* @param[in] port Optional, number port
* @param[in] fmtlen Optional, formato length
*/
Stream::Stream( const char* ip
              , uint16_t port
              , FmtLen fmtlen):_byteint(fmtlen),_fd{0}
{
  if(ip)
  {
    std::strncpy(this->_ip,ip,sizeof(this->_ip));
  }
  else
  {
    std::strncpy(this->_ip,"0.0.0.0",sizeof(this->_ip));    
  }      
  snprintf(this->_port,sizeof(this->_port)-1,"%u",port); 
}              

/**
 * @brief Construct a new Stream Server object
 * 
 * @param[in] ip CStyle string with ip for stream socket server
 * @param[in] port CStyle string with port for stream socket server
 * @param[in] fmtlen formato length
 */
Stream::Stream( const char* ip
              , const char* port
              , FmtLen fmtlen):_byteint(fmtlen),_fd{0}
{
  if(ip)
  {
    std::strncpy(this->_ip,ip,sizeof(this->_ip));
  }
  else
  {
    std::strncpy(this->_ip,"0.0.0.0",sizeof(this->_ip));
  }
  if(port)
  {
    std::strncpy(this->_port,port,sizeof(this->_port));
  }
  else {
    std::strncpy(this->_port,"0",sizeof(this->_port));
  } 
}          

/**
* @brief destructor por defecto
*/
Stream::~Stream()
{ 
  INFO();
}


/**
* @brief metodo para el envio de mensaja mediante un socket
* Mensaje del tipo CStyle String.
* @param[in] msg mensaje que se desea enviar
* @param[in] len longitud del mensaje que se desea enviar
* por defecto este es '-1', con lo que envia el mensja completo
* @return cantidad de bytes del mensjae enviado
*/
uint32_t Stream::Send(const char* msg, uint32_t l)
{
  if(!msg)
    return 0;
  
  uint32_t len;
  if(l == 0)
    len = std::strlen(msg);
  else
    len = l;

  int numbytes=0,i;

  if(this->_byteint._len != FmtLen::FMTNONE)
  {    
    numbytes = send ( this->_fd
                    , (const void*) this->_byteint.number2binary(len)
                    , this->_byteint._len
                    , 0
                    );    
    if(numbytes == 0)
    {  
      return errno;
    }
  }
  i = 0;
  do{      
    numbytes = send(this->_fd, (const void*) &msg[i],len,0);
    if(numbytes == 0)
    {  
      return errno;
    }
    len -= numbytes;
    i += numbytes;
  }while(len);
  return 0; 
}

/**
* @brief metodo para el envio de mensaja mediante un socket
* Mensaje de tipo std::string 
* @param[in] msg mensaje que se desea enviar
* @param[in] len longitud del mensaje que se desea enviar
* por defecto este es '-1', con lo que envia el mensja completo
* @return cantidad de bytes del mensjae enviado
*/
uint32_t Stream::Send(const std::string& msg, uint32_t l)
{
  uint32_t len;
  if(l == 0)
    len = msg.size();
  else
    len = l;

  int numbytes=0,i;

  if(this->_byteint._len != FmtLen::FMTNONE)
  {    
    numbytes = send ( this->_fd
                    , (const void*) this->_byteint.number2binary(len)
                    , this->_byteint._len
                    , 0
                    );                   
    if(numbytes == 0)
    {  
      return errno;
    }
  }
  const char* pmsg = msg.c_str();
  i = 0;
  do{      
    numbytes = send(this->_fd, (const void*) &pmsg[i],len,0);
    if(numbytes == 0)
    {  
      return errno;
    }
    len -= numbytes;
    i += numbytes;
  }while(len);
  return 0;

}

/**
* @brief metodo para recibir un mensaje mediante un socket
* @param[in,out] buf buffer donde se colocara el mensaje recibido
* @param[in] len longitud del bufer \p buf
* \param[in] reentry Opcional, para indicar si es una reentrada por
* bytes pendientes ( \p len < byte_recv ) segund length in header.
* @return cantidad de bytes recibidos sin leer
*/
uint32_t Stream::Recv(char* buf, uint32_t len, bool reentry)
{
  if(!buf)
    throw EXCEPTION ( "EINVAL buf null");

  uint64_t bytes;
  int flags = 0;
  int errn;

  char header[4];
  uint32_t len2read;
  buf[0] = '\0';
  if(!reentry && this->_byteint._len != FmtLen::FMTNONE)
  {
    bytes = recv( this->_fd, (void*) header
                , this->_byteint._len
                , flags
                );    
    errn = errno;
    if( errn != 0)
    {         
      if(errno == EAGAIN)
        throw EXCEPTION ( "ERROR DE COMUNICACION TIMEOUT AGOTADO");

      throw EXCEPTION ( "recv():%s-%s"
                      , mstrerrorname_np(errn),mstrerrordesc_np(errn)
                      );
    }
    
    len2read = this->_byteint.binary2number(header);
    if(len2read == 0 )    
      return 0;    
  }

  bytes = recv(this->_fd, (void*) buf, len-1, flags);
  errn = errno;
  if( errn != 0 )
  {
    if(errno == EAGAIN)
        throw EXCEPTION ( "ERROR DE COMUNICACION TIMEOUT AGOTADO");

    throw EXCEPTION ( "recv():%s-%s"
                    , mstrerrorname_np(errn),mstrerrordesc_np(errn)
                    );
  }
  buf[bytes] = '\0';
  return (len2read-bytes);
}

/**
 * @brief metodo para recibir un mensaje mediante un socket
 * 
 * @param[out] rcv string donde colocaremos el dato recibido
 * @param[in] len  cantidad de bytes a leer y colocar en \p rcv
 * \param[in] reentry Opcional, para indicar si es una reentrada por
 * bytes pendientes ( \p len < byte_recv ) segund length in header.
 * @return uint32_t 
 */
uint32_t Stream::Recv(std::string& rcv, uint32_t len, bool reentry)
{
  uint64_t bytes;
  int flags = 0;
  int errn;
  uint32_t len2read=0;
  char header[4];

  if(!reentry && this->_byteint._len != FmtLen::FMTNONE)
  {
    bytes = recv( this->_fd, (void*) header
                , this->_byteint._len
                , flags
                );    
    
    errn = errno;
    if( errn != 0)
    {         
      if(errno == EAGAIN)
        throw EXCEPTION ( "ERROR DE COMUNICACION TIMEOUT AGOTADO");

      throw EXCEPTION ( "recv():%s-%s"
                      , mstrerrorname_np(errn),mstrerrordesc_np(errn)
                      );
    }
    len2read = this->_byteint.binary2number(header);    
    if(len2read ==0 )
      return 0;    
  }

  if(len == 0)
  {
    if(len2read)
      len = len2read + 1;
    else
      len = 64;
  }
    
  #if 1
  std::unique_ptr<char[]> buf(new char[len],std::default_delete<char[]>());
  bytes = recv(this->_fd, (void*) buf.get(), len, flags);  
  #else
  std::string ret(len,'\0');
  bytes = recv(this->_fd, (void*) &ret.data()[0], len, flags);
  #endif
  
  errn = errno;
  if( errn != 0)
  {      
    if(errno == EAGAIN)
        throw EXCEPTION ( "ERROR DE COMUNICACION TIMEOUT AGOTADO");

    throw EXCEPTION ( "recv():%s-%s"
                    , mstrerrorname_np(errn),mstrerrordesc_np(errn)
                    );
  }
  #if 1
  buf[bytes] = '\0';
  rcv += std::string(buf.get());  
  #else
  rcv += ret;
  #endif
  if(reentry)
    return 0;

  return (len2read-bytes);
}


/**
* @brief metodo de recepccion con timeout
* 
* @param[in,out] rcv string donde se concatena el dato recibido
* @param len cantidad de bytes maximos a recibir
* @param timeout tiempo de espera en milisegundos
* @param reentry opcional, si es reentry solo toma datos desde
* el socket sin leer primero la longitud del header.
* @return std::pair<uint32_t,uint32_t> 
*  + \b first : cantidad de bytes pendiente para ser leidos
*  + \b second : tiempo de espera remanente
*/
uint32_t Stream::Recv( std::string& rcv, double timeout
                      , uint32_t len , bool reentry)
{
  this->RecvTimeout(timeout);  
  return this->Recv(rcv,len,reentry); 
}


/**
* @brief metodo de recepccion con timeout
* 
* @param[in,out] buf buffer donde se colocara los datos recibido
* @param len longitud del buffer \p buf
* @param timeout tiempo de espera en milisegundos
* @param reentry opcional, si es reentry solo toma datos desde
* el socket sin leer primero la longitud del header.
* @return std::pair<uint32_t,uint32_t> 
*  + \b first : cantidad de bytes pendiente para ser leidos
*  + \b second : tiempo de espera remanente
*/
uint32_t Stream::Recv ( char* buf, uint32_t len
                      , double timeout, bool reentry)
{ 
  this->RecvTimeout(timeout);
  return this->Recv(buf,len,reentry);
}      


/**
* @brief metodo para establecer el time out de rececpion
* @param[in] timeout tiempo de espra maximo en segundos
*/
void Stream::RecvTimeout(double timeout)
{
  using timeval_t = struct timeval;   
  int errn; 
  timeval_t time {};
  std::pair<uint32_t,uint32_t> ret;  

  time.tv_sec = int(timeout);
  timeout -= double(time.tv_sec);
  time.tv_usec = int(timeout*1000000);
  
  /* establecemos el timeout */
  errn = setsockopt ( this->_fd
                    , SOL_SOCKET, SO_RCVTIMEO
                    , &time
                    , sizeof(timeval_t)
                    );
  if (errn < 0)
  {    
    throw EXCEPTION ( "setsockopt():%s-%s"
                    , mstrerrorname_np(errn),mstrerrordesc_np(errn)
                    );
  } 
}


StreamServer::StreamServer( const char* ip
                          , uint16_t port
                          , FmtLen fmtlen
                          ):Stream(ip,port,fmtlen),_fdsrv{0}
{ }

StreamServer::StreamServer( const char* ip
                          , const char* port
                          , FmtLen fmtlen
                          ):Stream(ip,port,fmtlen),_fdsrv{0}
{ }

/**
 * @brief destructor por defecto
 */
StreamServer::~StreamServer()
{ 
  if(Stream::_fd == 0 && this->_fdsrv == 0)
    return;
  this->Disconnect();
}

/**
 * @brief Operador de asignacion por copia
 * @param[in] obj  
 * @return 
 */
StreamServer& StreamServer::operator=(const StreamServer& obj)
{
  std::strncpy(Stream::_ip,obj._ip,sizeof(Stream::_ip));
  std::strncpy(Stream::_port,obj._port,sizeof(Stream::_port));  
  Stream::_byteint._len = obj._byteint._len;
  this->_fdsrv = obj._fdsrv;
  Stream::_fd = obj._fd;
  this->_backlog = obj._backlog;
  return *this;
}

/**
 * @brief Operacion de asingacion por movimiento
 * @param[in] obj
 * @return 
 */
StreamServer& StreamServer::operator=(StreamServer&& obj)
{
  // copy 
  std::strncpy(Stream::_ip,obj._ip,sizeof(Stream::_ip));
  std::strncpy(Stream::_port,obj._port,sizeof(Stream::_port));
  Stream::_byteint._len = obj._byteint._len;
  this->_fdsrv = obj._fdsrv;
  Stream::_fd = obj._fd;
  this->_backlog = obj._backlog;

  // setting default
  std::memset(obj._ip,'\0',sizeof(obj._ip));
  std::memset(obj._port,'\0',sizeof(obj._port));
  obj._byteint._len = FmtLen::FMTNONE;
  obj._fdsrv = 0;
  obj._fd = 0;
  obj._backlog = 0;
  return *this;
}


/**
 * @brief metodo para establecer la conexion
 * @param[in] thr flag opcional para habilitar el throw
 * de excepccion en caso de falla. 
 * @return estado si \b thr es false
 *  + 0 success
 *  + !=0 failure, errno
 */
int StreamServer::Connect(char* info, int linfo)
{  
  int option = 1;
  int errn;  
  addrinfo_t hints;
  addrinfo_t *pr_result = nullptr;
  addrinfo_t *_rp = nullptr;
  
  /* Obtain address(es) matching host/port */
  memset(&hints, 0, sizeof(addrinfo_t));
  hints.ai_family   = AF_INET;        /* solo IPv4 */
  hints.ai_socktype = SOCK_STREAM;    /* stram TCP/IP socket */
  hints.ai_flags    = AI_NUMERICHOST | AI_PASSIVE;  /* host numerico 'ip-port'*/
  hints.ai_protocol = 0;              /* Any protocol */
  
    
  errn = getaddrinfo(Stream::_ip, Stream::_port, &hints, &pr_result);
  std::unique_ptr<addrinfo_t,void(*)(addrinfo_t*)> result {pr_result,freeaddrinfo};

  if (errn != 0 || !result) 
  {
    throw EXCEPTION("getaddrinfo(): %s", gai_strerror(errn));
  }

  for( _rp = result.get(); _rp != nullptr; _rp = _rp->ai_next) 
  {
    this->_fdsrv = socket( _rp->ai_family
                , _rp->ai_socktype
                , _rp->ai_protocol);
    if (this->_fdsrv < 0 )
      continue;

    if( bind(this->_fdsrv, _rp->ai_addr, _rp->ai_addrlen) == 0)
    {
      /* Success, por lo tanto salimos del recorrido de
       * la lista enlazada, con una direccion valida.
       */
      break;
    }    
    close(this->_fdsrv);
  }
  
  /* si rp es NULL, quiere decir que recorrimos toda 
   * la lista sin poder vincularnos a una dirreccion 
   * valida
   */
  if (!_rp) 
  { 
    throw EXCEPTION("Could not bind to <%s:%s>",Stream::_ip,Stream::_port);
  }    

  /* para que el socket este disponible de forma inmediata al cerrarse la comunicacion */
  errn = setsockopt(this->_fdsrv, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(option));
  errn = errno;    
  if( errn < 0 ) 
  { 
    throw EXCEPTION("setsockopt(): %s-%s", strerrorname_np(errn),strerrordesc_np(errn));
  }  

  if(listen(this->_fdsrv,this->_backlog) < 0)
  {
    /* llamada a listen() */
    errn = errno;    
    close(this->_fdsrv);
    throw EXCEPTION("listen(): %s-%s", strerrorname_np(errn),strerrordesc_np(errn));
  }  

  if(!info || linfo == 0)
    return 0;

  char hbuf[64], sbuf[64]; 
  if( (errn=getnameinfo( (const struct sockaddr*) _rp->ai_addr, _rp->ai_addrlen
                  , hbuf, sizeof(hbuf)
                  , sbuf, sizeof(sbuf)
                  , NI_NUMERICHOST | NI_NUMERICSERV
              )) == 0 )
  {   
    snprintf( info,linfo-1,"%s:%s", hbuf,sbuf);
    return 0;
  }  

  close(this->_fdsrv);
  throw EXCEPTION ( "Error <%s> in call to getnameinfo()"
                  ,  gai_strerror(errn)
                  );
  return 0;
}


/**
 * @brief Metodo para desconectar un socket
 * @return 
 *  + 0 success
 *  + !=0 failure, errno
 */
int StreamServer::Disconnect(void)
{
  INFO();
  int errn = 0;
  if(Stream::_fd != 0)
  {
    if(shutdown(Stream::_fd, SHUT_RDWR) < 0)
      errn = errno;
      
    /* cierra fd2 */  
    if(close(Stream::_fd<0) )
      errn = errno;
  }
  
  if(this->_fdsrv)
  {
    if(shutdown(this->_fdsrv, SHUT_RDWR) < 0)
      errn = errno;
    
    /* cierra fd1 */ 
    if(close(this->_fdsrv)<0)  
      errn = errno;
  }    
  /* */
  Stream::_fd = 0;
  this->_fdsrv= 0;
  return errn;  
}



/**
 * @brief funcion expropiativa que acepta una conexion, cuando 
 * esta se  concreta sigue el thread de ejeccion.
 * 
 * @param[in,out] info buffer opcional donde podemos colocar la info
 * de la conexion
 * @param[in] linfo longitud del buffer
 *  + 0 success
 *  + !=0 failure, errno
 */
int StreamServer::Accept(char* info, int linfo)
{
  int errn = 0;
  int sin_size;
  /* socket addres para el cliente */
  struct sockaddr_in client;   

  sin_size = (int) sizeof(struct sockaddr_in);
  Stream::_fd = accept(this->_fdsrv,(struct sockaddr *) &client,(socklen_t*) &sin_size);
  errn = errno;
  if( Stream::_fd < 0 ) 
  {    
    throw EXCEPTION ( "accept():%s-%s"
                    , mstrerrorname_np(errn),mstrerrordesc_np(errn)
                    );
  }

  /* Imprimimos la direccion del cliente conectado 
   * Debemos colocarlo en un log   */  
  if(!info || linfo == 0)
    return 0;
  
  snprintf( info, linfo-1
          , "%s:%i"
          , inet_ntoa(client.sin_addr)
          , client.sin_port
          );
  return 0;
}


/**
* @brief Construct a new Stream Socket Client object
* 
* @param[in] ip Optional, CStyle string with ip for stream socket Client
* @param[in] port Optional, number port
* @param[in] fmtlen Optional, formato length
*/
StreamClient::StreamClient( const char* ip
                          , uint16_t port
                          , FmtLen fmtlen):Stream(ip,port,fmtlen)
{ }

/**
 * @brief Construct a new Stream Client object
 * 
 * @param[in] ip CStyle string with ip for stream socket Client
 * @param[in] port CStyle string with port for stream socket Client
 * @param[in] fmtlen formato length
 */
StreamClient::StreamClient( const char* ip
                          , const char* port
                          , FmtLen fmtlen):Stream(ip,port,fmtlen)
{ }

/**
* @brief destructor por defecto
*/
StreamClient::~StreamClient()
{ 
  if(Stream::_fd == 0)
    return;
  this->Disconnect();  
}

/**
* @brief Operador de asignacion por copia
* @param[in] obj  
* @return 
*/
StreamClient& StreamClient::operator=(const StreamClient& obj)
{
  std::strncpy(Stream::_ip,obj._ip,sizeof(Stream::_ip));
  std::strncpy(Stream::_port,obj._port,sizeof(Stream::_port));  
  Stream::_byteint._len = obj._byteint._len;
  Stream::_fd = obj._fd;
  return *this;
}

/**
* @brief Operacion de asingacion por movimiento
* @param[in] obj
* @return 
*/
StreamClient& StreamClient::operator=(StreamClient&& obj)
{
  // copy 
  std::strncpy(Stream::_ip,obj._ip,sizeof(Stream::_ip));
  std::strncpy(Stream::_port,obj._port,sizeof(Stream::_port));
  Stream::_byteint._len = obj._byteint._len;
  Stream::_fd = obj._fd;
  
  // setting default
  std::memset(obj._ip,'\0',sizeof(obj._ip));
  std::memset(obj._port,'\0',sizeof(obj._port));
  obj._byteint._len = FmtLen::FMTNONE;
  obj._fd = 0;
  return *this;
}


/**
* @brief metodo para establecer la conexion
* \param[in,out] info buffer opcional donde podemos colocar la info
* de la conexion
* \param[in] linfo longitud del buffer     
* @return estado si \b thr es false
*  + 0 success
*  + !=0 failure, errno
*/
int StreamClient::Connect(char* info, int linfo)
{
  int errn;  
  addrinfo_t hints;
  addrinfo_t *pr_result = nullptr;
  addrinfo_t *_rp = nullptr;
  //this->_rp = nullptr;
  
  /* Obtain address(es) matching host/port */
  memset(&hints, 0, sizeof(addrinfo_t));
  hints.ai_family   = AF_INET;        /* solo IPv4 */
  hints.ai_socktype = SOCK_STREAM;    /* stram TCP/IP socket */
  hints.ai_flags    = AI_NUMERICHOST; /* host numerico 'ip-port'*/
  hints.ai_protocol = 0;              /* Any protocol */
  
    
  errn = getaddrinfo(Stream::_ip, Stream::_port, &hints, &pr_result);
  std::unique_ptr<addrinfo_t,void(*)(addrinfo_t*)> result {pr_result,freeaddrinfo};
  if (errn != 0 || !result) 
  {
    throw EXCEPTION("getaddrinfo(): %s", gai_strerror(errn));
  }


  for( _rp = result.get(); _rp != nullptr; _rp = _rp->ai_next) 
  {
    Stream::_fd = socket( _rp->ai_family
                , _rp->ai_socktype
                , _rp->ai_protocol);
    if (Stream::_fd < 0 )
      continue;


    if(connect(Stream::_fd, _rp->ai_addr, _rp->ai_addrlen) == 0)
    {
      /* Success, por lo tanto salimos del recorrido de
       * la lista enlazada, con una direccion valida.
       */
      break;
    }    
    close(Stream::_fd);
  }
  
  /* si rp es NULL, quiere decir que recorrimos toda 
   * la lista sin poder vincularnos a una dirreccion valida
   */
  if (!_rp) 
  {     
    throw EXCEPTION("Could not bind to Server <%s:%s>",Stream::_ip,Stream::_port);
  }   


  if(!info || linfo == 0)
    return 0;

  char hbuf[64], sbuf[64]; 
  if( (errn=getnameinfo( (const struct sockaddr*) _rp->ai_addr, _rp->ai_addrlen
                  , hbuf, sizeof(hbuf)
                  , sbuf, sizeof(sbuf)
                  , NI_NUMERICHOST | NI_NUMERICSERV
              )) == 0 )
  {      
    snprintf( info,linfo-1,"%s:%s", hbuf,sbuf);    
    return 0;
  }    
  close(Stream::_fd);
  throw EXCEPTION ( "Error <%s> in call to getnameinfo()"
                  , gai_strerror(errn)
                  );
  return 0;
}

/**
* @brief Metodo para desconectar un socket
* @return 
*  + 0 success
*  + !=0 failure, errno
*/
int StreamClient::Disconnect(void)
{
  INFO();
  int errn = 0;  
  if(Stream::_fd == 0)
    return 0;
  
  if(shutdown(Stream::_fd, SHUT_RDWR) < 0)
    errn = errno;
  
  if(close(Stream::_fd) < 0 )  
    errn = errno;
  
  /* */
  Stream::_fd = 0;
  return errn;  
}


};

/*
 * =============================[ END   class interfaces ]=======================================
 */

