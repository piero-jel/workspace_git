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
@file registro.hpp
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
Author         Date                 Version      Brief
JEL            2026.05.28     0.0.1   Version Inicial no release

* ********************************************************************************** */
#ifndef __registro_hpp__
#define __registro_hpp__ /**<@brief header module name idem to pragma once */

#include <string>
#include <cstring>
#include <iostream>
#include <fstream>
#include <iomanip>  /* std::setfill, std::setw */
#include <cstdint>

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
        explicit Registro(int64_t v=0);

        /**
        * @brief Construct por copia
        * @param[in] obj objeto que se copiara para crear este
        */
        Registro(const Registro& obj){ this->__val = obj.__val;}

        /**
        * @brief Construct a new Registro object
        * @param[in] str value format CStyle string
        */
        explicit Registro(const char* str);

        /**
        * @brief Construct a new Registro object
        * @param[in] str value format string
        */
        explicit Registro(const std::string& str);

        /**
        * @brief redefinicon del operador de coparacion igual
        * @param[in] v value a comparar
        * @return true equal
        * @return false not equal
        */
        bool operator == (int64_t v) const noexcept ;
        bool operator != (int64_t v) const noexcept ;

        /**
        * @brief metodo para establecer el valor del registro
        * mediante un string
        * @param[in] str CStyle string
        */
        void set(const char* str);
        void set(const std::string& str);
        void set(int64_t val) noexcept;
        int64_t get(void) const noexcept ;

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

#endif /* #ifndef __registro_hpp__ */
