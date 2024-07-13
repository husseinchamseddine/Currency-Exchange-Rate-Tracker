package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class setDate {

    @SerializedName("start_date")
    public String startDate;

    @SerializedName("end_date")
    public String endDate;

    public setDate(String s, String e){
        this.startDate = s;
        this.endDate = e;
    }

}
