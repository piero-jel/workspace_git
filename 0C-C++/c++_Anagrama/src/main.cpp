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
* \brief Verificacion de palabras, \b Anagrama.
* \details Una palabra es \b Anagrama de otra si las dos tienen las mismas letras, con el mismo número de apariciones,
* pero en un orden diferente.

* \version 0.0.1.
* \date Jueves 6 de Junio de 2024.
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



/* checkAnagrama */
#include <iostream>
#include <exception>
#include <vector>
#include <algorithm>

#include <check_anagrama.hpp>


/**
 * \brief Funcion Principal
 * \param[in] argc : cantidad de Argumentos pasados al invocar la app.
 * \param[in] argv : puntero a puntero que contiene el listado de
 * \return status de la ejecucion de la app.
 *    - 0, success
 *    - 1, failure 
 * **/
int main(int argc, char **argv) {  
    using Container = std::vector<std::string>;
    using Size = std::vector<std::string>::size_type;
    using IT = Container::iterator;
    using CIT = Container::const_iterator;

    Container vcta,vctb;
    if(argc>1 && (argc-1)%2 ){
        std::fputs("La cantidad de palabras debe ser par: <op1> <op2>, para el anagrama\n",stdout);
        exit(EXIT_SUCCESS);
    }

    try{ 
        if(argc < 2){
            for(const auto& it :{"Hola","caro","fresa","emanuel"}){
                vcta.emplace_back(it);
            }
            for(const auto& it : {"chau","roca","fresa","Lalo"}){
                vctb.emplace_back(it);
            }
        }
        else{
            for(int i=1; i<argc; i +=2){
                vcta.emplace_back(argv[i]);
                vctb.emplace_back(argv[i+1]);
            }
        }

        const auto lmb_checkAnagrama = [](const std::string& src1, 
            const std::string& src2 ) -> bool {
            if(src1.length() != src2.length())
                return false;
            std::string a = src1, b = src2;
            std::sort(a.begin(),a.end());
            std::sort(b.begin(),b.end());
            
            return (a == b)?true:false;
        };

        /* usando la expresion lamda */
        std::fputs("usando la expresion lamda lmb_checkAnagrama()\n",stdout);
        const Size& max = vcta.size();
        Size i;
        for(i = 0; i < max ;i++){
            if(lmb_checkAnagrama(vcta.at(i),vctb.at(i)))
                std::fprintf(stdout,"Datagram <%s> - <%s>\n",
                    vcta.at(i).c_str(),vctb.at(i).c_str());
            else
                std::fprintf(stdout,"No Datagram <%s> - <%s>\n",
                    vcta.at(i).c_str(),vctb.at(i).c_str());        
        }  
        
        /* usando la funcion */        
        CIT end = vcta.cend();

        IT ita;
        IT itb;
        std::fputs("\n\nUsando la funcion checkAnagrama([std::string])\n",stdout);
        for(ita = vcta.begin(),itb = vctb.begin(); ita != end ; ita++,itb++){
            if(checkAnagrama(*ita,*itb,true))            
                std::fprintf(stdout,"Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());            
            else
                std::fprintf(stdout,"No Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());            
        }
        std::fputs("\n\nUsando la funcion checkAnagrama([char*])\n",stdout);
        for(ita = vcta.begin(),itb = vctb.begin(); ita != end ; ita++,itb++) {
            if(checkAnagrama(ita->c_str(),itb->c_str(),true))
                std::fprintf(stdout,"Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());
            else
                std::fprintf(stdout,"No Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());
        } 
    }
    catch(const std::exception &e){
        std::fprintf(stdout,"Excepcion Capturada \"%s\"\n",e.what());
    }
    catch(...) {
        std::fputs("Excepcion Desconocida",stdout);
    }    
    std::fputc('\n',stdout);
    exit(EXIT_SUCCESS);
}   


