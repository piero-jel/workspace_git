/** ***********************************************************************************//**
\addtogroup FinancialTransaction
\copyright Copyright &copy; 2026, Jesus Emanuel Luccioni
All rights reserved.

This file is part of devops for Open Container (in this case docker )

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
contributors may be used to endorse or promote products derived from this
software without specific prior written permission.

THIS SCRIPT IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SCRIPT, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
@file server.cpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.1.
@date Miercoles 27 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version      Brief
JEL            2026.05.27     0.0.1        Version Inicial no release

* ********************************************************************************** */
#include <iostream>
#include <cstdlib>
#include <string>
#include <unistd.h>

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
        char *port, *ip = nullptr;
        if(argc < 2){
            std::fprintf(stdout, "Usage: <%s [ip] [port]> host port msg...\n", argv[0]);
            exit(EXIT_SUCCESS);
        }
        if(argc > 2){
            ip = argv[1];
            port = argv[2];
        }
        else{
            port = argv[1];
        }
        char buf[1024];   // buffer para el print de info
        std::string response;
        std::string code;  // get input message from cli

        PSocket::StreamServer sck ( (const char*) ip,(const char*) port);

        sck.Connect(buf,sizeof(buf));
        std::fprintf(stdout, "Server Up in <%s>\n", buf);
        int fd = sck.Accept(buf,sizeof(buf));
        std::fprintf(stdout, "Connected to Client <%s>\n", buf);

        PSocket::Stream stream (fd,PSocket::FmtLen::FMT4B);
        stream.Recv(buf,sizeof(buf));
        if(buf[0] == '\0'){
            std::fputs("End Chat, bye...\n",stdout);
            exit(EXIT_SUCCESS);
        }
        std::fprintf(stdout,"Msg Arrivado <%s>\n", buf);

        std::fputs("Ingrese Codigo de Respuesta: ",stdout);
        std::cin>>code;
        if(code == "" ){
            stream.Send("");
            usleep(1000);
            exit(EXIT_SUCCESS);
        }
        response = "0210" + code;
        stream.Send(response);
        usleep(1000); //wait 1 mSec to proccess response
        stream.Disconnect();
        sck.Disconnect();
    }
    catch(const std::exception &e){
        std::fprintf(stdout,"Excepcion Capturada '%s'\n",e.what());
    }
    catch(...){
        std::fputs("Excepcion Desconocida\n",stdout);
    }
    std::fputc('\n',stdout);
    exit(EXIT_SUCCESS);
}
