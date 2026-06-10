/** ***********************************************************************************//**
* \addtogroup PryTemplateName 
* @{ 
* \copyright  
* 2023, Luccioni Jesús Emanuel \n
* All rights reserved.\n 
* This file is part of PryTemplateName .\n
* Redistribution is not allowed on binary and source forms, with or without \n
* modification. Use is permitted with prior authorization by the copyright 
* holder. &copy;
* \file main.hpp
* \author <b> JEL </b> - <i> Jesus Emanuel Luccioni </i>.    
* \brief unittests utilstr namespace
* \details unit test aplicado a las funciones definidas dentro del namespace utilstr 
*
* \version version number.
* \date day ${NroDayOfMonth} de month, ${year}.
* \pre pre, condiciones que deben cuplirse antes del llamado, example: First
* initialize the system.
* \bug bug, depuracion example: Not all memory is freed when deleting an object 
* of this class.
* \warning mensaje de precaucion, warning.
* \note nota.
* \par meil
* <PRE> + <b><i> piero.jel@gmail.com </i></b></PRE>
* @} doxygen end group definition 
* ********************************************************************************** */


/* build in libc */
#include <cstdlib>
#include <cstdio>
/* build in c++/STL */
#include <iostream>
#include <string>

/* project header */
#include <utilstr>
#include <unittest>

using String = std::string;
using CString = const std::string&;

struct SplitTwoString:public unittest::TestCase {
    using Array = std::array<String,2>;

    void split_two_string_nf(void){
        String text = "Hola Como estas";
        const auto [s1,s2] = utilstr::split_two(text,"como");
        this->assert_true(s1.empty(),contex());
        this->assert_true(s2.empty(),contex());
    }
    void split_two_char_nf(void){
        String text = "Hola | estas";
        const auto [s1,s2] = utilstr::split_two(text,'&');
        this->assert_true(s1.empty(),contex());
        this->assert_true(s2.empty(),contex());
    }

    void split_two_string_v1(void){
        String text = "Hola Como estas";
        const auto [s1,s2] = utilstr::split_two(text," ");
        this->assert_equal<String>(s1,"Hola",contex());
        this->assert_equal<String>(s2,"Como estas",contex());
    }
    void split_two_char_v1(void){        
        String text = "Hola Como estas";
        const auto [s1,s2] = utilstr::split_two(text,' ');
        this->assert_equal<String>(s1,"Hola",contex());
        this->assert_equal<String>(s2,"Como estas",contex());
    }

    void split_two_string_v2(void){
        String text = "ColumnA = 100 AND ColumB = 100";
        const auto [s1,s2] = utilstr::split_two(text,"AND");
        this->printf("s1: <%s> | s2: <%s> ",s1.c_str(),s2.c_str());
        this->assert_equal<String>(s1,"ColumnA = 100 ",contex());
        this->assert_equal<String>(s2," ColumB = 100",contex());
    }
    void split_two_char_v2(void){        
        String text = "ColumnA > ColumB";
        const auto [s1,s2] = utilstr::split_two(text,'>');
        this->assert_equal<String>(s1,"ColumnA ",contex());
        this->assert_equal<String>(s2," ColumB",contex());
    }

    void split_two_string_v3(void){
        /* habilitamos el trim */
        String text = "ColumnA = 100 AND ColumB = 100";
        const auto [s1,s2] = utilstr::split_two(text,"AND",true);
        this->printf("s1: <%s> | s2: <%s> ",s1.c_str(),s2.c_str());
        this->assert_equal<String>(s1,"ColumnA = 100",contex());
        this->assert_equal<String>(s2,"ColumB = 100",contex());
    }
    void split_two_char_v3(void){    
        String text = "ColumnA > ColumB";
        /* habilitamos el trim */
        const auto [s1,s2] = utilstr::split_two(text,'>',true);
        this->assert_equal<String>(s1,"ColumnA",contex());
        this->assert_equal<String>(s2,"ColumB",contex());
    }

    void split_two_string_v4(void){
        /* habilitamos el trim */
        String text = "ColumnA=100ANDColumB=100";
        const auto [s1,s2] = utilstr::split_two(text,"AND",true);
        this->printf("s1: <%s> | s2: <%s> ",s1.c_str(),s2.c_str());
        this->assert_equal<String>(s1,"ColumnA=100",contex());
        this->assert_equal<String>(s2,"ColumB=100",contex());
    }
    void split_two_char_v4(void){    
        String text = "ColumnA>ColumB";
        /* habilitamos el trim */
        const auto [s1,s2] = utilstr::split_two(text,'>',true);
        this->assert_equal<String>(s1,"ColumnA",contex());
        this->assert_equal<String>(s2,"ColumB",contex());
    }

