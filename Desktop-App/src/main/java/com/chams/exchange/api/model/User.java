package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class User {
    @SerializedName("id")
    Integer id;
    @SerializedName("user_name")
    public String username;
    @SerializedName("password")
    public String password;
    @SerializedName("email")
    public String email;


}


