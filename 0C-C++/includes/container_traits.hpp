/** ***********************************************************************************//**
\addtogroup utilities
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
@file container_traits.hpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   STL container traits
@details template trait for check in template methos or functions
@version 0.0.1.
@date Viernes 22 de Mayo de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version      Brief
JEL            2026.05.22     0.0.1        Version Inicial no release

* ********************************************************************************** */
#ifndef __container_traits_hpp__
#define __container_traits_hpp__ /**<@brief header module name idem to pragma once */


/* header file list fo namespace utilities */
#include <concepts>
#include <list>
#include <forward_list>
#include <vector>
#include <map>
#include <deque>
#include <utility>

namespace utilities {

    template <typename P>
    concept is_pair = requires {
        typename P::first_type;
        typename P::second_type;
    } && std::same_as<P, std::pair<typename P::first_type, typename P::second_type>>;

    template <typename C>
    concept is_vector = requires {
        typename C::value_type;
    } && std::same_as<C, std::vector<typename C::value_type, typename C::allocator_type>>;

    template <typename C>
    concept is_nested_vector = requires {
        typename C::value_type;
        typename C::value_type::value_type;
    } && std::same_as<typename C::value_type, 
        std::vector<typename C::value_type::value_type, 
            typename C::value_type::allocator_type>
    >;

    template <typename C>
    concept is_list = requires {
        typename C::value_type;
    } && std::same_as<C, std::list<typename C::value_type, typename C::allocator_type>>;
    
    template <typename C>
    concept is_nested_list = requires {
        typename C::value_type;
        typename C::value_type::value_type;
    } && std::same_as<typename C::value_type, 
        std::list<typename C::value_type::value_type, 
            typename C::value_type::allocator_type>
    >;

    template <typename C>
    concept is_forward_list = requires {
        typename C::value_type;
    } && std::same_as<C, std::forward_list<typename C::value_type, typename C::allocator_type>>;

    template <typename C>
    concept is_nested_forward_list= requires {
        typename C::value_type;
        typename C::value_type::value_type;
    } && std::same_as<typename C::value_type, 
        std::forward_list<typename C::value_type::value_type, 
            typename C::value_type::allocator_type>
    >;

    template <typename C>
    concept is_deque = requires {
        typename C::value_type;
    } && std::same_as<C, std::deque<typename C::value_type, typename C::allocator_type>>;

    template <typename C>
    concept is_nested_deque = requires {
        typename C::value_type;
        typename C::value_type::value_type;
    } && std::same_as<typename C::value_type, 
        std::deque<typename C::value_type::value_type, 
            typename C::value_type::allocator_type>
    >;


    template <typename C>
    concept is_map = requires {
        typename C::key_type;
        typename C::mapped_type;
    } && std::same_as<C, std::map<typename C::key_type, typename C::mapped_type,
    typename C::key_compare, typename C::allocator_type>>;
};
#endif /* #ifndef __container_traits_hpp__ */