    /* test over Array  */
    void split_two_string_v5(void){
        String text = "Hola Como estas";
        Array res;
        bool st = utilstr::split_two(text," ",res);
        this->assert_true(st,contex());
        this->assert_container_equal<Array>(res,Array{"Hola","Como estas"},contex());
    }
    void split_two_char_v5(void){
        String text = "Hola Como estas";
        Array res;
        auto st = utilstr::split_two(text,' ',res);
        this->assert_true(st,contex());
        this->assert_container_equal<Array>(res,Array{"Hola","Como estas"},contex());
    }

    void split_two_string_v6(void){        
        String text = "ColumnA = 100 AND ColumB = 100";
        Array res;
        auto st = utilstr::split_two(text,"AND",res);        
        this->assert_true(st,contex());
        this->assert_container_equal<Array>(res,Array{"ColumnA = 100 "," ColumB = 100"},contex());
    }
    void split_two_char_v6(void){        
        String text = "ColumnA > ColumB";
        Array res;
        auto st = utilstr::split_two(text,'>',res);
        this->assert_true(st,contex());
        this->assert_container_equal<Array>(res,Array{"ColumnA "," ColumB"},contex());
    }

    void split_two_string_v7(void){
        Array res;
        String text = "ColumnA = 100 AND ColumB = 100";
        /* habilitamos el trim */
        auto st = utilstr::split_two(text,"AND",res,true);
        this->assert_true(st);
        this->assert_equal<String>(res[0],"ColumnA = 100",contex());
        this->assert_equal<String>(res[1],"ColumB = 100",contex());
    }
    void split_two_char_v7(void){    
        Array res;
        String text = "ColumnA > ColumB";
        /* habilitamos el trim */
        auto st = utilstr::split_two(text,'>',res,true);
        this->assert_true(st);
        this->assert_equal<String>(res[0],"ColumnA",contex());
        this->assert_equal<String>(res[1],"ColumB",contex());
    }

    void split_two_string_v8(void){
        Array res;
        String text = "ColumnA=100ANDColumB=100";
        /* habilitamos el trim */
        auto st = utilstr::split_two(text,"AND",res,true);
        this->assert_true(st);
        this->assert_equal<String>(res[0],"ColumnA=100",contex());
        this->assert_equal<String>(res[1],"ColumB=100",contex());
    }
    void split_two_char_v8(void){
        Array res;
        String text = "ColumnA>ColumB";
        /* habilitamos el trim */
        auto st = utilstr::split_two(text,'>',res,true);
        this->assert_true(st);
        this->assert_equal<String>(res[0],"ColumnA",contex());
        this->assert_equal<String>(res[1],"ColumB",contex());
    }

    virtual void register_method(void){
        
        this->add_method("split_two_string_nf",&SplitTwoString::split_two_string_nf);
        this->add_method("split_two_string_v1",&SplitTwoString::split_two_string_v1);
        this->add_method("split_two_string_v2",&SplitTwoString::split_two_string_v2);
        this->add_method("split_two_string_v3",&SplitTwoString::split_two_string_v3);
        this->add_method("split_two_string_v4",&SplitTwoString::split_two_string_v4);
        this->add_method("split_two_string_v5",&SplitTwoString::split_two_string_v5);
        this->add_method("split_two_string_v6",&SplitTwoString::split_two_string_v6);
        this->add_method("split_two_string_v7",&SplitTwoString::split_two_string_v7);
        this->add_method("split_two_string_v8",&SplitTwoString::split_two_string_v8);

        this->add_method("split_two_char_nf",&SplitTwoString::split_two_char_nf);
        this->add_method("split_two_char_v1",&SplitTwoString::split_two_char_v1);
        this->add_method("split_two_char_v2",&SplitTwoString::split_two_char_v2);
        this->add_method("split_two_char_v3",&SplitTwoString::split_two_char_v3);
        this->add_method("split_two_char_v4",&SplitTwoString::split_two_char_v4);
        this->add_method("split_two_char_v5",&SplitTwoString::split_two_char_v5);
        this->add_method("split_two_char_v6",&SplitTwoString::split_two_char_v6);
        this->add_method("split_two_char_v7",&SplitTwoString::split_two_char_v7);
        this->add_method("split_two_char_v8",&SplitTwoString::split_two_char_v8);
    }
};


struct SplitString:public unittest::TestCase{
    using Vector = std::vector<String>;
    void init(){ this->puts<LVL_INFO>("\nInicio de la ejecucion Class SplitString\n");}
    void deinit(){ this->puts<LVL_INFO>("Fin    de la ejecucion Class SplitString\n\n");}


