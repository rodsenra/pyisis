<html>
<head><title>xmlrpc</title></head>
<body>
<h1>XMLRPC Client PHP-5</h1>
<h2>CRUD Operations - ISIS-NBP</h2>

<?php
    include("xmlrpc.inc");

    function prtsend($func){
 	print "<pre>Sending the following request:\n\n" . htmlentities($func->serialize()) . "\n\nDebug info of server data follows...\n\n";
    }

    function prtresult($result) {

	if(!$result->faultCode()) {
		$v=$result->value();
		print "</pre><br/><< ". htmlspecialchars($v->scalarval()) . "<br/>";
	} else {
		print "Error! Code: " . htmlspecialchars($r->faultCode())
			. " Reason: '" . htmlspecialchars($r->faultString()) . "'</pre><br/>";
	}
    }

    if(!isset($HTTP_POST_VARS) && isset($_POST)) {
		$HTTP_POST_VARS = $_POST;
    }

    $c=new xmlrpc_client("/web/xmlrpc/", "192.168.0.21", 8000);
    $c->setDebug(0);
	
    $database = new xmlrpcval(
       array (
	'collection' => new xmlrpcval('sample','string'),
	'database'  => new xmlrpcval('phpdb','string')
       ),'struct'); 

    //Delete Database
    $f=new xmlrpcmsg('deleteDB',array(php_xmlrpc_encode($database)));
    prtsend($f);
    $r=&$c->send($f);
    prtresult($r);
	
    //Create Database
    $f=new xmlrpcmsg('createDB',array(php_xmlrpc_encode($database)));
    prtsend($f);
    $r=&$c->send($f);
    prtresult($r);

    $database = new xmlrpcval(
       array (
	'collection' => new xmlrpcval('sample','string'),
	'database' => new xmlrpcval('phpdb','string'),
	'24' => new xmlrpcval('Techniques for the measurement of transpiration of individual plants','string'),
	'26' => new xmlrpcval('^aParis^bUnesco^c-1965','string'),
	'30' => new xmlrpcval('^ap. 211-224^billus.','string'),
	'44' => new xmlrpcval('Methodology of plant eco-physiology: proceedings of the Montpellier Symposium','string'),
	'50' => new xmlrpcval('Incl. bibl.','string'),
	'69' => new xmlrpcval('Paper on: <plant physiology><plant transpiration><measurement and instruments>','string'),
	//subfiled
	'70' => new xmlrpcval(
			array (
			        new xmlrpcval('Magalhaes, A.C','string'),
			        new xmlrpcval('Franco, C.M.','string')
			), 'array'),
       ),'struct'); 


    //Create Record
    $f=new xmlrpcmsg('createRecord',array(php_xmlrpc_encode($database)));
    prtsend($f);
    $r=&$c->send($f);
    prtresult($r);


    $database = new xmlrpcval(
       array (
	'collection' => new xmlrpcval('sample','string'),
	'database' => new xmlrpcval('phpdb','string'),
	'24' => new xmlrpcval('XXX Techniques for the measurement of transpiration of individual plants','string'),
	'26' => new xmlrpcval('^aXXX Paris^bXXX Unesco^cXXX -1965','string'),
	'30' => new xmlrpcval('^aXXX p. 211-224^b XXXillus.','string'),
	'44' => new xmlrpcval('XXX Methodology of plant eco-physiology: proceedings of the Montpellier Symposium','string'),
	'50' => new xmlrpcval('XXX Incl. bibl.','string'),
	'69' => new xmlrpcval('XXX Paper on: <plant physiology><plant transpiration><measurement and instruments>','string'),
	//subfield
	'70' => new xmlrpcval(
			array (
			        new xmlrpcval('XXX Magalhaes, A.C','string'),
			        new xmlrpcval('XXX Franco, C.M.','string')
			), 'array'),
	'mfn' => new xmlrpcval(1,'int')
       ),'struct'); 

    //Update Record
    $f=new xmlrpcmsg('updateRecord',array(php_xmlrpc_encode($database)));
    prtsend($f);
    $r=&$c->send($f);
    prtresult($r);


    $database = new xmlrpcval(
       array (
	'collection' => new xmlrpcval('sample','string'),
	'database' => new xmlrpcval('phpdb','string'),
	'mfn' => new xmlrpcval(1,'int')
       ),'struct'); 

    //Delete Record
    $f=new xmlrpcmsg('deleteRecord',array(php_xmlrpc_encode($database)));
    prtsend($f);
    $r=&$c->send($f);
    prtresult($r);


    $database = new xmlrpcval(
       array (
	'collection' => new xmlrpcval('sample','string'),
	'database' => new xmlrpcval('phpdb','string'),
	'from' => new xmlrpcval(1,'int'),
	'to' => new xmlrpcval(1,'int'),
	'count' => new xmlrpcval(1,'int'),
	'reverse' => new xmlrpcval('off','string'),
	'gizmo' => new xmlrpcval('gunima','string')
       ),'struct'); 

    //Read Record
    $f=new xmlrpcmsg('readRecord',array(php_xmlrpc_encode($database)));
    prtsend($f);
    $r=&$c->send($f);
    prtresult($r);

?>
<hr/>
</body>
</html>
