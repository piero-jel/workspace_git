/** ***********************************************************************************//**
\addtogroup utilstr
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
@file utilstr.hpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   ...
@details ...
@version 0.0.1.
@date Viernes 5 de Junio de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date                 Version      Brief
JEL            2026.06.05     0.0.1   Version Inicial no release

* ********************************************************************************** */
#ifndef __utilstr_hpp__
#define __utilstr_hpp__ /**<@brief header module name idem to pragma once */

#include <cstring>
#include <cstdint>
#include <cstdarg>

#include <string>
#include <algorithm>
#include <sstream>
#include <utility>
#include <array>
#include <functional>


/* header file list fo namespace utilstr */
#include <container_traits.hpp>

namespace utilstr {

    /**
     * @brief funcion que se encarga de realizar el split en dos parte de un string      
     * @param[in] src string fuente de la operacion 
     * @param[in] target caracter que se tomara para realizar el split
     * @param[in] trim oppcional por defecto deshabilitado. flag para habilitar el trim luego del split
     * @return std::pair<std::string,std::string> 
     * @note si no localiza el \b target retonra dos striong vacios
     */
    std::pair<std::string,std::string> split_two(const std::string& src,char target,bool trim=false){
        std::size_t pos;
        if( (pos = src.find(target)) == std::string::npos)
            return std::make_pair<std::string,std::string>({},{});

        auto p1 = pos+1;
        if(trim){
            if (src[pos-1] == ' ')
                pos--;

            if (src[p1] == ' ')
                p1++;
        }
        return std::pair<std::string,std::string>(src.substr(0,pos),src.substr(p1));
    }

    /**
     * @brief funcion que se encarga de realizar el split en dos parte de un string 
     * @param[in] src string fuente de la operacion 
     * @param[in] target string substring que se tomara para realizar el split
     * @param[in] trim oppcional por defecto deshabilitado. flag para habilitar el trim luego del split
     * @return std::pair<std::string,std::string> 
     * @note si no localiza el \b target retonra dos striong vacios
     */
    std::pair<std::string,std::string> split_two(const std::string& src,const std::string& target,bool trim=false){
        std::size_t pos;            
        if( (pos = src.find(target)) == std::string::npos)
            return std::make_pair<std::string,std::string>({},{});

        auto p1 = pos+target.length();
        if(trim){
            if (src[pos-1] == ' ')
                pos--;

            if (src[p1] == ' ')
                p1++;
        }
        return std::pair<std::string,std::string>(src.substr(0,pos),src.substr(p1));
    }

    /**
     * @brief funcion que se encarga de realizar el split en dos parte de un string 
     * @tparam N longitud del array donde se colocara el resultado
     * @param[in] src string fuente de la operacion 
     * @param[in] target string substring que se tomara para realizar el split
     * @param[in] dst array destino de la operacion tomadno el index 0 para la prime porcion
     * y el siguente para la otra.
     * @param[in] trim oppcional por defecto deshabilitado. flag para habilitar el trim luego del split
     * @return true \b target localizado y array actualizado
     * @return false \b no se localizo el \b target
     */
    template<std::size_t N=2>
    bool split_two(const std::string& src,const std::string& target,std::array<std::string,N>& dst,bool trim=false){
        std::size_t pos;            
        if( (pos = src.find(target)) == std::string::npos)
            return false;

        auto p1 = pos+target.length();
        if(trim){
            if (src[pos-1] == ' ')
                pos--;

            if (src[p1] == ' ')
                p1++;
        }
        dst[0] = src.substr(0,pos);
        dst[1] = src.substr(p1);
        return true;
    }

