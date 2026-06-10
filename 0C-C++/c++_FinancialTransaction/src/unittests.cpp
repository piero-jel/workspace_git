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
#include <financial_transaction.hpp>
#include <PSocket.hpp>
#include <thread>


using namespace utilities;
constexpr uint16_t VER = 0;
constexpr uint32_t N = 256; /* valor por defecto para el buffer de Exception */
constexpr const char* PATH_RANGE = "files/local/ranges.dat";
constexpr const char* PATH_CARDS = "files/local/cards.dat";
//constexpr const char* SERVER_IP   = "0.0.0.0";
constexpr const char* SERVER_IP   = "127.0.0.1";
//constexpr const char* SERVER_PORT = "3030";
constexpr uint16_t SERVER_PORT = 3030;

struct Input{
    std::string val {};

    void value(const char* val){
        this->val = val;
    }

    const char* value(void){
        return this->val.c_str();
    }

    void operator()(char* b,uint32_t l){
        if(this->val.length() < 1){
            val = "\r";
        }
        std::strncpy(b,this->val.c_str(),l);
    }
};

struct Server{
    Server(std::function<std::string(const char*)> handler={},
            uint16_t port=SERVER_PORT,const char* ip=SERVER_IP){
        this->socket = PSocket::StreamServer(ip,port);
        this->handler = handler;
    }

    void handler_client(int fd){
        PSocket::Stream socket (fd);
        char buf[1024];
        while(true){
            socket.Recv(buf,sizeof(buf));
            if(buf[0] == '\0'){
                break;
            }
            socket.Send(handler(buf));
        }
        socket.Disconnect();
    }

    void handler_server(void){
        /* un solo client */
        int fd = this->socket.Accept();
        std::thread th (&Server::handler_client,this,fd);
        th.join();
        /*
        while(true){
            int fd = this->socket.Accept();
            std::thread th (&Server::handler_client,this,fd);
            th.detach();
        }*/
    }

    void run(std::function<std::string(const char*)> handler={}){
        this->handler = handler;
        this->socket.Connect();
        this->srv = std::thread(&Server::handler_server,this);
    }

    void join(void){
        this->srv.join();
    }

    void close(void){
        int err = this->socket.Disconnect();
        std::cout<<"close() err :"<<err<<'\n';
    }
    
    //enum class Handler {Echo,RespOk,Respnok};
    std::function<std::string(const char*)> handler{};
    PSocket::StreamServer socket{};
    std::thread srv{};
    //std::vector<std::thread> threads{};
    
};


struct TestCardNumber:public unittest::TestCase {
    Input in{};

    void get_stdin(void) {
        std::string card_number = GetCardNumber(
            [](char* buf,uint32_t len){
                std::fputs("Ingrese el Numero de Tarjeta ( 13 ~ 99 decimales): ",stdout);                
                std::fgets(buf,len-1,stdin);
            }
        );
        this->log->printf<LVL_INFO>("Card number: %s\n",card_number.c_str());
    }

    void get_ok(void) {
        this->in.value("4517650654628311");
        std::string card_number = GetCardNumber(this->in);
        this->assert_equal(card_number,this->in.val,contex());
    }

    void get_ok_list(void) {
        using List = std::vector<const char*>;
        List v_ok {
            "4517650654628311",
            "4517650654628311\n",
            "4517650654628311\r"
        };
        std::string card_number;
        for (const auto& it : v_ok){
            this->in.value(it);
            card_number = GetCardNumber(this->in);
            this->assert_equal<std::string>(card_number,"4517650654628311",contex());
        }
    }

    void get_too_short(void) {
        this->assert_exception<Exception<N>>(
            [this](void){                
                this->in.value("0123456789");
                GetCardNumber(this->in);
            }
        );
    }

    void get_not_number(void) {
        this->assert_exception<Exception<N>>(
            [this](void){                
                this->in.value("0123456789ABCDEF");
                GetCardNumber(this->in);
            }
        );
    }

    void init(){
        this->log->puts<LVL_SUCCESS>("Inicio de la ejecucion Class TestCardNumber\n");
    }
    void deinit(){
        this->log->puts<LVL_SUCCESS>("Fin    de la ejecucion Class TestCardNumber\n\n");
    }

    virtual void register_method(void){
        //this->add_method("get_stdin",&TestGetAmount::get_stdin);
        this->add_method("get_ok",&TestCardNumber::get_ok);
        this->add_method("get_ok_list",&TestCardNumber::get_ok_list);
        this->add_method("get_too_short",&TestCardNumber::get_too_short);
        this->add_method("get_not_number",&TestCardNumber::get_not_number);
        
        
        this->add_method(Method::Init,&TestCardNumber::init);
        this->add_method(Method::deInit,&TestCardNumber::deinit);
    }
};