    void split_string_not_found(void){
        String text = ">>Hola>> >>Como>> >> esta>> ";
        Vector v1 = utilstr::split<Vector>(text,"and");        
        this->assert_true(v1.empty(),contex());
    }
    void split_char_not_found(void){
        String text = "|Hola| |Como| | esta| ";   
        Vector v1 = utilstr::split<Vector>(text,'&');        
        this->assert_true(v1.empty(),contex());
    }

    void split_string_v1(void){
        String text = "Hola Como estas";
        auto v1 = utilstr::split<Vector>(text," ");
        this->assert_container_equal<Vector>(v1,Vector{"Hola","Como","estas"},contex());
    }
    void split_char_v1(void){
        String text = "Hola Como estas";
        auto v1 = utilstr::split<Vector>(text,' ');
        this->assert_container_equal<Vector>(v1,Vector{"Hola","Como","estas"},contex());        
    }

    void split_string_v2(void){
        String text = "ColumnA = 100 AND ColumB = 100 AND ColumC == 500";
        auto v1 = utilstr::split<Vector>(text,"AND");
        this->assert_container_equal<Vector>(v1,
            Vector{"ColumnA = 100 "," ColumB = 100 "," ColumC == 500"},
            contex()
        );
    }
    void split_char_v2(void){
        String text = "ColumnA = 100 > ColumB = 100 > ColumC == 500";
        auto v1 = utilstr::split<Vector>(text,'>');
        this->assert_container_equal<Vector>(v1,
            Vector{"ColumnA = 100 "," ColumB = 100 "," ColumC == 500"},
            contex()
        );
    }

    void split_string_v3(void){
        String text1 = "ColumnA = 100 and ColumB = 100 and ColumC == 500";
        String text2 = " ColumnA = 100 or ColumB = 100 or ColumC == 500 ";
        Vector target {"ColumnA = 100","ColumB = 100","ColumC == 500"};
        /* set trim in true */
        auto v1 = utilstr::split<Vector>(text1,"and",false,true);
        auto v2 = utilstr::split<Vector>(text2,"or",false,true);
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        //this->printf("v2: [\"%s\"]\t",utilstr::join(v2,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
        this->assert_container_equal<Vector>(v2,target,contex());
    }
    void split_char_v3(void){
        String text1 = "ColumnA = 100 > ColumB = 100 > ColumC == 500";
        String text2 = " ColumnA = 100 > ColumB = 100 > ColumC == 500 ";
        Vector target {"ColumnA = 100","ColumB = 100","ColumC == 500"};
        /* set trim in true */
        auto v1 = utilstr::split<Vector>(text1,'>',false,true);
        auto v2 = utilstr::split<Vector>(text2,'>',false,true);
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        //this->printf("v2: [\"%s\"]\t",utilstr::join(v2,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
        this->assert_container_equal<Vector>(v2,target,contex());
    }

    void split_string_v4(void){
        String text1 = "ColumnA = 100 OR ColumB = 200 OR ColumNAC == 500 OR ColumAD == 300";
        String text2 = " ColumnA = 100  and   ColumB = 200 and ColumNAC == 500   and   ColumAD == 300  ";
        Vector target {"ColumnA = 100","ColumB = 200","ColumNAC == 500","ColumAD == 300"};
        /* set trim in true */
        auto v1 = utilstr::split<Vector>(text1,"OR",false,true);
        auto v2 = utilstr::split<Vector>(text2,"and",false,true);
        
        
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        //this->printf("v2: [\"%s\"]\t",utilstr::join(v2,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
        this->assert_container_equal<Vector>(v2,target,contex());
    }
    void split_char_v4(void){
        String text1 = "ColumnA = 100 > ColumB = 200 > ColumNAC == 500 > ColumAD == 300";
        String text2 = " ColumnA = 100  >   ColumB = 200 > ColumNAC == 500   >   ColumAD == 300  ";
        Vector target {"ColumnA = 100","ColumB = 200","ColumNAC == 500","ColumAD == 300"};
        /* set trim in true */
        auto v1 = utilstr::split<Vector>(text1,'>',false,true);
        auto v2 = utilstr::split<Vector>(text2,'>',false,true);
        
        //auto v1 = utilstr::split<Vector>(text,'>');
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        //this->printf("v2: [\"%s\"]\t",utilstr::join(v2,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
        this->assert_container_equal<Vector>(v2,target,contex());
    }

    void split_string_v5(void){
        String text = " Hola   Como  estas ";
        Vector target {"","Hola","","","Como","","estas",""};
        auto v1 = utilstr::split<Vector>(text," ",true);
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
    }
    void split_char_v5(void){
        String text = " Hola   Como  estas ";
        Vector target {"","Hola","","","Como","","estas",""};
        auto v1 = utilstr::split<Vector>(text,' ',true);
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
    }

