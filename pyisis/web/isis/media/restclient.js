lin_id = 1;

function showForm(taction,divblock,caption){
  hideAll();
  $('doActionForm').value = taction;
  $('resultText').value="";
  $('sentText').value="";  
  $(divblock).style.display = 'block';
  $('titlediv').value = caption;
}

function hideAll(){
    var divsblocked = ["deletedbdiv","createrecdiv","readrecdiv","deleterecdiv","createdbdiv"];
    for (var x = 0; x < divsblocked.length; x++) {
        $(divsblocked[x]).style.display  = 'none';
    }
}


function AjaxResponse(req){
   $('resultText').value = req.responseText;
}

function fillSentText(method,url, body){
	$('sentText').value = "Method: "+method+"\nURL: "+ url + "\nBody/Parameters:\n"+body;
}


function deleteDB(){
    var dbname = $('dbnamed').value.strip();
    var collection = $('collection_name').value.strip();
    var url = '/web/restapi/'+collection+'/'+dbname+'/';

    if (!collection) {
	alert("No collection specified.");
	return;
    }

    if (!dbname) {
	alert("No database specified.");
	return;
    }
	
	fillSentText("DELETE",url,"");
	
    ajaxReq = new Ajax.Request(
                   url,
                   {
                    method: 'delete',
		    		postBody: "",
                    onSuccess: AjaxResponse,
                    onFailure: AjaxResponse
                   });
}


function createDB() {
    var dbname = $("dbnamec").value.strip();
    var collection = $("collection_name").value.strip();

    if (!collection) {
	alert("No collection specified.");
	return;
    }

    if (!dbname) {
	alert("No database specified.");
	return;
    }

    var body = '<?xml version="1.0" encoding="utf-8"?><parameters><database>'+dbname+'</database></parameters>'; 
    var url = '/web/restapi/'+collection+'/';
    
	fillSentText("POST",url,body);
	
	ajaxReq = new Ajax.Request(
                   url,
                   {
                    method: 'post',
		    		postBody: body,
                    onSuccess: AjaxResponse,
                    onFailure: AjaxResponse
                   });
}


function readRecord() {
     var freverse   = 'off';
     var dbname     = $("database").value.strip();
     var collection = $("collection_name").value.strip();
     var from_reg   = $("from_reg").value;
     var to_reg     = $("to_reg").value;
     var count_reg  = $("count_reg").value;
     var gizmo      = $("gizmo").value;
     if ($("reverse").checked == true) freverse = 'on';

    if (!collection) {
	alert("No collection specified.");
	return;
    }

    if (!dbname) {
	alert("No database specified.");
	return;
    }
     
    var params = $H({ gizmo:gizmo, from:from_reg, to:to_reg, count:count_reg, reverse:freverse });
    var url = '/web/restapi/'+collection+'/'+dbname+"/";
 
    fillSentText("GET",url,params.toQueryString());
	
    ajaxReq = new Ajax.Request(
                   url,
                   {
                    method: 'get',
		    		postBody: "",
                    parameters: params.toQueryString(),
                    onSuccess: AjaxResponse,
                    onFailure: AjaxResponse
                   });
}


function getsubField(fieldValue){
  var result = new Array();
  var first_tag = fieldValue.indexOf('^');
  if ( first_tag > -1) {
    var fields = fieldValue.split('^');
    for (var i=0; i < fields.length; i++){
      field_data = fields[i];
      if (field_data.length > 0) {
        if ( i == 0 && first_tag > 0) {
          result[i] = ["",field_data];
        } else {
          result[i] = [field_data.substr(0,1), field_data.substr(1)];
        }
      }
    }
  } else {
    result[0] = ["",fieldValue];
  }
  return result;
}


