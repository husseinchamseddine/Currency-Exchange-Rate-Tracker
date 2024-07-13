package com.chams.exchange.moreInfo;

import com.chams.exchange.api.Exchange;
import com.chams.exchange.api.ExchangeService;
import com.chams.exchange.api.model.*;
import javafx.fxml.FXML;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Label;
import javafx.application.Platform;
import javafx.scene.control.TextField;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

import java.util.List;

public class MoreInfoController {

    public TextField startDate;
    public TextField endDate;
    public TextField startGraph;
    public TextField endGraph;
    @FXML
    private LineChart<Number, Number> exchangeRateChart;



    @FXML
    private Label maxUsdBuyRateLabel;

    @FXML
    private Label maxUsdBuyDateLabel;

    @FXML
    private Label maxUsdSellRateLabel;

    @FXML
    private Label maxUsdSellDateLabel;

    @FXML
    private Label minUsdBuyRateLabel;

    @FXML
    private Label minUsdBuyDateLabel;

    @FXML
    private Label minUsdSellRateLabel;

    @FXML
    private Label minUsdSellDateLabel;

    @FXML
    private Label buyRateSDLabel;
    @FXML
    private Label sellRateSDLabel;
    @FXML
    private Label usdBuyAverageLabel;
    @FXML
    private Label usdSellAverageLabel;
    @FXML
    private Label totalUSDLabel;
    @FXML
    private Label totalLBPLabel;


    @FXML
    private LineChart<String, Number> buyChart;

    @FXML
    private LineChart<String, Number> sellChart;

    public void initialize() {

    }

    public void scale(){
        setDate date = new setDate(startDate.getText(),endDate.getText());

        ExchangeService.exchangeApi().scale(date).enqueue(new Callback<setDate>() {
            @Override
            public void onResponse(Call<setDate> call, Response<setDate> response) {
                if (response.isSuccessful() && response.body() != null) {

                    Platform.runLater(() -> {
                        fetchMinMaxRates();
                        fetchSDAverage();
                        fetchTotalAmounts();
                    });
                } else {
                    // Handle unsuccessful response
                    System.err.println("Failed: " + response.message());
                }
            }

            @Override
            public void onFailure(Call<setDate> call, Throwable throwable) {
                // Handle failure
                System.err.println("Failed: " + throwable.getMessage());
            }
        });
    }


    public void fetchMinMaxRates() {

        ExchangeService.exchangeApi().getMinMaxRates().enqueue(new Callback<minMax>() {
            @Override
            public void onResponse(Call<minMax> call, Response<minMax> response) {
                minMax exchangeRates = response.body();
                if (exchangeRates != null) {
                    // Update UI with the fetched min-max rates data
                    Platform.runLater(() -> {
                        // Update UI labels with the fetched data
                        // Replace these with actual labels in your FXML file

                        // Max USD Buy Rate
                        if (exchangeRates.maxUsdBuy != null) {
                            maxUsdBuyRateLabel.setText(exchangeRates.maxUsdBuy.toString());
                        } else {
                            maxUsdBuyRateLabel.setText("N/A"); // or any default value you want to show
                        }
                        maxUsdBuyDateLabel.setText(exchangeRates.maxUsdBuyDate != null ? exchangeRates.maxUsdBuyDate : "N/A");

                        // Max USD Sell Rate
                        if (exchangeRates.maxUsdSell != null) {
                            maxUsdSellRateLabel.setText(exchangeRates.maxUsdSell.toString());
                        } else {
                            maxUsdSellRateLabel.setText("N/A");
                        }
                        maxUsdSellDateLabel.setText(exchangeRates.maxUsdSellDate != null ? exchangeRates.maxUsdSellDate : "N/A");

                        // Min USD Buy Rate
                        if (exchangeRates.minUsdBuy != null) {
                            minUsdBuyRateLabel.setText(exchangeRates.minUsdBuy.toString());
                        } else {
                            minUsdBuyRateLabel.setText("N/A");
                        }
                        minUsdBuyDateLabel.setText(exchangeRates.minUsdBuyDate != null ? exchangeRates.minUsdBuyDate : "N/A");

                        // Min USD Sell Rate
                        if (exchangeRates.minUsdSell != null) {
                            minUsdSellRateLabel.setText(exchangeRates.minUsdSell.toString());
                        } else {
                            minUsdSellRateLabel.setText("N/A");
                        }
                        minUsdSellDateLabel.setText(exchangeRates.minUsdSellDate != null ? exchangeRates.minUsdSellDate : "N/A");
                    });
                } else {
                    System.err.println("Response body is null.");
                }
            }


            @Override
            public void onFailure(Call<minMax> call, Throwable t) {
                System.err.println("Failed to fetch min-max rates: " + t.getMessage());
            }
        });
    }

