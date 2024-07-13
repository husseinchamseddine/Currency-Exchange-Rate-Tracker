package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class acceptTransaction {


    @SerializedName("transaction_id")
    public String ID;

    @SerializedName("accept")
    public boolean accept;



    public acceptTransaction(String ID, boolean accept){
        this.ID = ID;
        this.accept = accept;
    }


}