function createRecord(){
  var dataValues = new Array();
  var dataTags = new Array();
  var tagGroup = new Array();
  var collection = $('collection_name').value.strip();
  var dbname = $('databasecr').value.strip();  
  var table = $('taglist');
  var url = '/web/restapi/'+collection+'/'+dbname+'/';   
  var xml = '<?xml version="1.0" encoding="utf-8"?><record>';
  
  if (!collection) {
      alert("No collection specified.");
      return;
  }

  if (!dbname) {
      alert("No database specified.");
      return;
  }

  if (table.rows.length == 1) {
     alert("No data!");
     return;
  }
  
  var index_a = 0;
  for (var i=1; i < table.rows.length; i++){
    dataTags[index_a] = table.rows[i].cells[1].firstChild.value;
    dataValues[index_a] = table.rows[i].cells[2].firstChild.value;
    index_a += 1;
  }
  
  for (var i=0; i< dataTags.length; i++){
    var currentTag = dataTags[i];
    if (!currentTag) continue;
    xml += '<field tag="'+ currentTag +'">';
    xml += '<occ>';
    var result = getsubField(dataValues[i]);
    for (var x=0; x < result.length; x++) {
      if (!result[x]) continue;
      xml += '<subfield tag="'+ result[x][0] +'">'+ result[x][1] +'</subfield>';
    }
    xml += '</occ>';
    xml += '</field>';
  }
  xml += '</record>';
 
  fillSentText("POST",url,xml);
  ajaxReq = new Ajax.Request(
                 url,
                 {
                  method: 'post',
		  		  postBody: xml,
                  onSuccess: AjaxResponse,
                  onFailure: AjaxResponse
                  });    
}


function deleteRecord(){

  var collection = $('collection_name').value.strip();
  var dbname = $('databasedr').value.strip();  
  var mfn = parseInt($('mfn').value);  
  var url = '/web/restapi/'+collection+'/'+dbname+'/'+mfn+'/';

  if (!collection) {
      alert("No collection specified.");
      return;
  }

  if (!dbname) {
      alert("No database specified.");
      return;
  }
  
  if (isNaN(mfn)) {
      alert("Invalid MFN number!");
      return;
  }
  fillSentText('DELETE',url,"");
  ajaxReq = new Ajax.Request(
                  url,
                  {
                    method: 'delete',
		    		postBody: "",
                    onSuccess: AjaxResponse,
                    onFailure: AjaxResponse
                   });
}


function sendForm() {
	$("sentText").value = "";
    $("resultText").value = "";
    var action = $('doActionForm').value;
    if (action == 'createdb') createDB();    
    if (action == 'deletedb') deleteDB();
    if (action == 'createrec') createRecord();
    if (action == 'readrec') readRecord();
    if (action == 'deleterec') deleteRecord(); 
}


function putCheckBox (cel_id) {
    var td = document.createElement('TD');
    var xinput = document.createElement('INPUT');
    xinput.setAttribute('type', 'checkbox');
    xinput.id = cel_id;
    xinput.name = "checkcut";
    td.appendChild(xinput);
    return td;
}


function putCel (cel_id,sz) {
    var td = document.createElement('TD');
    var xinput = document.createElement('INPUT');
    xinput.value = "";
    xinput.id = cel_id;
    xinput.name = cel_id;
    xinput.size = sz;
    td.appendChild(xinput);
    return td;
}


function removeRow(idrow){
   var table = $('tbody');
   for (var i=0; i < table.rows.length; i++) {
      if (table.rows[i].id == 'lin_id_'+idrow) {
        table.deleteRow(i);
	break;
      }
   } 
}


function delLinha() {
   var lista = new Array();
   var table = $("taglist"); 
   for (var i=1; i < table.rows.length; i++){
       var checkboxcut = table.rows[i].cells[0];
       if (checkboxcut.firstChild.checked == true) {
	  lista[checkboxcut.firstChild.id] = checkboxcut.firstChild.id;
       }
   }
   for (var i=0;i < lista.length; i++){
      if (!lista[i]) continue;
      removeRow(lista[i]);
   } 
}

function bla(){
	
}

function putLinha() {
    var tabbody = $('tbody'); 
    var tr = document.createElement('TR');
    var linha_id = 'lin_id_' + String(lin_id);
    var td = putCheckBox(lin_id);
    tr.setAttribute('id', linha_id);
    tr.appendChild(td);
    td = putCel('ed_tag_' + lin_id, 6);
    tr.appendChild(td);
    td = putCel('ed_value_' + lin_id, 60);
    tr.appendChild(td);
    tabbody.appendChild(tr);
    lin_id += 1;
}

