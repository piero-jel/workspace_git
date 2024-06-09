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
#include <iostream>
#include <fstream>
#include <exception>
#include <forward_list>
#include <algorithm>
#include <string>
#include <iomanip>  /* std::setfill, std::setw */
/* header c */
#include <cstring>
#include <cstdint>
#include <cstdlib>
#include <cstdarg>

//#include <bits/stdc++.h>

/* BEGIN class Exception */
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
    * catch(const Exception& e)
    * {
    *   std::cout<<"catch(const Exception& e):      "<<e.what();
    * }
    * \endcode
    */
    virtual const char* what(void) const noexcept
    { return (const char*) this->_buff; }     
};
/* END   class Exception */

/* BEGIN class Registro */
/**
 * @brief Objeto para el manejo de los Registros 
 * Numericos.
 */
class Registro {
  int64_t __val{};

  public:
    static constexpr uint32_t LEN = 10;
    static constexpr char FILL = '0';
    /**
     * @brief Construct a new Registro object
     * @param[in] v optional value 
     */
    Registro(int64_t v=0);

    #if 0 /* en este caso no es necesario no tenemos grandes 
     recursos y los metodos usados no implican el uso de este     
     */
    /**
     * @brief Construct por movimiento.
     * @param obj 
     */
    Registro(Registro&& obj)
    {
      this->__val = obj.__val;
      obj.__val = 0;
    }
    #endif
    /**
     * @brief Construct por copia
     * @param[in] obj objeto que se copiara para crear este
     */
    Registro(const Registro& obj)
    {
      this->__val = obj.__val;
    }

    /**
     * @brief Construct a new Registro object
     * @param[in] str value format CStyle string
     */
    Registro(const char* str);

    /**
     * @brief Construct a new Registro object
     * @param[in] str value format string
     */
    Registro(const std::string& str);

    /**
     * @brief redefinicon del operador de coparacion igual
     * @param[in] v value a comparar
     * @return true equal
     * @return false not equal
     */
    bool operator == (int64_t v) const noexcept  ;
    bool operator != (int64_t v) const noexcept  
    {
      return (this->__val != v)?true:false;
    }

    /**
     * @brief metodo para establecer el valor del registro
     * mediante un string
     * @param[in] str CStyle string
     */
    void set(const char* str);

  /**
   * @brief metodos friend que se encarga de sacar un
   * objeto por \p std::ostream
   * Este metodo como tal tendran acceso a metodos/miembros privados/protected
   * @param[in,out] ou std::ostream
   * @param[in] obj objeto
   * @return std::ostream&
   */
    friend std::ostream& operator<< (std::ostream& ou,const Registro& obj);

  /**
   * @brief metodos friend que se encarga llenar un objeto obteniendo los datos 
   * desde \p std::istream. Este metodo como tal tendra acceso a 
   * metodos/miembros privados/protected
   *
   * @param[in,out] in std::istream
   * @param[in] obj Objeto
   * @return std::istream&
   */
    friend std::istream& operator>> (std::istream& in,Registro& obj);
};
/* END   class Registro */

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
int main(int /*argc*/, char* /*argv*/ [])
{  
  using T = Registro;
  using Container = std::forward_list<T>;
  std::string pathfle;
  try
  { 
    const auto lmb_print = []( const char* msg
                          , const auto& container
                          , const char* sep = "\n"
                          , std::ostream& ou=std::cout) -> void 
    {
      if(msg)
        ou<<msg;      

      auto len = std::distance(std::begin(container),std::end(container));
      for(const auto& it : container)
      {
        ou<<it;
        if(sep && --len > 0)
          ou<<sep;
      }
    };
    Container regs;
    T val;
    do
    {
      std::cout<<"Ingrese un Registro Numerico de hasta 10 Digitos: ";
      std::cin>>val;
      if(val == 0)
        break;
      regs.emplace_front(val);
    }while(1);
    regs.reverse();
    lmb_print("lista de registros:\n",regs);
    std::cout<<'\n';

    
    std::cout<<"Ingrese path/name del Archivo donde se volcara el listado de Registro: ";
    std::cin>>pathfle;

    std::ofstream f2write;
    f2write.exceptions ( std::ifstream::failbit | std::ifstream::badbit );
    f2write.open(pathfle,std::ofstream::out) ;
    if(!f2write.is_open())
    {    
      throw Exception("Error to open path name 'src<%s> source.",pathfle.c_str());      
    }
    
    /* // usamos la expresion lambda en su lugar
    using IT = Container::iterator;
    using CIT = Container::const_iterator;
    CIT itend = std::end(regs);
    for(IT it = std::begin(regs); it != itend; it++)
    {
      f2write<<*it<<'\n';
    }
    */
    lmb_print(nullptr,regs,"\n",f2write);
    f2write.close();
    std::cout <<"Registros volcado al archivo "
              <<pathfle
              <<" de forma Sastifactoria"
              <<'\n';
  }
  catch( const Exception<> &e)  
  {
    std::cout<<"Excepcion Capturada \"" 
             << e.what() <<'\"'<< '\n';
  }
  catch( const std::ifstream::failure& e) {
    std::cout << "Exception opening/writing/closing file "
              << pathfle
              <<'\n';
  }
  catch(...)
  {
    std::cout<<"Excepcion Desconocida"<<'\n';
  }
  std::cout<<std::endl;
  exit(EXIT_SUCCESS);
}   


