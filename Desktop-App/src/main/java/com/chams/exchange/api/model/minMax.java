package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class minMax {

    @SerializedName("max_usd_buy_rate")
    public Float maxUsdBuy;
    @SerializedName("max_usd_buy_rate_date")
    public String maxUsdBuyDate;
    @SerializedName("max_usd_sell_rate")
    public Float maxUsdSell;
    @SerializedName("max_usd_sell_rate_date")
    public String maxUsdSellDate;
    @SerializedName("min_usd_buy_rate")
    public Float minUsdBuy;
    @SerializedName("min_usd_buy_rate_date")
    public String minUsdBuyDate;
    @SerializedName("min_usd_sell_rate")
    public Float minUsdSell;
    @SerializedName("min_usd_sell_rate_date")
    public String minUsdSellDate;



}
