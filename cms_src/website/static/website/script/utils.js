function showhide() {
    for(var i = 0; i < arguments.length; i++){
      var e = document.getElementById(arguments[i]);
      e.style.display = (e.style.display == 'block') ? 'none' : 'block';
    }
  }

function changeField(field_name,value,display_element,hide_element) {
	document.getElementById(field_name).value              = value;
	document.getElementById(display_element).style.display = "block";
	document.getElementById(hide_element).hidden           = 'True';
}