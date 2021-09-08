


function toggleEnable(id) {
    var textbox = document.getElementById(id);
    
    if (textbox.disabled) {
       // If disabled, do this 
        document.getElementById(id).disabled = false;
     } else {
        // Enter code here
         document.getElementById(id).disabled = true;
      }
 }