/** ******************************************************************************************************//**
* \addtogroup CardsRegister
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
* \file CardsRegister.hpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief clases y metodos para manejo de registros de tarjetas.
* \details Modelo que describe los registros de lebels de tarjetas

* \version 0.0.1.
* \date Viernes 7 de Junio de 2024.
* \pre pre, condiciones que deben cuplirse antes del llamado,
* \bug bug, depuracion example: Not all memory is freed when deleting an object
* of this class.
* \warning
* \note
* \par \b Change History:
* Author         Date                 Version     Brief
* JEL            2024.05.07           0.0.1       Version Inicial no release
*
* @} doxygen end group definition
* ********************************************************************************************************* */
#ifndef __CardsRegister_hpp__
#define __CardsRegister_hpp__

#include <Exception.hpp>
#include <string>
#include <cstring>
#include <ostream>
#include <istream>
#include <fstream>
#include <cstdint>
#include <iomanip>  /* std::setfill, std::setw */

/* =========================[ BEGIN class Register in File   ]=========================*/
/**
 * @brief Defincion del objeto CardsRegister que modela
 * los registros del archivo de tarjetas
 * LABEL(12)~ID(4BYTES)
 */
struct CardsRegister
{
  char label[13]{}; /**<@brief LABEL(12) el 13° es el terminador '\0' */
  uint16_t id{};  /**<@brief ID(4)  0 ~ 9999 */
  
  
  /**
   * @brief Construct a new CardsRegister object
   * @param[in] i id de tarjeta
   * @param[in] l label de tarjeta   
   */
  CardsRegister( uint16_t i = 0
                , const char* l = nullptr
               ): id{i}
  {
    if(!l)
      return ;
    this->__check_digits(l,0,"Label");
    if(l)
      std::strncpy(this->label,l,sizeof(this->label));
  }

  /**
   * @brief Construct a new CardsRegister object, constructor
   * por \b copia
   * @param o objeto, el cual se va a copiar.
   */
  CardsRegister(const CardsRegister& o)
  {        
    this->id = o.id;
    std::memcpy(this->label,o.label,sizeof(this->label));
  }

  /**
   * @brief Construct a new Cards Register object
   * @param[in] str CStyle string para construir el nuevo objeto
   */
  CardsRegister(char* str)
  { this->set(str); }

  /**
   * @brief Metodo para establecer un objeto CardsRegister
   * en funcion de uns \p str .
   * @param[in] str CStyle string para establecer CardsRegister
   * @return CardsRegister& 
   */
  CardsRegister& set(char* str)
  {
    //this->__check_digits(str,12,"Label");
    this->__check_digits(&str[13],4,"ID");

    char buf[16];
    memcpy(this->label,str,12);
    this->label[12] = '\0';
  
    memcpy(buf,&str[13],4);  
    buf[4] = '\0';
    this->id = atoi(buf);    
    return *this;
  }

  /**
   * @brief redefinicion del operando de asignacion
   * @param[in] o objeto que se tomara como fuente de la copia
   * @return CardsRegister&
   * \note este es usado indirectamente en los algoritmos
   */
  CardsRegister& operator= (const CardsRegister& o)
  {
    this->id = o.id;
    std::memcpy(this->label,o.label,sizeof(this->label));
    return *this;
  }

  /**
   * @brief redefinicon del operador '<' en funcion
   * del time and tps
   * @param[in] o objeto, operando derecho
   * @return true
   * @return false
   * \note en caso de trabajar con contenedores del tipo
   * \p std::set<T> necesitaremos esta sobrecarga de operador.
   */
  bool operator< (const CardsRegister& o) const
  { return ( this->id < o.id)? true:false; }

  /**
   * @brief redefinicion del operador de comparacion
   * @param[in] o objeto, operando derecho
   * @return true
   * @return false
   */
  bool operator== (const CardsRegister& o) const
  {
    if(this->id == o.id && std::strcmp(this->label,o.label)==0 )
      return true;
    return false;
  }

  /**
   * @brief metodos friend que se encarga de sacar un
   * objeto por \p std::ostream
   * Este metodo como tal tendran acceso a
   * metodos/miembros privados/protected
   * @param[out] ou std::ostream
   * @param[in] e  objeto
   * @return std::ostream&
   */
  friend std::ostream& operator<<(std::ostream& ou, const CardsRegister& e);

  /**
   * @brief metodos friend que se encarga llenar un
   * objeto obteniendo los datos desde \p std::istream
   * Este metodo como tal tendra acceso a
   * metodos/miembros privados/protected
   *
   * @param[in] in std::istream
   * @param[out] e Objeto 
   * @return std::istream&
   */
  friend std::istream& operator>>(std::istream& in, CardsRegister& e);

  private:
    void __check_digits(const char* src,uint32_t len=0, const char* msg=nullptr)
    {
      if(len == 0)
        len = std::strlen(src);

      for(uint32_t i = 0; i<len; i++)
      {
        if( std::isdigit(src[i]) == 0)
        {
          throw EXCEPTION ( "%s <%.*s> no esta compuesto solo por digitos"
                          , (msg)?msg:" "
                          , len,src
                          );          
        }
      }
    }
};

/**
 * @brief Redefinicion del operador '<<' para el tipo de dato \p CardsRegister
 * @param[out] ou
 * @param[in] e
 * @return std::ostream&
 */
std::ostream& operator<<(std::ostream& ou, const CardsRegister& e)
{
  /* LABEL(12)~ID(4BYTES) */  
  ou<< e.label << ' '
    << std::setfill('0')<<std::setw(4)<<e.id  << ' ' ;    
  return ou;
}

/**
 * @brief redefinicion del operador '>>' para tipos de datos \p CardsRegister
 * @param[in] in
 * @param[out] e
 * @return std::istream&
 */
std::istream& operator>>(std::istream& in, CardsRegister& e)
{
  char buf[1024];
  buf[0] = '\0';

  in.getline(buf,sizeof(buf),'\n');
  if(in.good())
  {
    e.set(buf);
    return in;
  }
  auto st = in.rdstate();
  if(st && std::ifstream::eofbit)
    throw EXCEPTION ("End-of-File reached on input operation, buf len <%i> bytes"
                    , sizeof(buf)); 

  if(st && std::ifstream::failbit)
    throw EXCEPTION("Logical error on i/o operation"); 
  
  if(st && std::ifstream::badbit)
    throw EXCEPTION("Read/writing error on i/o operation"); 

  throw EXCEPTION("Error desconocido <%i>",st);
}
/* =========================[ END   class Register in File   ]=========================*/
#endif /* #ifndef __CardsRegister_hpp__ */
