#ifndef __main_hpp__
#define __main_hpp__

//#include <thread>

// BEGIN Setting PERROR
/** FIXME En caso de necesitar deshabilitar las api strerrorname_np() y  strerrordesc_np() 
 * debemos descomentar las siguentes lineas: */
#define STRERROR_NP       1 /* Enable/disable el uso carga de strerror apis NP */


#if (STRERROR_NP == 0)
  #ifdef _GNU_SOURCE 
    #undef _GNU_SOURCE   
  #endif 
#endif

#include <cstdio>     /* for printf */
#include <cstdlib>    /* for exit */
#include <iostream>
#include <cstring>

#ifdef _GNU_SOURCE 
  #define mstrerrorname_np(Errno) strerrorname_np(Errno)
  #define mstrerrordesc_np(Errno) strerrordesc_np(Errno)
  #define mbasename(Argv0) basename(Argv0)
#else
  #ifndef mstrerrorname_np
    static inline char* fn_mstrerrorname_np(int errnum)
    {
      static char rval[32];
      snprintf(rval, sizeof(rval)-1,"N%04d",errnum);
      return rval;
    }
    #define mstrerrorname_np(Errno) fn_mstrerrorname_np(Errno)
  #endif
  #ifndef mstrerrordesc_np
    #define mstrerrordesc_np(Errno) strerror(Errno)
  #endif
  #ifndef mbasename
    static inline const char* fn_basename(const char* arg0)
    {
      const char *cp = std::strrchr(arg0, '/');
      return (cp ? cp+1 : arg0);
    }
    #define mbasename(Argv0) fn_basename(Argv0)
  #endif

