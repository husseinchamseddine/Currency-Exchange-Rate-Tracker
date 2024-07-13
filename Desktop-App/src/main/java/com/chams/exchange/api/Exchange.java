package com.chams.exchange.api;

import com.chams.exchange.api.model.*;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.Header;
import retrofit2.http.POST;

import java.util.List;

public interface Exchange {
    @POST("/create-user")
    Call<User> addUser(@Body User user);

    @POST("/authentication")
    Call<Token> authenticate(@Body User user);

    @GET("/fetch-exchange-rate")
    Call<ExchangeRates> getExchangeRates();
    @POST("/transaction")
    Call<Object> addTransaction(@Body Transaction transaction,
                                @Header("Authorization") String authorization);
    @GET("/transaction")
    Call<List<Transaction>> getTransactions(@Header("Authorization")
                                            String authorization);

    @GET("/statistics/min-max-rates")
    Call<minMax> getMinMaxRates();

    @GET("/statistics/std-avg")
    Call<SD> getSDAverage();

    @GET("/statistics/total-amount-exchanged")
    Call<totalAmounts> getTotalAmounts();

    @POST("/fluctuation-graph")
    Call<graph> getGraph(@Body graph d);

    @POST("/predict-rate")
    Call<MLModel> predict(@Body MLModel date);

    @POST("/predict-rate")
    Call<PredictionResponse> getPrediction(@Body MLModel date);

    @GET("/fetch-balance")
    Call<Balances> fetchBalance(@Header("Authorization") String authorization);

    @POST("/add-balance")
    Call<Balances> addBalance(@Body Balances add, @Header("Authorization") String authorization);

    @POST("/add-credit-card")
    Call<Card> addCard(@Body Card card, @Header("Authorization") String authorization);

    @POST("/send-transaction-to-user")
    Call<sendTransaction> transfer(@Body sendTransaction money, @Header("Authorization") String authorization);

    @POST("/accept-decline-transaction")
    Call<acceptTransaction> receive(@Body acceptTransaction money, @Header("Authorization") String authorization);

    @GET("/fetch-email")
    Call<Email> fetchEmail(@Header("Authorization") String authorization);

    @POST("/change-password")
    Call<changePassword> changeP(@Body changePassword password, @Header("Authorization") String authorization);

    @POST("/change-email")
    Call<Email> changeE(@Body Email email, @Header("Authorization") String authorization);

    @POST("/change-credit-card")
    Call<changeCard> changeC(@Body changeCard card, @Header("Authorization") String authorization);

    @POST("/set-date-range")
    Call<setDate> scale(@Body setDate date);
}