    /**
     * @brief funcion que se encarga de realizar el split en dos parte de un string 
     * @tparam N longitud del array donde se colocara el resultado
     * @param[in] src string fuente de la operacion 
     * @param[in] target caracter que se tomara para realizar el split
     * @param[in] dst array destino de la operacion tomadno el index 0 para la prime porcion
     * y el siguente para la otra.
     * @param[in] trim oppcional por defecto deshabilitado. flag para habilitar el trim luego del split
     * @return true \b target localizado y array actualizado
     * @return false \b no se localizo el \b target
     */
    template<std::size_t N=2>
    bool split_two(const std::string& src,char target,std::array<std::string,N>& dst,bool trim=false){
        std::size_t pos;            
        if( (pos = src.find(target)) == std::string::npos)
            return false;

        auto p1 = pos+1;
        if(trim){
            if (src[pos-1] == ' ')
                pos--;

            if (src[p1] == ' ')
                p1++;
        }
        dst[0] = src.substr(0,pos);
        dst[1] = src.substr(p1);
        return true;
    }

    /**
     * @brief funcion para realizar el split de un string en funcion de un substring como separador
     * @tparam C template tipo para el contenedor donde se almacenara el resultado
     * @param[in] src string donde se realizara la busqueda y se creara los slice
     * @param[in] slp string que se tomara para realizar al separacion
     * @param[in] empty opcional flag para habilitar si se desea considerar los slice vacios.
     * @param[in] trim flag para habilitar el trim de los slice. Este quita los espacios de los extremos del slice
     * @return C contendor con el resultado del split, si no se localiza el separador este estara vacio o en su defecto
     * (para el caso de los array) todos sus item lo estaran.
     */
    template <typename C>
    C split(const std::string& src,const std::string& slp,bool empty=false,bool trim=false){
        
        static_assert( utiltraits::is_vector<C>||utiltraits::is_list<C>||utiltraits::is_deque<C>
                || utiltraits::is_array<C> ,
            "Container Tipe not tabulate");

        C ret;
        const auto append = [&ret,&empty,&trim](const std::string& s,std::size_t pos,std::size_t len = 0)-> std::string {
            std::string ret;
            if (len == 0 ) len = s.length()-pos;
            
            if(trim){
                while(s[pos] == ' ' && pos < (pos+len)) pos++,len--;
            }                
            if(trim){
                while( s[pos+len-1] == ' ' && len > 1) len--;
            }
            ret = s.substr(pos,len);

            return ret;
        };

        if constexpr (utiltraits::is_vector<C>||utiltraits::is_list<C>||utiltraits::is_deque<C>||utiltraits::is_forward_list<C>) {
            std::size_t beg=0;
            std::size_t end = src.find(slp);
            std::string tmp;
            const auto lmb_insert = [&ret,&empty](const std::string& v={}){
                if(v.empty() && !empty) return;

                if constexpr (utiltraits::is_vector<C>||utiltraits::is_list<C>||utiltraits::is_deque<C>){
                    ret.emplace_back(std::move(v));
                }
                else if constexpr (utiltraits::is_forward_list<C>){
                    ret.emplace_front(std::move(v));
                }
            };

            while( end != std::string::npos){
                if(end == beg){
                    lmb_insert();
                    beg = end + slp.length();
                    end = src.find(slp,beg);
                    continue;
                }
                tmp = append(src,beg,end-beg);
                lmb_insert(tmp);
                beg = end + slp.length();
                end = src.find(slp,beg);
            }
            if(beg > 0){
                tmp = append(src,beg);
                lmb_insert(tmp);
                if constexpr (utiltraits::is_forward_list<C>)
                    ret.reverse();
            }
        }

        if constexpr (utiltraits::is_array<C>){
            uint32_t len = static_cast<uint32_t>(ret.size());
            std::size_t beg = 0, end = src.find(slp);
            uint32_t i = 0;
            std::string tmp;
            const auto lmb_insert = [&ret,&empty,&i](uint32_t idx,const std::string& v={}){
                if(v.empty() && !empty) {
                    i--;
                    return;
                }
                ret[idx] = v;
            };

            for(i = 0; i < len ; i++){
                if( end == std::string::npos)
                    break;
                if(end == beg){
                    lmb_insert(i);
                    beg = end + slp.length();
                    end = src.find(slp,beg);
                    continue;
                }
                tmp = append(src,beg,end-beg);
                lmb_insert(i,tmp);
                beg = end + slp.length();
                end = src.find(slp,beg);
            }
            if (i > 0 && i < len){
                tmp = append(src,beg);
                lmb_insert(i,tmp);
            }
        }
        return ret;
    }

