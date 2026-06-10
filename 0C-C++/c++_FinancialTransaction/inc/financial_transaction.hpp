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
@file financial_transaction.hpp
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
#ifndef __financial_transaction_hpp__
#define __financial_transaction_hpp__ /**<@brief header module name idem to pragma once */


#include <string>
#include <set>
#include <tuple>
#include <vector>
#include <list>
#include <forward_list>
#include <cstdint>
#include <algorithm>
#include <iostream>
#include <functional>


#include <RangesRegister.hpp>
#include <CardsRegister.hpp>

#if ( STD_VER >= 2017 )
    /* c++17 >    */
    #define IS_SAME(OBJ1,OBJ2) std::is_same_v<OBJ1, OBJ2>
#else
    #define IS_SAME(OBJ1,OBJ2) std::is_same<OBJ1, OBJ2>::value
#endif



/**
 * @brief metodo para la verificacion del card number
 *
 * @param[in] card_number numero de tarjeta
 * @param[in] frange path/file-rango
 * @param[in] fcards path/file-cards
 * @return std::tuple<bool,RangesRegister,CardsRegister>
 *  + bool true succes , false not found
 *  + RangesRegister localizado (si bool es true de lo contrario empty)
 *  + CardsRegister localizado (si bool es true de lo contrario empty)
 */
std::tuple<bool,RangesRegister,CardsRegister>
VerifyCardNumber(std::string card_number,std::string frange,std::string fcards);

/**
 * @brief Get the Card Number object
 * @param[in] msg mensage para la peticion
 * @param lmin longitud minima
 * @param lmax longitud maxima
 * @return std::string con el Numuro de tarjeta
 */
std::string GetCardNumber(const std::function<void(char*,uint32_t)>& in, uint8_t lmin = 13, uint8_t lmax = 99);

/**
 * @brief Get the Card Code object
 * @param[in] msg mensage para la peticion
 * @return std::string con el card code
 */
std::string GetCardCode(const std::function<void(char*,uint32_t)>& in,uint8_t len = 3);

/**
 * @brief Get the Amount object
 * @param[in] msg mensaje
 * @param len longitud maxima
 * @return N valor de amount ingresado
 */
int64_t GetAmount(const std::function<void(char*,uint32_t)>& in,uint8_t len_max=12);

/**
 * @brief Get the Request object
 * @tparam N template type for amount, default int64_t
 * @param[in] sld saldo
 * @param[in] ncard numero de tarjeta
 * @param[in] ccard codigo de tarjeta
 * @return std::string con el request armado
 */
std::string GetRequest(int64_t sld, const std::string& ncard, const std::string& ccard);





#endif /* #ifndef __financial_transaction_hpp__ */
