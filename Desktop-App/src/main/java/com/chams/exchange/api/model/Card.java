package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class Card {

    @SerializedName("card_number")
    public String cardNumber;
    @SerializedName("month")
    public String month;

    @SerializedName("year")
    public String year;

    @SerializedName("cvv")
    public String cvv;

    public Card(String cardNumber, String month, String year, String cvv){
        this.cardNumber = cardNumber;
        this.month = month;
        this.year = year;
        this.cvv = cvv;
    }


}
