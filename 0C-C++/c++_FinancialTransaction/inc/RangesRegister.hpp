/** ******************************************************************************************************//**
* \addtogroup RangesRegister
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
* \file RangesRegister.hpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief clases y metodos para manejo de registros de rango.
* \details Modelo que describe los registros de rango
* \version 0.0.1.
* \date Viernes 7 de Junio de 2024.
* \pre pre, condiciones que deben cuplirse antes del llamado,
* \bug bug, depuracion example: Not all memory is freed when deleting an object
* of this class.
* \warning
* \note
* \par \b Change History:
* Author         Date                 Version     Brief
* JEL            2024.05.07          0.0.1       Version Inicial no release
*
* @} doxygen end group definition
* ********************************************************************************************************* */
#ifndef __RangesRegister_hpp__
#define __RangesRegister_hpp__

#include <Exception.hpp>
#include <ostream>
#include <istream>
#include <fstream>
#include <cstdint>
#include <iomanip>  /* std::setfill, std::setw */


/* =========================[ BEGIN class Register in File   ]=========================*/
/**
 * @brief Defincion del objeto RangesRegister que modela
 * los registros del archivo de rangos
 * RANGE_LOW(8)~RANGE_HIGHT(8)~LEN(2BYTES)~ID(4BYTES)
 */
struct RangesRegister
{
  char low[9]{};  /**<@brief RANGE_LOW(8) el 9° es el terminador '\0' */
  char high[9]{}; /**<@brief RANGE_HIGHT(8) el 9° es el terminador '\0' */  
  uint8_t len{};  /**<@brief LEN(2) 0 ~   99 */
  uint16_t id{};  /**<@brief ID(4)  0 ~ 9999 */
  
  /**
   * @brief Construct a new RangesRegister object.
   * @param[in] rl low range
   * @param[in] rh higth range
   * @param[in] l length
   * @param[in] i id
   */
  RangesRegister( const char* rl = nullptr
                , const char* rh = nullptr
                , uint8_t l=0
                , uint16_t i = 0)
  :len{l},id{i}
  {
    if(!rl || !rh)
      return ;
    if(!this->__check_digits(rl))
      throw EXCEPTION ("Low range <%s> no esta compuesto solo por digitos"
                      ,rl);
    
    if(!this->__check_digits(rh))
      throw EXCEPTION ("Hight range <%s> no esta compuesto solo por digitos"
                      ,rh);
    
    if(rl)
      std::strncpy(this->low,rl,sizeof(this->low));

    if(rh)
      std::strncpy(this->high,rh,sizeof(this->high));
  }

  /**
   * @brief Construct a new Cards RangesRegister object
   * @param[in] str CStyle string para construir el nuevo objeto
   */
  RangesRegister(char* buf)
  { this->set(buf); }

  /**
   * @brief Construct a new RangesRegister object, constructor
   * por \b copia
   * @param[in] o objeto, el cual se va a copiar.
   */
  RangesRegister(const RangesRegister& o)
  {        
    this->id = o.id;
    this->len = o.len;

    std::memcpy(this->low,o.low,sizeof(this->low));
    std::memcpy(this->high,o.high,sizeof(this->high));
  }

  /**
   * @brief Metodo para establecer un objeto RangesRegister
   * en funcion de uns \p str .
   * @param[in] str CStyle string para establecer RangesRegister
   * @return RangesRegister& 
   */
  RangesRegister& set(char* str)  
  {
    char buf[8];
    const char* exmsg = "no esta compuesto solo por digitos";
    
    if(!this->__check_digits(str,8))
      throw EXCEPTION ("Part low range <%.*s> %s"
                      ,8,str,exmsg);
    
    if(!this->__check_digits(&str[9],8))
      throw EXCEPTION("Part high range <%.*s> %s"
                      ,8,&str[9],exmsg);

    if(!this->__check_digits(&str[18],2))
      throw EXCEPTION("Part len <%.*s> %s"
                      ,2,&str[18],exmsg);

    if(!this->__check_digits(&str[21],4))
      throw EXCEPTION("Part id <%.*s> %s"
                      ,4,&str[21],exmsg);

    std::memcpy(this->low,str,8);
    this->low[8] = '\0';
    std::memcpy(this->high,&str[9],8);
    this->high[8] = '\0';

    std::memcpy(buf,&str[18],2);
    buf[2] = '\0';
    this->len = uint8_t(atoi(buf));

    std::memcpy(buf,&str[21],4);
    buf[4] = '\0';
    this->id = uint16_t(atoi(buf));
    return *this;
  }

