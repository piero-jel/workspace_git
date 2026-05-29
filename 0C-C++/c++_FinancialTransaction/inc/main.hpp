/** ******************************************************************************************************//**
* \addtogroup main
* @{ }// delete this
* \copyright
* Copyright 2024, Jesus Emanuel Luccioni
* All rights reserved.
* 
* Redistribution and use in source and binary forms, with or without
* modification, are permitted provided that the following conditions are met:
* 
*  1. Redistributions of source code must retain the above copyright notice,
*     this list of conditions and the following disclaimer.
* 
*  2. Redistributions in binary form must reproduce the above copyright notice,
*     this list of conditions and the following disclaimer in the documentation
*     and/or other materials provided with the distribution.
* 
*  3. Neither the name of the copyright holder nor the names of its
*     contributors may be used to endorse or promote products derived from this
*     software without specific prior written permission.
* 
* THIS SOURCE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
* IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
* ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
* LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
* SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
* INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
* CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
* ARISING IN ANY WAY OUT OF THE USE OF THIS SOURCE, EVEN IF ADVISED OF THE
* POSSIBILITY OF SUCH DAMAGE.
*
* \file main.hpp
* \author Jesus Emanuel Luccioni - piero.jel@gmail.com.
* \brief Financial Transaction.
* \details Financial Transaction se basa en un software que simule una transaccion financiera.
*
* \version 0.0.1.
* \date Sabado 8 de Junio de 2024.
* \pre pre, condiciones que deben cuplirse antes del llamado,
* \bug bug, depuracion example: Not all memory is freed when deleting an object
* of this class.
* \warning
* \note
* \par \b Change History:
* Author         Date                 Version     Brief
* JEL            2024.05.06           0.0.1       Version Inicial no release
*
* @} doxygen end group definition
* ********************************************************************************************************* */
#ifndef __main_hpp__
#define __main_hpp__







#include <iostream>
#include <string>
#include <cstdint>
#include <cstdlib>

/* header c */
#include <unistd.h> 
/* getopt();
 * extern char *optarg; 
 * extern int optind, opterr, optopt; 
 */
                      
#include <libgen.h> 
/* 
  + char *dirname(char *path);
  + char *basename(char *path);
*/                      

/**
 * @brief Objeto para el manejo de las opciones
 * ingresada por linea de comando 'CLI'
 * 
 */
struct CliApp {
    enum Flag:uint8_t {
        IP      = 0x01,
        PORT    = 0x02,
        TIMEOUT = 0x04,
        FRANGE  = 0x08,
        FCARDS  = 0x10,
        ALL     = 0x1F,
        NONE    = 0x00
    };
    
    /* BEGIN attributes */
    std::string app{};    /**<@brief apliction name */
    std::string ip{};     /**<@brief -i ip server */
    uint16_t port{};      /**<@brief -p port server, para almacenar el numero de puerto */
    uint32_t timeout{};   /**<@brief -t timeout receive */
    std::string frange{}; /**<@brief -r path/file range */
    std::string fcards{}; /**<@brief -c path/file cards */
    /* END   attributes */
  
    /* BEGIN methods */
    /**
     * @brief Construct a new Cli App object
     * @param[in] argc opcional numero de arguements
     * @param[in] argv opcional array de arguements
     * @param[in,out] ou opcional, FILE stream para el print
     * de info en caso de ser necesario. Por defecto es stdout.
     */
    CliApp(int argc=0,char* argv[]=nullptr,FILE* ou= stdout);

    /**
     * @brief Este metodo realiza el parsin e inicializa
     * todas las opciones de linea de comando de la aplicacion
     * @param[in] argc numero de arguements
     * @param[in] argv array de arguements
     * @param[in,out] ou opcional, FILE stream para el print
     * de info en caso de ser necesario. Por defecto es stdout.
     */
    void parser(int argc,char** argv,FILE* ou= stdout);

    /**
     * @brief Para el print del help
     * @param[in,out] ou opcional, FILE stream para el print
     * de info en caso de ser necesario. Por defecto es stdout.
     */
    void help(FILE* ou= stdout);

    /**
     * @brief Metodo para establecer el estado de un flag,
     * de esta forma podemos chequear que parametros se pasaron
     * y cuales nos. 
     * @param[in] flag a establecer \p Flags
     * @param[in] st estado para el flag
     */
    void flags(Flag flag,bool st);

    /**
     * @brief Metodo para obtener el estado de un flag o un grupo de flags
     * @param flag que se desea consultar \p Flags
     * @return true se paso el argumentos relacionado
     * @return false No se paso.
     */
    bool flags(Flag flag);
    /* END   methods */

    /**
     * @brief metodo para depuracion
     * @param[in,out] ou opcional, FILE stream para el print
     * de info en caso de ser necesario. Por defecto es stdout.
     */
    void print(FILE* ou=stdout);


    private:
        uint8_t __flag{};
};




  



#endif /*#ifndef __main_hpp__ */
