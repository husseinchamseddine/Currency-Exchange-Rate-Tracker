package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class totalAmounts {

    @SerializedName("total_usd_amount_exchanged")
    public Float totalUSDAmount;
    @SerializedName("total_lbp_amount_exchanged")
    public Float totalLBPAmount;

}
