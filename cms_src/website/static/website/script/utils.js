function editURL(url,path,q_args){
	window.location = url + path.value + '?order_mode=' + q_args; 
	return false;
}

function changeField(field_name,value,element,display,name_div,name) {
	document.getElementById(field_name).value      = value;
	document.getElementById(element).style.display = display;
	document.getElementById(name_div).innerHTML    = name;
}