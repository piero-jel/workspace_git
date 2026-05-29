/** ***********************************************************************************//**
\addtogroup financial_transaction
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
@file CardsRegister.cpp
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
Author         Date                 Version      Brief
JEL            2026.05.27     0.0.1   Version Inicial no release

* ********************************************************************************** */
#include <CardsRegister.hpp>







/**
 * @brief Redefinicion del operador '<<' para el tipo de dato \p CardsRegister
 * @param[out] ou
 * @param[in] e
 * @return std::ostream&
 */
std::ostream& operator<<(std::ostream& ou, const CardsRegister& e){
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
std::istream& operator>>(std::istream& in, CardsRegister& e){
    char buf[1024];
    buf[0] = '\0';

    in.getline(buf,sizeof(buf),'\n');
    if(in.good()){
        e.set(buf);
        return in;
    }
    auto st = in.rdstate();
    if(st && std::ifstream::eofbit){
        throw Exception ("End-of-File reached on input operation, buf len <%i> bytes", sizeof(buf));
    }

    if(st && std::ifstream::failbit) throw Exception("Logical error on i/o operation");

    if(st && std::ifstream::badbit) throw Exception("Read/writing error on i/o operation");

    throw Exception("Error desconocido <%i>",st);
}
