import { ARRAY_IdGauges } from "./settings.js";
import { URL, PORT } from "./constants.js";



class WebSocketClient{
    /** constructor */
    constructor(url,port,receive_callback=null,close_callback=null,error_callback=null){
        
        this.status = true;
        this.wssocket = new WebSocket(`${url}:${port}`);

        if (this.wssocket == undefined || this.wssocket == null){
            this.status = false;
            return; /* no tenemos objeto */
        }
        
        if(receive_callback != null){
            this.wssocket.onmessage = (data) =>{
                receive_callback(data);
                this.wssocket.send("ok");
            };
        }
        if (close_callback != null){
            this.wssocket.onclose = ()=> {
                this.status = false;
                close_callback();                        
            }
        }
        if (error_callback != null ){
            this.wssocket.onerror = (err) => {
                this.status = false;
                console.log('call to error_callback with:', err);
                error_callback(err);
            } 
        }
        else{
            this.wssocket.onerror = (err) => {
                this.status = false;
                console.log('WebSocket Error:',err);              
            } 
        }

    }            
    close(){
        this.wssocket.close();
        this.status = false;
    }
}

function gauge_set_value(value=0,id=1,color='#005578'){
    const fill = document.getElementById(`gauge-${id}-fill`);
    const text = document.getElementById(`gauge-${id}-text`);
    if (fill == null || text == null) return;

    // Calculamos la rotación: 
    // 0% = 0turn | 100% = 0.5turn (media vuelta)
    const rotation = value / 200; 

    // Aplicamos el estilo directamente al elemento
    fill.style.transform = `rotate(${rotation}turn)`;
    fill.style.background = color;
    // Actualizamos el texto central
    text.textContent = `${value}%`;
    
    // Opcional: Cambiar el color del texto según el valor
    if(value > 80) 
        text.style.color = "#f44336";
    else if(value > 50)
        text.style.color = "#ff9800";
    else 
        text.style.color = "#FFFFFF";
}

function clean_gauges(){
    ARRAY_IdGauges.forEach((item)=>{
        gauge_set_value(0,item);
        console.log(`gauge_set_value(0,${item});`);
    }); 
}



function set_buttons(status){
    let btn_send = document.getElementById("btn-start");
    if (btn_send != null){
        if(status){
            btn_send.classList.remove("btn-start-nok");
            btn_send.classList.add("btn-start-ok");
        }
        else{
            btn_send.classList.remove("btn-start-ok");
            btn_send.classList.add("btn-start-nok");
        }
    }
}

window.addEventListener("DOMContentLoaded", () => {
    // Initialize the UI.    
    const wsclient = new WebSocketClient(
        URL,PORT,
        (event) => {
            let arr = JSON.parse(event.data)
            console.log('Message from server:',arr);
            arr.forEach((item,idx)=>{
                gauge_set_value(item[1],idx+1,item[0]);
            });
        },
        (error) => {
            console.log('WebSocket Error:' ,error);
            set_buttons(this);
        },
        () => console.log(`Connection closed`)
    );  
    // set gauges en zero
    clean_gauges();
    
    if ( wsclient != null){
        /* set los handler para cada button */
        let btn_clean = document.getElementById("btn-clean");
        let btn_stop = document.getElementById("btn-stop");
        set_buttons(true);
    
        if (btn_clean != null){
            btn_clean.addEventListener("click",()=>{
                //console.log('Boton clean presionado');
                clean_gauges();
                //set_buttons(false);
                
            });
        }
        if(btn_stop != null){
            btn_stop.addEventListener("click",()=>{
                //console.log('Peticion de cierre de Socket');
                wsclient.close();
                set_buttons(false);
            });
        }        
    }    
});