    void split_string_v6(void){
        String text = " Hola   Como  estas ";
        Vector target {"Hola","Como","estas"};
        auto v1 = utilstr::split<Vector>(text," ");
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
    }
    void split_char_v6(void){
        String text = " Hola   Como  estas ";
        Vector target {"Hola","Como","estas"};
        auto v1 = utilstr::split<Vector>(text,' ');
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        this->assert_container_equal<Vector>(v1,target,contex());
    }
    

    void split_string_v7(void){
        String text = " >>Hola >> >>  Como>> >> esta  >> ";        
        Vector v1 = utilstr::split<Vector>(text,">>",true);
        this->assert_container_equal<Vector>(v1,
            Vector{" ","Hola "," ","  Como"," "," esta  "," "},contex());
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        Vector v2 = utilstr::split<Vector>(text,">>",true,true);
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v2,"\",\"").c_str());
        this->assert_container_equal<Vector>(v2,
            Vector{"","Hola","","Como","","esta",""},contex());
    }
    void split_char_v7(void){
        String text = " <Hola < <  Como< < esta  < ";        
        Vector v1 = utilstr::split<Vector>(text,'<',true);
        this->assert_container_equal<Vector>(v1,
            Vector{" ","Hola "," ","  Como"," "," esta  "," "},contex());        
        
            Vector v2 = utilstr::split<Vector>(text,'<',true,true);        
        this->assert_container_equal<Vector>(v2,
            Vector{"","Hola","","Como","","esta",""},contex());
    }

    virtual void register_method(void){ 
        this->add_method(Method::Init,&SplitString::init);
        this->add_method(Method::deInit,&SplitString::deinit);

        this->add_method("split_string_not_found",&SplitString::split_string_not_found);
        this->add_method("split_string_v1",&SplitString::split_string_v1);
        this->add_method("split_string_v2",&SplitString::split_string_v2);
        this->add_method("split_string_v3",&SplitString::split_string_v3);
        this->add_method("split_string_v4",&SplitString::split_string_v4);
        this->add_method("split_string_v5",&SplitString::split_string_v5);
        this->add_method("split_string_v6",&SplitString::split_string_v6);
        this->add_method("split_string_v7",&SplitString::split_string_v7);

        this->add_method("split_char_not_found",&SplitString::split_char_not_found);
        this->add_method("split_char_v1",&SplitString::split_char_v1);
        this->add_method("split_char_v2",&SplitString::split_char_v2);
        this->add_method("split_char_v3",&SplitString::split_char_v3);
        this->add_method("split_char_v4",&SplitString::split_char_v4);
        this->add_method("split_char_v5",&SplitString::split_char_v5);
        this->add_method("split_char_v6",&SplitString::split_char_v6);
        this->add_method("split_char_v7",&SplitString::split_char_v7);
    }
};


struct SplitStringInArray:public unittest::TestCase{
    using Vector = std::vector<String>;

    template <typename C>
    void print_container(const char* msg,const C& c){
        this->printf("%s: [\"%s\"]\t",msg,utilstr::join(c,(const char*)"\",\"").c_str());
    }
    void init(){ this->puts<LVL_INFO>("\nInicio de la ejecucion Class SplitStringInArray\n");}
    void deinit(){ this->puts<LVL_INFO>("Fin    de la ejecucion Class SplitStringInArray\n\n");}


    void split_string_not_found(void){
        using Array = std::array<String,4>;
        String text = ">>Hola>> >>Como>> >> esta>> ";
        Array a1 = utilstr::split<Array>(text,"and");        
        this->print_container("a1: ",a1);
        std::for_each(std::begin(a1),std::end(a1),[this](CString s){
            this->assert_true(s.empty(),contex());  
        });        
    }    
    void split_char_not_found(void){
        using Array = std::array<String,4>;
        String text = "|Hola| |Como| | esta| ";   
        Array a1 = utilstr::split<Array>(text,'&');
        this->print_container("a1: ",a1);
        std::for_each(std::begin(a1),std::end(a1),[this](CString s){
            this->assert_true(s.empty(),contex());
        });
    }

    void split_string_v1(void){
        using Array = std::array<String,3>;
        String text = "Hola Como estas";
        auto a1 = utilstr::split<Array>(text," ");
        this->assert_container_equal<Array>(a1,Array{"Hola","Como","estas"},contex());
    }
    void split_char_v1(void){
        using Array = std::array<String,3>;
        String text = "Hola Como estas";
        auto a1 = utilstr::split<Array>(text,' ');
        this->assert_container_equal<Array>(a1,Array{"Hola","Como","estas"},contex());        
    }

