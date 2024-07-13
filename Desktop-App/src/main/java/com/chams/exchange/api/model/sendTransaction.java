package com.chams.exchange.api.model;
import com.google.gson.annotations.SerializedName;
public class sendTransaction {

    @SerializedName("email_of_recipient")
    public String email;

    @SerializedName("amount")
    public Float amount;

    @SerializedName("usd_or_lbp")
    public String usdOrLbp;

    public sendTransaction(String email, Float amount, String usdOrLbp){
        this.email = email;
        this.amount = amount;
        this.usdOrLbp = usdOrLbp;
    }



}
