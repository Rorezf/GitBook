// 函数getPerfTime用于返回页面性能的基本时间
function getPerfTime(){
	var tim = window.performance.timing;
	var Ent = performance.getEntriesByType("resource");
	var time = {};
	//time.white_screen = (chrome.loadTimes().firstPaintTime - chrome.loadTimes().startLoadTime)*1000;
	time.fist_byte = tim.responseStart - tim.navigationStart;
	time.domready = tim.domContentLoadedEventEnd - tim.navigationStart;
	time.domtree = tim.domComplete - tim.domInteractive;
	time.request = tim.responseEnd - tim.responseStart;
	time.tcp = tim.connectEnd - tim.connectStart;
	time.dns = tim.domainLookupEnd - tim.domainLookupStart;	
	time.redirect = tim.redirectEnd - tim.redirectStart;
	time.http = tim.responseEnd - tim.requestStart;
	time.resourceLoad = Ent[Ent.length-1].responseEnd - Ent[0].startTime;
	time.onload = tim.loadEventEnd - tim.navigationStart;
	time.wholeTime = time.redirect + time.dns + time.tcp + time.http + time.resourceLoad;
	time.wholeTime = time.onload > time.wholeTime? time.onload : time.wholeTime;
	return time;
}

// 函数reg用于正则判断performance.getEntries()中各元素的name属性，据此返回资源的类型
function reg(str){
	// name以css结尾或含有css?的，判断为css资源
	if(/css$/.test(str) || /css\?/.test(str)){
		return "css";
	}
	// name以js结尾或含有js?的，判断为js资源
	else if(/js$/.test(str) || /js\?/.test(str)){
		return "js";
	}
	// name以jpg png gif结尾或含有jpg? png? gif?的，判断为img资源
	else if(/jpg$/.test(str) || /jpg\?/.test(str) || /png$/.test(str) || /png\?/.test(str) ||  /gif$/.test(str) || /gif\?/.test(str)){
		return "img";
	}
	// 无法从name中判断的，先归类为其他，后面根据initiatorType作进一步判断
	else{
		return "others";
	}
}

// 函数getResource用于对资源进行分类，返回各类资源的大小、数量和加载时间
function getResource(){
	var Ent = performance.getEntries();		// 获取所有有效请求，无法请求不在列表中
	var resource = {}, etime = {}, str;
	var size = {"zimg":0, "zcss":0, "zjs":0, "zhtml":0, "zother":0};
	var count = {"cimg":0, "ccss":0, "cjs":0, "chtml":0, "cother":0}; 
	var stime = {"simg":0, "scss":0, "sjs":0, "shtml":0};
	// 资源是多种类多个同时加载的，同类型资源的加载时间为该类型最末资源加载完成时间responseEnd减去该类型首个资源开始加载时间startTime
	// 资源的大小可从transferSize属性得到，单位为B
	// 资源的分类先按name属性进行分类，无法分类的再根据initiatorType进一步分类
	for(var i = 0; i < Ent.length; i++){
	    str = reg(Ent[i].name);
	    switch(str){
	    	case "img":
	    		count.cimg++;
	    		size.zimg += Ent[i].transferSize;
	    		if(stime.simg == 0){
	    			stime.simg = Ent[i].startTime;
	    		}
	    		etime.eimg = Ent[i].responseEnd;
	    		break;
	    	case "css":
	    		count.ccss++;
	    		size.zcss += Ent[i].transferSize;
	    		if(stime.scss == 0){
	    			stime.scss = Ent[i].startTime;
	    		}
	    		etime.ecss = Ent[i].responseEnd;
	    		break;
	    	case "js":
	    		count.cjs++;
	    		size.zjs += Ent[i].transferSize;
	    		if(stime.sjs == 0){
	    			stime.sjs = Ent[i].startTime;
	    		}
	    		etime.ejs = Ent[i].responseEnd;
	    		break;
	    	case "others":
				switch(Ent[i].initiatorType){
			    	case "img":
			    		count.cimg++;
			    		size.zimg += Ent[i].transferSize;
			    		if(stime.simg == 0){
			    			stime.simg = Ent[i].startTime;
			    		}
			    		etime.eimg = Ent[i].responseEnd;
			    		break;
			    	case "css":
			    		count.ccss++;
			    		size.zcss += Ent[i].transferSize;
			    		if(stime.scss == 0){
			    			stime.scss = Ent[i].startTime;
			    		}
			    		etime.ecss = Ent[i].responseEnd;
			    		break;
			    	case "script":
			    		count.cjs++;
			    		size.zjs += Ent[i].transferSize;
			    		if(stime.sjs == 0){
			    			stime.sjs = Ent[i].startTime;
			    		}
			    		etime.ejs = Ent[i].responseEnd;
			    		break;
			    	case "xmlhttprequest":
			    		count.chtml++;
			    		size.zhtml += Ent[i].transferSize;
			    		if(stime.shtml == 0){
			    			stime.shtml = Ent[i].startTime;
			    		}
			    		etime.ehtml = Ent[i].responseEnd;
			    		break;
			    	default:
			    		count.cother++;
			    		if(Ent[i].transferSize){
			    			size.zother += Ent[i].transferSize;
			    		}
			    		break;
			    }
	    	default: break;
	    }
	}
	resource.amount = Ent.length;
	resource.imgNum = count.cimg;
	resource.imgTime = etime.eimg - stime.simg;
	resource.cssNum = count.ccss;
	resource.cssTime = etime.ecss - stime.scss;
	resource.jsNum = count.cjs;
	resource.jsTime = etime.ejs - stime.sjs;
	resource.htmlNum = count.chtml;
	resource.htmlTime = etime.ehtml - stime.shtml;
	resource.othersNum = count.cother;
	resource.imgSize = size.zimg/1024;
	resource.cssSize = size.zcss/1024;
	resource.jsSize = size.zjs/1024;
	resource.htmlSize = size.zhtml/1024;
	resource.othersSize = size.zother/1024;
	resource.wholeSize = (size.zimg + size.zcss + size.zjs + size.zhtml + size.zother)/1024;
	return resource;
}
