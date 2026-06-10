/** ***********************************************************************************//**
\addtogroup registronumerico
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
@file registro.cpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.1.
@date Jueves 28 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version      Brief
JEL            2026.05.28     0.0.1        Version Inicial no release

* ********************************************************************************** */
#include <registro.hpp>
#include <utilities>

using namespace utilities;


Registro::Registro(int64_t v) {
    std::string snum = std::to_string(v);
    this->set(snum.c_str());
}

Registro::Registro(const char* str) { this->set(str); }

/**
 * @brief Construct a new Registro object
 * @param[in] str value format string
 */
Registro::Registro(const std::string& str) { this->set(str.c_str()); }

int64_t Registro::get(void) const noexcept {
    return this->__val;
}

void Registro::set(int64_t val) noexcept{
    this->__val = val;
}
void Registro::set(const std::string& str){
    return this->set(str.c_str());
}

void Registro::set(const char* str) {
    if(!str){
        throw Exception("str is nullptr");
    }

    if( auto len = std::strlen(str); len > Registro::LEN) {
        throw Exception ("str<%s> length<%i> is too long",str,len);
    }

    char* tmp;
    uint64_t v = std::strtoll(str,&tmp,10);
    if(tmp && *tmp != '\0'){
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
bool Registro::operator == (int64_t v) const noexcept { return (this->__val == v)?true:false; }
bool Registro::operator != (int64_t v) const noexcept { return (this->__val != v)?true:false; }

/**
 * @brief metodos friend que se encarga de sacar un
 * objeto por \p std::ostream
 * Este metodo como tal tendran acceso a metodos/miembros privados/protected
 * @param[out] ou std::ostream
 * @param[in] obj objeto
 * @return std::ostream&
 */
std::ostream& operator<< (std::ostream& ou,const Registro& obj){
    ou  << std::setfill(Registro::FILL)
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
std::istream& operator>> (std::istream& in,Registro& obj) {
    char buf[16];
    buf[0] = '\0';
    std::memset(buf,'\0',sizeof(buf));
    in.getline(buf,sizeof(buf)-1,'\n');
    if(in.good()){
        obj.set((const char*)buf);
        return in;
    }

    auto st = in.rdstate();
    if(st && std::ifstream::eofbit)
        throw Exception("End-of-File reached on input operation, buf len <%i> bytes",sizeof(buf));

    if(st && std::ifstream::failbit)
        throw Exception("'Logical error on i/o operation");

    if(st && std::ifstream::badbit)
        throw Exception("Read/writing error on i/o operation");

    throw Exception("Error desconocido <%i>",st);
}


