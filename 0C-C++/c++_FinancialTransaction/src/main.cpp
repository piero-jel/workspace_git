/** ******************************************************************************************************//**
* \addtogroup main
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
* \file main.cpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief Financial Transaction.
* \details Financial Transaction se basa en un software que simule una transaccion financiera.

* \version 0.0.1.
* \date Viernes 7 de Junio de 2024.
* \pre pre, condiciones que deben cuplirse antes del llamado,
* \bug bug, depuracion example: Not all memory is freed when deleting an object
* of this class.
* \warning
* \note
* \par Change History:
* Author         Date                 Version     Brief
* JEL            2024.05.06           0.0.1       Version Inicial no release
*
* @} doxygen end group definition
* ********************************************************************************************************* */
/** 
 * \b VERSION  0 : Financial Transaction version 0.0.1
 * \b VERSION  1 : PSocket::StreamServer for response 0210
 * \b VERSION  2 : 
 * \b VERSION  3 :
 * \b VERSION  4 :
 * \b VERSION  5 :
 * 
 * \b VERSION 10 :
 * \b VERSION 11 :
 * \b VERSION 12 :
 * \b VERSION   :
 * \b VERSION   :
 * 
 * 
 */
#if (!defined(VERSION))
  #define VERSION 0
#endif




#if (VERSION == 0 )
/* Financial Transaction0.0.1 */
#include <main.hpp>
#include <PSocket.hpp>

#if ( IS_SAME >= 2017 )
  /* c++17 >    */
  #define IS_SAME(OBJ1,OBJ2) std::is_same_v<OBJ1, OBJ2>
#else
  #define IS_SAME(OBJ1,OBJ2) std::is_same<OBJ1, OBJ2>::value
#endif

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char* argv[])
{ 
  try
  {
    char buf[1024];
    CliApp cli(argc,argv);
    cli.print();

    PSocket::StreamClient socket {
        cli.ip.c_str()
      , cli.port
      , PSocket::FmtLen::FMT4B 
    };
    // 1° conect to Server
    /*
    socket.Connect(buf,sizeof(buf));

    fprintf(stdout, "Client Connect to <%s>\n", buf);
    */
    // 2° Get Amount
    int64_t amount = GetAmount("Ingrese el monto (hasta 2 decimales Implicitos): ");
    
    // 3° Get Card Number
    std::string card_number = GetCardNumber("Ingrese el Numero de Tarjeta ( 13 ~ 99 decimales): ");

    // 4° Verify the card number
    #if ( IS_SAME >= 2017 )
    auto [st,reg_rng,reg_card] = VerifyCardNumber (card_number
                                                  ,cli.frange
                                                  ,cli.fcards);
    #else
    auto ret = VerifyCardNumber (card_number
                                                  ,cli.frange
                                                  ,cli.fcards);
    auto st = std::get<0>(ret);
    //auto reg_rng = std::get<1>(ret);
    auto reg_card = std::get<2>(ret);
    #endif  
    
    if(!st)
    {
      fprintf(stdout,"TARJETA <%s> NO SOPORTADA\n",card_number.c_str());
      exit(EXIT_SUCCESS);
    }
    fprintf ( stdout,"TARJETA <%s>, CARD LABEL <%s>\n"
            , card_number.c_str()
            , reg_card.label
            );
    // 5° Get Card Code 
    std::string card_code = GetCardCode("Ingrese el Codigo de Seguridad (hasta 3 digitos): ");
    
       
    //std::cout<<"El Saldo ingresado es: "<<float(amount/100)<<'\n';
    fprintf(stdout,"El Saldo ingresado es: %012.2f\n",float(amount/100));
    std::cout<<"El Numero de tarjeta ingresado es: "<<card_number<<'\n';
    std::cout<<"El Codigo de tarjeta ingresado es: "<<card_code<<'\n';
    
    // 6° put together the petition
    std::string response, request = GetRequest(amount,card_number,card_code);
    std::cout<<"Request to send: "<<request<<'\n';

    // 7° Send Request and Wait Response
    socket.Send(request);    
    socket.Recv(response,double(cli.timeout/1000));

    // 8° Verify the Response
    if(response.length() < 6)
    {
      fprintf ( stdout,"Response <%s> error, empty or length too short\n"
              , response.c_str() );
      exit(EXIT_SUCCESS);
    }
    std::cout<<"Response: "<<response<<'\n';
    std::string mtid = response.substr(0,4);
    std::string respcode = response.substr(4,2);
    if(mtid != "0210")
    {
      fprintf ( stdout,"MTID <%s> no esperado operacion abortada\n"
              , mtid.c_str() );
      exit(EXIT_SUCCESS);
    }

    if(respcode == "00")
    {
      std::cout<<"OPERACION APROVADA\n";
    }
    else
    {
      fprintf ( stdout,"OPERACION RECHAZADA CON EL CODIGO <%s>\n"
              , respcode.c_str() );
    }
  }
  catch(const std::exception &e)  
  {
    std::cout<<"Error \"" 
             << e.what() <<'\"'<< std::endl;
  }
  catch(...)
  {
    std::cout<<"Error Desconocida"<<std::endl;
  }
  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
} 


