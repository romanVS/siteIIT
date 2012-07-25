	var _activeElement = null;
	
	function setActive(e)
	{
		_activeElement = e;
	}

	function clearActive()
	{
		_activeElement = null;
	}

	function getActive()
	{
		if (_activeElement == null) return false;
		return true;
	}
	
	function returnTextArea(el)
	{
		document.getElementById(el).focus();
	}

	function ctrlEnter(event)
	{
		if(event.ctrlKey && event.keyCode==13 && getActive()==true)
		{
			document.getElementById("input").click();
		}
	}
				
	if (document.addEventListener) { 
        	document.addEventListener('keydown', ctrlEnter, false);
    	}