    void split_string_v2(void){
        using Array = std::array<String,3>;
        String text = "ColumnA = 100 AND ColumB = 100 AND ColumC == 500";
        auto a1 = utilstr::split<Array>(text,"AND");
        this->assert_container_equal<Array>(a1,
            Array{"ColumnA = 100 "," ColumB = 100 "," ColumC == 500"},
            contex()
        );
    }
    void split_char_v2(void){
        using Array = std::array<String,3>;
        String text = "ColumnA = 100 > ColumB = 100 > ColumC == 500";
        auto a1 = utilstr::split<Array>(text,'>');
        this->assert_container_equal<Array>(a1,
            Array{"ColumnA = 100 "," ColumB = 100 "," ColumC == 500"},
            contex()
        );
    }

    void split_string_v3(void){
        using Array = std::array<String,3>;
        String text1 = "ColumnA = 100 and ColumB = 100 and ColumC == 500";
        String text2 = " ColumnA = 100 or ColumB = 100 or ColumC == 500 ";
        Array target {"ColumnA = 100","ColumB = 100","ColumC == 500"};
        /* set trim in true */
        auto a1 = utilstr::split<Array>(text1,"and",false,true);
        auto a2 = utilstr::split<Array>(text2,"or",false,true);
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        //this->printf("v2: [\"%s\"]\t",utilstr::join(v2,"\",\"").c_str());
        this->assert_container_equal<Array>(a1,target,contex());
        this->assert_container_equal<Array>(a2,target,contex());
    }
    void split_char_v3(void){
        using Array = std::array<String,3>;
        String text1 = "ColumnA = 100 > ColumB = 100 > ColumC == 500";
        String text2 = " ColumnA = 100 > ColumB = 100 > ColumC == 500 ";
        Array target {"ColumnA = 100","ColumB = 100","ColumC == 500"};
        /* set trim in true */
        auto a1 = utilstr::split<Array>(text1,'>',false,true);
        auto a2 = utilstr::split<Array>(text2,'>',false,true);
        //this->printf("v1: [\"%s\"]\t",utilstr::join(v1,"\",\"").c_str());
        //this->printf("v2: [\"%s\"]\t",utilstr::join(v2,"\",\"").c_str());
        this->assert_container_equal<Array>(a1,target,contex());
        this->assert_container_equal<Array>(a2,target,contex());
    }

    void split_string_v4(void){
        using Array = std::array<String,4>;
        String text1 = "ColumnA = 100 OR ColumB = 200 OR ColumNAC == 500 OR ColumAD == 300";
        String text2 = " ColumnA = 100  and   ColumB = 200 and ColumNAC == 500   and   ColumAD == 300  ";
        Array target {"ColumnA = 100","ColumB = 200","ColumNAC == 500","ColumAD == 300"};
        /* set trim in true */
        auto a1 = utilstr::split<Array>(text1,"OR",false,true);
        auto a2 = utilstr::split<Array>(text2,"and",false,true);        
        this->assert_container_equal<Array>(a1,target,contex());
        this->assert_container_equal<Array>(a2,target,contex());
    }
    void split_char_v4(void){
        using Array = std::array<String,4>;
        String text1 = "ColumnA = 100 > ColumB = 200 > ColumNAC == 500 > ColumAD == 300";
        String text2 = " ColumnA = 100  >   ColumB = 200 > ColumNAC == 500   >   ColumAD == 300  ";
        Array target {"ColumnA = 100","ColumB = 200","ColumNAC == 500","ColumAD == 300"};
        /* set trim in true */
        auto a1 = utilstr::split<Array>(text1,'>',false,true);
        auto a2 = utilstr::split<Array>(text2,'>',false,true);
                                
        this->assert_container_equal<Array>(a1,target,contex());
        this->assert_container_equal<Array>(a2,target,contex());
    }

    void split_string_v5(void){
        using Array = std::array<String,10>;
        String text = " Hola   Como  estas ";
        Array target {"","Hola","","","Como","","estas",""};
        auto a1 = utilstr::split<Array>(text," ",true);
        //this->print_container("a1: ",a1);
        this->assert_container_equal<Array>(a1,target,contex());
    }
    void split_char_v5(void){
        using Array = std::array<String,10>;
        String text = " Hola   Como  estas ";
        Array target {"","Hola","","","Como","","estas",""};
        auto a1 = utilstr::split<Array>(text,' ',true);
        //this->print_container("a1: ",a1);
        this->assert_container_equal<Array>(a1,target,contex());
    }

