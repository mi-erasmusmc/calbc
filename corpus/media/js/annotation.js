function goto(url){
	window.open(url,"_self");
}

function SetAndSubmit( eltName, value ){
	document.getElementById( eltName ).value = value;
	document.getElementById('form').submit();
}

function getElementsByClassName(elt, needle) { 
	var s = elt.getElementsByTagName('*'), i = s.length, r = [], e, c; 
	needle = ' ' + needle + ' '; 

    while (i--) 
    { 
        e = s.item(i); 

        if (e.className) 
        { 
            c = ' ' + e.className + ' '; 
            if (c.indexOf(needle) != -1) r.push(e); 
        } 
    } 

    return r; 
}
