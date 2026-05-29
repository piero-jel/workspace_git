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
@file containers.hpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   STL container utilities
@details templates functions for hadler STL containers
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
#ifndef __containers_hpp__
#define __containers_hpp__ /**<@brief header module name idem to pragma once */


/* header file list fo namespace utilities */
#include <cstring>
#include <iostream>
#include <cstdint>
#include <memory>    /* std::unique_ptr<T,D> */

#include <container_traits.hpp>

namespace utilities {

    template <typename V>
    concept is_unique_ptr = requires {
        typename V::element_type;
        typename V::deleter_type;
    } && std::same_as<V, std::unique_ptr<typename V::element_type, typename V::deleter_type>>;

    template <typename Value>
    void value_print(const Value value,std::FILE* ou= stdout,const char* beg=nullptr,const char* end=nullptr){
        if constexpr (std::is_same_v<Value, std::string>){                
            if (beg && end)
                std::fprintf(ou,"%s%s%s",beg,value.c_str(),end);
            else if (end)
                std::fprintf(ou,"%s%s",value.c_str(),end);
            else 
                std::fprintf(ou,"%s",value.c_str());
        }
        else if constexpr (std::is_same_v<Value, const char*> || std::is_same_v<Value, char*>){
            if (beg && end)
                std::fprintf(ou,"%s%s%s",beg,value,end);
            else if (end)
                std::fprintf(ou,"%s%s",value,end);
            else 
                std::fprintf(ou,"%s",value);
        }
        else if constexpr (std::is_same_v<Value, bool>){        
            if (beg && end)
                std::fprintf(ou,"%s%s%s",beg,(value)?"true":"false",end);
            else if (end)
                std::fprintf(ou,"%s%s",(value)?"true":"false",end);
            else 
                std::fprintf(ou,"%s",(value)?"true":"false");
        }
        else if constexpr (std::is_same_v<Value, int>){        
            if (beg && end)
                std::fprintf(ou,"%s%i%s",beg,value,end);
            else if (end)
                std::fprintf(ou,"%i%s",value,end);
            else 
                std::fprintf(ou,"%i",value);
        }
        else if constexpr (std::is_same_v<Value, float>){        
            if (beg && end)
                std::fprintf(ou,"%s%.3f%s",beg,value,end);
            else if (end)
                std::fprintf(ou,"%.3f%s",value,end);
            else 
                std::fprintf(ou,"%.3f",value);
        }
    }

    
     /**
      * @brief funcion template que se encarga de imprimir el contenido de un contenedor
      * 
      * @tparam C tipo de contenedor
      * @param[in] v objeto contenedor
      * @param[in] msg Opcional, mensaje que se imprimira previo al contenido del contenedor
      * @param[in] sep opcional, separador entre elementos del contenedor
      * @param[in] end Opcional, mensjae final
      * @param[in] pre Opcional, mensaje previo a cada elemento del contenedor
      * @param[in] ou Opcional, Sream/File donde se imprimira la informacion
      */
    template <typename C=std::vector<std::string>>
    void container_print(const C& v,
            const char* msg=nullptr,
            const char* sep=nullptr,
            const char* end=nullptr,
            const char* pre=nullptr,
            std::FILE* ou= stdout){

        if (msg) std::fputs(msg,ou);

        if constexpr (utilities::is_map<C>){
            using KeyValue = typename C::key_type;
            using Value = typename C::mapped_type;
            
            typename C::const_iterator it,it_end = std::end(v);
            for (it = std::begin(v); it != it_end; it++){            
                if constexpr (utilities::is_vector<Value> || utilities::is_list<Value> ||
                        utilities::is_forward_list<Value> || utilities::is_deque<Value>){

                    utilities::value_print<KeyValue>(it->first,ou,nullptr," : [ ");
                    utilities::container_print<Value>(it->second,nullptr,nullptr,"");
                    std::fputs(" ]\n",ou);
                }
                else{
                    utilities::value_print<KeyValue>(it->first,ou,nullptr," : ");
                    utilities::value_print<Value>(it->second,ou,nullptr,"\n");
                }            
            }            
        }
        /** nested containers */    
        else if constexpr (utilities::is_nested_vector<C>||utilities::is_nested_list<C> ||
                utilities::is_nested_forward_list<C>||utilities::is_nested_deque<C>){
            
            using Value = typename C::value_type;
            if (!msg) std::fputs("[\n",ou);
            for (const auto& it : v){
                std::fputs((pre)?pre:"    [",ou);
                utilities::container_print<Value>(it,nullptr,nullptr,"");
                std::fputs((sep)?sep:" ],\n",ou);
            }
            std::fputs((end)?end:"]\n",ou);
        }
        /** containers */    
        else if constexpr (utilities::is_vector<C> || utilities::is_list<C> ||
                utilities::is_forward_list<C> || utilities::is_deque<C>){

            using Value = typename C::value_type;
            typename C::const_iterator it,it_end = std::end(v);
            uint32_t last = static_cast<uint32_t>(std::distance(std::begin(v),std::end(v)))-1;
            uint32_t i=0;
            if constexpr (utilities::is_unique_ptr<Value>){

                using RValue = typename C::value_type::element_type;
                for (it = std::begin(v); it != it_end; it++,i++){
                    if (i == last){
                        if(pre && sep)
                            utilities::value_print<RValue>(*(it->get()),ou,pre,sep);
                        else
                            utilities::value_print<RValue>(*(it->get()),ou,pre);
                    }
                    else
                        utilities::value_print<RValue>(*(it->get()),ou,pre,(sep)?sep:", ");
                }

            }
            else{
                for (it = std::begin(v); it != it_end; it++,i++){
                    if (i == last){
                        if(pre && sep)
                            utilities::value_print<Value>(*it,ou,pre,sep);
                        else
                            utilities::value_print<Value>(*it,ou,pre);  
                    }                        
                    else
                        utilities::value_print<Value>(*it,ou,pre,(sep)?sep:", ");
                }
            }
            
            std::fputs((end)?end:"\n",ou);
        }
    }
};
#endif /* #ifndef __containers_hpp__ */
