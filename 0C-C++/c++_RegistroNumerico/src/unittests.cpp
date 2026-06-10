/** ***********************************************************************************//**
\addtogroup unittest
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
@file unittests.cpp
@author Jesus Emanuel Luccioni - jeluccioni@gmail.com.
@brief   unit test for modules
@details Test cases and execute unit test for functions
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

#include <unittest>
#include <utilities>
#include <registro.hpp>

using namespace utilities;



struct TestRegistro:public unittest::TestCase {

    

    void get_ok(void) {
        std::string val = "9876543210";
        this->reg.set(val);        
        this->assert_equal(this->reg.get(),std::stol(val),contex());
    }
    void const_char_get_ok(void) {
        const char* val = "123456789";        
        this->reg.set(val);
        this->assert_equal(this->reg.get(),std::atol(val),contex());
    }

    
    void get_ok_list(void) {
        using List = std::vector<const char*>;
        List v_ok {
            "17066311",
            "170311",
            "17031"
        };        
        for (const auto& it : v_ok){
            this->reg.set(it);
            this->assert_equal(this->reg.get(),std::stol(it),contex());            
        }
    }
    
    void get_nullptr(void) {
        this->assert_exception<Exception<>>(
            [this](void){
                this->reg.set(nullptr);                
            }
        );
    }

    void get_too_long(void) {
        this->assert_exception<Exception<>>(
            [this](void){
                this->reg.set("9876543210123");
            }
        );
    }
    void get_not_int(void) {
        this->assert_exception<Exception<>>(
            [this](void){
                this->reg.set("98765.123");
            }
        );
    }
    
    void init(){
        this->log->puts<LVL_SUCCESS>("Inicio de la ejecucion Class TestRegistro\n");
    }
    void deinit(){
        this->log->puts<LVL_SUCCESS>("Fin    de la ejecucion Class TestRegistro\n\n");
    }
    void start_up(){
        this->reg.set(int64_t(0));
    }
    virtual void register_method(void){
        
        this->add_method("get_ok",&TestRegistro::get_ok);
        this->add_method("const_char_get_ok",&TestRegistro::const_char_get_ok);
        this->add_method("get_ok_list",&TestRegistro::get_ok_list);
        this->add_method("get_nullptr",&TestRegistro::get_nullptr);
        this->add_method("get_too_long",&TestRegistro::get_too_long);
        this->add_method("get_not_int",&TestRegistro::get_not_int);

        this->add_method(Method::Init,&TestRegistro::init);
        this->add_method(Method::deInit,&TestRegistro::deinit);
        this->add_method(Method::startUp,&TestRegistro::start_up);
    }

    Registro reg{};
};


/**
 * \brief Funcion Principal
 * \param[in] argc : cantidad de Argumentos pasados al invocar la app.
 * \param[in] argv : puntero a puntero que contiene el listado de
 * \return status de la ejecucion de la app.
 *    - 0, success
 *    - 1, failure **/
int main(int /*argc*/, char* /*argv*/[]) {
    try{


        std::cout<<"\nTest ExecuteTestCases, current pointer\n";
        unittest::ExecuteTestCases operations{
            new TestRegistro()
        };
        operations.run();

        std::fputc('\n',stdout);
    }
    catch(const std::exception &e){
        std::fprintf(stdout,"Excepcion Capturada \"%s\"\n",e.what());
    }
    catch(...){
        std::fputs("Excepcion Desconocida",stdout);
    }
    std::fputc('\n',stdout);
    exit(EXIT_SUCCESS);
}
