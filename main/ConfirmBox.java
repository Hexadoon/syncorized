
import javafx.scene.*;
import javafx.stage.*;
import javafx.scene.layout.*;
import javafx.scene.control.*;
import javafx.geometry.*;


public class ConfirmBox {

    static boolean value;

    public static boolean display(String title, String message){
        Stage window = new Stage();
        window.initModality(Modality.APPLICATION_MODAL); //block user interaction with other windows 

        window.setTitle(title);
        window.setMinWidth(250);

        Label label = new Label();
        label.setText(message);

        Button yesButton = new Button("Yes");
        Button noButton = new Button("No");

        yesButton.setOnAction(e -> {
            value = true;
            window.close();
        });
        noButton.setOnAction(e -> {
            value = false;
            window.close();
        });

        VBox layout = new VBox(10);
        layout.setPadding(new Insets(10, 0, 10, 0));
        layout.getChildren().addAll(label, yesButton,noButton);
        layout.setAlignment(Pos.CENTER);

        Scene scene = new Scene(layout);
        window.setScene(scene);
        window.showAndWait();

        return value;
    }
}