
let container = document.getElementsByClassName('takePhoto');
let button = document.getElementById('startButton');
let otherContainer = document.getElementsByClassName("otherButtons");
let button1 = null;
let button2 = null;
let img = null;

function startSelfie(event){
    img = document.createElement('img');
    img.src = "photo";
    container[0].append(img);
    button.style.display = "none";  // hide button
    button1 = document.createElement('button');
    button2 = document.createElement('button');
    button1.id = 'TakePhoto';
    button2.id = 'STOP';
    button1.textContent = 'Take Selfie 😊';
    button2.textContent = 'Stop';
    otherContainer[0].append(button1);
    otherContainer[0].append(button2);


}

function takeSelfie(event){
    let source = "{{url_for('selfie')}}"
    img.src = source
}

button1.addEventListener('click', takeSelfie)






// clear

function clearPic(event){
    if (img != null){
        button.style.display = "block";
        container[0].removeChild(img);

    }

}
button2.addEventListener('click', clearPic);