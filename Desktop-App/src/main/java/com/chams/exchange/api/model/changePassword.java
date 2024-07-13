package com.chams.exchange.api.model;

import com.google.gson.annotations.SerializedName;

public class changePassword {


    @SerializedName("old_password")
    String oldPassword;

    @SerializedName("new_password")
    String newPassword;

    @SerializedName("confirm_password")
    String confirmPassword;

    public changePassword(String old, String pass, String confirm){
        this.oldPassword = old;
        this.newPassword = pass;
        this.confirmPassword = confirm;
    }


}