Registro::Registro(int64_t v)
{ 
  std::string snum = std::to_string(v);
  this->set(snum.c_str());
}

Registro::Registro(const char* str)
{ this->set(str); }

/**
 * @brief Construct a new Registro object
 * @param[in] str value format string
 */
Registro::Registro(const std::string& str)
{ this->set(str.c_str()); }


void Registro::set(const char* str)
{
  if(!str)
  {
    throw Exception("str is nullptr");  
  }
  
  if( auto len = std::strlen(str); len > Registro::LEN)
  {
    throw Exception ("str<%s> length<%i> is too long"
                    ,str,len);
  }

  char* tmp;
  uint64_t v = std::strtoll(str,&tmp,10);
  if(tmp && *tmp != '\0')
  {    
    throw Exception("'%s' not integer value",str);    
  }
  this->__val = v;
}

/**
 * @brief redefinicon del operador de coparacion igual
 * @param[in] v value a comparar
 * @return true equal
 * @return false not equal
 */
bool Registro::operator == (int64_t v) const noexcept  
{ return (this->__val == v)?true:false; }

/**
 * @brief metodos friend que se encarga de sacar un
 * objeto por \p std::ostream
 * Este metodo como tal tendran acceso a metodos/miembros privados/protected
 * @param[out] ou std::ostream
 * @param[in] obj objeto
 * @return std::ostream&
 */
std::ostream& operator<< (std::ostream& ou,const Registro& obj)
{
  ou << std::setfill(Registro::FILL) 
     << std::setw(Registro::LEN)
     << obj.__val;
  return ou;
}

/**
 * @brief metodos friend que se encarga llenar un objeto obteniendo los datos 
 * desde \p std::istream. Este metodo como tal tendra acceso a 
 * metodos/miembros privados/protected
 *
 * @param[in] in std::istream
 * @param[out] obj Objeto
 * @return std::istream&
 */
std::istream& operator>> (std::istream& in,Registro& obj)
{
  char buf[16];
  buf[0] = '\0';
  std::memset(buf,'\0',sizeof(buf));
  in.getline(buf,sizeof(buf)-1,'\n');
  if(in.good())
  {
    obj.set((const char*)buf);
    return in;
  }

  auto st = in.rdstate();
  if(st && std::ifstream::eofbit)
    throw Exception ("End-of-File reached on input operation, buf len <%i> bytes"
                    , sizeof(buf)); 

  if(st && std::ifstream::failbit)
    throw Exception("'Logical error on i/o operation"); 
  
  if(st && std::ifstream::badbit)
    throw Exception("Read/writing error on i/o operation"); 

  throw Exception("Error desconocido <%i>",st);
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