    public void fetchSDAverage(){
        ExchangeService.exchangeApi().getSDAverage().enqueue(new Callback<SD>() {
            @Override
            public void onResponse(Call<SD> call, Response<SD> response) {
                SD exchangeRates = response.body();
                if (exchangeRates != null) {
                    // Update UI with the fetched min-max rates data
                    Platform.runLater(() -> {
                        // Update UI labels with the fetched data
                        // Replace these with actual labels in your FXML file

                        // Max USD Buy Rate
                        if (exchangeRates.usdBuySD != null) {
                            buyRateSDLabel.setText(exchangeRates.usdBuySD.toString());
                        } else {
                            buyRateSDLabel.setText("N/A"); // or any default value you want to show
                        }

                        // Max USD Sell Rate
                        if (exchangeRates.usdSellSD != null) {
                            sellRateSDLabel.setText(exchangeRates.usdSellSD.toString());
                        } else {
                            sellRateSDLabel.setText("N/A");
                        }

                        // Min USD Buy Rate
                        if (exchangeRates.usdBuyAverage != null) {
                            usdBuyAverageLabel.setText(exchangeRates.usdBuyAverage.toString());
                        } else {
                            usdBuyAverageLabel.setText("N/A");
                        }

                        // Min USD Sell Rate
                        if (exchangeRates.usdSellAverage != null) {
                            usdSellAverageLabel.setText(exchangeRates.usdSellAverage.toString());
                        } else {
                            usdSellAverageLabel.setText("N/A");
                        }
                    });
                } else {
                    System.err.println("Response body is null.");
                }
            }


            @Override
            public void onFailure(Call<SD> call, Throwable t) {
                System.err.println("Failed to Standard Deviation & Average rates: " + t.getMessage());
            }
        });
    }

    public void fetchTotalAmounts(){
        ExchangeService.exchangeApi().getTotalAmounts().enqueue(new Callback<totalAmounts>() {
            @Override
            public void onResponse(Call<totalAmounts> call, Response<totalAmounts> response) {
                totalAmounts exchangeRates = response.body();
                if (exchangeRates != null) {
                    // Update UI with the fetched min-max rates data
                    Platform.runLater(() -> {
                        // Update UI labels with the fetched data
                        // Replace these with actual labels in your FXML file

                        // Max USD Buy Rate
                        if (exchangeRates.totalUSDAmount != null) {
                            totalUSDLabel.setText(exchangeRates.totalUSDAmount.toString());
                        } else {
                            totalUSDLabel.setText("N/A"); // or any default value you want to show
                        }

                        // Max USD Sell Rate
                        if (exchangeRates.totalLBPAmount != null) {
                            totalLBPLabel.setText(exchangeRates.totalLBPAmount.toString());
                        } else {
                            totalLBPLabel.setText("N/A");
                        }

                    });
                } else {
                    System.err.println("Response body is null.");
                }
            }


            @Override
            public void onFailure(Call<totalAmounts> call, Throwable t) {
                System.err.println("Failed to fetch Standard Deviation & Average rates: " + t.getMessage());
            }
        });
    }

    public void fetchGraph(){

        graph d = new graph(startGraph.getText(), endGraph.getText());

        ExchangeService.exchangeApi().getGraph(d).enqueue(new Callback<graph>() {
            @Override
            public void onResponse(Call<graph> call, Response<graph> response) {
                graph exchangeRates = response.body();
                if (exchangeRates != null) {
                    Platform.runLater(() -> {
                        List<Float> buyRates = exchangeRates.usdBuyRates;
                        List<Float> sellRates = exchangeRates.usdSellRates;
                        List<String> buyDates = exchangeRates.usdBuyDates;
                        List<String> sellDates = exchangeRates.usdSellDates;

                        // Clear existing data
                        buyChart.getData().clear();
                        sellChart.getData().clear();

                        // Add data series for buy and sell rates to respective charts
                        addSeriesToChart(buyChart, buyDates, buyRates, "USD Buy Rate");
                        addSeriesToChart(sellChart, sellDates, sellRates, "USD Sell Rate");
                    });
                } else {
                    System.err.println("Response body is null.");
                }
            }

            @Override
            public void onFailure(Call<graph> call, Throwable t) {
                System.err.println("Failed to fetch the Graph: " + t.getMessage());
            }
        });
    }

    private void addSeriesToChart(LineChart<String, Number> chart, List<String> dates, List<Float> rates, String seriesName) {
        XYChart.Series<String, Number> series = new XYChart.Series<>();
        series.setName(seriesName);

        // Add data to the series
        for (int i = 0; i < dates.size(); i++) {
            String dateString = dates.get(i);
            Float rate = rates.get(i);

            // Directly use the date string as the x-value
            series.getData().add(new XYChart.Data<>(dateString, rate));
        }

        // Add series to the chart
        chart.getData().add(series);
    }




}