    /**
     * @brief funcion para realizar el split de un string en funcion de un caracter como separador
     * @tparam C template tipo para el contenedor donde se almacenara el resultado
     * @param[in] src string donde se realizara la busqueda y se creara los slice
     * @param[in] slp caracter que se tomara para realizar al separacion
     * @param[in] empty opcional flag para habilitar si se desea considerar los slice vacios.
     * @param[in] trim flag para habilitar el trim de los slice. Este quita los espacios de los extremos del slice
     * @return C contendor con el resultado del split, si no se localiza el caracter este estara vacio o en su defecto
     * (para el caso de los array) todos sus item lo estaran.
     */
    template <typename C>
    C split(const std::string& src,char slp,bool empty=false,bool trim=false){
        C ret;
        static_assert( utiltraits::is_vector<C>||utiltraits::is_list<C>||utiltraits::is_deque<C>
                || utiltraits::is_array<C> ,
            "Container Tipe not tabulate");

        const auto append = [&ret,&trim](const std::string& s,std::size_t pos,std::size_t len = 0){
            std::string tmp;
            if (len == 0 ) len = s.length()-pos;
            
            if(trim){
                while(s[pos] == ' ' && pos < (pos+len)) pos++,len--;
            }                
            if(trim){
                while( s[pos+len-1] == ' ' && len > 1) len--;
            }
            return s.substr(pos,len);
        };

        if constexpr (utiltraits::is_vector<C>||utiltraits::is_list<C>||utiltraits::is_deque<C>||utiltraits::is_forward_list<C>) {
            std::size_t beg=0;
            std::size_t end = src.find(slp);
            std::string tmp;
            const auto lmb_insert = [&ret,&empty](const std::string& v={}){
                if(v.empty() && !empty) return;

                if constexpr (utiltraits::is_vector<C>||utiltraits::is_list<C>||utiltraits::is_deque<C>){
                    ret.emplace_back(std::move(v));
                }
                else if constexpr (utiltraits::is_forward_list<C>){
                    ret.emplace_front(std::move(v));
                }
            };

            while( end != std::string::npos){
                if(end == beg){
                    lmb_insert();
                    beg = end + 1;
                    end = src.find(slp,beg);
                    continue;
                }
                tmp = append(src,beg,end-beg);
                lmb_insert(tmp);
                beg = end + 1;
                end = src.find(slp,beg);
            }
            if(beg > 0){
                tmp = append(src,beg);
                lmb_insert(tmp);
                if constexpr (utiltraits::is_forward_list<C>)
                    ret.reverse();
            }
        }

        if constexpr (utiltraits::is_array<C>){
            uint32_t len = static_cast<uint32_t>(ret.size());
            std::size_t beg = 0, end = src.find(slp);
            uint32_t i = 0;
            std::string tmp;
            const auto& lmb_insert = [&ret,&empty,&i](uint32_t idx,const std::string& v={}){
                if(v.empty() && !empty) {
                    i--; /* si i == 0, pasa al maximo y en la proxima iteraccion se coloca en 0 nuevamente */
                    return;
                }
                ret[idx] = v;
            };
            
            for(i = 0; i < len ; i++){
                if( end == std::string::npos)
                    break;
                if(end == beg){
                    lmb_insert(i);
                    beg = end + 1;
                    end = src.find(slp,beg);
                    continue;
                }
                tmp = append(src,beg,end-beg);
                lmb_insert(i,tmp);
                beg = end + 1;
                end = src.find(slp,beg);
            }
            if (i > 0 && i < len){
                tmp = append(src,beg);
                lmb_insert(i,tmp);
            }
        }
        return ret;
    }

