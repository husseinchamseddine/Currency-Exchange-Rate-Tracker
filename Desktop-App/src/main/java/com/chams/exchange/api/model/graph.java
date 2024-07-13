package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

import java.util.List;

public class graph {

    @SerializedName("usd_buy_rates")
    public List<Float> usdBuyRates;
    @SerializedName("usd_buy_dates")
    public List<String> usdBuyDates;
    @SerializedName("usd_sell_rates")
    public List<Float> usdSellRates;
    @SerializedName("usd_sell_dates")
    public List<String> usdSellDates;

    @SerializedName("start_date")
    public String startDate = null;

    @SerializedName("end_date")
    public String endDate = null;

    public graph(String s, String e){
        this.startDate = s;
        this.endDate = e;
    }

}
