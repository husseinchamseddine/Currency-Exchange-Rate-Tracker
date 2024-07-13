package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class changeCard {

    @SerializedName("new_card_number")
    public String cardNumber;
    @SerializedName("new_month")
    public String month;

    @SerializedName("new_year")
    public String year;

    @SerializedName("new_cvv")
    public String cvv;

    public changeCard(String cardNumber, String month, String year, String cvv){
        this.cardNumber = cardNumber;
        this.month = month;
        this.year = year;
        this.cvv = cvv;
    }


}
