package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class SD {

    @SerializedName("usd_buy_rate_standard_deviation")
    public Float usdBuySD;
    @SerializedName("usd_sell_rate_standard_deviation")
    public Float usdSellSD;
    @SerializedName("usd_buy_rate_average")
    public Float usdBuyAverage;
    @SerializedName("usd_sell_rate_average")
    public Float usdSellAverage;


}
