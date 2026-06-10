/** ***********************************************************************************//**
\addtogroup unittests
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
@file unittest.hpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   unittest header file
@details class base for unittest case and execute
@version 0.0.1.
@date Viernes 22 de Junio de 2026.
@pre condiciones que deben cuplirse antes del llamado,
@bug depuracion example: Not all memory is freed when deleting an object of this class.
@warning
@note
@Change History:
Author         Date                 Version      Brief
JEL            2026.05.22           0.0.1        Version Inicial no release

* ********************************************************************************** */
#ifndef __unittest_hpp__
#define __unittest_hpp__ /**<@brief header module name idem to pragma once */


/* header file list fo namespace unittests */
#include <cstring>
#include <memory>
#include <map>
#include <vector>
#include <utility>
#include <initializer_list>
#include <stdarg.h> /* stdarg(3) */
#include <cstdio>   /* printf(3) */
#include <functional>
#include <container_traits.hpp>
#include <logger.hpp>

#define contex() __FILE__,__PRETTY_FUNCTION__,__LINE__

namespace unittest {
    constexpr const char* FC_FAILURE = "\033[1m\033[31m";    
    constexpr const char* FC_SUCCES  = "\033[1m\033[32m";
    constexpr const char* FC_RESET   = "\x1b[0m";
    constexpr const char* FMT_FAILURE = "%s: [%s:%s:%u Failure] ";
    constexpr const char* FMT_FAILURE_DETAIL = "%s: [%s:%s:%u Failure, detail %s] ";

    struct TestCaseAsserts {
        using AssertCallback = std::function<bool (void)> ;
        
        /**
         * @brief metodo para establecer el logger a utilizar
         * @param[in] log smart pointer/shared
         */
        void logger(std::shared_ptr<utillog::Logger> log){ this->log = log; }

        /**
         * @brief metodo para imprimir un string sobre el log
         * @tparam LOG Opcional, level log para el set de color
         * - \b LVL_ERROR   set colour for error
         * - \b LVL_WARNING set colour for warning
         * - \b LVL_INFO    set colour for information
         * - \b LVL_SUCCESS set colour for success
         * @param[in] msg mensjae a imprimir sobre el lob
         */
        template <int LOG=0>
        void puts(const char* msg){
            if (!this->log || !msg) return;
            return this->log->puts<LOG>(msg);
        }

        /**
         * @brief metodo para imprimir un mensaje con formato sobre el log
         * @tparam LOG Opcional, level log para el set de color
         * - \b LVL_ERROR   set colour for error
         * - \b LVL_WARNING set colour for warning
         * - \b LVL_INFO    set colour for information
         * - \b LVL_SUCCESS set colour for success
         * @param[in] fmt string CStyel con el formato, este sigue el formato de \b std::printf()
         * @param ... parametros para el string format
         */
        template <int LOG=0>
        void printf(const char* fmt,...){
            if (!this->log || !fmt) return;
            va_list args;
            va_start(args, fmt );
            return this->log->vprintf<LOG>(fmt,args);            
        }

        /**
         * @brief metodo para verificar si el parametro es true, o `bool(op) == true`.
         * @tparam T tipo item
         * @param[in] op item u operando a verificar.
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         */
        template <typename T>
        void assert_true(const T& op,
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0){
            this->_assert([&op]{return (op)? true:false;},__func__,file,fn,nline);
        }

        /**
         * @brief metodo para verificar si el parametro es false, o `bool(op) == false`.
         * @tparam T tipo item
         * @param[in] op item u operando a verificar.
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         */
        template <typename T>
        void assert_false(const T& op,
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0){
            this->_assert([&op]{ return (op)? false : true;},__func__,file,fn,nline);
        }

        /**
         * @brief metodo para verificar si dos item u operandos son iguales en valor
         * @tparam T tipo item
         * @param[in] op1 item u operando uno
         * @param[in] op2 item u operando dos
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         * @param[in] cmp Opcional function, en caso de necesitar una comparacion especial entre items
         */
        template <typename T>
        void assert_equal(const T& op1,const T& op2,            
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                std::function<bool (const T &, const T &)> cmp = {} ){
            if (!cmp) cmp = this->_gen_comp<T>(true);
            this->_assert_compare(op1,op2,__func__,file,fn,nline,cmp);
        }