    /**
     * @brief funcion para obtener la conversion TO UPPER de un string (todos los caracteres en 
     * mayusculas).
     * @param[in] src striung fuente de la operacion
     * @return std::string 
     */
    static inline std::string to_upper(const std::string& src){
        std::string ret = src;
        std::string::iterator it,end = std::end(ret);
        for (it = std::begin(ret);it < end;it++){
            *it = std::toupper(*it);
        }
        return ret;
    }

    /**
     * @brief funcion para realizar la tranformacion de un string, todos sus caracteres a upper case
     * @param[in] src puntero al string donde se realizar la operacion.
     * @return true se realizo la transformacion.
     * @return false No se pudo realizar String vacio o puntero invalido
     */
    static inline bool to_upper(std::string* src){
        if (!src || src->empty()) return false;

        std::string::iterator it,end = src->end();
        for (it = src->begin();it < end;it++){
            *it = std::toupper(*it);
        }
        return true;
    }

    /**
     * @brief funcion para obtener la conversion TO LOWER de un string (todos los caracteres en 
     * minusculas).
     * @param[in] src striung fuente de la operacion
     * @return std::string 
     */
    static inline std::string to_lower(const std::string& src){
        std::string ret = src;
        std::string::iterator it,end = std::end(ret);
        for (it = std::begin(ret);it < end;it++){
            *it = std::tolower(*it);
        }
        return ret;
    }
    /**
     * @brief funcion para realizar la tranformacion de un string, todos sus caracteres a lower case
     * @param[in] src puntero al string donde se realizar la operacion.
     * @return true se realizo la transformacion.
     * @return false No se pudo realizar String vacio o puntero invalido
     */
    static inline bool to_lower(std::string* src){
        if (!src || src->empty()) return false;

        std::string::iterator it,end = src->end();
        for (it = src->begin();it < end;it++){
            *it = std::tolower(*it);
        }
        return true;
    }

    /**
     * @brief template function para obtener un string desede un obejto que tiene definido
     * el operadir `std::ostream operator<<(std::ostream&,const T&)`
     * @tparam T type del objeto del cual se desa obtener el std::string con la representacion
     * @param[in] obj objeto
     * @return std::string string con la representacion.
     */
    template <typename T>
    static inline std::string to_string(const T& obj) {
        std::ostringstream ss;
        ss << obj;
        return std::string(ss.str());
    }

    /**
     * @brief funcion para realizar el join de item de un contenedor
     * @tparam C template type para el contenedor
     * @tparam V template type Opcional, para especificar el tipo de datos en caso de un tipo no
     * integrado, util para el caso de tipo con la sobrecarga del `operator<<`
     * @tparam S template type Opcional, para el separador este debe ser uno de los
     * tipos `std::string`, `char` or `const char*`
     * que posea la sobrecarga del operador <<
     * @param[in] c contendor con los item que se usaran para la operaciopn
     * @param[in] sep separador que se utilizara
     * @param[in] trn opcional, puntero a funcion/expresion lambda o funtor con la transformacion del
     * item a string.
     * @return std::string string con el join de los item y separador (entre cada item)
     */
    template <typename C,typename V=std::string, typename S=std::string>
    static inline std::string join(const C& c,const S& sep=",",
            std::function<std::string(typename C::const_iterator)> trn={}) {
        static_assert(std::same_as<S,std::string>||std::same_as<S,char>||std::same_as<S,const char*>,
                      "S (separtor) type not suported, only `std::string`, `char` or `const char*`");

        std::string ret = "";
        using Value = typename C::value_type;
        using It = typename C::const_iterator;

        static_assert(std::same_as<Value,std::string>||std::same_as<Value,V>,
                      "Value type in container not suported");

        if constexpr (std::same_as<Value,std::string>){
            It it = std::begin(c),end = std::end(c);
            uint32_t last = static_cast<uint32_t>(std::distance(it,end))-1;
            uint32_t i=0;
            if(trn){
                for (; it != end; it++,i++){
                    ret += trn(it);
                    if (i != last)
                        ret += sep;
                }
            }
            else{
                for (; it != end; it++,i++){
                    ret += *it;
                    if (i != last)
                        ret += sep;
                }
            }

        }
        else if constexpr (std::same_as<Value,V>){
            /* consideramos que V tiene sobrecargado `operator<<` */
            It it = std::begin(c),end = std::end(c);
            uint32_t last = static_cast<uint32_t>(std::distance(it,end))-1;
            uint32_t i=0;
            if(trn){
                for (; it != end; it++,i++){
                    ret += trn(it);
                    if (i != last)
                        ret += sep;
                }
            }
            else{
                for (; it != end; it++,i++){
                    ret += utilstr::to_string(*it);
                    if (i != last)
                        ret += sep;
                }
            }
        }
        return ret;
    }

