let url = "{{url_for('video')}}"
let button = document.getElementById("start_button");
let centerBox = document.getElementsByClassName("centerBox");
let img = null;



function record(event){
    if (button.textContent == "START"){
         //  create img tag
        img = document.createElement("img");
        img.src = url;
        // append img tag
        centerBox.prepend(img);
        button.style.backgroundColor = "hsl(0, 98%, 51%)";
        button.textContent = "STOP";
        button.id = "stop_button"
    }
    else{
        if(img && centerBox.contains(img)){
            // remove img tag
            centerBox[0].removeChild(img);
        }
        // change button content
        button.textContent == "START";
        button.style.backgroundColor = "hsl(120, 81%, 55%)"
        button.removeAttribute("id");
        
    }
   
    
}
button.addEventListener("click", record);