struct TestCardCode:public unittest::TestCase {
    Input in{};
    void get_stdin(void) {
        std::string card_code = GetCardCode(
            [](char* buf,uint32_t len){
                std::fputs("Ingrese el codigo de tarjet 3-Digitos): ",stdout);                
                std::fgets(buf,len-1,stdin);
            }
        );
        this->log->printf<LVL_INFO>("Card code: %s\n",card_code.c_str());
    }

    void get_ok(void) {
        this->in.value("123");
        std::string card_code = GetCardCode(this->in);
        this->assert_equal(card_code,this->in.val);
    }

    void get_ok_list(void) {
        using List = std::vector<const char*>;
        List v_ok {
            "321",
            "321\n",
            "321\r",
        };
        std::string card_code;
        for (const auto& it : v_ok){
            this->in.value(it);
            card_code = GetCardCode(this->in);
            this->assert_equal<std::string>(card_code,"321");
        }
    }

    void get_too_long(void) {
        this->assert_exception<Exception<N>>(
            [this](void){                
                this->in.value("123456789");
                GetCardCode(this->in);
            }
        );
    }

    void get_not_number(void) {
        this->assert_exception<Exception<N>>(
            [this](void){                
                this->in.value("1B2");
                GetCardCode(this->in);
            }
        );
    }


    void init(){
        this->log->puts<LVL_SUCCESS>("Inicio de la ejecucion Class TestCardCode\n");
    }
    void deinit(){
        this->log->puts<LVL_SUCCESS>("Fin    de la ejecucion Class TestCardCode\n\n");
    }

    virtual void register_method(void){        
        //this->add_method("get_stdin",&TestCardCode::get_stdin);
        this->add_method("get_ok",&TestCardCode::get_ok);
        this->add_method("get_ok_list",&TestCardCode::get_ok_list);
        this->add_method("get_too_long",&TestCardCode::get_too_long);
        this->add_method("get_not_number",&TestCardCode::get_not_number);
        
        
        this->add_method(Method::Init,&TestCardCode::init);
        this->add_method(Method::deInit,&TestCardCode::deinit);
    }
};

struct TestAmount:public unittest::TestCase {
    Input in{};

    void get_stdin(void) {
        int64_t amount = GetAmount(
            [](char* buf,uint32_t len){
                std::fputs("Ingrese el monto (hasta 2 decimales Implicitos): ",stdout);          
                std::fgets(buf,len-1,stdin);
            }
        );
        this->log->printf<LVL_INFO>("Amount: %ld\n",amount);
    }

    void get_ok(void) {
        this->in.value("124.54");
        int64_t amount = GetAmount(this->in);
        this->assert_equal(amount,int64_t(std::atof(this->in.value())*100));
    }

    void get_ok_list(void) {
        using List = std::vector<const char*>;
        List v_ok {
            "12365.55",
            "12365.55\n",
            "12365.55\r",
        };
        int64_t amount;
        const char* vamoun = "12365.55";
        for (const auto& it : v_ok){
            this->in.value(it);
            amount = GetAmount(this->in);
            this->assert_equal(amount,int64_t(std::atof(vamoun)*100));
        }
    }

    void get_too_long(void) {
        this->assert_exception<Exception<N>>(
            [this](void){                
                this->in.value("1234567898.9888");
                GetAmount(this->in);
            }
        );
    }

    void get_neg_value(void) {
        this->assert_exception<Exception<N>>(
            [this](void){                
                this->in.value("-123458.988");
                GetAmount(this->in);
            }
        );
    }

    void get_not_number(void) {
        this->assert_exception<Exception<N>>(
            [this](void){                
                this->in.value("123458.9B8");
                GetAmount(this->in);
            }
        );
    }

    void init(){
        this->log->puts<LVL_SUCCESS>("Inicio de la ejecucion Class TestAmount\n");
    }
    void deinit(){
        this->log->puts<LVL_SUCCESS>("Fin    de la ejecucion Class TestAmount\n\n");
    }

    virtual void register_method(void){        
        //this->add_method("get_stdin",&TestAmount::get_stdin);
        this->add_method("get_ok",&TestAmount::get_ok);
        this->add_method("get_ok_list",&TestAmount::get_ok_list);
        this->add_method("get_too_long",&TestAmount::get_too_long);
        this->add_method("get_neg_value",&TestAmount::get_neg_value);
        this->add_method("get_not_number",&TestAmount::get_not_number);
        
        
        this->add_method(Method::Init,&TestAmount::init);
        this->add_method(Method::deInit,&TestAmount::deinit);
    }
};

