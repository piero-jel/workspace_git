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
@file financial_transaction.cpp
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
#include <cstdlib>

#include <utilities>
#include <financial_transaction.hpp>

using namespace utilities;


/**
 * @brief este template nos permite leer desde un \p std::iftream (un archivo)
 * y realizar el parsing para llenar un contenedor.
 * El tipo \p C::value_type debe contener un constructor
 * que admite un buffer " \p char* " el cual tiene la linea para construir el
 * el elemento.
 *
 * @tparam C tipo de contenedor
 * @tparam LEN \b Opcional, parameto para establecer la longitud del buffer
 * de lectura del archivo. Valor por defecto \p LEN \b 1024
 *
 * @param[in] src pathname del archivo que se lee.
 * @param[out] container contenedo que se llenara, debe poseer el metodo
 * \p push_back() "Podemos definir un insert, pero para este debemos considerar
 * el orden del mismo, por defecto al inicio del contenedor"
 * @param[in] comm Opcional, caracter de comentario para poder descartar
 * una linea leida desde el archivo.
 */
template <typename C,int LEN=1024>
void ReadAndFillContainer(const std::string& pathname , C& container, char comm='#'){
    std::ifstream f2read { pathname, std::ifstream::in };
    if(!f2read.is_open()){
        throw Exception ("Error to open path name <%s>",pathname.c_str());
    }
    using Value = typename C::value_type;

    /* Clean de flags y nos paramos en el inicio del archivo */
    f2read.clear(); /* relizamos el clear de los flags */
    f2read.seekg(0 /*offset*/, std::ios_base::beg);

    char buf[LEN];
    buf[0] = '\0';
    do{
        f2read.getline(buf,sizeof(buf),'\n');
        if(!f2read.good())
            break;

        /* descartamos las lineas vacias y las comentadas */
        if( buf[0] == comm || buf[0] == '\0' )
            continue;

        /* El metodo depende contenedor destino
         * tenemos dos opciones, creamos uno interno y usamos std::copy()
         * o definimos los diferentes constexpr para cada uno.
         * El metodo mejor establecido es emplace()
         *
         *  + std::list<T>::emplace(IT i,T Obj);
         *  + std::vector<T>::emplace(IT i,T Obj);
         *  + std::forward_list<T>::emplace_front(T Obj);
         *  + std::set<T>::emplace(T Obj);
         *  + std::multiset<T>::emplace(T Obj);
         *
         */
        if constexpr ( IS_SAME(C, std::vector<Value>)||IS_SAME(C, std::list<Value>)){
            container.emplace_back(Value(buf));
        }
        else if constexpr (IS_SAME(C, std::set<Value>)||IS_SAME(C, std::multiset<Value>)){
            container.emplace(Value(buf));
        }
        else if constexpr ( IS_SAME(C, std::forward_list<Value>) ){
            container.emplace_front(Value(buf));
        }
        else{
            static_assert( false,"type C is not tabulate");
        }
    }while(!f2read.eof());


    /* en caso de error lo reportamos al finalizar */
    if(!f2read.eof()){
        auto st = f2read.rdstate();
        if(st && std::ifstream::eofbit)
            throw Exception ("End-of-File reached on input operation, buf len <%i> bytes",sizeof(buf));

        if(st && std::ifstream::failbit)
            throw Exception("Logical error on i/o operation");

        if(st && std::ifstream::badbit)
            throw Exception("Read/writing error on i/o operation");

        throw Exception("Error desconocido <%i>",st);
    }
    f2read.close();

    if constexpr ( IS_SAME(C, std::forward_list<Value>)) {
        if( std::distance(std::begin(container),std::end(container)) == 0)
            throw Exception ("Archivo <%s> Vacio (o solo contiene comentarios)",pathname.c_str());
    }
    else{
        if(container.size() == 0)
            throw Exception ("Archivo <%s> Vacio (o solo contiene comentarios)",pathname.c_str());
    }
}



