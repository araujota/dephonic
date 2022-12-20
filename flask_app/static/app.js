var media = ["music", "podcast", "audio book", "message"];

var part = 0;
var partIndex = 0;
var intervalVal;

var element = document.getElementById("media");

function type() {
    var text = media[part].substring(0, partIndex+1);
    element.innerHTML = text;
    partIndex +=1;

    if(text === media[part]) {
        clearInterval(intervalVal);
        setTimeout(function() {
            intervalVal = setInterval(untype, 100);
        }, 1000);
    }
}

function untype() {
    var text = media[part].substring(0, partIndex-1);
    media.innerHTML = text;
    partIndex -=1;

    if(text==='') {
        clearInterval(intervalVal);

        if(part == (media.length-1)) {
            part = 0;
        } else {
            part ++;
        }
        partIndex=0;

        setTimeout(function() {
            intervalVal = setInterval(type, 100);
        }, 200);
    }
}

intervalVal = setInterval(type, 100);

