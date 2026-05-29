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
#include <check_anagrama.hpp> /* dut */

struct TestCaseAnagram:public unittest::TestCase {


    void string_same_word(void) {
        std::string w1 = "carlos",w2="carlos";
        this->assert_false(checkAnagrama(w1,w2),contex());
    }
    void const_char_same_word(void) {
        const char* w1 = "carlos";
        const char* w2="carlos";
        this->assert_false(checkAnagrama(w1,w2),contex());
    }

    void string_diff_len(void) {
        std::string w1 = "carlos",w2="carlo";
        this->assert_false(checkAnagrama(w1,w2),contex());
    }
    void const_char_diff_len(void) {
        const char *w1 = "carlos",*w2="carlo";
        this->assert_false(checkAnagrama(w1,w2),contex());
    }

    void string_ok(void) {
        using List = std::vector<std::pair<std::string,std::string>> ;
        List v_ok = {
            {"carlos","solarc"},
            {"nacionalista","altisonancia"},            
        };
        
        for (const auto& [i1,i2]:v_ok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s)\n",i1.c_str(),i2.c_str());
            this->assert_true(checkAnagrama(i1,i2),contex());
        }
    }
    void string_nok(void) {
        using List = std::vector<std::pair<std::string,std::string>> ;
        List v_ok = {
            {"carlos","alberto"},
            {"Nacionalista","Altisonancia"},
            {"Raiz","zi a"},
        };
        
        for (const auto& [i1,i2]:v_ok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s)\n",i1.c_str(),i2.c_str());
            this->assert_false(checkAnagrama(i1,i2),contex());
        }
    }
    void string_sensitive(void) {
        using List = std::vector<std::pair<std::string,std::string>> ;
        List v_ok = {
            {"carlos","solarc"},
            {"Nacionalista","Altisonancia"},
            {"Roma","amor"},
            {"fresa","Frase"},
            {"GATO","gota"},
            {"Sergio","riesgo"},
        };
        
        for (const auto& [i1,i2]:v_ok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s,true)\n",i1.c_str(),i2.c_str());
            this->assert_true(checkAnagrama(i1,i2,true),contex());
        }        
    }
    void string_sensitive_nok(void) {
        using List = std::vector<std::pair<std::string,std::string>> ;
        List v_nok = {
            {"carlOs","Alberto"},
            {"internacional","Altisonancia"},
            {"CARLOS","carlos"},
            {"CARLOS","Acaraz"},
        };
        
        for (const auto& [i1,i2]:v_nok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s,true)\n",i1.c_str(),i2.c_str());
            this->assert_false(checkAnagrama(i1,i2,true),contex());
        }        
    }
    void const_char_ok(void) {
        using List = std::vector<std::pair<const char*,const char*>> ;
        List v_ok = {
            {"carlos","solarc"},
            {"nacionalista","altisonancia"},            
        };
        
        for (const auto& [i1,i2]:v_ok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s)\n",i1,i2);
            this->assert_true(checkAnagrama(i1,i2),contex());
        }
    }
    void const_char_nok(void) {
        using List = std::vector<std::pair<const char*,const char*>> ;
        List v_ok = {
            {"carlos","alberto"},
            {"Nacionalista","Altisonancia"},
            {"Raiz","zi a"},
        };
        
        for (const auto& [i1,i2]:v_ok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s)\n",i1,i2);
            this->assert_false(checkAnagrama(i1,i2),contex());
        }
    }

    void const_char_sensitive(void) {
        using List = std::vector<std::pair<const char*,const char*>> ;
        List v_ok = {
            {"carlos","solarc"},
            {"Nacionalista","Altisonancia"},
            {"carlos","solarc"},
            {"Nacionalista","Altisonancia"},
            {"Roma","amor"},
            {"fresa","Frase"},
            {"GATO","gota"},
            {"Sergio","riesgo"}
        };
        
        for (const auto& [i1,i2]:v_ok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s,true)\n",i1,i2);
            this->assert_true(checkAnagrama(i1,i2,true),contex());
        }        
    }
    void const_char_sensitive_nok(void) {
        using List = std::vector<std::pair<const char*,const char*>> ;
        List v_nok = {
            {"carlOs","Alberto"},
            {"internacional","Altisonancia"},
            {"CARLOS","carlos"},
            {"CARLOS","Acaraz"}
        };
        
        for (const auto& [i1,i2]:v_nok){
            this->assert_not_equal(i1,i2,contex());
            this->log->printf("checkAnagrama(%s,%s,true)\n",i1,i2);
            this->assert_false(checkAnagrama(i1,i2,true),contex());
        }        
    }


    void init(){
        this->log->puts<LVL_SUCCESS>("Inicio de la ejecucion Class TestCaseAnagram\n");
    }
    void deinit(){
        this->log->puts<LVL_SUCCESS>("Fin    de la ejecucion Class TestCaseAnagram\n");
    }

    virtual void register_method(void){
        this->add_method("string_same_word",&TestCaseAnagram::string_same_word);
        this->add_method("const_char_same_word",&TestCaseAnagram::const_char_same_word);
        this->add_method("string_diff_len",&TestCaseAnagram::string_diff_len);
        this->add_method("const_char_diff_len",&TestCaseAnagram::const_char_diff_len);
        this->add_method("string_ok",&TestCaseAnagram::string_ok);
        this->add_method("string_nok",&TestCaseAnagram::string_nok);
        this->add_method("string_sensitive",&TestCaseAnagram::string_sensitive);
        this->add_method("string_sensitive_nok",&TestCaseAnagram::string_sensitive_nok);
        this->add_method("const_char_ok",&TestCaseAnagram::const_char_ok);
        this->add_method("const_char_nok",&TestCaseAnagram::const_char_nok);
        this->add_method("const_char_sensitive",&TestCaseAnagram::const_char_sensitive);
        this->add_method("const_char_sensitive_nok",&TestCaseAnagram::const_char_sensitive_nok);
        
        
        this->add_method(Method::Init,&TestCaseAnagram::init);
        this->add_method(Method::deInit,&TestCaseAnagram::deinit);
    }
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
        
        {
            std::cout<<"\nTest ExecuteTestCases, smart pointer\n";
            unittest::ExecuteTestCases operations{
                std::make_unique<TestCaseAnagram>()
            };
            operations.run();
        }

        if constexpr(0) {
            std::cout<<"\nTest ExecuteTestCases, current pointer\n";
            unittest::ExecuteTestCases operations{
                new TestCaseAnagram()            
            };
            operations.run();
        }      



        
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
