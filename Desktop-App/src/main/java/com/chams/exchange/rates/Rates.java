package com.chams.exchange.rates;

import com.chams.exchange.api.model.Authentication;

import com.chams.exchange.api.ExchangeService;
import com.chams.exchange.api.model.*;
import javafx.event.ActionEvent;

import javafx.scene.control.*;

import javafx.fxml.FXML;
import javafx.application.Platform;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;


public class Rates {
    @FXML
    public Label buyUsdRateLabel;
    @FXML
    public Label sellUsdRateLabel;
    @FXML
    public TextField lbpTextField;
    @FXML
    public TextField usdTextField;
    @FXML
    public ToggleGroup transactionType;
    public Label predictedRate;

    public TextField inputDate;

    @FXML
    private RadioButton usdToLbpRadio;


    @FXML
    private TextField amountField;


    @FXML
    private Label resultLabel;




    @FXML
    private void calculate(ActionEvent event) {
        RadioButton selectedRadioButton = (RadioButton) transactionType.getSelectedToggle();

        if (selectedRadioButton != null) {
            boolean isUsdtoLbp = selectedRadioButton == usdToLbpRadio;

            // Retrieve the amount from the text field
            float amount = 0.0f;
            try {
                amount = Float.parseFloat(amountField.getText());
            } catch (NumberFormatException e) {
                // Handle invalid input gracefully
                System.err.println("Invalid amount input: " + e.getMessage());
                return;
            }

            // Retrieve the appropriate exchange rate based on the selected conversion direction
            float exchangeRate = isUsdtoLbp ? Float.parseFloat(sellUsdRateLabel.getText()) :
                    Float.parseFloat(buyUsdRateLabel.getText());

            // Perform the currency conversion calculation
            float result = isUsdtoLbp ? amount * exchangeRate : amount / exchangeRate;

            // Update the result label with the calculated value
            resultLabel.setText(String.valueOf(result));
        }
    }


    public void initialize() {
        fetchRates();
    }

    private void fetchRates() {
        ExchangeService.exchangeApi().getExchangeRates().enqueue(new Callback<ExchangeRates>() {
            @Override
            public void onResponse(Call<ExchangeRates> call, Response<ExchangeRates> response) {
                ExchangeRates exchangeRates = response.body();
                Platform.runLater(() -> {
                    if (exchangeRates != null && exchangeRates.lbpToUsd != null) {
                        buyUsdRateLabel.setText(exchangeRates.lbpToUsd.toString());
                    }
                    if (exchangeRates != null && exchangeRates.usdToLbp != null) {
                        sellUsdRateLabel.setText(exchangeRates.usdToLbp.toString());
                    }


                });
            }

            @Override
            public void onFailure(Call<ExchangeRates> call, Throwable throwable) {
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });
    }

    @FXML
    public void addTransaction(ActionEvent actionEvent) {
        boolean isSellUsd = ((RadioButton) transactionType.getSelectedToggle()).getText().equals("Sell USD");

        Transaction transaction = new Transaction(
                Float.parseFloat(usdTextField.getText()),
                Float.parseFloat(lbpTextField.getText()),
                isSellUsd
        );

        String userToken = Authentication.getInstance().getToken();
        String authHeader = userToken != null ? "Bearer " + userToken : null;
        ExchangeService.exchangeApi().addTransaction(transaction, authHeader).enqueue(new Callback<Object>() {
            @Override
            public void onResponse(Call<Object> call, Response<Object> response) {
                if (response.isSuccessful()) {
                    fetchRates();
                    Platform.runLater(() -> {
                        usdTextField.setText("");
                        lbpTextField.setText("");
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed to add transaction: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<Object> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed to add transaction: " + throwable.getMessage());
            }
        });
    }



    public void predict(ActionEvent actionEvent) {
        MLModel PD = new MLModel(inputDate.getText());

        ExchangeService.exchangeApi().predict(PD).enqueue(new Callback<MLModel>() {
            @Override
            public void onResponse(Call<MLModel> call, Response<MLModel>
                    response) {
                ExchangeService.exchangeApi().getPrediction(PD).enqueue(new Callback<PredictionResponse>() {
                    @Override
                    public void onResponse(Call<PredictionResponse> call, Response<PredictionResponse> response) {
                        if (response.isSuccessful() && response.body() != null) {

                            Platform.runLater(() -> {
                                predictedRate.setText(response.body().getPredictedRate().toString());
                                inputDate.setText("");
                            });
                        } else {
                            System.out.println("Error");
                        }
                    }

                    @Override
                    public void onFailure(Call<PredictionResponse> call, Throwable
                            throwable) {
                    }
                });
            }

            @Override
            public void onFailure(Call<MLModel> call, Throwable throwable) {
            }
        });

    }
}