  /**
   * @brief redefincion del operando de asignacion
   * @param o objeto, operando derecho
   * @return RangesRegister&
   * \note este es usado indirectamente en los algoritmos
   */
  RangesRegister& operator= (const RangesRegister& o)
  {
    this->id = o.id;
    this->len = o.len;
    std::memcpy(this->low,o.low,sizeof(this->low));
    std::memcpy(this->high,o.high,sizeof(this->high));
    return *this;
  }

  /**
   * @brief redefinicon del operador '<' en funcion del id
   * @param[in] o objeto, operando derecho
   * @return true
   * @return false
   * \note en caso de trabajar con contenedores del tipo
   * \p std::set<T> necesitaremos esta sobrecarga de operador.
   */
  bool operator< (const RangesRegister& o) const
  { return ( this->id < o.id) ? true : false ;  }

  /**
   * @brief redefinicion del operando de comparacion
   * @param[in] o objeto, con el cual compara
   * @return true
   * @return false
   */
  bool operator== (const RangesRegister& o) const
  {
    if(this->id == o.id && this->len == o.len
      && (std::strcmp(this->high,o.high) == 0)
      && (std::strcmp(this->low,o.low) == 0)
      )
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
  friend std::ostream& operator<<(std::ostream& ou, const RangesRegister& e);

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
  friend std::istream& operator>>(std::istream& in, RangesRegister& e);
  private:
    bool __check_digits(const char* src,uint32_t len=0)
    {
      if(len == 0)
        len = std::strlen(src);

      for(uint32_t i = 0; i<len; i++)
      {
        if( std::isdigit(src[i]) == 0)
        {
          return false;
        }
      }
      return true;
    }
};

/**
 * @brief Redefinicion del operador '<<' para el tipo de dato \p RangesRegister
 *
 * @param[out] ou
 * @param[in] e
 * @return std::ostream&
 */
std::ostream& operator<<(std::ostream& ou, const RangesRegister& e)
{
  /* RANGE_LOW(8)~RANGE_HIGHT(8)~LEN(2BYTES)~ID(4BYTES) */  
  ou<< e.low  <<' '
    << e.high <<' '
    << std::setfill('0')<<std::setw(2)<<e.len << ' '
    << std::setfill('0')<<std::setw(4)<<e.id  << ' ' ;
  return ou;
}

/**
 * @brief redefinicion del operador '>>' para tipos de datos \p RangesRegister
 * @param[in] in
 * @param[out] e
 * @return std::istream&
 */
std::istream& operator>>(std::istream& in, RangesRegister& e)
{
  char buf[1024];
  buf[0] = '\0';

  in.getline(buf,sizeof(buf)-1,'\n');
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


struct PredicateRange
{
  char cardn[9];
  PredicateRange(const std::string& c)
  {
    std::memcpy(this->cardn,c.c_str(),8);
    this->cardn[8] = '\0';
  }

  bool operator()(const RangesRegister& o)
  {   
    int cmp; 
    /* verificamos si esta debajo de high -1 
    * int strcmp(const char *s1, const char *s2);
    *  + 0, if the s1 and s2 are equal;
    *  + a negative value if s1 is less than s2;
    *  + a positive value if s1 is greater than s2.
    */
    cmp = std::strcmp(this->cardn,o.high);
    if(cmp == 0)
      return true;

    if (cmp > 0 )
      return false;

    cmp = std::strcmp(this->cardn,o.low);
    if(cmp >= 0)
      return true;

    return false;
  }
};

/* =========================[ END   class Register in File   ]=========================*/
#endif /* #ifndef __RangesRegister_hpp__ */
