package org.fmi.aq.addons2.development;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author johanssl
 */
public class EnfuserAPI {
   
    
   public static void main(String[] args) {
       double lat = 60.2;//example coordinates
       double lon = 25.0;
       
       String user = "";//add your user name here.
       String password = "";//add your password here.
       String token = fetchAccessToken(user, password);

       String date1 = "2025-02-28T12:00:00Z";//example time span
       String date2 = "2025-02-28T14:00:00Z";
       try {
           String resp = fetchResponse(token,lat, lon, date1, date2);
           System.out.println(resp);
           
       } catch (Exception ex) {
           Logger.getLogger(EnfuserAPI.class.getName()).log(Level.SEVERE, null, ex);
       } 
   } 
   
   /**
    * Make a query for Enfuser point service API for the given time span and location.
    * @param token your access token
    * @param lat latitude coordinate
    * @param lon longitude coordinate
    * @param date1 optional start time (if null then 'now' is used as default)
    * @param date2 optional end time (if start time is null then this should also
    * be null)
    * @return String JSON response
    * @throws Exception something went wrong
    */
    public static String fetchResponse(String token, double lat, double lon,
            String date1, String date2) throws Exception {
        String address = "https://enfuser-portal.2.rahtiapp.fi/enfuser/point-data?lat="
                +lat+"&lon="+lon;
        if (date1!=null) address+=  "&startTime="+date1;
        if (date2!=null) address+=  "&endTime="+date2;
        
        System.out.println("Opening connection to "+address);
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
        .GET()
        .uri(new URI(address))
        .header("Authorization","Bearer "+token)
        .build();
        
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println("Status code: "+ response.statusCode());
        return response.body();
} 
   
   /**
    * Fetch access token from Enfuser point service API using your user name
    * and password.
    * @param user username
    * @param pwd password
    * @return temporary access token information as JSON
    */ 
   public static String fetchAccessToken(String user, String pwd) {
        try {
            System.out.println("Fetching access token...");
            // URL for the request             
            URL url = new URL(" https://epk.2.rahtiapp.fi/realms/enfuser-portal/protocol/openid-connect/token");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();// Create a connection object
            connection.setRequestMethod("POST");// Set the request method to POST
            // Set headers
            connection.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            connection.setDoOutput(true);
            // Prepare the data for the body
            String requestBody = "grant_type=password" +
                                 "&username=" + user +
                                 "&password=" + pwd +
                                 "&client_id=point-service";
            // Send the request body
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = requestBody.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }
            // Get the response code
            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);
            
            // Read the response
            BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) response.append(line);
            reader.close();
            // Print the response as a String
            String responseString = response.toString();
            connection.disconnect();
            
            //parse
            ObjectMapper objectMapper = new ObjectMapper();   
            Map<String, Object> map = objectMapper.readValue(responseString,new TypeReference<Map<String,Object>>(){});
            String token = map.get("access_token").toString();
            System.out.println("Access token fetched.");
            return token;
           
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    } 
    
    
}