std::tuple<bool,RangesRegister,CardsRegister>
  VerifyCardNumber(std::string card_number
                  ,std::string frange
                  ,std::string fcards)
{
  /*using CRange = std::list<RangesRegister>;
  using CCards = std::list<CardsRegister>;*/
  using CRange = std::forward_list<RangesRegister>;
  using CCards = std::forward_list<CardsRegister>;

  
  /* 1° parsin de archivos */
  CRange crange;
  CCards ccards;
  ReadAndFillContainer(frange,crange,'#');
  ReadAndFillContainer(fcards,ccards,'#');

  std::tuple<bool,RangesRegister,CardsRegister> ret{false,RangesRegister(),CardsRegister()};

  /* 2° find RangesRegister */  
  // predicado para la busqueda del RangesRegister 
  PredicateRange pred_rng(card_number);
  CRange::iterator it_rng = std::find_if(std::begin(crange)
                                        ,std::end(crange)
                                        ,pred_rng
                                        );
  if(it_rng == std::end(crange))
  {
    return ret;    
  }    

  /* 3° find CardsRegister */  
  CCards::iterator it_crd = std::find_if(std::begin(ccards)
                                        ,std::end(ccards)
                                        ,[&it_rng](const CardsRegister& o) -> bool {
                                          return (o.id == it_rng->id)?true:false;
                                        }
                                        );
  if(it_crd == std::end(ccards))
  {
    return ret;    
  }    

  /* 4° fill ret */
  std::get<0>(ret) = true;  
  std::get<1>(ret) = *it_rng;  
  std::get<2>(ret) = *it_crd;
  return ret;
}                  

template<typename N>
std::string GetRequest( N sld
                      , const std::string& ncard
                      , const std::string& ccard
                      )
{
  std::ostringstream ss;
  ss << "0200"
     << std::setfill('0')<<std::setw(2)<<ncard.length()
     << ncard
     << std::setfill('0')<<std::setw(12)<<sld
     << ccard;
  return std::string(ss.str());
}                      


template<typename N>
N GetAmount(const std::string& msg,uint8_t len)
{
  std::string ret ;
  std::cout<<msg;
  std::cin>>ret;
  /*
  if( ret.length() > len )
  {
    throw Exception ("%s Amount <%s> length<%i> is too long"
                    ,__PRETTY_FUNCTION__,ret.c_str(), ret.length());
  }
  */
  auto it = std::begin(ret);
  while(*it == ' ') it++;

  if(*it =='-')
  {
    throw EXCEPTION ("Negative Amount <%s> not allowed"
                    ,ret.c_str(), ret.length());
  }

  if(*it == '+' || *it =='-')
    it++;
  
  /* usamos la longitud efectiva */
  if( std::distance(it,std::end(ret)) > len )
  {
    throw EXCEPTION ("Amount <%s> length<%i> is too long"
                    ,ret.c_str(), ret.length());
  }

  std::for_each(it,std::end(ret),
    [&ret](char v)-> void {
      if( std::isdigit(v) == 0 && v != '.' && v != ',')
      {
        throw EXCEPTION ("Amount <%s> It is not composed only of digits"
                        ,ret.c_str());
      }
    }
  );
  return N(std::stold(ret)*100);
}

std::string GetCardNumber ( const std::string& msg
                          , uint8_t lmin
                          , uint8_t lmax
                          )
{
  std::string ret ;
  std::cout<<msg;
  std::cin>>ret;
  auto len = ret.length();
  if(  len < lmin || len > lmax )
  {
    throw EXCEPTION ("Card Number <%s> length<%i> incorrect"
                    ,ret.c_str(), len);
  }

  /* verificamos que todas sean valores numericos */
  std::for_each(std::begin(ret),std::end(ret),
    [&ret](char v)-> void{
      if( std::isdigit(v) == 0)
      {
        throw EXCEPTION ("Card Number <%s> It is not composed only of digits"
                        ,ret.c_str());
      }
    }
  );
  return ret;
}                          


