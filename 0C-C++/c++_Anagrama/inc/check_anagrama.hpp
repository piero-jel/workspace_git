/** ***********************************************************************************//**
\addtogroup anagrama
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
@file check_anagrama.hpp
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
Author         Date           Version      Brief
JEL            2026.05.27     0.0.1        Version Inicial no release

* ********************************************************************************** */
#ifndef __check_anagrama_hpp__
#define __check_anagrama_hpp__ /**<@brief header module name idem to pragma once */

#include <string>

/**
 * @brief Funcion para verificar si dos palabras son un anagrama.
 * Una cadena es un anagrama de otra si la segunda es simplemente un 
 * reordenamiento de la primera. Por ejemplo, \b 'fresa' y \b 'frase' son 
 * anagramas. Las cadenas \b 'caro' y \b 'roca' son también anagramas.
 * 
 * @param[in] op1 operando uno de la operacion
 * @param[in] op2 operando dos de la operacion
 * \param[in] sen optional, este nos permite habilitar o deshabilitar la 
 * comparacion sensitiva entre mayuscula y minuscula. Por defecto \b false 
 * 'deshabilitado el sensistive case'
 * @return true es un anagrama
 * @return false no es un anagrema
 */
bool checkAnagrama( const std::string& op1, const std::string& op2,bool sen=false);

/**
 * @brief Funcion para verificar si dos palabras son un anagrama. 
 * Una cadena es un anagrama de otra si la segunda es simplemente un 
 * reordenamiento de la primera. Por ejemplo, \b 'fresa' y \b 'frase' son 
 * anagramas. Las cadenas \b 'caro' y \b 'roca' son también anagramas.
 * 
 * @param[in] op1 operando uno de la operacion
 * @param[in] op2 operando dos de la operacion
 * \param[in] sen optional, este nos permite habilitar o deshabilitar la 
 * comparacion sensitiva entre mayuscula y minuscula. Por defecto \b false 
 * 'deshabilitado el sensistive case'
 * @return true es un anagrama
 * @return false no es un anagrema
 */
bool checkAnagrama( const char* op1, const char* op2,bool sen=false);


#endif /* #ifndef __check_anagrama_hpp__ */