std::tuple<bool,RangesRegister,CardsRegister>
VerifyCardNumber(std::string card_number,std::string frange,std::string fcards) {

    using CRange = std::forward_list<RangesRegister>;
    using CCards = std::forward_list<CardsRegister>;


    /* 1° parsing de archivos */
    CRange crange;
    CCards ccards;
    ReadAndFillContainer(frange,crange,'#');
    ReadAndFillContainer(fcards,ccards,'#');
    std::tuple<bool,RangesRegister,CardsRegister> ret{false,RangesRegister(),CardsRegister()};

    /* 2° find RangesRegister */
    // predicado para la busqueda del RangesRegister
    PredicateRange pred_rng(card_number);
    CRange::iterator it_rng = std::find_if(
        std::begin(crange),std::end(crange),pred_rng
    );

    if(it_rng == std::end(crange)){
        return ret;
    }

    /* 3° find CardsRegister */
    CCards::iterator it_crd = std::find_if(
        std::begin(ccards),
        std::end(ccards),
        [&it_rng](const CardsRegister& o) -> bool {
            return (o.id == it_rng->id)?true:false;
        }
    );

    if(it_crd == std::end(ccards)) {
        return ret;
    }

    /* 4° fill ret */
    std::get<0>(ret) = true;
    std::get<1>(ret) = *it_rng;
    std::get<2>(ret) = *it_crd;
    return ret;
}



std::string GetCardNumber(const std::function<void(char*,uint32_t)>& in,
                          uint8_t lmin, uint8_t lmax){
    char buf[128];
    in(buf,128);
    auto len = std::strlen(buf);
    if (buf[len-1] == '\n'|| buf[len-1] == '\r') {
        len--;
        buf[len] = '\0';
    }
    if(  len < lmin || len > lmax ){
        throw Exception ("Card Number <%s> length<%i> incorrect",buf, len);
    }

    /* verificamos que todas sean valores numericos */
    std::for_each(
        buf,
        buf+len,
        [&buf](char v)-> void {
            if( std::isdigit(v) == 0){
                throw Exception ("Card Number <%s> It is not composed only of digits ('0x%X' is not digit)",buf,v);
            }
        }
    );
    return std::string(buf);
}


std::string GetCardCode(const std::function<void(char*,uint32_t)>& in,uint8_t len) {
    char buf[32];
    in(buf,32);
    auto lin = std::strlen(buf);
    if (buf[lin-1] == '\n' || buf[lin-1] == '\r') {
        lin--;
        buf[lin] = '\0';
    }

    if( lin > len ) {
        throw Exception ("Card Code <%s> length<%i> is too long",buf, lin);
    }

    std::for_each(
        buf,
        buf+lin,
        [&buf](char v)-> void {
            if( std::isdigit(v) == 0){
                throw Exception ("Card Code <%s> It is not composed only of digits",buf);
            }
        }
    );
    return std::string(buf);
}

int64_t GetAmount(const std::function<void(char*,uint32_t)>& in,uint8_t len_max){

    char buf[32];
    in(buf,32);
    auto len = std::strlen(buf);

    if (buf[len-1] == '\n' || buf[len-1] == '\r' ) {
        len--;
        buf[len] = '\0';
    }
    uint32_t idx = 0;
    while(buf[idx] == ' ') idx++;

    if(buf[idx] =='-'){
        throw Exception ("Negative Amount <%s> not allowed",buf, len);
    }

    if(buf[idx] == '+') idx++;

    /* usamos la longitud efectiva */
    if( (len-idx) > len_max  ){
        throw Exception ("Amount <%s> length<%i> is too long",buf, len);
    }

    std::for_each(
        buf+idx,
        buf+len,
        [&buf](char v)-> void {
            if( std::isdigit(v) == 0 && v != '.' && v != ','){
                throw Exception ("Amount <%s> It is not composed only of digits",buf);
            }
        }
    );
    return int64_t(std::atof(buf)*100);
}


std::string GetRequest(int64_t sld, const std::string& ncard, const std::string& ccard){
    std::ostringstream ss;
    ss  << "0200"
        << std::setfill('0')<<std::setw(2)<<ncard.length()
        << ncard
        << std::setfill('0')<<std::setw(12)<<sld
        << ccard;

    return std::string(ss.str());
}