    void split_string_v6(void){
        using Array = std::array<String,3>;
        String text = " Hola   Como  estas ";
        Array target {"Hola","Como","estas"};
        auto a1 = utilstr::split<Array>(text," ");
        //this->print_container("a1: ",a1);
        this->assert_container_equal<Array>(a1,target,contex());
    }
    void split_char_v6(void){
        using Array = std::array<String,3>;
        String text = " Hola   Como  estas ";
        Array target {"Hola","Como","estas"};
        auto a1 = utilstr::split<Array>(text,' ');
        //this->print_container("a1: ",a1);
        this->assert_container_equal<Array>(a1,target,contex());
    }

    void split_string_v7(void){
        using Array = std::array<String,10>;
        String text = " >>Hola >> >>  Como>> >> esta  >> ";        
        Array a1 = utilstr::split<Array>(text,">>",true);
        this->assert_container_equal<Array>(a1,
            Array{" ","Hola "," ","  Como"," "," esta  "," "},contex());
        
        Array a2 = utilstr::split<Array>(text,">>",true,true);
        
        this->assert_container_equal<Array>(a2,
            Array{"","Hola","","Como","","esta",""},contex());
    }
    void split_char_v7(void){
        using Array = std::array<String,10>;
        String text = " <Hola < <  Como< < esta  < ";        
        Array a1 = utilstr::split<Array>(text,'<',true);
        this->assert_container_equal<Array>(a1,
            Array{" ","Hola "," ","  Como"," "," esta  "," "},contex());        
        
        Array a2 = utilstr::split<Array>(text,'<',true,true);        
        this->assert_container_equal<Array>(a2,
            Array{"","Hola","","Como","","esta",""},contex());
    }

    virtual void register_method(void){ 
        this->add_method(Method::Init,&SplitStringInArray::init);
        this->add_method(Method::deInit,&SplitStringInArray::deinit);

        this->add_method("split_string_not_found",&SplitStringInArray::split_string_not_found);
        this->add_method("split_string_v1",&SplitStringInArray::split_string_v1);
        this->add_method("split_string_v2",&SplitStringInArray::split_string_v2);
        this->add_method("split_string_v3",&SplitStringInArray::split_string_v3);
        this->add_method("split_string_v4",&SplitStringInArray::split_string_v4);
        this->add_method("split_string_v5",&SplitStringInArray::split_string_v5);
        this->add_method("split_string_v6",&SplitStringInArray::split_string_v6);
        this->add_method("split_string_v7",&SplitStringInArray::split_string_v7);

        this->add_method("split_char_not_found",&SplitStringInArray::split_char_not_found);
        this->add_method("split_char_v1",&SplitStringInArray::split_char_v1);
        this->add_method("split_char_v2",&SplitStringInArray::split_char_v2);
        this->add_method("split_char_v3",&SplitStringInArray::split_char_v3);
        this->add_method("split_char_v4",&SplitStringInArray::split_char_v4);
        this->add_method("split_char_v5",&SplitStringInArray::split_char_v5);
        this->add_method("split_char_v6",&SplitStringInArray::split_char_v6);
        this->add_method("split_char_v7",&SplitStringInArray::split_char_v7);
    }
};



template <typename T>
struct Point {  
    T x{},y{},z{};  
    Point(T x={}, T y={}, T z={}):x{x},y{y},z{z} { 
    }
    // ...
    template <typename G>
    friend std::ostream& operator<< ( std::ostream& ou, const Point<G>& p );    
};
template <typename T>
std::ostream& operator<< (std::ostream& ou, const Point<T> &p){
    ou <<"( "<<p.x<<"; "<<p.y<<"; "<<p.z<<" )";
    return ou;
}                    

struct SplitToUpprtAndToLowe:public unittest::TestCase{
    void init(){ this->puts<LVL_INFO>("\nInicio de la ejecucion Class SplitToUpprtAndToLowe\n");}
    void deinit(){ this->puts<LVL_INFO>("Fin    de la ejecucion Class SplitToUpprtAndToLowe\n\n");}
  
    void to_upper_v1(void){
        String text = "Hola Como Estas";
        String target = "HOLA COMO ESTAS";
        auto s1 = utilstr::to_upper(text);
        this->assert_equal<String>(s1,target,contex());
    }
    void to_upper_v2(void){
        String text = "hola como estas";
        String target = "HOLA COMO ESTAS";
        auto st = utilstr::to_upper(&text);
        //this->printf("st<%s> | text: %s\t",(st)?"true":"false",text.c_str());
        this->assert_equal<String>(text,target,contex());
        this->assert_true(st);
    }