std::string GetCardCode(const std::string& msg,uint8_t len)
{
  std::string ret ;
  std::cout<<msg;
  std::cin>>ret;
  if( ret.length() > len )
  {
    throw EXCEPTION ("Card Code <%s> length<%i> is too long"
                    ,ret.c_str(), ret.length());
  }

  std::for_each(std::begin(ret),std::end(ret),
    [&ret](char v)-> void{
      if( std::isdigit(v) == 0)
      {
        throw EXCEPTION ("Card Code <%s> It is not composed only of digits"
                        ,ret.c_str());
      }
    }
  );
  return ret;
}




CliApp::CliApp(int argc,char* argv[],FILE* ou)
{ 
  /* Inicializamos argumentos para el control del 
   * listado de parametro
   */
  if(argc == 0 || !argv )
    return;
  this->parser(argc,argv,ou);
}

void CliApp::parser(int argc,char** argv,FILE* ou)
{
  if(!argv || argc < 1)
  {     
    throw EXCEPTION("EINVAL argv equal to null");
  }
  
  if(!ou)
    ou = stdout;
  
  /* lo primero a establecer para que este disponible en el 
   * heap()
   */
  this->app = basename(argv[0]);
  this->__flag = 0x00;
  if(argc < 2)
  {
    fprintf(ou,"Not Option Pass\n");
    this->help(ou);   
  }
  int opt;
   
  /*
  -i ip server 
  -p port server
  -t timeout receive 
  -r path/file range 
  -c path/file cards 
  */
  while ((opt = getopt(argc, argv, "i:p:t:r:c:h")) != -1) 
  {
    switch (opt) 
    {
      case 'c':
        if(!optarg)
        {
          fprintf ( ou,"opcion -c sin path/file-cards\n");
          this->help(ou);           
        }
        /* FIXME se deberia realizar el check del tipo 
         * usando std::strtol(str,&remainder,base)
         */
        this->fcards = std::string(optarg);
        this->flags(Flag::FCARDS,true);
        break;

      case 'r':
        if(!optarg)
        {
          fprintf ( ou,"opcion -r sin path/file-range\n");
          this->help(ou);        
        }
        /* FIXME se deberia realizar el check del tipo 
         * usando std::strtol(str,&remainder,base)
         */
        this->frange = std::string(optarg);
        this->flags(Flag::FRANGE,true);
        break;

      case 't':
        if(!optarg)
        {
          fprintf ( ou,"opcion -t sin cantidad de mili segundos\n");
          this->help(ou);
        }
        /* FIXME se deberia realizar el check del tipo 
         * usando std::strtol(str,&remainder,base)
         */
        this->timeout = std::atoi(optarg);
        this->flags(Flag::TIMEOUT,true);
        break;

      case 'p':
        if(!optarg)
        {
          fprintf ( ou,"opcion -p sin numero de puero\n");
          this->help(ou);          
        }
        /* FIXME se deberia realizar el check del tipo 
         * usando std::strtol(str,&remainder,base)
         */
        this->port = std::atoi(optarg);
        this->flags(Flag::PORT,true);
        break;
      case 'i':
        if(!optarg)
        {
          fprintf ( ou,"opcion -i sin numero de ip\n");
          this->help(ou);
        }
        this->ip = std::string(optarg);
        this->flags(Flag::IP,true);
        break;

      case 'h':
        this->help(ou); 
        break; /* para evitar warning */

      default:
        fprintf(ou,"Option <%c> not found\n",opt);
        this->help(ou);         
    }
  }

  if (optind < argc)
  {
    /* Se pasaron mas arguementos de los devidos */
    fprintf(ou,"Se pasaron argumentos no permitido:\n ");
    for(int i = 1 ; i< argc;i++)
      fprintf(ou,"argv[%03d] <%s>\n",i,argv[i]);
    
    fputs("\n",ou);
    this->help(ou);
  }
  /* Realizamos el check de los parametros mandatorios */
  if(!this->flags( Flag(Flag::FCARDS|Flag::FRANGE) ))
  {
    fprintf(ou, "-c <path/card-file> or -r <path/range-file> not found"
            "They are mandatory\n" );
    this->help(ou);  
    exit(EXIT_SUCCESS);
  }  
  /* Realizamos el fill de los opcionales */
  if(!this->flags(Flag::IP))
    this->ip = "0.0.0.0";
  
  if(!this->flags(Flag::PORT))
    this->port = 3000 ;

  if(!this->flags(Flag::TIMEOUT))
    this->timeout = 5000;
}

