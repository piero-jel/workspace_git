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
 * \b VERSION  1 : 
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
#include <financial_transaction.hpp>
#include <PSocket.hpp>




/**
 * \brief Funcion Principal
 * \param[in] argc : cantidad de Argumentos pasados al invocar la app.
 * \param[in] argv : puntero a puntero que contiene el listado de
 * \return status de la ejecucion de la app.
 *    - 0, success
 *    - 1, failure **/
int main(int argc, char* argv[]){
    try{
        char buf[1024];
        CliApp cli(argc,argv);
        cli.print();

        PSocket::StreamClient socket { 
            cli.ip.c_str(),
            cli.port,
            PSocket::FmtLen::FMT4B 
        };
        // 1° conect to Server    
        socket.Connect(buf,sizeof(buf));

        std::fprintf(stdout, "Client Connect to <%s>\n", buf);
        
        // 2° Get Amount
        int64_t amount = GetAmount(
            [](char* ret,uint32_t len){
                std::fputs("Ingrese el monto (hasta 2 decimales Implicitos): ",stdout);
                std::fgets(ret,len-1,stdin);
            }
        );
        
        // 3° Get Card Number
        std::string card_number = GetCardNumber(
            [](char* ret,uint32_t len){
                std::fputs("Ingrese el Numero de Tarjeta ( 13 ~ 99 decimales): ",stdout);                
                std::fgets(ret,len-1,stdin);
            }
        );

        // 4° Verify the card number
        #if ( STD_VER >= 2017 )
        auto [st,reg_rng,reg_card] = VerifyCardNumber (
            card_number,
            cli.frange,
            cli.fcards
        );
        #else
        auto ret = VerifyCardNumber (card_number,
            cli.frange,
            cli.fcards
        );
        auto st = std::get<0>(ret);
        //auto reg_rng = std::get<1>(ret);
        auto reg_card = std::get<2>(ret);
        #endif  
        
        if(!st){
            std::fprintf(stdout,"TARJETA <%s> NO SOPORTADA\n",card_number.c_str());
            exit(EXIT_SUCCESS);
        }
        std::fprintf(stdout,"TARJETA <%s>, CARD LABEL <%s>\n", card_number.c_str(), reg_card.label);
        // 5° Get Card Code 
        std::string card_code = GetCardCode(
            [](char* ret,uint32_t len){
                std::fputs("Ingrese el Codigo de Seguridad (hasta 3 digitos): ",stdout);
                std::fgets(ret,len-1,stdin);
            }
        );
            
        //std::cout<<"El Saldo ingresado es: "<<float(amount/100)<<'\n';
        std::fprintf(stdout,"El Saldo ingresado es: %012.2f\n",float(amount/100));
        std::fprintf(stdout,"El Numero de tarjeta ingresado es: %s\n",card_number.c_str());
        std::fprintf(stdout,"El Codigo de tarjeta ingresado es: %s\n",card_code.c_str());
        
        // 6° put together the petition
        std::string response, request = GetRequest(amount,card_number,card_code);
        std::fprintf(stdout,"Request to send: %s\n",request.c_str());

        // 7° Send Request and Wait Response
        socket.Send(request);    
        socket.Recv(response,double(cli.timeout/1000));

        // 8° Verify the Response
        if(response.length() < 6){
            std::fprintf(stdout,"Response <%s> error, empty or length too short\n",
                response.c_str());
            exit(EXIT_SUCCESS);
        }

        std::fprintf(stdout,"Response: %s\n",response.c_str());
        std::string mtid = response.substr(0,4);
        std::string respcode = response.substr(4,2);
        if(mtid != "0210"){
            std::fprintf ( stdout,"MTID <%s> no esperado operacion abortada\n", mtid.c_str() );
            exit(EXIT_SUCCESS);
        }

        if(respcode == "00"){
            std::fputs("OPERACION APROVADA\n",stdout);
        }
        else{
            std::fprintf(stdout,"OPERACION RECHAZADA CON EL CODIGO <%s>\n", respcode.c_str() );
        }
    }
    catch(const std::exception &e){
        std::fprintf(stdout,"Error \"%s\"",e.what());
    }
    catch(...){
        std::fputs("Error Desconocida",stdout);
    }
    std::fputc('\n',stdout);
    exit(EXIT_SUCCESS);
} 





CliApp::CliApp(int argc,char* argv[],FILE* ou){     
    if(argc == 0 || !argv ) return;
    this->parser(argc,argv,ou);
}

