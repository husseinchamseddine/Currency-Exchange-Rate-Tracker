package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class Balances {

    @SerializedName("usd_balance")
    public Float usdbalance;
    @SerializedName("lbp_balance")
    public Float lbpbalance;

    @SerializedName("amount")
    public Float amount;

    @SerializedName("usd_or_lbp")
    public String usdOrLbp;

    public Balances(Float amount, String usdOrLbp){
        this.amount = amount;
        this.usdOrLbp = usdOrLbp;
    }

}