        /**
         * @brief metodo para verificar si dos item u operandos son diferentes en valor
         * @tparam T tipo item
         * @param[in] op1 item u operando uno 
         * @param[in] op2 item u operando dos
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         * @param[in] cmp Opcional function, en caso de necesitar una comparacion especial entre items
         */
        template <typename T>
        void assert_not_equal(const T& op1,const T& op2,
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                std::function<bool (const T &, const T &)> cmp = {} ){

            if (!cmp) cmp = this->_gen_comp<T>(false);
            this->_assert_compare(op1,op2,__func__,file,fn,nline,cmp);
        }

        /**
         * @brief metodo para verificar que dos contenedores son iguales
         * @tparam C tipo de contenedor
         * @param[in] c1 contenedor u operando uno de la comparacion
         * @param[in] c2 contenedor u operando dos de la comparacion 
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         * @param[in] cmp Opcional function, en caso de necesitar una comparacion especial entre items
         */
        template <typename C>
        void assert_container_equal(const C& c1,const C& c2,                
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                std::function<bool (const typename C::value_type&, const typename C::value_type&)> cmp={}
            ){
            using Item = typename C::value_type;
            if (!cmp) cmp = this->_gen_comp<Item>(true);
            this->_assert_container(c1,c2,__func__,file,fn,nline,cmp,"Item in position %lu not equal");
        }

        /**
         * @brief metodo para verificar que dos contenedores no son iguales
         * @tparam C tipo de contenedor
         * @param[in] c1 contenedor u operando uno de la comparacion
         * @param[in] c2 contenedor u operando dos de la comparacion 
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         * @param[in] cmp Opcional function, en caso de necesitar una comparacion especial entre items
         */
        template <typename C>
        void assert_container_not_equal(const C& c1,const C& c2,                
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                std::function<bool (const typename C::value_type&, const typename C::value_type&)> cmp={}
            ){
            using Item = typename C::value_type;
            if (!cmp) cmp = this->_gen_comp<Item>(false);
            this->_assert_container<C,C,false>(c1,c2,__func__,file,fn,nline,cmp,"All (%lu) items are equal");
        }

        /**
         * @brief metodo para verificar si un item igual se localizar en un contenedor
         * @tparam C tipo de contenedor
         * @param[in] v valor o item a buscar
         * @param[in] c contenedor donde se buscara el item
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         * @param[in] cmp Opcional function, en caso de necesitar una comparacion especial entre items
         */
        template <typename C>
        void assert_in_container(const typename C::value_type& v, const C& c,
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                std::function<bool (const typename C::value_type&, const typename C::value_type&)> cmp={}
            ){
            using Item = typename C::value_type;
            if (!cmp) cmp = this->_gen_comp<Item>(true);
            this->_assert_container<Item,C,false>(v,c,__func__,file,fn,nline,cmp,"Item not found in container of %lu elements.");
        }

        /**
         * @brief metodo para verificar que un item (por valor) no se localizar en un contenedor
         * @tparam C tipo de contenedor
         * @param[in] v valor o item a buscar
         * @param[in] c contenedor donde se buscara el item
         * @param[in] file nombre del source file del caller
         * @param[in] fn nombre del metodo del caller
         * @param[in] nline numero de linea del caller
         * @param[in] cmp Opcional function, en caso de necesitar una comparacion especial entre items
         */
        template <typename C>
        void assert_not_in_container(const typename C::value_type& v, const C& c,
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                std::function<bool (const typename C::value_type&, const typename C::value_type&)> cmp={}
            ){
            using Item = typename C::value_type;
           if (!cmp) cmp = this->_gen_comp<Item>(false);
            this->_assert_container<Item,C,true>(v,c,__func__,file,fn,nline,cmp,"Item found in position %lu.");
        }

        /**
         * @brief template method para el catch de una exception
         * @tparam E template param para indicar el tipo de exception a recibir
         * @param fn funccion cuyo body debe lanzar la exception del tipo \b E
         */
        template <typename E>
        void assert_exception(std::function<void(void)> fn){
            try{
                fn();
                this->_status = false;
            }
            catch(const E& e ){
                this->_status = true;
            }
            catch( ... ){
                this->_status = false;
            }            
        }

        virtual ~TestCaseAsserts(){}

        protected:
            std::shared_ptr<utillog::Logger> log {};
            bool _status{}; /* estado del test */

            /**
             * @brief template method que ejecuta un assert con function sin operandos
             * @param[in] op function que se encarga de realizar la comparacion
             * @param[in] lfn nombre del assert que invoco
             * @param[in] file nombre del source file del caller final
             * @param[in] fn nombre de la clase/method del caller final
             * @param[in] nline numero de linea del caller final
             */
            void _assert(AssertCallback op,const char* lfn,
                const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0){
                    if (!op()){
                        this->_status = false;
                        if(this->log)
                            this->log->printf<LVL_ERROR>(FMT_FAILURE ,(lfn)?lfn:"",(file)?file:"",(fn)?fn:"",nline);
                    }
            }