    /**
     * @brief funcion para obtener un string desde una format CStyle string
     * @tparam LEN template opcional para fijar la longitud maxima del string
     * @param fmt string format 
     * @param ... listado de parametros
     * @return std::string resultado de la operacion.
     */
    template <uint32_t LEN=128>
    static inline std::string format(const char* fmt, ...)noexcept {
        if (!fmt) return std::string();
        char buf[LEN];
        va_list args;
        va_start(args, fmt );
        std::vsnprintf(buf,LEN-1, fmt, args );
        /* cerramos la lista de argumentos */
        va_end( args );
        return std::string(buf);
    }

    /**
     * @brief funcion para obtener un string desde un variadic format argument
     * @tparam LEN template opcional para fijar la longitud maxima del string
     * @param fmt string format
     * @param args va_list con el listado de parametros
     * @param close opcional, por defecto true. Flag para indicar que no debe cerrarse el listado
     * \b args . Por defecto este es cerrado.
     * @return std::string resultado de la operacion.
     */
    template <uint32_t LEN=128>
    static inline std::string format_va(const char* fmt, va_list args, bool close=true)noexcept {
        if (!fmt){
            if(close)
                va_end( args );
            return std::string();
        }

        char buf[LEN];
        std::vsnprintf(buf,LEN-1, fmt, args );
        /* cerramos la lista de argumentos */
        if(close)
            va_end( args );

        return std::string(buf);
    }


    
    /**
     * @brief funcion que localiza y remplaza todas las apariciones de un substring sobre otro string
     * @param[in,out] src puntero al string donde se realizara la oepracion, este es modificado segun corresponda
     * @param[in] from string a localizar para luego ser reemplazado por \b to 
     * @param[in] to string que se usara para realizar el remplazo.
     * @return numero de remplazos.     
     */
    static inline uint32_t replace_all(std::string* src, const std::string& from, const std::string& to) {
        if (!src || src->empty()) return false;
        std::size_t pos = 0;
        uint32_t i=0;        
        while ((pos = src->find(from, pos)) != std::string::npos) {
            src->replace(pos, from.length(), to);
            pos += to.length(); // Advance past the replacement
            i++;
        }
        return i;
    }

    /**
     * @brief funcion que localiza y remplaza todas las apariciones de un caracter sobre un string
     * @param[in,out] src puntero al string donde se realizara la oepracion, este es modificado segun corresponda
     * @param[in] from caracter a localizar para luego ser reemplazado por \b to 
     * @param[in] to caracter que se usara para realizar el remplazo.
     * @return numero de remplazos.
     */
    static inline uint32_t replace_all(std::string* src, char from, char to) {
        if (!src || src->empty()) return false;

        std::size_t pos = 0;
        uint32_t i = 0;
        while ((pos = src->find(from, pos)) != std::string::npos) {
            src->at(pos) = to;
            pos += 1;
            i++;
        }
        return i;
    }

