function showhide() {
    for(var i = 0; i < arguments.length; i++){
      var e = document.getElementById(arguments[i]);
      e.style.display = (e.style.display == 'block') ? 'none' : 'block';
    }
  }

function changeField(field_name,value,element,display,name_div,name) {
	document.getElementById(field_name).value      = value;
	document.getElementById(element).style.display = display;
	document.getElementById(name_div).innerHTML    = name;
}