    void to_lower_v1(void){
        String text = "Hola Como Estas";
        String target = "hola como estas";
        auto s1 = utilstr::to_lower(text);
        this->assert_equal<String>(s1,target,contex());
    }
    void to_lower_v2(void){
        String text = "hola COMO estas";
        String target = "hola como estas";
        auto st = utilstr::to_lower(&text);
        //this->printf("st<%s> | text: %s\t",(st)?"true":"false",text.c_str());
        this->assert_equal<String>(text,target,contex());
        this->assert_true(st);
    }

    void to_string_v1(void){
        const char* text = "hola COMO estas";
        String s1 = utilstr::to_string(text);        
        this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(String(text),s1,contex());        
    }
    void to_string_v2(void){
        Point<int> p1 (1,2,3);
        std::cout<<"p1: "<<p1<<"\t";
        String s1 = utilstr::to_string(p1);        
        this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(String{"( 1; 2; 3 )"},s1,contex());        
    }
    
    virtual void register_method(void){ 
        this->add_method(Method::Init,&SplitToUpprtAndToLowe::init);
        this->add_method(Method::deInit,&SplitToUpprtAndToLowe::deinit);

        this->add_method("to_upper_v1",&SplitToUpprtAndToLowe::to_upper_v1);
        this->add_method("to_upper_v2",&SplitToUpprtAndToLowe::to_upper_v2);

        this->add_method("to_lower_v1",&SplitToUpprtAndToLowe::to_lower_v1);
        this->add_method("to_lower_v2",&SplitToUpprtAndToLowe::to_lower_v2);

        this->add_method("to_string_v1",&SplitToUpprtAndToLowe::to_string_v1);
        this->add_method("to_string_v2",&SplitToUpprtAndToLowe::to_string_v2);
    }
};

struct JoinCont:public unittest::TestCase{
    void init(){ this->puts<LVL_INFO>("\nInicio de la ejecucion Class JoinCont\n");}
    void deinit(){ this->puts<LVL_INFO>("Fin    de la ejecucion Class JoinCont\n\n");}
    
    void vct_join_v1(void){
        using Vector = std::vector<String>;
        Vector v1 {"Lunes","Martes","Jueves"};
        String target = "Lunes||Martes||Jueves";
        auto s1 = utilstr::join(v1,String{"||"});        
        //this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(s1,target,contex());
    }
    void vct_join_v2(void){
        using Vector = std::vector<Point<int>>;
        Vector v1 {
            Point<int>{1,2,3},
            Point<int>{2,3,1},
            Point<int>{3,1,2}
        };
        String target = "( 1; 2; 3 )||( 2; 3; 1 )||( 3; 1; 2 )";
        auto s1 = utilstr::join<Vector,Point<int>>(v1,String{"||"});        
        //this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(s1,target,contex());
    }
    void vct_join_v3(void){
        using Vector = std::vector<String>;
        Vector v1 {"Lunes","Martes","Jueves"};
        String target = "LUNES||MARTES||JUEVES";
        auto s1 = utilstr::join(v1,String{"||"},
            [](Vector::const_iterator it) -> std::string {
                std::string tmp = *it;
                utilstr::to_upper(&tmp);
                return tmp;
            }
        );
        //this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(s1,target,contex());
    }
    void vct_join_v4(void){
        using Vector = std::vector<Point<int>>;
        Vector v1 {
            Point<int>{1,2,3},
            Point<int>{2,3,1},
            Point<int>{3,1,2}
        };
        String target = "03;02;01||01;03;02||02;01;03";
        auto s1 = utilstr::join<Vector,Point<int>>(v1,String{"||"},
            [](Vector::const_iterator it) -> std::string {
                Point<int> p = *it;                
                return utilstr::format("%02d;%02d;%02d",p.z,p.y,p.x);
            }
        );
        //this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(s1,target,contex());
    }

    void arr_join_v1(void){
        using Array = std::array<Point<int>,3>;
        Array v1 {
            Point<int>{1,2,3},
            Point<int>{2,3,1},
            Point<int>{3,1,2}
        };
        String target = "03;02;01||01;03;02||02;01;03";
        auto s1 = utilstr::join<Array,Point<int>>(v1,String{"||"},
            [](Array::const_iterator p) -> std::string {
                return utilstr::format("%02d;%02d;%02d",p->z,p->y,p->x);
            }
        );
        //this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(s1,target,contex());
    }


    virtual void register_method(void){ 
        this->add_method(Method::Init,&JoinCont::init);
        this->add_method(Method::deInit,&JoinCont::deinit);

        this->add_method("vct_join_v1",&JoinCont::vct_join_v1);
        this->add_method("vct_join_v2",&JoinCont::vct_join_v2);
        this->add_method("vct_join_v3",&JoinCont::vct_join_v3);
        this->add_method("vct_join_v4",&JoinCont::vct_join_v4);
        this->add_method("arr_join_v1",&JoinCont::arr_join_v1);
    }
    
};

