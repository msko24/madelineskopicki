

let today= new Date();

let day=today.getDate();
let month = today.getMonth()+1;
let year=today.getFullYear();
let min=today.getMinutes();
let hour=today.getHours();
let time=hour +":" + min;
let ampm = "";

if(min<10){
    min="0" + min;
}

if(day<10){
    day="0"+ day;
}

if(month<10){
    month="0" + month;
}

if(hour / 12 > 1){
    ampm="PM";
    time = (today.getHours() % 12) + ":" + min;
}else{
    ampm = "AM"
    time = (today.getHours() % 12) + ":" + min;
}

if (min<10){
    min="0"+min;
}

document.getElementById("time-date").innerHTML=
    `<h3>${time+ampm}</h3>
     <h5>${month+"/"+day+"/"+year}</h5>
    `
;