            /**
             * @brief template metodo que se encarga de realizar una comparacion
             * @tparam T template of the item to compare
             * @param[in] v1 valor uno 
             * @param[in] v2 valor dos
             * @param[in] lfn nombre del assert que invoco
             * @param[in] file nombre del source file del caller final
             * @param[in] fn nombre de la clase/method del caller final
             * @param[in] nline numero de linea del caller final
             * @param[in] cmp 
             */
            template <typename T>
            void _assert_compare(const T& v1,const T& v2,const char* lfn,                
                    const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                    std::function<bool (const T&, const T&)> cmp={}){

                if (!cmp(v1,v2)){
                    this->_status = false;
                    if(this->log)
                        this->log->printf<LVL_ERROR>(FMT_FAILURE ,(lfn)?lfn:"",(file)?file:"",(fn)?fn:"",nline);
                }            
            }

            /**
             * @brief template method que ejecuta un assert sobre un contenedor STL
             * @tparam C1 template para el contendor 1
             * @tparam C2 template para el contendor 1
             * @tparam Full bool template para indicar si debe ser completo o solo para un item valido/invalido
             * @param[in] c1 contenedor uno
             * @param[in] c2 contendor dos
             * @param[in] lfn nombre del assert publico que invoco
             * @param[in] file nombre del source file del caller final
             * @param[in] fn nombre de la class/method del caller final
             * @param[in] nline numero de linea del caller final
             * @param[in] cmp object function que se utilizara para la comparacion
             * @param[in] msg opcional, mensaje que se debe agregar en caso de failure
             */
            template <typename C1,typename C2,bool Full=true>
            void _assert_container(const C1& c1,const C2& c2,const char* lfn,                
                    const char* file=nullptr,const char* fn=nullptr,std::size_t nline=0,
                    std::function<bool (const typename C2::value_type&, const typename C2::value_type&)> cmp={},
                    const char* msg=nullptr
                ){
                using It = typename C2::const_iterator;
                bool nitem = false;
                char buf[128];
                if constexpr (Full && std::same_as<C1,C2>){
                    if constexpr (utiltraits::is_forward_list<C2>){
                        nitem = std::distance(std::begin(c1),std::end(c1)) == std::distance(std::begin(c2),std::end(c2));
                    }
                    else{
                        nitem = c1.size() == c2.size();
                    }
                    if (!nitem){
                        if(this->log)
                            this->log->printf<LVL_ERROR>(FMT_FAILURE_DETAIL,lfn,(file)?file:"",(fn)?fn:"",nline,"size not equal");

                        this->_status = false;
                        return;
                    }
                }
                
                std::size_t idx = 0;
                if constexpr (std::same_as<C1,C2>){
                    It it1=std::begin(c1),it2=std::begin(c2), e1 = std::end(c1);                
                    if constexpr (Full){
                        nitem = true;
                        for (; it1 != e1; it1++,it2++,idx++){
                            if(!cmp(*it1,*it2)){
                                nitem = false;
                                break;
                            }
                        }
                    }
                    else{
                        nitem = false;
                        for (; it1 != e1; it1++,it2++,idx++){
                            if(!cmp(*it1,*it2)){
                                continue;
                            }
                            nitem = true;
                            break;
                        }
                    }
                }
                else{
                    It it=std::begin(c2),e1 = std::end(c2);                
                    if constexpr (Full){
                        nitem = true;
                        for (; it != e1; it++,idx++){
                            if(!cmp(c1,*it)){
                                nitem = false;
                                break;
                            }
                        }
                    }
                    else{
                        nitem = false;
                        for (; it != e1; it++,idx++){
                            if(!cmp(c1,*it)){
                                continue;
                            }
                            nitem = true;
                            break;
                        }
                    }
                }
                if (nitem) return;
                this->_status = false;
                if(this->log){
                    std::snprintf(buf,sizeof(buf)-1,msg,idx);
                    this->log->printf(FMT_FAILURE_DETAIL,lfn,(file)?file:"",(fn)?fn:"",nline,buf);
                }
            }