void CliApp::help(FILE* ou)
{
  if(!ou)
    ou = stdout;

  fprintf( ou, "Usage: %s [-i ip] [-p port] [-t timeout] "
          "-c path/card-file -r path/range-file\n"
          , this->app.c_str()
         );
  fprintf(ou, "-i <ip>      : numero de ip Server, opcional por defecto localhost\n");  
  fprintf(ou, "-p <port>    : numero de puerto, opcional por defecto 3000\n");
  fprintf(ou, "-t <timeout> : tiempo de espera maximo por respuesta del server, opcional por defecto 5000 [mSec]\n");
  fprintf(ou, "-c <path/card-file>: ruta y nombre de archivo de tarjetas\n");
  fprintf(ou, "-r <path/range-file>: ruta y nombre de archivo de rangos\n");
  fprintf(ou, "-h print this help message\n");
  exit(EXIT_SUCCESS);
}

void CliApp::print(FILE* ou)
{
  if(!ou)
  {
    ou = stdout;
  }
  fprintf(ou, "-i <ip>      : %s\n",this->ip.c_str());
  fprintf(ou, "-p <port>    : %i\n",this->port);
  fprintf(ou, "-t <timeout> : %i [mSec]\n",this->timeout);
  fprintf(ou, "-c <path/card-file>: %s\n",this->fcards.c_str());
  fprintf(ou, "-r <path/range-file>: %s\n",this->frange.c_str());
}

void CliApp::flags(Flag flag,bool st)
{
  if(flag > Flag::ALL || flag == Flag::NONE)
    return ;
  
  if(st)
  {
    this->__flag |= flag;
  }
  else
  {
    this->__flag |= ~flag;
  }  
}

bool CliApp::flags(Flag flag)
{
  return (this->__flag & flag)?true:false;
}


template <typename C,int LEN>
void ReadAndFillContainer(const std::string& pathname, C& container, char comment)
{
  
  std::ifstream f2read {pathname,std::ifstream::in} ;
  if(!f2read.is_open())
  {    
    throw EXCEPTION ("Error to open path name <%s>"
                    ,pathname);    
  }  

  /* Clean de flags y nos paramos en el inicio del archivo */
  f2read.clear(); /* relizamos el clear de los flags */  
  f2read.seekg(0 /*offset*/, std::ios_base::beg);

  char buf[LEN];
  buf[0] = '\0';
  do{
    f2read.getline(buf,sizeof(buf),'\n');
    if(!f2read.good())
      break;

    /* descartamos las lineas vacias y las comentadas */
    if( buf[0] == comment || buf[0] == '\0' )
      continue;    

    /* El metodo depende contenedor destino
      * tenemos dos opciones, creamos uno interno y usamos std::copy()
      * o definimos los diferentes constexpr para cada uno.
      * El metodo mejor establecido es emplace()
      *
      *  + std::list<T>::emplace(IT i,T Obj);
      *  + std::vector<T>::emplace(IT i,T Obj);
      *  + std::forward_list<T>::emplace_front(T Obj);
      *  + std::set<T>::emplace(T Obj);
      *  + std::multiset<T>::emplace(T Obj);
      *
    */
    if constexpr ( IS_SAME(C, std::vector<typename C::value_type>)
                || IS_SAME(C, std::list<typename C::value_type>)
                )
    {
      container.emplace_back(typename C::value_type(buf));
    }
    
    else if constexpr (  IS_SAME(C, std::set<typename C::value_type>)
                      || IS_SAME(C, std::multiset<typename C::value_type>)
                      )
    {
      container.emplace(typename C::value_type(buf));
    }
    else if constexpr ( IS_SAME(C, std::forward_list<typename C::value_type>) )
    {
      container.emplace_front(typename C::value_type(buf));
    }   
    else
    {
      static_assert( false,"type C is not tabulate");
    }    
  }while(!f2read.eof());

  
  /* en caso de error lo reportamos al finalizar */
  if(!f2read.eof())
  {
    auto st = f2read.rdstate();
    if(st && std::ifstream::eofbit)
      throw EXCEPTION ("End-of-File reached on input operation, buf len <%i> bytes"
                      ,sizeof(buf)); 

    if(st && std::ifstream::failbit)
      throw EXCEPTION("Logical error on i/o operation"); 
    
    if(st && std::ifstream::badbit)
      throw EXCEPTION("Read/writing error on i/o operation");

    throw EXCEPTION("Error desconocido <%i>",st);
  }  
  f2read.close();

  if constexpr ( IS_SAME(C, std::forward_list<typename C::value_type>))
  {    
    if( std::distance(std::begin(container),std::end(container)) == 0)
      throw EXCEPTION ("Archivo <%s> Vacio (o solo contiene comentarios)"
                      ,pathname);
  }   
  else
  {
    if(container.size() == 0)
      throw EXCEPTION ("Archivo <%s> Vacio (o solo contiene comentarios)"
                      ,pathname);
  }  
}

