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
* \brief Registro de Numeros de hasta 10 digitos.
* \details Se registran \b N numeros ingresados por el usaurio y cuando este ingrese 
* el valor '0' se finaliza el ingreso y se vuelca el listado de nuemros en un 
* archivo. El cual su path/files es peticionado al usuario.

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
/** 
 * \b VERSION  0 : Registro Numerico version 0.0.1
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
/* Registro Numerico version 0.0.1 */


#include <forward_list>
#include <algorithm>

/* header c */
#include <cstdlib>
//#include <cstdarg>

// workspace header
#include <registro.hpp>
#include <Exception.hpp>





/**
 * \brief Funcion Principal
 * \param[in] argc : cantidad de Argumentos pasados al invocar la app.
 * \param[in] argv : puntero a puntero que contiene el listado de
 * \return status de la ejecucion de la app.
 *    - 0, success
 *    - 1, failure **/
int main(int /*argc*/, char* /*argv*/ []) {  
    using Container = std::forward_list<Registro>;
    std::string pathfle;
    try{ 
        const auto lmb_print = [](
            const char* msg, 
            const auto& container,
            const char* sep = "\n",
            std::ostream& ou=std::cout) -> void {

            if(msg)
                ou<<msg;

            auto len = std::distance(std::begin(container),std::end(container));
            for(const auto& it : container){
                ou<<it;
                if(sep && --len > 0) ou<<sep;
            }
        };
        Container regs;
        Registro val;
        do{
            std::fputs("Ingrese un Registro Numerico de hasta 10 Digitos: ",stdout);
            std::cin>>val;
            if(val == 0) break;
            regs.emplace_front(val);
        }while(1);

        regs.reverse();
        lmb_print("lista de registros:\n",regs);
        std::cout<<'\n';
        
        std::fputs("Ingrese path/name del Archivo donde se volcara el listado de Registro: ",stdout);
        std::cin>>pathfle;

        std::ofstream f2write;
        f2write.exceptions ( std::ifstream::failbit | std::ifstream::badbit );
        f2write.open(pathfle,std::ofstream::out) ;
        if(!f2write.is_open()) {    
            throw Exception("Error to open path name 'src<%s> source.",pathfle.c_str());      
        }
        
        lmb_print(nullptr,regs,"\n",f2write);
        f2write.close();
        std::fprintf(stdout,"Registros volcado al archivo '%s' de forma Sastifactoria\n",
            pathfle.c_str());                
    }
    catch( const Exception<> &e){
        std::fprintf(stdout,"Excepcion Capturada \"%s\"\n",e.what());
    }
    catch( const std::ifstream::failure& e) {
        std::fprintf(stdout,"Exception opening/writing/closing file %s\n",pathfle.c_str());        
    }
    catch(...) {
        std::fputs("Excepcion Desconocida\n",stdout);
    }
    std::fputc('\n',stdout);
    exit(EXIT_SUCCESS);
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
