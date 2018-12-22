#  Functions

---

## Chars

```
function escapeHtml(string) {
    var entityMap = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': '&quot;',
        "'": '&#39;',
        "/": '&#x2F;'
    };
    return String(string).replace(/[&<>"'\/]/g, function (s) {
        return entityMap[s];
    });
}

var projectIDReg = new RegExp("{projectID}", 'g');

```

---

## Array

```
function arrayFunctionInit(){
	Array.prototype.uniquelize = function(){  
		var ra = new Array();  
		for(var i = 0; i < this.length; i ++){  
			if(!ra.contains(this[i])){
				ra.push(this[i]);  
			}
		}  
		return ra;  
	};

	Array.prototype.each = function(fn){  
		fn = fn || Function.K;  
		var a = [];  
		var args = Array.prototype.slice.call(arguments, 1);  
		for(var i = 0; i < this.length; i++){  
			var res = fn.apply(this,[this[i],i].concat(args));  
			if(res != null) a.push(res); 
		}  
		return a;  
	};

	Array.prototype.contains = function (obj) {  
		var i = this.length;  
		while (i--) {  
			if (this[i] === obj) {  
				return true;  
			}  
		}  
		return false;  
	};

	Array.minus = function(a, b){  
		return a.uniquelize().each(function(o){return b.contains(o) ? null : o});  
	};
}
```

---

## Checkbox

```
var check = document.getElementsByClassName("ipt_checkbox");
var caseId_array = new Array();
for(var i = 0; i < check.length; i++) {
	if (check[i].checked) {
		caseId_array.push(check[i].id.split('_')[1])
	}
}
```

---

## Sort

```
caseId_array.sort(function(a,b){return Number(a)-Number(b);});

var responseTextDataKey = Object.keys(responseText["data"]).sort(function(a,b){
			return Number(responseText["data"][a]['index'])-Number(responseText["data"][b]['index']);
		});
```

---

## Ajax

```
'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()

var formObj = document.getElementById(ID);
var formData = new FormData(formObj);

contentType: false
processData: false
```

---

## Cookie

```
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = cookies[i].trim();
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function setCookie(c_name,value,expiredays){
	var exdate=new Date();
	exdate.setDate(exdate.getDate()+expiredays);
	// exdate.setTime(exdate.getTime()+expiresDays*24*3600*1000);
	document.cookie=c_name+ "=" +escape(value)+
	((expiredays==null) ? "" : ";expires="+exdate.toGMTString());
}
```