void CliApp::parser(int argc,char** argv,FILE* ou){
    if(!argv || argc < 1) {     
        throw Exception("EINVAL argv equal to null");
    }
    
    if(!ou) ou = stdout;
    
    /* lo primero a establecer para que este disponible en el 
    * heap()
    */
    this->app = basename(argv[0]);
    this->__flag = 0x00;
    if(argc < 2){
        std::fprintf(ou,"Not Option Pass\n");
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
    while ((opt = getopt(argc, argv, "i:p:t:r:c:h")) != -1){
        switch (opt){
            case 'c':
                if(!optarg){
                    std::fprintf(ou,"opcion -c sin path/file-cards\n");
                    this->help(ou);
                }            
                this->fcards = std::string(optarg);
                this->flags(Flag::FCARDS,true);
                break;

            case 'r':
                if(!optarg){
                    std::fprintf ( ou,"opcion -r sin path/file-range\n");
                    this->help(ou);        
                }            
                this->frange = std::string(optarg);
                this->flags(Flag::FRANGE,true);
                break;

            case 't':
                if(!optarg){
                    std::fprintf ( ou,"opcion -t sin cantidad de mili segundos\n");
                    this->help(ou);
                }            
                this->timeout = std::atoi(optarg);
                this->flags(Flag::TIMEOUT,true);
                break;

            case 'p':
                if(!optarg){
                    std::fprintf ( ou,"opcion -p sin numero de puero\n");
                    this->help(ou);
                }            
                this->port = std::atoi(optarg);
                this->flags(Flag::PORT,true);
                break;
            case 'i':
                if(!optarg){
                    std::fprintf ( ou,"opcion -i sin numero de ip\n");
                    this->help(ou);
                }
                this->ip = std::string(optarg);
                this->flags(Flag::IP,true);
                break;

            case 'h':
                this->help(ou); 
                break; /* para evitar warning */

            default:
                std::fprintf(ou,"Option <%c> not found\n",opt);
                this->help(ou);         
        }
    }

    if (optind < argc){
        /* Se pasaron mas arguementos de los devidos */
        std::fprintf(ou,"Se pasaron argumentos no permitido:\n ");
        for(int i = 1 ; i< argc;i++)
            std::fprintf(ou,"argv[%03d] <%s>\n",i,argv[i]);
        
        std::fputc('\n',ou);
        this->help(ou);
    }
    /* Realizamos el check de los parametros mandatorios */
    if(!this->flags( Flag(Flag::FCARDS|Flag::FRANGE) )){
        std::fprintf(ou,"-c <path/card-file> or -r <path/range-file> not found"
            "They are mandatory\n" );
        this->help(ou);  
        exit(EXIT_SUCCESS);
    }  
    /* Realizamos el fill de los opcionales */
    if(!this->flags(Flag::IP)) this->ip = "0.0.0.0";
    
    if(!this->flags(Flag::PORT)) this->port = 3000 ;

    if(!this->flags(Flag::TIMEOUT)) this->timeout = 5000;
}

void CliApp::help(FILE* ou){
    if(!ou) ou = stdout;

    std::fprintf( ou, "Usage: %s [-i ip] [-p port] [-t timeout] "
            "-c path/card-file -r path/range-file\n",
            this->app.c_str()
    );
    std::fprintf(ou, "-i <ip>      : numero de ip Server, opcional por defecto localhost\n");  
    std::fprintf(ou, "-p <port>    : numero de puerto, opcional por defecto 3000\n");
    std::fprintf(ou, "-t <timeout> : tiempo de espera maximo por respuesta del server, opcional por defecto 5000 [mSec]\n");
    std::fprintf(ou, "-c <path/card-file>: ruta y nombre de archivo de tarjetas\n");
    std::fprintf(ou, "-r <path/range-file>: ruta y nombre de archivo de rangos\n");
    std::fprintf(ou, "-h print this help message\n");
    exit(EXIT_SUCCESS);
}

void CliApp::print(FILE* ou){
    if(!ou) ou = stdout;
    
    std::fprintf(ou, "-i <ip>      : %s\n",this->ip.c_str());
    std::fprintf(ou, "-p <port>    : %i\n",this->port);
    std::fprintf(ou, "-t <timeout> : %i [mSec]\n",this->timeout);
    std::fprintf(ou, "-c <path/card-file>: %s\n",this->fcards.c_str());
    std::fprintf(ou, "-r <path/range-file>: %s\n",this->frange.c_str());
}

void CliApp::flags(Flag flag,bool st){
    if(flag > Flag::ALL || flag == Flag::NONE) return ;
  
    if(st) 
        this->__flag |= flag;
    else
        this->__flag |= ~flag;

}

bool CliApp::flags(Flag flag) {
    return (this->__flag & flag)?true:false;
}




#elif ( VERSION == 1 )
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