    /**
     * @brief funcion que localiza y remplaza todas las apariciones de un substring sobre otro string
     * @param[in,out] src string donde se realizara la oepracion, este es modificado segun corresponda
     * @param[in] from string a localizar para luego ser reemplazado por \b to 
     * @param[in] to string que se usara para realizar el remplazo.
     * @return numero de remplazos.
     */
    static inline uint32_t replace_all_inplace(std::string& src, const std::string& from,
        const std::string& to) {        
        if (src.empty()) return false;

        std::size_t pos = 0;
        uint32_t i = 0;
        while ((pos = src.find(from, pos)) != std::string::npos) {
            src.replace(pos, from.length(), to);
            pos += to.length(); // Advance past the replacement
            i++;
        }
        return i;
    }
    
    /**
     * @brief funcion que localiza y remplaza todas las apariciones de un caracter sobre otro string
     * @param[in,out] src string donde se realizara la oepracion, este es modificado segun corresponda
     * @param[in] from caracter a localizar para luego ser reemplazado por \b to 
     * @param[in] to caracter que se usara para realizar el remplazo.
     * @return numero de remplazos.
     */
    static inline uint32_t replace_all_inplace(std::string& src, char from, char to) {        
        if (src.empty()) return false;

        std::size_t pos = 0;
        uint32_t i = 0;
        while ((pos = src.find(from, pos)) != std::string::npos) {
            src[pos] = to;
            pos += 1;
            i++;
        }
        return i;
    }

    /**
     * @brief funcion que crea una copia del \b src para luego localizar y remplaza
     * sobre la copia, todas las apariciones de un substring con otro.
     * @param[in,out] src string donde se realizara la oepracion, este es modificado segun corresponda
     * @param[in] from string a localizar para luego ser reemplazado por \b to 
     * @param[in] to string que se usara para realizar el remplazo.
     * @return std::string 
     */
    static inline std::string replace_all(const std::string& src, const std::string& from,
        const std::string& to) {
        std::string ret = src;
        utilstr::replace_all_inplace(ret,from,to);
        return ret;        
    }

    /**
     * @brief funcion que crea una copia del \b src para luego localizar y remplaza
     * sobre la copia, todas las apariciones de un caracter con otro.
     * @param[in,out] src string donde se realizara la oepracion, este es modificado segun corresponda
     * @param[in] from caracter a localizar para luego ser reemplazado por \b to 
     * @param[in] to caracter que se usara para realizar el remplazo.
     */
    static inline std::string replace_all(const std::string& src, char from,char to) {
        std::string ret = src;
        utilstr::replace_all_inplace(ret,from,to);
        return ret;        
    }


    /**
     * @brief funcion para verificar si un string inicia con un substring
     * @param[in] src string donde se relaizara la operacion
     * @param[in] beg string que se usara para verificacion
     * @return true \b src inicia con \b beg 
     * @return false 
     * @note c++20 contamos con std::string::starts_with() y std::string::ends_with()
     */
    static inline bool start_with(const std::string& src, const std::string& beg) {        
        return src.compare(0,beg.length(),beg);
    }


    /**
     * @brief funcion para verificar si un string finaliza con un substring
     * @param[in] src string donde se relaizara la operacion
     * @param[in] end string que se usara para verificacion
     * @return true \b src finaliza con \b end
     * @return false 
     * @note c++20 contamos con std::string::starts_with() y std::string::ends_with()
     */
    static inline bool end_with(const std::string& src, const std::string& end) {
        auto lsrc = src.length();
        auto lend = end.length();
        return lsrc >= lend && src.compare(lsrc-lend,lend,end);
    }
};

#endif /* #ifndef __utilstr_hpp__ */
