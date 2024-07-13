package com.chams.exchange.transactions;

import com.chams.exchange.api.model.Authentication;
import com.chams.exchange.api.ExchangeService;
import com.chams.exchange.api.model.Transaction;
import javafx.fxml.Initializable;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import java.net.URL;
import java.util.List;
import java.util.ResourceBundle;
public class Transactions implements Initializable {

    public TableColumn<Transaction, Long> lbpAmount;
    public TableColumn<Transaction, Long> usdAmount;
    public TableColumn<Transaction, String> transactionDate;
    public TableView<Transaction> tableView;

    @Override
    public void initialize(URL url, ResourceBundle resourceBundle) {
        lbpAmount.setCellValueFactory(new PropertyValueFactory<>("lbpAmount"));
        usdAmount.setCellValueFactory(new PropertyValueFactory<>("usdAmount"));
        transactionDate.setCellValueFactory(new PropertyValueFactory<>("addedDate"));

        ExchangeService.exchangeApi().getTransactions("Bearer " +
                        Authentication.getInstance().getToken()).enqueue(new Callback<>() {
                    @Override
                    public void onResponse(Call<List<Transaction>> call,
                                           Response<List<Transaction>> response) {
                        tableView.getItems().setAll(response.body());
                    }
                    @Override
                    public void onFailure(Call<List<Transaction>> call,
                                          Throwable throwable) {
                    }
                });
    }
}