#endif
// END   Setting PERROR
/*==============================[ BEGIN PERROR()                  ]==============================*/
#define PERROR_cout(Fmt, arg...)\
  fprintf( stdout,"<%03d><%s: %s> " Fmt\
         , errno,mstrerrorname_np(errno),mstrerrordesc_np(errno)\
         , ##arg)

#define PERROR_cerr(Fmt, arg...)\
{\
  fprintf(stderr,"<%03d><%s: %s> " Fmt\
         , errno,mstrerrorname_np(errno),mstrerrordesc_np(errno)\
         , ##arg);\
  exit(EXIT_FAILURE);\
}

#define PERROR_fcout(Fmt, arg...)\
  fprintf(stdout,"%s:%s():%ld  <%03d><%s: %s> " Fmt\
         , __FILE__,__func__,(long int)__LINE__\
         , errno,mstrerrorname_np(errno),mstrerrordesc_np(errno)\
         , ##arg)

#define PERROR_fcerr(Fmt, arg...)\
{\
  fprintf(stderr,"%s:%s():%ld  <%03d><%s: %s> " Fmt\
         , __FILE__,__func__,(long int)__LINE__\
         , errno,mstrerrorname_np(errno),mstrerrordesc_np(errno)\
         , ##arg);\
  exit(EXIT_FAILURE);\
}
  
/**
 * @brief Macro funcion para el print de la info de error relacionada a \b errno (varible global).
 * \param[in] Std std ostream este debe ser uno de los siguiente: 
 *  \b cout ostream estandar de salida, no ejecuta exit()
 *  \b cerr ostream estandar para error, Ejecuta 'exit( \b EXIT_FAILURE )'
 *  \b fcerr idem to \p cout add print Frame (file, function and nro linea)
 *  \b fcerr idem to \p cerr add print Frame (file, function and nro linea)
 * \param[in] Fmt  CStyle string con formato
 * \param ...  Demas arg relacionados \p Fmt y el resto de parametros si son requeridos 
 * \code {.c++}
    PERROR( cout,"Warning Error <%s - %s():%d>",__FILE__,__func__,__LINE__);
    PERROR( fcout,"Warning  Error");
 * \endcode
 * 
 */
#define PERROR(Std,Fmt, arg...)\
  PERROR_##Std(Fmt "\n",##arg)
/*==============================[ END   PERROR()                  ]==============================*/


/*==============================[ BEGIN NPERROR()                 ]==============================*/
//
#define NPERROR_cout(Errno,Fmt, arg...)\
  fprintf( stdout,"<%03d><%s: %s> " Fmt\
         , Errno,mstrerrorname_np(Errno),mstrerrordesc_np(Errno)\
         , ##arg)

#define NPERROR_cerr(Errno,Fmt, arg...)\
{\
  fprintf(stderr,"<%03d><%s: %s> " Fmt\
         , Errno,mstrerrorname_np(Errno),mstrerrordesc_np(Errno)\
         , ##arg);\
  exit(EXIT_FAILURE);\
}


#define NPERROR_fcout(Errno,Fmt, arg...)\
  fprintf(stdout,"%s:%s():%ld  <%03d><%s: %s> " Fmt\
         , __FILE__,__func__,(long int)__LINE__\
         , Errno,mstrerrorname_np(Errno),mstrerrordesc_np(Errno)\
         , ##arg)

#define NPERROR_fcerr(Errno,Fmt, arg...)\
{\
  fprintf(stderr,"%s:%s():%ld  <%03d><%s: %s> " Fmt\
         , __FILE__,__func__,(long int)__LINE__\
         , Errno,mstrerrorname_np(Errno),mstrerrordesc_np(Errno)\
         , ##arg);\
  exit(EXIT_FAILURE);\
}
/**
 * @brief Macro funcion para el print de la info de error relacionada a \b Errno pasado como
 * argumento.
 * \param[in] Std std ostream este debe ser uno de los siguiente
 *  \b cout ostream estandar de salida
 *  \b cerr ostream estandar para error, y \b exit(EXIT_FAILURE)
 *  \b fcout idem to \p cout add print frame (file, function and nro linea)
 *  \b fcerr idem to \p cerr add print frame (file, function and nro linea)
 * \param[in] Errno numero de error, positivo. 
 * \param[in] Fmt  CStyle string con formato
 * \param ...  Demas arg relacionados \p Fmt y el resto de parametros si son requeridos 
 * \code {.c++}
    NPERROR( cout,EINVAL,"Error args pass <%s - %s():%d>",__FILE__,__func__,__LINE__);
    NPERROR( fcout,EINVAL,"Error args pass");
 * \endcode
 * 
 */
#define NPERROR(Std,Errno,Fmt, arg...)\
  NPERROR_##Std(Errno,Fmt "\n",##arg)
/*==============================[ END   NPERROR()                 ]==============================*/


/*==============================[ BEGIN FPERROR()                 ]==============================*/
/**
 * @brief Macro funcion para el FILE printf de la info de error relacionada a \b errno (varible global).
 * \param[in] File \p FILE* previamente abierto, pueden emplearse los standart
 *  \b stdout ostream estandar de salida
 *  \b stderr ostream estandar para error 
 * \param[in] Fmt Formato string CStyle 
 * \param ...  Demas arg relacionados \p Fmt y el resto de parametros si son requeridos 
 * \code {.c++}
    FILE* ou = fopen(pathname,mode);
    //...
    FPERROR( ou,"Warning  Error");
 * \endcode
 */
#define FPERROR(File,Fmt, arg...)\
  fprintf(File,"<%03d><%s: %s> " Fmt\
         , errno,mstrerrorname_np(errno),mstrerrordesc_np(errno)\
         , ##arg)
/*==============================[ END   FPERROR()                 ]==============================*/


/*==============================[ BEGIN NFPERROR()                ]==============================*/
/**
 * @brief Macro funcion para el FILE printf de la info de error relacionada a \b Errno (varible global).
 * \param[in] Errno numero de error que que representa lo sucedido.
 * \param[in] File \p FILE* previamente abierto, pueden emplearse los standart.
 *  \b stdout ostream estandar de salida
 *  \b stderr ostream estandar para error 
 * \param[in] Fmt Formato string CStyle 
 * \param ...  Demas arg relacionados \p Fmt y el resto de parametros si son requeridos 
 * \code {.c++}
    FILE* ou = fopen(pathname,mode);
    int err;
    //...
    NFPERROR(err, ou,"Warning  Error");
 * \endcode
 */
#define NFPERROR(Errno,File,Fmt, arg...)\
  fprintf(File,"<%03d><%s: %s> " Fmt\
         , Errno,mstrerrorname_np(Errno),mstrerrordesc_np(Errno)\
         , ##arg)

/*==============================[ END   NFPERROR()                ]==============================*/


/**
 * @brief funcion simil a snprintf pero sin la necesidad de especificar 
 * la lonngitud del buffer.
 * \param buff buffer
 * \param ...  Cstyle string con el fmt y el resto de parametros si son requeridos 
 */
#define SNPRINTF(buff, ...) \
  snprintf(buff, sizeof(buff) - 1, __VA_ARGS__)

/**
 * @brief funcion simil SNPRINTF pero saca directamente los datos por sts stream
 * \param Std std ostream este debe ser uno de los siguiente
 *  \b cout ostream estandar de salida
 *  \b cerr ostream estandar para error
 * \param buff buffer
 * \param ...  Cstyle string con el fmt y el resto de parametros si son requeridos 
 */
#define STD_SNPRINTF(Std,Buff, ...) \
{\
  snprintf(Buff, sizeof(Buff) - 1, __VA_ARGS__);\
  std::Std<<buff;\
}


#if 0 /* podemos seleccionar cual usamos */
/**
 * @brief funcion 
 * \param Std std ostream este debe ser uno de los siguiente
 *  \b cout ostream estandar de salida
 *  \b cerr ostream estandar para error
 * \param buff buffer
 * \param Fmt  CStyle string con formato
 * \param ...  Demas arg relacionados \p Fmt y el resto de parametros si son requeridos 
 * \code {.c++}
    STD_PERROR( cout,"Error <%s - %s():%d>\n",__FILE__,__func__,__LINE__);
 * \endcode
 * 
 */
#define STD_PERROR(Std,buff, Fmt, arg...) \
{\
  snprintf(buff, sizeof(buff) - 1, Fmt "<%d><%s: %s>\n", ##arg ,errno,strerrorname_np(errno),strerrordesc_np(errno));\
  std::Std<<buff;\
}
#else
#define STD_PERROR_cout(Fmt, arg...)\
  fprintf(stdout,"<%d><%s: %s> " Fmt, errno,strerrorname_np(errno),strerrordesc_np(errno), ##arg)

#define STD_PERROR_cerr(Fmt, arg...)\
  fprintf(stderr,"<%d><%s: %s> " Fmt, errno,strerrorname_np(errno),strerrordesc_np(errno), ##arg)

/*
stdout
stderr
*/
#define STD_PERROR(Std,Fmt, arg...)\
  STD_PERROR_##Std(Fmt,##arg)
#endif

/**
 * @brief funcion simil \p STD_SNPRINTF pero esta visulaiza el frame actual de donde 
 * se invoco (nombre de archivo, funcion y numero de linea)
 * Este llamado saca directamente los datos por std stream .
 * \param Std std ostream este debe ser uno de los siguiente .
 *  \b cout ostream estandar de salida
 *  \b cerr ostream estandar para error
 * \param buff buffer que usara temporalmente para sacas los datos por el stream
 * \param ...  Cstyle string con el fmt y el resto de parametros si son requeridos 
 */
#define STD_FSNPRINTF(Std,buff, Fmt , arg... ) \
{\
  snprintf(buff, sizeof(buff) - 1,"%s:%s():%d: " Fmt ,__FILE__,__func__,__LINE__,##arg);\
  std::Std<<buff;\
}

/**
 * @brief funcion simil STD_SNPRINTF pero termina la ejecucion del programa con un valor de 
 * retrono especificado.
 * \param Std std ostream este debe ser uno de los siguiente
 *  \b cout ostream estandar de salida
 *  \b cerr ostream estandar para error
 * \param buff buffer
 * \param Exit estado de terminacion para el caller, este debe ser
 *  \p SUCCES
 *  \p FAILURE
 * \param ...  Cstyle string con el fmt y el resto de parametros si son requeridos 
 */
#define STD_ERR_EXIT(Std,buff,Exit, Fmt, arg...) \
{\
  snprintf(buff, sizeof(buff) - 1, Fmt "\n", ##arg );\
  std::Std<<buff;\
  exit(EXIT_##Exit);\
}  

/**
 * @brief funcion simil \p STD_ERR_EXIT pero esta visulaiza el frame actual de donde 
 * se invoco (nombre de archivo, funcion y numero de linea)
 * \param Std std ostream este debe ser uno de los siguiente
 *  \b cout ostream estandar de salida
 *  \b cerr ostream estandar para error
 * \param buff buffer
 * \param Exit estado de terminacion para el caller, este debe ser
 *  \p SUCCES
 *  \p FAILURE
 * \param ...  Cstyle string con el fmt y el resto de parametros si son requeridos 
 */
#define STD_FERR_EXIT(Std,buff,Exit, Fmt , arg...) \
{\
  snprintf(buff, sizeof(buff) - 1,"%s:%s():%d: " Fmt "\n",__FILE__,__func__,__LINE__,##arg);\
  std::Std<<buff;\
  exit(EXIT_##Exit);\
}

/**
 * @brief macro funcion para obtener el tamaño de una array
 * no la cantidad de bytes, si no el numero de elementos.
 * \param[in] Arr : nombre del array en cuestion
 * \return cantidad de items que contiene \p Arr 
 */
#define ARRAY_SIZE(Arr) (sizeof(Arr)/sizeof(Arr[0]))

/**
 * @brief macro funcion para obtener el iterador que apunta 
 * al inicio del array \p Arr .
 * \param[in] Arr : nombre del array en cuestion .
 * \return iterador que apunta al inicio del array \p Arr . 
 */
#define ARRAY_BEGIN(Arr) Arr

/**
 * @brief macro funcion para obtener un iterador que apunta
 * al final del array \p Arr .
 * \param[in] Arr : nombre del array en cuestion .
 * \return iterador que apunta al inicio del array \p Arr .  
 */
#define ARRAY_END(Arr) Arr+(sizeof(Arr)/sizeof(Arr[0]))

/**
 * @brief Macro funcion para obtere el rango de un array \p Arr .
 * El rango es considerado de como el par de iteradores [it_beg , it_end).
 * Donde \b it_beg apunta al inicio del array (este valor se puede tomar), 
 * mientras \b it_end apunta a una posicion mas alla del final ( este valor
 * no puede ser tomado es solamente para fijar limite superior ).
 * \param[in] Arr : nombre del array en cuestion .
 * \return rango especificado mediante los iteradores [ \b it_beg , \b it_end) . 
 */
#define ARRAY_RANGE(Arr) Arr,Arr+(sizeof(Arr)/sizeof(Arr[0]))




template<typename IT>
void container_print(
                      IT first, IT last
                    , const char* msg = nullptr
                    , const char* sep = " , "
                    , const char* end = "\n\n"
                    , std::ostream& ou = std::cout
                    )
{
  if(msg)
    ou<<msg;
  auto it = first;
  while(it != last)
  {
    ou<<*it;
    it++;
    if( sep && it != last )
      ou<<sep;
  }
  if(end)
    ou<<end;
}


/** Generalizando */
template<typename v>
void print_array(const std::string& name, v& vct)
{   
  for(size_t i = 0 ; i < vct.size(); i++)
  {
    std::cout<<"\t"<<name<<"[ "<<i<<" ] = "<<vct[i]<<std::endl;    
  }
  std::cout<<std::endl;
}
#define PRINT_ARRAY(var) print_array(#var,var)


/* void casting */
#define CAST_VOID_UINT2PVOID(i)  (void*)(uintptr_t)(i)
#define CAST_VOID_PVOID2UINT(p)  (unsigned int)(uintptr_t)(p)
#define CAST_VOID_INT2PVOID(i)   (void*)(intptr_t)(i)
#define CAST_VOID_PVOID2INT(p)   (signed int)(intptr_t)(p)
  
#define CAST_VOID_PVOID2F32(p)   (*((float*) p))
  
#define CAST_VOID_UINT2PPVOID(p)    (void**) &p
#define CAST_VOID_INT2PPVOID(p)     (void**) &p
#define CAST_VOID_FLOAT2PPVOID(p)   (void**) &p
#define CAST_VOID_DOUBLE2PPVOID(p)  (void**) &p  
#define CAST_VOID_PCHAR2PPVOID(p)   (void**) &p
#define CAST_VOID_PPCHAR2PPVOID(p)  (void**) &p
#define CAST_VOID_STRUCT2PPVOID(p)  (void**) &p
#define CAST_VOID_PSTRUCT2PPVOID(p) (void**) &p


/**
* 
* ********************************************************************************
* \def CAST_VOID(Type,Op)
* \brief Macro funcion para realizar el casting de puntero a void a contenedores
* del tipo entero con y sin signo { uint16_t|int16_t|uint32_t|int32_t }
* \param Type : Tipo de casting
*   \li UINT2PVOID    -> CAST_VOID(UINT2PVOID,varname) : casting de entero sin signo a puntero void 
*   \li PVOID2UINT    -> CAST_VOID(PVOID2UINT,varname) : casting de puntero void a entero sin signo 
*   \li INT2PVOID
*   \li PVOID2INT
* 
*   \li PVOID2F32   float
*   \li PVOID2F64   double
*   \li PVOID2FMAX  long double
* 
*   \li UINT2PPVOID   -> CAST_VOID(UINT2PPVOID,varname)
*   \li INT2PPVOID    -> CAST_VOID(INT2PPVOID,varname)
*   \li FLOAT2PPVOID  -> CAST_VOID(FLOAT2PPVOID,varname)
*   \li DOUBLE2PPVOID -> CAST_VOID(DOUBLE2PPVOID,varname)
*   \li PCHAR2PPVOID  -> CAST_VOID(PCHAR2PPVOID,varname)
*   \li PPCHAR2PPVOID -> CAST_VOID(PPCHAR2PPVOID,varname)
*   \li PPCHAR2PPVOID -> CAST_VOID(STRUCT2PPVOID,varname)
*   \li PPCHAR2PPVOID -> CAST_VOID(PSTRUCT2PPVOID,varname)
* 
* \param Op : Operando sobre el cual se realiza el casting, este puede ser un
* litera, una variable o puntero.
* \return nothinig
* \code {.c++}
void * fn_example(void * loops)
{
  int loc, j;
  uint32_t max = CAST_VOID(PVOID2UINT,loops);
  //... more code
}
//...
uint32_t j = 1024*5/4;
fn_example(CAST_VOID(UINT2PVOID,j));
//...
fn_example(CAST_VOID(UINT2PVOID,(1024*5/4)));
* \endcode
*********************************************************************************/ 
#define CAST_VOID(Type,Op) CAST_VOID_##Type(Op)  



#if (VERSION == 0)

#elif (VERSION == 1)

#elif (VERSION == 3)

#elif (VERSION == 4)

#elif (VERSION == 5)

#elif (VERSION == 6)

#elif (VERSION == 7)

#elif (VERSION == 8)

#elif (VERSION == 9)

#elif (VERSION == 10)

#else 

#endif
  



#endif /*#ifndef __main_hpp__ */
