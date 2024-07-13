package com.chams.exchange.api.model;
import com.google.gson.annotations.SerializedName;

public class MLModel {

    @SerializedName("date")
    String date;

    public MLModel(String date){
        this.date = date;
    }

}
