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
@file logger.hpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   logger with colort
@details loger message in stream file with color for levels error, warning, info, success
@version 0.0.1.
@date Viernes 22 de Junio de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date           Version      Brief
JEL            2026.05.22     0.0.1        Version Inicial no release

* ********************************************************************************** */

#ifndef __logger_hpp__
#define  __logger_hpp__ /**<@brief header module name idem to pragma once */

#include <stdarg.h> /* stdarg(3) */
#include <cstdio>   /* printf(3) */
#include <cstring>  /* strerror(3) */

#define LVL_ERROR   10  /** Indicator for select colour of level error */
#define LVL_WARNING 11  /** Indicator for select colour of level warning */ 
#define LVL_INFO    12  /** Indicator for select colour of level information */
#define LVL_SUCCESS 13  /** Indicator for select colour of level success */

namespace utillog {
    /* Font Color
        - RESET          "\033[0m"
        - BLACK          "\033[30m"      
        - RED            "\033[31m"      
        - GREEN          "\033[32m"      
        - YELLOW         "\033[33m"      
        - BLUE           "\033[34m"      
        - MAGENTA        "\033[35m"      
        - CYAN           "\033[36m"      
        - WHITE          "\033[37m"      
        - BOLD BLACK     "\033[1m\033[30m" 
        - BOLD RED       "\033[1m\033[31m" 
        - BOLD GREEN     "\033[1m\033[32m" 
        - BOLD YELLOW    "\033[1m\033[33m" 
        - BOLD BLUE      "\033[1m\033[34m" 
        - BOLD MAGENTA   "\033[1m\033[35m" 
        - BOLD CYAN      "\033[1m\033[36m" 
        - BOLD WHITE     "\033[1m\033[37m"     
    */
    constexpr const char* FC_LOG_ERROR = "\033[1m\033[31m"; 
    constexpr const char* FC_LOG_WARN  = "\033[1m\033[33m";
    constexpr const char* FC_LOG_INFO  = "\033[1m\033[34m";
    constexpr const char* FC_LOG_DEBUG = "\033[1m\033[32m";
    constexpr const char* FC_LOG_RESET = "\x1b[0m";

    struct Logger{
        /**
         * @brief constructor para el objeto Logger
         */
        Logger(const char* fname=nullptr){
            if (fname){
                this->fname_ = std::string(fname);
                this->std_ = false;
            }
            else{
                this->std_ = true;
                this->ou_ = stdout;
            }                
        }
        Logger(const Logger&) = delete ;
        Logger operator=(const Logger&) = delete;

        /**
         * @brief put string in ostream file
         * 
         * @tparam LOG template params for Level colors
         * @param[in] msg CStyle string with message.
         */
        template <int LOG=0>    
        void puts(const char* msg){
            if (!msg) return;
            this->open_();
            if constexpr (LOG==LVL_ERROR){
                std::fputs(FC_LOG_ERROR,this->ou_);    
            }
            else if constexpr (LOG==LVL_WARNING){
                std::fputs(FC_LOG_WARN,this->ou_);
            }
            else if constexpr (LOG==LVL_INFO){
                std::fputs(FC_LOG_INFO,this->ou_);    
            }
            else if constexpr (LOG==LVL_SUCCESS){
                std::fputs(FC_LOG_DEBUG,this->ou_);    
            }
            std::fputs(msg,this->ou_);

            if constexpr (LOG==LVL_ERROR || LOG == LVL_WARNING || LOG == LVL_INFO || LOG == LVL_SUCCESS){
                std::fputs(FC_LOG_RESET,this->ou_);
            }
            this->close_();
        }

        /**
         * @brief put formated string in ostream file
         * 
         * @tparam LOG template params for Level colors
         * @param fmt CStyle string with formated message
         * @param ... param for string formated `fmt`
         */
        template <int LOG=0>
        void printf(const char* fmt,...){
            if (!fmt) return;
            va_list args;
            va_start(args, fmt );
            if constexpr (LOG==LVL_ERROR){
                return this->print_(FC_LOG_ERROR,fmt,args);    
            }
            if constexpr (LOG==LVL_WARNING){
                return this->print_(FC_LOG_WARN,fmt,args);    
            }
            if constexpr (LOG==LVL_INFO){
                return this->print_(FC_LOG_INFO,fmt,args);    
            }
            if constexpr (LOG==LVL_SUCCESS){
                return this->print_(FC_LOG_DEBUG,fmt,args);    
            }
            return this->print_(nullptr,fmt,args);
        }

        template <int LOG=0>
        void vprintf(const char* fmt, va_list args){
            if (!fmt) return;            
            if constexpr (LOG==LVL_ERROR){
                return this->print_(FC_LOG_ERROR,fmt,args);    
            }
            if constexpr (LOG==LVL_WARNING){
                return this->print_(FC_LOG_WARN,fmt,args);    
            }
            if constexpr (LOG==LVL_INFO){
                return this->print_(FC_LOG_INFO,fmt,args);    
            }
            if constexpr (LOG==LVL_SUCCESS){
                return this->print_(FC_LOG_DEBUG,fmt,args);    
            }
            return this->print_(nullptr,fmt,args);
        }

        protected:
            std::string fname_{};
            bool std_ {};
            std::FILE* ou_{};

            void open_(){
                if (this->std_) return;
                this->ou_ = std::fopen(this->fname_.c_str(), "a+");
                if (this->ou_) return;
                
                std::fprintf(stderr,"Error '%s' opening file '%s'\n",std::strerror(errno),this->fname_.c_str());
                this->ou_ = stdout;
                this->std_ = true;
            }
            
            void close_(){
                /* flush stream */
                std::fflush(this->ou_);
                if (this->std_) return;
                std::fclose(this->ou_);
            }

            /**
             * @brief metodo que se encarga de imprimir los datos peticionados sobre el 
             * stream file
             * 
             * @param[in] col color
             * @param[in] fmt CSting con formato
             * @param[in] args restos de argumentos que se imprimiran.
             */
            void print_(const char* col,const char* fmt,va_list args){  
                this->open_();
                if(col) std::fprintf( this->ou_,"%s",col);

                /* abrimos la lista de argumentos */  
                std::vfprintf( this->ou_, fmt, args );  
                /* cerramos la lista de argumentos */
                va_end( args );
                if(col) fprintf( this->ou_,"%s",FC_LOG_RESET);                
                this->close_();
            }
    };
};


#endif /* #ifndef __logger_hpp__ */
