package com.chams.exchange.api.model;
import com.google.gson.annotations.SerializedName;

import java.util.List;

public class ExchangeRates {
    @SerializedName("usd_to_lbp")
    public Float usdToLbp;
    @SerializedName("lbp_to_usd")
    public Float lbpToUsd;

}


