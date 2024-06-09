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
/** 
 * \b VERSION  0 : checkAnagrama() con metodo sort in string
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
/* checkAnagrama */
#include <iostream>
#include <exception>
#include <vector>
#include <algorithm>
#include <string>
#include <cstring>
#include <memory>

/**
 * @brief Funcion para verificar si dos palabras son un anagrama.
 * Una cadena es un anagrama de otra si la segunda es simplemente un 
 * reordenamiento de la primera. Por ejemplo, \b 'fresa' y \b 'frase' son 
 * anagramas. Las cadenas \b 'caro' y \b 'roca' son también anagramas.
 * 
 * @param[in] op1 operando uno de la operacion
 * @param[in] op2 operando dos de la operacion
 * \param[in] sen optional, este nos permite habilitar o deshabilitar la 
 * comparacion sensitiva entre mayuscula y minuscula. Por defecto \b false 
 * 'deshabilitado el sensistive case'
 * @return true es un anagrama
 * @return false no es un anagrema
 */
bool checkAnagrama( const std::string& op1, const std::string& op2,bool sen=false);

/**
 * @brief Funcion para verificar si dos palabras son un anagrama. 
 * Una cadena es un anagrama de otra si la segunda es simplemente un 
 * reordenamiento de la primera. Por ejemplo, \b 'fresa' y \b 'frase' son 
 * anagramas. Las cadenas \b 'caro' y \b 'roca' son también anagramas.
 * 
 * @param[in] op1 operando uno de la operacion
 * @param[in] op2 operando dos de la operacion
 * \param[in] sen optional, este nos permite habilitar o deshabilitar la 
 * comparacion sensitiva entre mayuscula y minuscula. Por defecto \b false 
 * 'deshabilitado el sensistive case'
 * @return true es un anagrama
 * @return false no es un anagrema
 */
bool checkAnagrama( const char* op1, const char* op2,bool sen=false);


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
  using Container = std::vector<std::string>;
  using Size = std::vector<std::string>::size_type;
  using IT = Container::iterator;
  using CIT = Container::const_iterator;
  /*
  Container vcta {"Hola","caro","fresa","emanuel"};
  Container vctb {"chau","roca","fresa","Lalo"};
  */
  Container vcta,vctb;
  if(argc>1 && (argc-1)%2 )
  {
    std::cout<<"La cantidad de palabras debe ser par: <op1> <op2>, para el anagrama\n";
    exit(EXIT_SUCCESS);
  }

  try
  { 
    if(argc < 2)
    {
      for(const auto& it :{"Hola","caro","fresa","emanuel"})
      {
        vcta.emplace_back(it);
      }
      for(const auto& it : {"chau","roca","fresa","Lalo"})
      {
        vctb.emplace_back(it);
      }
    }
    else
    {
      for(int i=1; i<argc; i +=2)
      {
        vcta.emplace_back(argv[i]);
        vctb.emplace_back(argv[i+1]);
      }
    }

    const auto lmb_checkAnagrama = [](const std::string& src1, const std::string& src2 ) -> bool {
      if(src1.length() != src2.length())
        return false;
      std::string a = src1, b = src2;
      std::sort(a.begin(),a.end());
      std::sort(b.begin(),b.end());
      if(a == b)
        return true;
      return false;
    };

    /* usando la expresion lamda */
    std::cout<<"usando la expresion lamda lmb_checkAnagrama()" << '\n';
    const Size& max = vcta.size();
    Size i;
    for(i = 0; i < max ;i++)
    {
      if(lmb_checkAnagrama(vcta.at(i),vctb.at(i)))
      {
        fprintf(stdout,"Datagram <%s> - <%s>\n", vcta.at(i).c_str(),vctb.at(i).c_str());
      }
      else
        fprintf(stdout,"No Datagram <%s> - <%s>\n", vcta.at(i).c_str(),vctb.at(i).c_str());        
    }  
    /* usando la funcion */    
    
    CIT end = vcta.cend();

    IT ita;
    IT itb;
    std::cout<<"\n\nUsando la funcion checkAnagrama([std::string])" << '\n';
    for(ita = vcta.begin(),itb = vctb.begin(); ita != end ; ita++,itb++)
    {
      if(checkAnagrama(*ita,*itb,true))
      {
        fprintf(stdout,"Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());
      }
      else
        fprintf(stdout,"No Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());
    }  

    std::cout<<"\n\nUsando la funcion checkAnagrama([char*])" << '\n';
    for(ita = vcta.begin(),itb = vctb.begin(); ita != end ; ita++,itb++)
    {
      if(checkAnagrama(ita->c_str(),itb->c_str(),true))
      {
        fprintf(stdout,"Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());
      }
      else
        fprintf(stdout,"No Datagram <%s> - <%s>\n", ita->c_str(),itb->c_str());
    } 
    
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

bool checkAnagrama( const std::string& op1
                  , const std::string& op2
                  , bool sen
                  )
{
  if (op1.length() != op2.length())
    return false;

  std::string a=op1,b=op2;

  if(sen)
  {
    const auto lmb_toupper = [](char l) -> char { return std::toupper(l);};
    std::transform( std::begin(op1),std::end(op1),std::begin(a)
                  , lmb_toupper);

    std::transform( std::begin(op2),std::end(op2),std::begin(b)
                  , lmb_toupper);
  } 

  std::sort(a.begin(),a.end());
  std::sort(b.begin(),b.end());
  if(a == b )
    return true;
  
  return false;  
}

bool checkAnagrama( const char* op1, const char* op2,bool sen)
{
  auto len = std::strlen(op1);
  if (!op1 || !op2 ||  len != std::strlen(op2))
    return false;

  std::unique_ptr<char[], void(*)(void*)> a (strdup(op1),free);
  std::unique_ptr<char[], void(*)(void*)> b (strdup(op2),free);
  
  if(sen)
  {
    const auto lmb_toupper = [](char l) -> char { return std::toupper(l);};
    std::transform( op1,op1+len,a.get()
                  , lmb_toupper);

    std::transform( op2,op2+len, b.get()
                  , lmb_toupper);
  }

  /* ordenamos cada uno*/
  std::sort(a.get(),a.get()+len);
  std::sort(b.get(),b.get()+len);
  
  return std::strcmp(a.get(),b.get())? false: true;

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