struct TestVerifyCardNumber:public unittest::TestCase {

    void get_ok(){
        std::string card_number = "4517650654628311";
        auto [st,reg_rng,reg_card] = VerifyCardNumber (card_number,PATH_RANGE,PATH_CARDS);
        this->assert_true(st);
        /* verificamos que los registros no esten vacios */
        this->assert_not_equal(reg_rng,RangesRegister());
        this->assert_not_equal(reg_card,CardsRegister());
        this->log->printf("Card Register  : <%s> | <%u>\n",reg_card.label,reg_card.id);
        this->log->printf("Range Register : <[%s] [%s]> | <%u> | <%u>\n",
            reg_rng.low,reg_rng.high,reg_rng.len,reg_rng.id);        
    }

    void get_nok(){
        std::string card_number = "4519650654628311";
        auto [st,reg_rng,reg_card] = VerifyCardNumber (card_number,PATH_RANGE,PATH_CARDS);
        this->assert_false(st);
        /* verificamos que los registros esten vacios */
        this->assert_equal(reg_rng,RangesRegister());
        this->assert_equal(reg_card,CardsRegister());        
    }

    void frange_notfound(){
        this->assert_exception<Exception<N>>(
            [](){
                VerifyCardNumber ("  ","file/notfound",PATH_CARDS);
            }
        );
    }
    void fcards_notfound(){
        this->assert_exception<Exception<N>>(
            [](){
                VerifyCardNumber ("  ",PATH_RANGE,"file/notfound");
            }
        );        
    }

    void init(){
        this->log->puts<LVL_SUCCESS>("Inicio de la ejecucion Class TestVerifyCardNumber\n");
    }    
    void deinit(){
        this->log->puts<LVL_SUCCESS>("Fin    de la ejecucion Class TestVerifyCardNumber\n\n");
    }
    virtual void register_method(void){
        this->add_method(Method::Init,&TestVerifyCardNumber::init);
        this->add_method(Method::deInit,&TestVerifyCardNumber::deinit);

        this->add_method("get_ok",&TestVerifyCardNumber::get_ok);
        this->add_method("get_nok",&TestVerifyCardNumber::get_nok);
        this->add_method("frange_notfound",&TestVerifyCardNumber::frange_notfound);
        this->add_method("fcards_notfound",&TestVerifyCardNumber::fcards_notfound);
    }
};

struct TestPSocket:public unittest::TestCase {
    void echo(){
        this->srv.run([](const char* b)-> std::string {
            return std::string(b);
        });


        PSocket::StreamClient client { 
            SERVER_IP,
            SERVER_PORT,
            PSocket::FmtLen::FMT4B 
        };
        client.Connect();

        char buf[32];
        for (int i = 0; i<5;i++){
            std::snprintf(buf,sizeof(buf)-1,"test %4d",i);
            client.Send(buf);
            std::string response;
            client.Recv(response,double(1.0));
            this->log->printf("response: %s\n",response.c_str());
            this->assert_equal<const char*>(buf,response.c_str(),contex(),
                [](const char* o1, const char* o2) -> bool {
                    return std::strcmp(o1,o2) == 0;
                }
            );
        }
        client.Send("\0");        
        int err = client.Disconnect();        
        std::cout<<"client.Disconnect() err :"<<err<<'\n';
    }

    void init(){
        this->log->puts<LVL_SUCCESS>("Inicio de la ejecucion Class TestPSocket\n");
    }    
    void deinit(){
        this->log->puts<LVL_SUCCESS>("Fin    de la ejecucion Class TestPSocket\n\n");
    }
    void tear_down(){        
        this->srv.join();
        this->srv.close();
        usleep(1000000);
    }

    virtual void register_method(void){
        this->add_method(Method::Init,&TestPSocket::init);
        this->add_method(Method::deInit,&TestPSocket::deinit);
        this->add_method(Method::tearDown,&TestPSocket::tear_down);
        this->add_method("echo",&TestPSocket::echo);
    }

    Server srv{};
    /* 
    sudo ss -tulnp | grep :3030
    sudo lsof -i :3030
    */

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
            new TestPSocket(),
            new TestAmount(),
            new TestCardCode(),
            new TestCardNumber(),
            new TestVerifyCardNumber()            
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
