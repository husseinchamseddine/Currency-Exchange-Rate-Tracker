package com.chams.exchange.api.model;
import com.google.gson.annotations.SerializedName;

public class PredictionResponse {

    @SerializedName("predicted_rate")
    public Float predictedRates;

    public Float getPredictedRate() {
        return predictedRates;
    }

}
