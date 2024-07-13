module com.chams.exchange {
    requires javafx.controls;
    requires javafx.fxml;
    requires retrofit2;
    requires java.sql;
    requires gson;
    requires retrofit2.converter.gson;
    requires java.prefs;
    exports com.chams.exchange;
    exports com.chams.exchange.rates;
    exports com.chams.exchange.login;
    exports com.chams.exchange.moreInfo;
    exports com.chams.exchange.profile;
    exports com.chams.exchange.balance;
    opens com.chams.exchange to javafx.fxml;
    opens com.chams.exchange.rates to javafx.fxml;
    opens com.chams.exchange.login to javafx.fxml;
    opens com.chams.exchange.register to javafx.fxml;
    opens com.chams.exchange.transactions to javafx.fxml;
    opens com.chams.exchange.profile to javafx.fxml;
    opens com.chams.exchange.moreInfo to javafx.fxml;
    opens com.chams.exchange.balance to javafx.fxml;
    exports com.chams.exchange.api.model;
    opens com.chams.exchange.api.model to gson, javafx.base, javafx.fxml;
}