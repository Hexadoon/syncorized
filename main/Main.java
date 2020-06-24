import javafx.application.Application;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import java.awt.Color;
import java.awt.Desktop;
import java.io.IOException;
import javax.swing.text.StyledEditorKit.UnderlineAction;
import javax.swing.JProgressBar;
import javafx.event.*;
import javafx.geometry.HPos;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.*;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.control.Slider;
import javafx.scene.control.ColorPicker;
import javafx.scene.control.ProgressBar;
import javafx.scene.control.ProgressIndicator;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.StackPane;
import javafx.scene.layout.VBox;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import java.io.File;

public class Main extends Application{
    Stage window;
    Scene scene1;
    String song_address = "";
    String image_address = "";
    private Desktop desktop = Desktop.getDesktop();

    public static void main(String[] args){
        launch(args);
    }
    @Override
    public void start(Stage primaryStage) throws Exception {
        window = primaryStage;
       
        window.setTitle("Syncorized");

        window.setOnCloseRequest(e -> {
            e.consume();
            closeProgram();
        });

        GridPane grid = new GridPane();
        grid.setPadding(new Insets(10, 10, 10, 10));
        grid.setVgap(8); // vertical spacing
        grid.setHgap(10); // horizontal spacing

        Label title_name = new Label("Syncorized");
        GridPane.setConstraints(title_name, 0, 0, 4, 1);
        GridPane.setHalignment(title_name, HPos.LEFT);


        Label author = new Label("By Lyli, Sammy and Sujay");
        GridPane.setConstraints(author, 3, 0);

        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Resource File");

        Label input_label = new Label("Input File Here:");
        GridPane.setConstraints(input_label, 0, 1);

        Button openButton = new Button(".mp3 file");
        GridPane.setConstraints(openButton, 1, 1);

        openButton.setOnAction(e -> {
            Label file_address;
            File file = fileChooser.showOpenDialog(window);
            if(song_address != "" && file != null){
                try {
                    if(((Label)grid.getChildren().get(grid.getChildren().size()-1)).getText() == song_address){
                        grid.getChildren().remove(grid.getChildren().size()-1);
                    } 
                } catch (Exception ex) {
                }
            }
            
            if(file != null){
                return_song_address(file.getAbsolutePath());

                file_address = new Label(file.getAbsolutePath());
                GridPane.setConstraints(file_address, 0, 2, 2, 1);
                grid.getChildren().add(file_address);
            }
        });
        
        Label frame_rate_label = new Label("Frame rate");
        GridPane.setConstraints(frame_rate_label, 2, 1);

        TextField frame_rate_input = new TextField();
        frame_rate_input.setMaxWidth(35);
        frame_rate_input.setPromptText("24");
        GridPane.setConstraints(frame_rate_input, 3, 1);

        Label width_and_height = new Label("Width x Height");
        GridPane.setConstraints(width_and_height, 2, 2);

        TextField width_height_input = new TextField();
        width_height_input.setMaxWidth(85);
        width_height_input.setPromptText("1920x1080");
        GridPane.setConstraints(width_height_input, 3, 2);

        Label background_label = new Label("Background:");
        background_label.setUnderline(true);
        GridPane.setConstraints(background_label, 0, 3, 2, 1);

        CheckBox insert_image_label = new CheckBox("Insert Image");
        GridPane.setConstraints(insert_image_label, 0, 4);

        CheckBox select_color_label = new CheckBox("Select Color");
        GridPane.setConstraints(select_color_label, 1, 4);

        Button open_image_button = new Button(".jpg/.png file");
        GridPane.setConstraints(open_image_button, 0, 5);


        open_image_button.setOnAction(e -> {
            Label file_address;
            File file = fileChooser.showOpenDialog(window);
            if(image_address != "" && file != null){
                try {
                    if(((Label)grid.getChildren().get(grid.getChildren().size()-1)).getText() == image_address){
                        grid.getChildren().remove(grid.getChildren().size()-1);
                    } 
                } catch (Exception ex) {
                }
            }

            if(file != null){
                return_image_address(file.getAbsolutePath());
                file_address = new Label(file.getAbsolutePath());
                GridPane.setConstraints(file_address, 0, 6, 2, 1);
                grid.getChildren().add(file_address);
            }
            
        });

        ColorPicker colorPicker1 = new ColorPicker();
        GridPane.setConstraints(colorPicker1, 0, 5, 2, 1);

        insert_image_label.setOnAction(e->{
            if(insert_image_label.isSelected()){
                if(select_color_label.isSelected()){
                    grid.getChildren().remove(colorPicker1);
                }
                select_color_label.setSelected(false);
                grid.getChildren().add(open_image_button);
            }else{
                grid.getChildren().remove(open_image_button);
                try {
                    if(((Label)grid.getChildren().get(grid.getChildren().size()-1)).getText() == image_address){
                        image_address = "";
                        grid.getChildren().remove(grid.getChildren().size()-1);
                    } 
                } catch (Exception ex) {
                }
            }
        });

        select_color_label.setOnAction(e->{
            if(select_color_label.isSelected()){
                if(insert_image_label.isSelected()){
                    grid.getChildren().remove(open_image_button);
                    try {
                        if(((Label)grid.getChildren().get(grid.getChildren().size()-1)).getText() == image_address){
                            image_address = "";
                            grid.getChildren().remove(grid.getChildren().size()-1);
                        } 
                    } catch (Exception ex) {
                    }
                }
                insert_image_label.setSelected(false);
                grid.getChildren().add(colorPicker1);
            } else {
                grid.getChildren().remove(colorPicker1);
            }
        });

        Label color_of_bars_label = new Label("Color of bars:");
        GridPane.setConstraints(color_of_bars_label, 0, 7);

        ColorPicker color_of_bars = new ColorPicker();
        GridPane.setConstraints(color_of_bars, 1, 7);

        Label color_of_border_label = new Label("Color of border:");
        GridPane.setConstraints(color_of_border_label, 0, 8);

        ColorPicker color_of_border = new ColorPicker();
        GridPane.setConstraints(color_of_border, 1, 8);

        Label main_bar_label = new Label("Bar Customization:");
        main_bar_label.setUnderline(true);
        GridPane.setConstraints(main_bar_label, 2, 3, 2, 1);

        Label bar_label = new Label("Select bar type:");
        GridPane.setConstraints(bar_label, 2, 4);

        ChoiceBox<String> bar_types = new ChoiceBox<String>();
        bar_types.getItems().addAll("Fill" , "Clear");
        bar_types.setValue("Fill");
        
        GridPane.setConstraints(bar_types, 3, 4);

        Label layout_label = new Label("Select layout type:");
        GridPane.setConstraints(layout_label, 2, 5);

        ChoiceBox<String> layout_types = new ChoiceBox<String>();
        layout_types.getItems().addAll("Normal", "Circular");
        layout_types.setValue("Normal");
        GridPane.setConstraints(layout_types, 3, 5);

        Label width_of_border_label = new Label("Width of border");
        GridPane.setConstraints(width_of_border_label, 2, 6, 2, 1);
        GridPane.setHalignment(width_of_border_label, HPos.CENTER);

        Slider width_of_border_slider = new Slider(0,100,40);
        width_of_border_slider.setValue(40);
        width_of_border_slider.setShowTickLabels(true);
        width_of_border_slider.setShowTickMarks(true);
        width_of_border_slider.setMajorTickUnit(50);
        width_of_border_slider.setMinorTickCount(5);
        width_of_border_slider.setBlockIncrement(10);
        GridPane.setConstraints(width_of_border_slider, 2, 7, 2, 1);

        Label border_value = new Label(Integer.toString((int)width_of_border_slider.getValue()));
        GridPane.setConstraints(border_value, 3, 6);
        GridPane.setHalignment(border_value, HPos.RIGHT);

        ProgressBar pb = new ProgressBar(0);
        pb.setMinWidth(490);
        pb.setMinHeight(25);
        pb.setProgress(.5);
        GridPane.setConstraints(pb, 0, 10, 4, 3);

        ProgressIndicator progressIndicator = new ProgressIndicator();
        JProgressBar progressBar = new JProgressBar(0, 100);
        
        width_of_border_slider.valueProperty().addListener(e-> {
            border_value.setText(Integer.toString((int)width_of_border_slider.getValue()));
        });

        Label num_of_bars_label = new Label("Number of bars:");
        GridPane.setConstraints(num_of_bars_label, 2, 8);

        TextField num_of_bars_input = new TextField();
        num_of_bars_input.setMaxWidth(35);
        num_of_bars_input.setPromptText("30");
        GridPane.setConstraints(num_of_bars_input, 3, 8);

        Button previewButton = new Button("Preview");
        GridPane.setConstraints(previewButton, 0, 9);

        Button render_button = new Button("Render");
        render_button.setMaxWidth(300);
        GridPane.setConstraints(render_button, 2, 9, 2, 1);

        previewButton.setOnAction(e -> {
            //still need to finish
            preview.display("Preview of your image", "Thats cool");
        });

        render_button.setOnAction(e -> {
            String[] error;
            System.out.println(width_height_input.getText());
            width_height_input.clear();
            
            System.out.println(frame_rate_input.getText());
            frame_rate_input.clear();

            System.out.println(bar_types.getValue());

            System.out.println(layout_types.getValue());

            System.out.println(width_of_border_slider.getValue());

            if(select_color_label.isSelected()){
                System.out.println(colorPicker1.getValue());
            }
            System.out.println(color_of_bars.getValue());
            System.out.println(color_of_border.getValue());

            System.out.println(image_address);
            System.out.println(song_address);
            // if(insert_image_label.isSelected()){
            //     System.out.println(image_file);
            // }
            

            //still need to finish
            //Process p = Runtime.getRuntime().exec("python yourapp.py");
        });
        
        grid.getChildren().addAll(title_name, author, input_label, openButton, previewButton, render_button, frame_rate_label, frame_rate_input, width_and_height);
        grid.getChildren().addAll(width_height_input, background_label, layout_types, bar_types, layout_label, bar_label, main_bar_label);
        grid.getChildren().addAll(width_of_border_label, width_of_border_slider, num_of_bars_label, num_of_bars_input, insert_image_label, select_color_label);
        grid.getChildren().addAll(color_of_bars_label, color_of_bars, color_of_border_label, color_of_border, border_value, pb);
        scene1 = new Scene(grid, 510,360);
        window.setScene(scene1);
        window.show();
    }
    private void closeProgram(){
        boolean answer = ConfirmBox.display("Confirm", "Are you sure that you want to exit?");
        if(answer){
            window.close();
        }
    }
    public void return_image_address(String name){
        image_address = name;
    }
    public void return_song_address(String name){
        song_address = name;
    }
}