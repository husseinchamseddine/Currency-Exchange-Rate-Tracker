package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class Email {

    @SerializedName("user_email")
    public String email;

    @SerializedName("new_email")
    public String newEmail;

    public Email(String newEmail){
        this.newEmail = newEmail;
    }


}
