function showhide() {
    for(var i = 0; i < arguments.length; i++){
      var e = document.getElementById(arguments[i]);
      e.style.display = (e.style.display == 'block') ? 'none' : 'block';
    }
  }