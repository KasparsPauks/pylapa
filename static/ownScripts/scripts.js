//Šis ir mans indivudālais js fais
function showTime(){
	var date = new Date();
    var h = date.getHours(); // 0 - 23
    var m = date.getMinutes(); // 0 - 59
    var s = date.getSeconds(); // 0 - 59
    var session = "24 h formātā";
    if(h  < 10){
    	h = "0" + h;
    }
    if(m<10){
    	m = "0" + m;
    }
    if(s<10){
    	s = "0" + s  ;
    }
    var time = h + ":" + m + ":" + s + " " + session ;
    document.getElementById("MyClockDisplay").textContent = time;
    setTimeout(showTime, 1000);
 }
// Iegūt fiksētu laiku un ielikt dokumentā:
function fixedTime(){
    var dt = new Date();
document.getElementById("fixedTime").innerHTML = dt.toLocaleString();
}
function palielinat(){
           var a = 1
           a=a+1
//           document.getElementById("palielinat") = a;
           console.log(a)


}