            template <typename V,int N>
            std::function<bool()> _gen_assert_fun(bool type=true,const V& op1={},const V& op2={}){
                if constexpr (N == 2){
                    if constexpr (utiltraits::is_pair<V>){
                        if (type){
                            return [&op1,&op2]() -> bool {
                                return op1.first == op2.first && op1.second == op2.second;
                            };
                        }
                        else {
                            return [&op1,&op2]() -> bool {
                                return op1.first != op2.first || op1.second != op2.second;
                            };
                        }
                    }
                    else{                
                        if (type){
                            return [&op1,&op2]() -> bool {
                                return op1 == op2;
                            };
                        }
                        else{
                            return [&op1,&op2]() -> bool {
                                return op1 != op2;
                            };
                        }
                    }
                }

            }

            template <typename V>
            std::function<bool (const V&, const V&)> _gen_comp(bool type=true){
                if constexpr (utiltraits::is_pair<V>){
                    if (type){
                        return [](const V& i1,const V& i2) -> bool {
                            return i1.first == i2.first && i1.second == i2.second;
                        };
                    }
                    else {
                        return [](const V& i1,const V& i2) -> bool {
                            return i1.first != i2.first || i1.second != i2.second;
                        };
                    }
                }
                else{                
                    if (type){
                        return [](const V& i1,const V& i2) -> bool {
                            return i1 == i2;
                        };
                    }
                    else{
                        return [](const V& i1,const V& i2) -> bool {
                            return i1 != i2;
                        };
                    }
                }
            }


    };

    class TestCase: public TestCaseAsserts {
        public:
            /* Definimo el tipo de dato con el cual almacenaremos el pointer a operacion */
            using MethodPtr = void (TestCase::*)(void);
            /**
             * @brief definicion de la enumeracion para los metodos especiales
             * - \b startUp metodo que se invocara previo a cada test case method
             * - \b tearDown metodo que se invocara luego de cada test case method
             * - \b Init metodo que se invocara previo a ejecutar todos los test case method de la test class
             * - \b deInit metodo que se invocara luego de ejecutar todos los test case method de la test class
             */
            enum class Method {
                startUp,tearDown,
                Init,deInit
            };

        private:
            MethodPtr __operation;  /* atributo donde almacenaremos el pointer  to sefl method */         

        protected:
            std::map<const char*, TestCase::MethodPtr> _test_cases{};
            std::map<Method, TestCase::MethodPtr> _method{};
            

        public:
            /** 
             * @brief cosntructor de la clase
             */
            TestCase() : __operation{nullptr} {}

        
            /* metodo que se encarga de establecer el self_method */
            void set(MethodPtr method=nullptr) {
                this->__operation = method;
                this->_status = true;
            }

            /**
             * @brief metodo que se encarga de llamar al metodo almacenado si este se asigno
             * @return true : succes test case, false failure to run test case             
             */
            bool caller(void) {
                try{
                    (this->*__operation)();                    
                }
                catch(const std::exception& e){
                    this->log->printf<LVL_ERROR>("Caller Exception detail %s \n",e.what());
                    return false;
                }
                return this->_status;
            }

            /**
             * @brief run special method
             * @param[in] name enumeration with method to run, should be:
             * - \b Method::startUp metodo que se invocara previo a cada test case method
             * - \b Method::tearDown metodo que se invocara luego de cada test case method
             * - \b Method::Init metodo que se invocara previo a ejecutar todos los test case method de la test class
             * - \b Method::deInit metodo que se invocara luego de ejecutar todos los test case method de la test class
             */
            void caller(const Method& name) {
                if (auto search = this->_method.find(name); search != this->_method.end()){
                    (this->*search->second)();
                }
            }

            /**
             * @brief metodo virtual abstracto que debera definir la clase derivada la cual contenga los 
             * test cases especificos. Mediante esta puede registrar los test case como asi tambien
             * los metodos espceiales:
             *   \b Method::startUp : metodo que se invocara previo a cada test case method
             *   \b Method::tearDown : metodo que se invocara liego de ejecutar cada test case method
             *   \b Method::Init : metodo que se invocara al inicio de los test cases
             *   \b Method::deInit : metodo que se invocara al finalizar los test cases
             */
            virtual void register_method(void) = 0;

            /**
             * @brief template function para registrar un metodo, como un test case method
             * @tparam T tipo de puntero
             * @param name nombre que recibira el test case method
             * @param method metodo, puntero al metodo
             */
            template<typename T>
            void add_method(const Method& name,T method) {
                this->_method.emplace(name,static_cast<TestCase::MethodPtr>(method));
            }
            
            /**
             * @brief metodo para registrar un metodo especial
             * @tparam T tipo de puntero
             * @param name enumeracion con el tipo especial del metodo a registrar.
             * @param method puntero al metodo que se desea registrar como especial.
             */
            template<typename T>
            void add_method(const char* name,T method) {
                this->_test_cases.emplace(name,static_cast<TestCase::MethodPtr>(method));
            }

