package com.chams.exchange.register;

import com.chams.exchange.api.model.Authentication;
import com.chams.exchange.OnPageCompleteListener;
import com.chams.exchange.PageCompleter;
import com.chams.exchange.api.ExchangeService;
import com.chams.exchange.api.model.Token;
import com.chams.exchange.api.model.User;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.scene.control.TextField;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class Register implements PageCompleter {
    public TextField usernameTextField;
    public TextField passwordTextField;
    public TextField emailTextField;
    private OnPageCompleteListener onPageCompleteListener;

    public void setOnPageCompleteListener(OnPageCompleteListener onPageCompleteListener) {
        this.onPageCompleteListener = onPageCompleteListener;
    }
    public void register(ActionEvent actionEvent) {
        User user = new User();
        user.username = usernameTextField.getText();
        user.password = passwordTextField.getText();
        user.email = emailTextField.getText();

        ExchangeService.exchangeApi().addUser(user).enqueue(new Callback<User>() {
            @Override
            public void onResponse(Call<User> call, Response<User> response) {
                ExchangeService.exchangeApi().authenticate(user).enqueue(new Callback<Token>() {
                     @Override
                     public void onResponse(Call<Token> call, Response<Token> response) {
                         if (response.isSuccessful() && response.body() != null) {
                             Authentication.getInstance().saveToken(response.body().getToken());
                             Platform.runLater(() -> {
                                 onPageCompleteListener.onPageCompleted();
                             });
                         } else {
                            System.out.println("x");
                             // Handle unsuccessful response
                             // For example, log an error message or inform the user
                         }
                     }
                     @Override
                     public void onFailure(Call<Token> call, Throwable
                             throwable) {
                     }
                 });
}
            @Override
            public void onFailure(Call<User> call, Throwable throwable) {
            }
        });
    }
}