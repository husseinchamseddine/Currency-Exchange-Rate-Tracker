package com.chams.exchange.api.model;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
public class APIClient {
    private static final String BASE_URL = "http://127.0.0.1:5000"; // Replace this with your actual backend URL

    public static void fetchMinMaxRates() {
        try {
            URL url = new URL(BASE_URL + "/Statistics/MinMaxRates");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String line;
                StringBuilder response = new StringBuilder();
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                reader.close();

                // Handle the response here
                System.out.println("Response: " + response.toString());
            } else {
                // Handle unsuccessful response
                System.err.println("Failed to fetch min-max rates. Response code: " + responseCode);
            }
        } catch (IOException e) {
            e.printStackTrace();
            // Handle IO exception
        }
    }
}
