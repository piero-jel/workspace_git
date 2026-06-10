/** ***********************************************************************************//**
\addtogroup utilcont
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
@file utilcont.hpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.1.
@date Lunes 8 de Junio de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date                 Version      Brief
JEL            2026.06.08     0.0.1   Version Inicial no release

* ********************************************************************************** */
#ifndef __utilcont_hpp__
#define __utilcont_hpp__ /**<@brief header module name idem to pragma once */


/* header file list fo namespace utilcont */
#include <container_traits.hpp>

namespace utilcont {


    /**
     * @brief funcion para realizar la extencion de un contenedor
     *
     * @tparam C template type para el tipo de contenedor
     * @tparam ORD template flag opcional, para habilitar la insercion ordenada en caso de forward list
     * @param[in] dst contenedor destion de la extencion
     * @param[in] src contenedor que se requeire concatenar al \b dst
     * @return C
     */
    template <typename C=std::vector<std::string>, bool ORD=false>
    static inline C extend(C& dst, const C& src){

        if constexpr (utiltraits::is_vector<C>){
            dst.reserve(dst.size()+src.size());
            dst.insert(dst.end(),src.cbegin(),src.cend());
        }
        else if constexpr (utiltraits::is_list<C>){
            dst.insert(dst.end(),src.cbegin(),src.cend());
        }
        else if constexpr (utiltraits::is_forward_list<C>){
            if constexpr (ORD){
                dst.reverse();
                dst.insert_after(dst.begin(),src.cbegin(),src.cend());
                dst.reverse();
            }
            else{
                dst.insert_after(dst.begin(),src.cbegin(),src.cend());
            }
        }
        return dst;
    }


    /**
     * @brief template function make factory para la creacion de un contenedor con
     * punteros ( ex: \b std::unique_ptr<T> )
     * @tparam C template type para el contenedor
     * @tparam Ptrs variadic params con los items, pointers from new operators,
     * con los que se lleranara el contenedor.
     * @param ptrs
     * @return auto
     */
    template<typename C, typename ... Ptrs>
    C make( Ptrs&& ... ptrs ) {
        C ret;
        if constexpr (utiltraits::is_vector<C> || utiltraits::is_list<C> ||
            utiltraits::is_deque<C>) {

            ( ret.emplace_back( std::forward<Ptrs>(ptrs) ), ... );
            return ret;
        }
        else if constexpr (utiltraits::is_forward_list<C> ){
            ( ret.emplace_front( std::forward<Ptrs>(ptrs) ), ... );
            ret.reverse();
        }
        else if constexpr (utiltraits::is_array<C> ){
            static_assert( sizeof...(ptrs) <= ret.size(),"Nro items is > to array len");
            using It = typename C::iterator;
            using ValueType = typename C::value_type;
            It it = std::begin(ret);
            ( ( *(it++) = ValueType(ptrs) ), ... );
        }
        return ret;
    }
};
#endif /* #ifndef __utilcont_hpp__ */