struct ReplaceStr:public unittest::TestCase{
    void init(){ this->puts<LVL_INFO>("\nInicio de la ejecucion Class ReplaceStr\n");}
    void deinit(){ this->puts<LVL_INFO>("Fin    de la ejecucion Class ReplaceStr\n\n");}


    void replace_string_v1(void){
        String txt = "Lunes||Martes||Jueves";
        String trg = "Lunes ,Martes ,Jueves";
        auto s1 = utilstr::replace_all(txt,"||"," ,");
        //this->printf("s1: %s\t",s1.c_str());
        this->assert_equal<String>(s1,trg,contex());
    }
    void replace_string_v2(void){
        String txt = "Lunes||Martes||Jueves";
        String trg = "Lunes ,Martes ,Jueves";
        utilstr::replace_all_inplace(txt,"||"," ,");
        this->assert_equal<String>(txt,trg,contex());
    }
    void replace_string_v3(void){
        String txt = "Lunes||Martes||Jueves";
        String trg = "Lunes ,Martes ,Jueves";
        auto st = utilstr::replace_all(&txt,"||"," ,");
        this->assert_true(st>0,contex());
        this->assert_equal<String>(txt,trg,contex());
    }

    void replace_string_nf_v1(void){
        String txt = "Lunes||Martes||Jueves";        
        auto st = utilstr::replace_all_inplace(txt,"&&"," ,");
        this->assert_false(st>0,contex());
    }
    void replace_string_nf_v2(void){
        String txt = "Lunes||Martes||Jueves";
        String trg = "Lunes ,Martes ,Jueves";
        auto st = utilstr::replace_all(&txt,"&&"," ,");
        this->assert_false(st>0,contex());        
    }


    void replace_char_v1(void){
        String txt = "Lunes | Martes | Jueves";
        String trg = "Lunes , Martes , Jueves";
        auto s1 = utilstr::replace_all(txt,'|',',');        
        this->assert_equal<String>(s1,trg,contex());
    }
    void replace_char_v2(void){
        String txt = "Lunes | Martes | Jueves";
        String trg = "Lunes , Martes , Jueves";
        utilstr::replace_all_inplace(txt,'|',',');
        this->assert_equal<String>(txt,trg,contex());
    }
    void replace_char_v3(void){
        String txt = "Lunes | Martes | Jueves";
        String trg = "Lunes , Martes , Jueves";
        auto st = utilstr::replace_all(&txt,'|',',');
        this->assert_true(st>0,contex());
        this->assert_equal<String>(txt,trg,contex());
    }

    void replace_char_nf_v1(void){
        String txt = "Lunes | Martes | Jueves";        
        auto st = utilstr::replace_all_inplace(txt,'&',',');
        this->assert_false(st>0,contex());
    }
    void replace_char_nf_v2(void){
        String txt = "Lunes | Martes | Jueves";
        auto st = utilstr::replace_all(&txt,'&',',');
        this->assert_false(st>0,contex());
    }

    virtual void register_method(void){ 
        this->add_method(Method::Init,&ReplaceStr::init);
        this->add_method(Method::deInit,&ReplaceStr::deinit);

        this->add_method("replace_string_v1",&ReplaceStr::replace_string_v1);
        this->add_method("replace_string_v2",&ReplaceStr::replace_string_v2);
        this->add_method("replace_string_v3",&ReplaceStr::replace_string_v3);
        
        this->add_method("replace_char_v1",&ReplaceStr::replace_char_v1);
        this->add_method("replace_char_v2",&ReplaceStr::replace_char_v2);
        this->add_method("replace_char_v3",&ReplaceStr::replace_char_v3);

        this->add_method("replace_string_nf_v1",&ReplaceStr::replace_string_nf_v1);
        this->add_method("replace_string_nf_v2",&ReplaceStr::replace_string_nf_v2);

        this->add_method("replace_char_nf_v1",&ReplaceStr::replace_char_nf_v1);
        this->add_method("replace_char_nf_v2",&ReplaceStr::replace_char_nf_v2);        
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
        
        std::fputs("\nTest ExecuteTestCases\n",stdout);
        unittest::ExecuteTestCases operations{
            new SplitTwoString(),
            new SplitString(),
            new SplitStringInArray(),
            new SplitToUpprtAndToLowe(),
            new JoinCont(),
            new ReplaceStr()
        };        
        operations.run();
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