            /**
             * @brief Get the methods object
             * @return std::map<const char*, TestCase::MethodPtr> 
             */
            const std::map<const char*, TestCase::MethodPtr>& get_methods(void){
                this->register_method();
                return this->_test_cases;
            }

            virtual ~TestCase(){}
    };

    class ExecuteTestCases {
        protected:
            std::shared_ptr<utillog::Logger> log_{};

        private:
            std::vector<std::unique_ptr<TestCase>> __tests_cases{};
            std::map<const char*, TestCase::MethodPtr> __map_op {};

        public:
            ExecuteTestCases(const ExecuteTestCases&) = delete;
            ExecuteTestCases operator=(const ExecuteTestCases&) = delete;

            /**
             * @brief Construct a new Execute Test Cases object
             * @param[in] test_case pointer to instance test case to execute
             * @param[in] fname Optional, path name to file log, default set stdout
             */
            ExecuteTestCases(TestCase* test_case,const char* fname=nullptr){
                this->__tests_cases.emplace_back(std::unique_ptr<TestCase>(test_case));                
                this->begin_(fname);
            }

            /**
             * @brief Construct a new Execute Test Cases object
             * @param[in] test_case unique pointer of the instance test case to execute
             * @param[in] fname Optional, path name to file log, default set stdout
             */
            ExecuteTestCases(std::unique_ptr<TestCase> test_case,const char* fname=nullptr){
                this->__tests_cases.emplace_back(std::move(test_case));                
                this->begin_(fname); 
            }

            /**
             * @brief Construct a new Execute Test Cases object
             * @param[in] tests_cases initializer list with the pointers to instances 
             * of test cases to execute.
             * @param[in] fname Optional, path name to file log, default set stdout
             */
            ExecuteTestCases(std::initializer_list<TestCase*> tests_cases,const char* fname=nullptr){
                for (const auto& tc:tests_cases){
                    this->__tests_cases.emplace_back(std::unique_ptr<TestCase>(tc));
                }        
                this->begin_(fname);
            }

            /**
             * @brief run particualar test case.
             * @param[in] operations name of case to run
             */
            void run(const char* operations) {
                std::size_t tc_ran=0,tc_ok=0,tc_nok=0;
                for (const auto& tc: this->__tests_cases){
                    this->__map_op = std::move(tc->get_methods());
                    if (auto search = this->__map_op.find(operations); search != this->__map_op.end()){
                        tc->caller(TestCase::Method::Init);
                        tc->caller(TestCase::Method::startUp); // incio del contexto especifico
                        tc->set(search->second);
                        tc_ran++;
                        if (tc->caller()){
                            tc_ok++;
                            this->log_->printf<LVL_SUCCESS>("Run Sucess Method %s \n",search->first);
                        }
                        else{
                            tc_nok++;
                            this->log_->printf<LVL_ERROR>("Error to run Method %s \n",search->first);
                        }
                        tc->caller(TestCase::Method::tearDown);
                        tc->caller(TestCase::Method::deInit);
                        return ;
                    }            
                }
                this->log_->printf<LVL_INFO>("Run %lu test case, %lu Success and %lu with error.\n",
                    tc_ran,tc_ok,tc_nok);             
            }

            /**
             * @brief run all test case.
             */
            void run(void) {
                std::size_t tc_ran=0,tc_ok=0,tc_nok=0;
                for (const auto& tc: this->__tests_cases){
                    this->__map_op = std::move(tc->get_methods());
                    tc->caller(TestCase::Method::Init);
                    for(const auto& [k,v]:this->__map_op){
                        tc->caller(TestCase::Method::startUp);
                        tc->set(v);
                        tc_ran++;
                        if (tc->caller()){
                            tc_ok++;
                            this->log_->printf<LVL_SUCCESS>("Run Sucess Method %s\n",k);
                        }
                        else{
                            tc_nok++;
                            this->log_->printf<LVL_ERROR>("Failure to run Method %s\n",k);
                        }
                        tc->caller(TestCase::Method::tearDown);
                    }
                    tc->caller(TestCase::Method::deInit);
                }
                this->log_->printf<LVL_INFO>("Run %lu test case, %lu Success and %lu with error.\n",
                    tc_ran,tc_ok,tc_nok);
            }

        protected:            
            void begin_(const char* fname=nullptr){
                this->log_ = std::make_shared<utillog::Logger>(fname);
                // init log for each TestCase
                for (const auto& tc:this->__tests_cases){
                    tc->logger(this->log_);
                }
            }
    };
};
#endif /* #ifndef __unittest__ */
