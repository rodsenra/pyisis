package br.com.gpr.javaclient;

import java.util.HashMap;
import java.net.URL;
import org.apache.xmlrpc.client.XmlRpcClient;
import org.apache.xmlrpc.client.XmlRpcClientConfigImpl;
import org.apache.xmlrpc.*;

public class JavaClient {

    private final static String server_url =
        "http://127.0.0.1:8000/web/xmlrpc/";
    
    static String result;
    
    public static void main (String [] args) {
        try {
        	
            XmlRpcClientConfigImpl config = new XmlRpcClientConfigImpl();
            config.setServerURL(new URL(server_url));
            XmlRpcClient client = new XmlRpcClient();
            client.setConfig(config);
            
            HashMap<String, String> params = new HashMap<String, String>();
            params.put("collection", "sample");
            params.put("database", "dbtest");
            
            Object[] params1 = new Object[]{params};
            result = (String) client.execute("deleteDB", params1);
            System.out.println("deleteDB >>: " + result);

            result = (String) client.execute("createDB", params1);            
            System.out.println("createDB >>: " + result);

            createRecord(client);
            updateRecord(client);
            deleteRecord(client);
            readRecord(client);

            
        } catch (XmlRpcException exception) {
            System.err.println("JavaClient: XML-RPC Fault #" +
                               Integer.toString(exception.code) + ": " +
                               exception.toString());
        } catch (Exception exception) {
            System.err.println("JavaClient: " + exception.toString());
        }
    }
    
    public static void createRecord(XmlRpcClient client){

    	try{
    		
	        HashMap<String, String> params = new HashMap<String, String>();
	        params.put("collection", "sample");
	        params.put("database", "dbtest");
	        params.put("24","Techniques for the measurement of transpiration of individual plants");
	        params.put("26","^aParis^bUnesco^c-1965");
	        params.put("30","^ap. 211-224^billus.");
	        params.put("44","Methodology of plant eco-physiology: proceedings of the Montpellier Symposium");
	        params.put("50","Incl. bibl.");
	        params.put("69","Paper on: <plant physiology><plant transpiration><measurement and instruments>");
	        params.put("70","Magalhaes, A.C. Franco, C.M.");
	        
	        Object[] params1 = new Object[]{params};
	        result = (String) client.execute("createRecord", params1);
	        System.out.println("createRecord >>: " + result);
 
    	} catch (XmlRpcException exception) {
    		System.err.println("JavaClient: XML-RPC Fault #" +
                           		Integer.toString(exception.code) + ": " +
                           		exception.toString());
    	} catch (Exception exception) {
    		System.err.println("JavaClient: " + exception.toString());
    	}
        
    }

    public static void updateRecord(XmlRpcClient client){

    	try{
    		
	        HashMap<String, String> params = new HashMap<String, String>();
	        params.put("collection", "sample");
	        params.put("database", "dbtest");
	        params.put("24","XXXTechniques for the measurement of transpiration of individual plants");
	        params.put("26","^aXXXParis^bXXXUnesco^cXXX-1965");
	        params.put("30","^aXXXp. 211-224^bXXXillus.");
	        params.put("44","XXXMethodology of plant eco-physiology: proceedings of the Montpellier Symposium");
	        params.put("50","XXXIncl. bibl.");
	        params.put("69","XXXPaper on: <plant physiology><plant transpiration><measurement and instruments>");
	        params.put("70","XXXMagalhaes, A.C. Franco, C.M.");
	        params.put("mfn","1");
	        	        
	        Object[] params1 = new Object[]{params};
	        result = (String) client.execute("updateRecord", params1);
	        System.out.println("updateRecord >>: " + result);
 
    	} catch (XmlRpcException exception) {
    		System.err.println("JavaClient: XML-RPC Fault #" +
                           		Integer.toString(exception.code) + ": " +
                           		exception.toString());
    	} catch (Exception exception) {
    		System.err.println("JavaClient: " + exception.toString());
    	}
        
    }

    public static void deleteRecord(XmlRpcClient client){

    	try{
    		
	        HashMap<String, String> params = new HashMap<String, String>();
	        params.put("collection", "sample");
	        params.put("database", "dbtest");
	        params.put("mfn","1");
	        
	        Object[] params1 = new Object[]{params};
	        result = (String) client.execute("deleteRecord", params1);
	        System.out.println("deleteRecord >>: " + result);
 
    	} catch (XmlRpcException exception) {
    		System.err.println("JavaClient: XML-RPC Fault #" +
                           		Integer.toString(exception.code) + ": " +
                           		exception.toString());
    	} catch (Exception exception) {
    		System.err.println("JavaClient: " + exception.toString());
    	}
    }    
    
    public static void readRecord(XmlRpcClient client){

    	try{
    		
	        HashMap<String, String> params = new HashMap<String, String>();
	        params.put("collection", "sample");
	        params.put("database", "dbtest");
	        params.put("mfn","1");
	        
	        Object[] params1 = new Object[]{params};
	        result = (String) client.execute("readRecord", params1);
	        System.out.println("readRecord >>: " + result);
 
    	} catch (XmlRpcException exception) {
    		System.err.println("JavaClient: XML-RPC Fault #" +
                           		Integer.toString(exception.code) + ": " +
                           		exception.toString());
    	} catch (Exception exception) {
    		System.err.println("JavaClient: " + exception.toString());
    	}
    }    
    
    
}