#elif ( VERSION == 1 )
/* PSocket::StreamServer for response 0210 */
#include <bits/stdc++.h>
#include <PSocket.hpp>

/*
* ******************************************************************************** 
* \fn int main(int argc, char* argv[]);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char* argv[])
{ 
  try
  {
    char *port, *ip = nullptr;
    if(argc < 2)
    {
      fprintf(stdout, "Usage: <%s [ip] [port]> host port msg...\n", argv[0]);
      exit(EXIT_SUCCESS);
    }    
    if(argc > 2)
    {
      ip = argv[1];
      port = argv[2];
    }
    else{
      port = argv[1];
    }
    char buf[1024];   // buffer para el print de info    
    std::string response;
    std::string code;  // get input message from cli

    PSocket::StreamServer sck ( (const char*) ip
                              , (const char*) port
                              , PSocket::FmtLen::FMT4B 
                              );
    sck.Connect(buf,sizeof(buf));
    fprintf(stdout, "Server Up in <%s>\n", buf);
    sck.Accept(buf,sizeof(buf));
    fprintf(stdout, "Connected to Client <%s>\n", buf);
    
    sck.Recv(buf,sizeof(buf));
    if(buf[0] == '\0')
    {
      std::cout<<"End Chat, bye...\n";  
      exit(EXIT_SUCCESS);
    }
    fprintf(stdout,"Msg Arrivado <%s>\n", buf);

    std::cout<<"Ingrese Codigo de Respuesta: ";
    std::cin>>code;      
    if(code == "" )
    {
      sck.Send("");
      usleep(1000);    
      exit(EXIT_SUCCESS);
    }      
    response = "0210" + code;
    sck.Send(response);
    usleep(1000); //wait 1 mSec to proccess response 
    sck.Disconnect();    
  }  
  catch(const std::exception &e)  
  {
    std::cout<<"Excepcion Capturada \"" 
            << e.what() <<'\"'<< std::endl;
  }
  catch(...)
  {
    std::cout<<"Excepcion Desconocida"<<std::endl;

  }
  
  std::cout << std::endl;
  exit(EXIT_SUCCESS);
} 

#elif ( VERSION == 2 )
/* FIXME */
#include <bits/stdc++.h>


/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{ 
  try
  { 
   
  }
  catch(const std::exception &e)  
  {
    std::cout<<"Excepcion Capturada \"" 
             << e.what() <<'\"'<< std::endl;
  }
  catch(...)
  {
    std::cout<<"Excepcion Desconocida"<<std::endl;
  }
  
  exit(EXIT_SUCCESS);
}   


#elif ( VERSION == 3 )
/* FIXME  */
#include <bits/stdc++.h>


/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{  
  try
  {

    
  }
  catch(const std::exception &e)
  {
    std::cout<<"Excepcion Capturada \"" 
            << e.what() <<'\"'<< std::endl;
  }
  catch(...)
  {
    std::cout<<"Excepcion Desconocida"<<std::endl;

  }
  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}

#elif ( VERSION == 4 )
/* FIXME  */
#include <bits/stdc++.h>

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{  
  
  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}                


#elif ( VERSION == 5 )
/* FIXME  */
#include <bits/stdc++.h>

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{  
  
  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}

#elif ( VERSION == 6 )
/* FIXME */
#include <bits/stdc++.h>

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{   

  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}

#elif ( VERSION == 7 )
/* FIXME */
#include <bits/stdc++.h>

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{   

  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}

#elif ( VERSION == 8 )
/* FIXME */
#include <bits/stdc++.h>

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{   

  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}

#elif ( VERSION == 9 )
/* FIXME */
#include <bits/stdc++.h>

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{   

  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}

#elif ( VERSION == 10 )
/* FIXME */
#include <bits/stdc++.h>

/*
* ******************************************************************************** 
* \fn int main(int argc, char **argv);
* \brief Funcion Principal
* \param argc : cantidad de Argumentos pasados al invocar la app.
* \param argv : puntero a puntero que contiene el listado de
* \return status de la ejecucion de la app.
*      \li 0, success
*      \li 1, failure
*********************************************************************************/
int main(int argc, char **argv)
{   

  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}
#else



#endif
