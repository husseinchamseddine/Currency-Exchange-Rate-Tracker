package com.chams.exchange.profile;

import com.chams.exchange.api.ExchangeService;
import com.chams.exchange.api.model.*;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ProfileController {


    public Label userEmail;
    public TextField oldPassword;
    public TextField newPassword;
    public TextField confirmPassword;
    public TextField newEmail;
    public TextField numberInput;
    public TextField monthInput;
    public TextField yearInput;
    public TextField cvvInput;

    public void initialize(){
        fetchEmail();
    }

    public void fetchEmail(){
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().fetchEmail(authHeader).enqueue(new Callback<Email>() {

            @Override
            public void onResponse(Call<Email> call, Response<Email> response) {
                Email email = response.body();
                if (email != null) {

                    Platform.runLater(() -> {

                        if (email.email != null) {
                            userEmail.setText(email.email);
                        }

                    });
                } else {
                    System.err.println("Response body is null.");
                }
            }


            @Override
            public void onFailure(Call<Email> call, Throwable t) {
                System.err.println("Failed to fetch: " + t.getMessage());
            }
        });
    }

    public void changeE(){
        Email PD = new Email(newEmail.getText());
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().changeE(PD, authHeader).enqueue(new Callback<Email>() {
            @Override
            public void onResponse(Call<Email> call, Response<Email> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        fetchEmail();
                        newEmail.setText("");
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed to add transaction: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<Email> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });

    }


    public void changeP(){
        changePassword PD = new changePassword(oldPassword.getText(), newPassword.getText(), confirmPassword.getText());
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().changeP(PD, authHeader).enqueue(new Callback<changePassword>() {
            @Override
            public void onResponse(Call<changePassword> call, Response<changePassword> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        oldPassword.setText("");
                        newPassword.setText("");
                        confirmPassword.setText("");

                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed to add transaction: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<changePassword> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });

    }

    public void addCard(ActionEvent actionEvent) {
        Card PD = new Card(numberInput.getText(), monthInput.getText(), yearInput.getText(), cvvInput.getText());
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().addCard(PD, authHeader).enqueue(new Callback<Card>() {
            @Override
            public void onResponse(Call<Card> call, Response<Card> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        numberInput.setText("");
                        monthInput.setText("");
                        yearInput.setText("");
                        cvvInput.setText("");
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed to add transaction: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<Card> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });


    }

    public void changeC(ActionEvent actionEvent) {
        changeCard PD = new changeCard(numberInput.getText(), monthInput.getText(), yearInput.getText(), cvvInput.getText());
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().changeC(PD, authHeader).enqueue(new Callback<changeCard>() {
            @Override
            public void onResponse(Call<changeCard> call, Response<changeCard> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        numberInput.setText("");
                        monthInput.setText("");
                        yearInput.setText("");
                        cvvInput.setText("");
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed to add transaction: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<changeCard> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });


    }

}





