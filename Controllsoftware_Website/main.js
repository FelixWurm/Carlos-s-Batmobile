// initGame...
/*function initAll(websocket, data){ //weird... data sind komisch
    websocket.addEventListener("open", () =>{
        //send an "init" event according to who is connecting
        const params = new URLSearchParams(window.location.search);//could we use this for the checkboxes?
        
        //only if plural clients and I don't really understand:
        //let event = { type: "init"};
        ##
        if(params.has("join")){
            //joining
            event.join = params.get("join");
        }
        else{ ##
        //add
        let event = {
            "type" : "data",
            "data" : data,
        }
        //}
        websocket.send(JSON.stringify(event));
    });
}*/
//code from html imbedded script
function InputControl(){
    var distance = document.getElementById('dist').value;
    var speed = document.getElementById('speed').value;
    var rotation = document.getElementById('rotat').value;

    //if no input, then value = undefined, so we need to change it to 0
    if(dist === undefined){
      distance = 0;
    }
    if(speed === undefined){
      speed = 0;
    }
    if(rotation === undefined){
      rotation = 0;
    }

    //to prevent incorrect input values for our functions
    if((speed> -40 && speed <40 && speed != 0)||(speed >100 || speed< -100)){
      showMessage("Please enter a positive or negative between 40 and 100");
      return false;
    }
    if(rotation< -360 || rotation > 360){
      showMessage("Please do maxiumum 360 degree turns only");
      return false;
    }

    let data = {
        "indicator": 1,
        "carlos": "john3",
        "distance": distance,
        "speed": speed,
        "rotation": rotation,
    }
    sendData(data);

}

//showMessage(message) for sending message... -> do we want this
function showMessage(message){
    window.setTimeout(()=> window.alert(message),50)
}

//new function instead of receiveMoves(board,websocket)
function ReceiveData(websocket){
    websocket.addEventListener("message",({data})=>{
        const event = JSON.parse(data);
        //just data!!!!!
        switch(event.type){
            // do we need init case?
            case "close": // needs to be added to tee.py!!!!! -> could be useful though
                websocket.close(1000);
                break;
            case "data":
                //save js or just evaluation and visualisation... preferably saved in scrollable and readable table?
                datafile = event.data;
                showMessage("data received");
                break;
            case "error": //tee.py --> but they don't have it there...
                showMessage("event.message"); //?
                break;
            default:
                throw new Error('Unsupported event type: ${event.type}.'); //maybe syntaxError...
        }
    });
}

function sendData(websocket, data){
    let event = {
        "type": "data",
        "data": data
    }
    websocket.send(JSON.stringify(event));
}

window.addEventListener("DOMContentLoaded", ()=>{
    //open the WebSocket connection and register handlers.
    const websocket = new WebSocket("ws://localhost:8001");
    //initAll(websocket);
    ReceiveData(websocket);
})


//code from the start
//window.addEventListener("DOMContentLoaded", () => {
    /* this was for stream of messages... now in show-messages?
      const messages = document.createElement("ul");
      document.body.appendChild(messages);
    
    
    const websocket = new WebSocket("ws://localhost:8001/");
      /*websocket.onmessage = ({ data }) => {
        const message = document.createElement("li");
        const content = document.createTextNode(data);
        message.appendChild(content);
       messages.appendChild(message);
     };
    //initAll(websocket);
    ReceiveData(websocket);
    sendData(websocket,data);
  // });
  */