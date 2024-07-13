package com.chams.exchange.balance;

import com.chams.exchange.api.ExchangeService;
import com.chams.exchange.api.model.*;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.scene.control.Label;
import javafx.scene.control.RadioButton;
import javafx.scene.control.TextField;
import javafx.scene.control.ToggleGroup;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class Balance {


    public Label usdBalance;
    public Label lbpBalance;

    public TextField addedBalance;
    public TextField currencyType;
    public TextField numberInput;
    public TextField monthInput;
    public TextField yearInput;
    public TextField cvvInput;
    public TextField moneyTransaction;
    public TextField transactionType;
    public TextField userEmail;
    public TextField transactionID;
    public ToggleGroup toggle;


    public void initialize() {
        fetchBalance();
    }

    public void fetchBalance() {
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().fetchBalance(authHeader).enqueue(new Callback<Balances>() {
            @Override
            public void onResponse(Call<Balances> call, Response<Balances> response) {
                Balances balances = response.body();
                if (balances != null) {
                    // Update UI with the fetched min-max rates data
                    Platform.runLater(() -> {
                        // Update UI labels with the fetched data
                        // Replace these with actual labels in your FXML file

                        // Max USD Buy Rate
                        if (balances.usdbalance != null) {
                            usdBalance.setText(balances.usdbalance.toString());
                        }
                        if (balances.lbpbalance != null) {
                            lbpBalance.setText(balances.lbpbalance.toString());
                        }
                    });
                } else {
                    System.err.println("Response body is null.");
                }
            }


            @Override
            public void onFailure(Call<Balances> call, Throwable t) {
                System.err.println("Failed to fetch min-max rates: " + t.getMessage());
            }
        });
    }

    public void addBalance(ActionEvent actionEvent) {
        Balances PD = new Balances(Float.parseFloat(addedBalance.getText()), currencyType.getText());
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().addBalance(PD, authHeader).enqueue(new Callback<Balances>() {
            @Override
            public void onResponse(Call<Balances> call, Response<Balances> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        fetchBalance();
                        addedBalance.setText("");
                        currencyType.setText("");
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed to add transaction: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<Balances> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });

    }



    public void transfer(ActionEvent actionEvent) {
        sendTransaction PD = new sendTransaction(userEmail.getText(), Float.parseFloat(moneyTransaction.getText()), transactionType.getText());
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().transfer(PD, authHeader).enqueue(new Callback<sendTransaction>() {
            @Override
            public void onResponse(Call<sendTransaction> call, Response<sendTransaction> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        fetchBalance();
                        moneyTransaction.setText("");
                        transactionType.setText("");
                        userEmail.setText("");
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("We are Here: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<sendTransaction> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });


    }

    public void receive(ActionEvent actionEvent) {

        boolean isAccepted = ((RadioButton) toggle.getSelectedToggle()).getText().equals("Accept");
        acceptTransaction PD = new acceptTransaction(transactionID.getText(), isAccepted);
        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().receive(PD, authHeader).enqueue(new Callback<acceptTransaction>() {
            @Override
            public void onResponse(Call<acceptTransaction> call, Response<acceptTransaction> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        fetchBalance();
                        transactionID.setText("");
                        transactionType.setText("");
                        userEmail.setText("");
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed to add transaction: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<acceptTransaction> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });


    }


}

