/** ***********************************************************************************//**
\addtogroup anagreama
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
@file check_anagrama.cpp
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
#include <string>
#include <cstring>
#include <memory>
#include <algorithm>

#include <cstdlib> /* qsort() */
#include <check_anagrama.hpp>


bool checkAnagrama( const std::string& op1, const std::string& op2, bool sen ) {
    if (op1.length() != op2.length() || op1 == op2 )
        return false;

    std::string a=op1,b=op2;

    if(sen){
        const auto lmb_toupper = [](char l) -> char { return std::toupper(l);};
        std::transform( std::begin(op1),std::end(op1),std::begin(a)
                    , lmb_toupper);

        std::transform( std::begin(op2),std::end(op2),std::begin(b)
                    , lmb_toupper);
    } 

    if(a == b ) return false;

    std::sort(a.begin(),a.end());
    std::sort(b.begin(),b.end());
    if(a == b )
        return true;
    
    return false;  
}

bool checkAnagrama( const char* op1, const char* op2,bool sen) {
    auto len = std::strlen(op1);
    if (!op1 || !op2 ||  len != std::strlen(op2) || std::strcmp(op1,op2) == 0)
        return false;

    std::unique_ptr<char[], void(*)(void*)> a (strdup(op1),free);
    std::unique_ptr<char[], void(*)(void*)> b (strdup(op2),free);
    
    if(sen){
        const auto lmb_toupper = [](char l) -> char { return std::toupper(l);};
        std::transform( op1,op1+len,a.get(),lmb_toupper);

        std::transform( op2,op2+len, b.get(),lmb_toupper);
    }

    if (std::strcmp(a.get(),b.get()) == 0) return false;
    /* ordenamos cada uno*/
    std::sort(a.get(),a.get()+len);
    std::sort(b.get(),b.get()+len);    
    return std::strcmp(a.get(),b.get())? false: true;
}



static inline int cmp_char(const void* pa,const void* pb){
    char a = *((char*) pa);
    char b = *((char*) pb);
    if ( a == b) return 0;
    return (a<b)? -1:1;
}

bool check_anagrama(const char* op1, const char* op2,bool sen) {
    auto len = std::strlen(op1);
    if (!op1 || !op2 ||  len != std::strlen(op2) || std::strcmp(op1,op2) == 0)
        return false;

    std::unique_ptr<char[], void(*)(void*)> a (strdup(op1),free);
    std::unique_ptr<char[], void(*)(void*)> b (strdup(op2),free);
  
  
    if(sen){
        const auto lmb_toupper = [](char l) -> char { return std::toupper(l);};
        std::transform( op1,op1+len,a.get(),lmb_toupper);

        std::transform( op2,op2+len, b.get(),lmb_toupper);
    }

    if (std::strcmp(a.get(),b.get()) == 0) return false;
    /* ordenamos cada uno*/
    std::qsort(a.get(),len,1,cmp_char);
    std::qsort(b.get(),len,1,cmp_char);
    
    return std::strcmp(a.get(),b.get())? false: true;
}
