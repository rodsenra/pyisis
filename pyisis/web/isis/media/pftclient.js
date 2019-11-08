function select_innerHTML(objeto,innerHTML){
/******
* select_innerHTML - corrige o bug do InnerHTML em selects no IE
* Veja o problema em: http://support.microsoft.com/default.aspx?scid=kb;en-us;276228
* Versão: 2.1 - 04/09/2007
* Autor: Micox - Náiron José C. Guimarães - micoxjcg@yahoo.com.br
* @objeto(tipo HTMLobject): o select a ser alterado
* @innerHTML(tipo string): o novo valor do innerHTML
*******/
    objeto.innerHTML = ""
    var selTemp = document.createElement("micoxselect")
    var opt;
    selTemp.id="micoxselect1"
    document.body.appendChild(selTemp)
    selTemp = document.getElementById("micoxselect1")
    selTemp.style.display="none"
    if(innerHTML.toLowerCase().indexOf("<option")<0){//se não é option eu converto
        innerHTML = "<option>" + innerHTML + "</option>"
    }
    innerHTML = innerHTML.toLowerCase().replace(/<option/g,"<span").replace(/<\/option/g,"</span")
    selTemp.innerHTML = innerHTML  
    
    for(var i=0;i<selTemp.childNodes.length;i++){
        var spantemp = selTemp.childNodes[i];
  
        if(spantemp.tagName){     
            opt = document.createElement("OPTION")
    
   			if(document.all){ //IE
    			objeto.add(opt)
   			}else{
    			objeto.appendChild(opt)
   		}       
    
    //getting attributes
   		for(var j=0; j<spantemp.attributes.length ; j++){
    		var attrName = spantemp.attributes[j].nodeName;
    		var attrVal = spantemp.attributes[j].nodeValue;
    		if(attrVal){
     		try{
      			opt.setAttribute(attrName,attrVal);
      			opt.setAttributeNode(spantemp.attributes[j].cloneNode(true));
     		}catch(e){}
    		}
   		}
   		//getting styles
   		if(spantemp.style){
  		  	for(var y in spantemp.style){
     			try{opt.style[y] = spantemp.style[y];}catch(e){}
    		}
   		}
   		//value and text
   		opt.value = spantemp.getAttribute("value")
   		opt.text = spantemp.innerHTML
   		//IE
   		opt.selected = spantemp.getAttribute('selected');
   		opt.className = spantemp.className;
  		} 
 	}    
 	document.body.removeChild(selTemp)
 	selTemp = null
}

function AjaxError(req){
   result = document.getElementById("resultdiv");
   result.innerHTML = req.responseText;
   result.style.color = "#ff0000";
}

function PopulateDB(req){
	select_innerHTML(document.getElementById("database_name"),req.responseText);
}

function getDatabases() {
    var collection = $("collection_name_id");
    collection_name = collection.item(collection.selectedIndex).value; 

    if (collection_name == "--Select--") {
      select_innerHTML(document.getElementById("database_name"),"");	
	  return;
    }
    
    var params = $H({ collection:collection_name});
    
    var url = '/web/pftget_databases/';
    ajaxReq = new Ajax.Request(
                   url,
                   {
                    method: 'post',
                    parameters: params.toQueryString(),
                    onSuccess: PopulateDB,
                    onFailure: AjaxError
                   });   
}

function sendForm(){
    var collection = $("collection_name_id");
    collection_name = collection.item(collection.selectedIndex).value; 
  
    var database = $("database_name");
    if (database.length == 0) {
       alert("Database not selected");
       return;
    }
    
    database_name = database.item(database.selectedIndex).value; 
    if (collection_name == "--Select--" || !database_name) {
	  alert("Please select collection and database");
	  return;
    }   

    var record = parseInt($("record").value);
    if (isNaN(record)) {
      alert("Invalid Record number!");
      return;
    }    
    
    pft = $('pft').value;
    if (pft == "") {
       alert("Function not defined!");
       return;
    }
    
    var params = $H({collection:collection_name, database:database_name, record:record, pft:pft});
    
    var url = '/web/pftfunction/';
    ajaxReq = new Ajax.Request(
                   url,
                   {
                    method: 'post',
                    parameters: params.toQueryString(),
                    onSuccess: PftResponse,
                    onFailure: AjaxError
                   });   
    
}

function PftResponse(req){
   $('resultdiv').innerHTML = req.responseText;
   $('resultdiv').style.color = "#000000";

}
