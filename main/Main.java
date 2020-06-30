
import javafx.application.Application;

//import javafx.beans.value.ChangeListener;
//import javafx.beans.value.ObservableValue;
//import java.awt.Color;
import java.awt.Desktop;
import java.io.IOException;
import javafx.embed.swing.SwingNode;
//import javax.swing.text.StyledEditorKit.UnderlineAction;
import javax.swing.JProgressBar;
//import javafx.event.*;
import javafx.geometry.HPos;
import javafx.geometry.Insets;
//import javafx.geometry.Pos;
import javafx.scene.*;
import javafx.scene.image.Image;
import javafx.scene.paint.Color;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.control.Slider;
import javafx.scene.control.ColorPicker;
//import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
//import javafx.scene.layout.HBox;
//import javafx.scene.layout.StackPane;
//import javafx.scene.layout.VBox;
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
        window.setResizable(false);
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
        bar_types.getItems().addAll("1. Normal" , "2. Curved");
        bar_types.setValue("1. Normal");
        
        GridPane.setConstraints(bar_types, 3, 4);

        Label layout_label = new Label("Select layout type:");
        GridPane.setConstraints(layout_label, 2, 5);

        ChoiceBox<String> layout_types = new ChoiceBox<String>();
        layout_types.getItems().addAll("1. Normal", "2. Circular");
        layout_types.setValue("1. Normal");
        GridPane.setConstraints(layout_types, 3, 5);

        Label width_of_border_label = new Label("Width of border");
        GridPane.setConstraints(width_of_border_label, 2, 6, 2, 1);
        GridPane.setHalignment(width_of_border_label, HPos.CENTER);

        Slider width_of_border_slider = new Slider(0,100,10);
        width_of_border_slider.setValue(10);
        width_of_border_slider.setShowTickLabels(true);
        width_of_border_slider.setShowTickMarks(true);
        width_of_border_slider.setMajorTickUnit(50);
        width_of_border_slider.setMinorTickCount(5);
        width_of_border_slider.setBlockIncrement(10);
        GridPane.setConstraints(width_of_border_slider, 2, 7, 2, 1);

        Label border_value = new Label(Integer.toString((int)width_of_border_slider.getValue()));
        GridPane.setConstraints(border_value, 3, 6);
        GridPane.setHalignment(border_value, HPos.RIGHT);

        SwingNode swingNode = new SwingNode();
        JProgressBar progressBar = new JProgressBar(0, 100);
        //progressBar.setSize(500, 100);
        // progressBar.addChangeListener(l -> {
        //     progressBar.setValue();
        // });
        progressBar.setStringPainted(true);
        swingNode.setContent(progressBar);

        GridPane.setConstraints(swingNode, 0, 10, 4, 4);
        
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
            PreviewBox.display("Preview of your image", "Thats cool");
        });

        render_button.setOnAction(e -> {
            String error = "";
            String message = "python3 ../videotools/brain.py ";

            if(song_address != ""){
                if(song_address.substring(song_address.length()-4).equals(".mp3")){
                    message += song_address + " ";
                }else {
                    //wrong input
                    error += "Incorrect Input for song address. Please input a \".mp3\" file. ";
                }
            }else{
                //no input
                error += "No song address given. ";
            }

            if(frame_rate_input.getText() != null && !frame_rate_input.getText().isEmpty()){
                try {
                    if(Integer.parseInt(frame_rate_input.getText()) < 100 && Integer.parseInt(frame_rate_input.getText()) > 0){
                        message += "-f " + frame_rate_input.getText() + " ";
                        frame_rate_input.clear();
                    }else {
                        //either too big or too small
                        error += "Invalid value for frame rate. Enter a number between 0 and 100. ";
                    }
                } catch (Exception ex) {
                    // incorrect input
                    error += "Incorrect input frame rate. Enter a number between 0 and 100. ";
                }
            }else{
                // set to default 
                //message += "-f 24 ";
            }

            if(width_height_input.getText() != null && !width_height_input.getText().isEmpty()){
                if(width_height_input.getText().indexOf('x') == -1){
                    //x doesnt exist, wrong format
                    error += "Incorrect format for width and height. Please enter your values in the proper format. Ex. 1920x1080 ";
                }else{
                    String width_height = width_height_input.getText().replaceAll("\\s","");
                    String width = width_height.substring(0, width_height.indexOf('x'));
                    String height = width_height.substring(width_height.indexOf('x')+1, width_height.length());
                    try {
                        int w = Integer.parseInt(width);
                        int h = Integer.parseInt(height);
                        message += "-r " + width + " " + height + " ";
                        width_height_input.clear();
                    } catch (Exception ex) {
                        //not integers 
                        error += "Incorrect input for width and height. Please enter your values in the proper format. Ex. 1920x1080 ";
                    }
                }
            }else{
                //no input, set to default
                //message += "-r 1920 1080 ";
            }
            // Not done
            System.out.println(bar_types.getValue());
            // Not done 
            System.out.println(layout_types.getValue());

            int width_border = ((int)width_of_border_slider.getValue());
            double convert_width_border = ((double)width_border)/100 ;
            message += "-BO " +convert_width_border + " ";

            if(num_of_bars_input.getText() != null && !num_of_bars_input.getText().isEmpty()){
                try {
                    String num_bars = num_of_bars_input.getText().replaceAll("\\s","");
                    int bars = Integer.parseInt(num_bars);
                    message += "-b " + num_bars + " ";
                    num_of_bars_input.clear();
                } catch (Exception ex) {
                    error += "Incorrect input for number of bars. Please enter one number. Ex. 100";
                }
            }else{
                //no input, set default 
                //message += "-b 100 ";
            }

            if(select_color_label.isSelected()){
                //color for background
                int red = Integer.parseInt(colorPicker1.getValue().toString().substring(2,4), 16);
                int blue = Integer.parseInt(colorPicker1.getValue().toString().substring(4,6), 16);
                int green = Integer.parseInt(colorPicker1.getValue().toString().substring(6,8), 16);
                message += "-BG " +red + " " + blue + " " + green + " ";

            }else if(insert_image_label.isSelected()){ // not finished 
                if(image_address != ""){
                    if(image_address.substring(image_address.length()-4).equals(".png") || image_address.substring(image_address.length()-4).equals(".jpg")){
                        //fix the one here 
                        message += "-BG "+ image_address + "1 ";
                    }else {
                        //wrong input
                        error += "Incorrect Input for image Address. Please input a \".png\" or \".jpg\" file. ";
                    }
                }else{
                    //no input
                    error += "No image address given. ";
                }
            }else {
                //select color or image_address are not selected
                error += "Please select a color or an image.";
            }

            //color of bars 
            int bar_red = Integer.parseInt(color_of_bars.getValue().toString().substring(2,4), 16);
            int bar_blue = Integer.parseInt(color_of_bars.getValue().toString().substring(4,6), 16);
            int bar_green = Integer.parseInt(color_of_bars.getValue().toString().substring(6,8), 16);
            message += "-BC " +bar_red + " " + bar_blue + " " + bar_green + " ";

            //color of border 
            int border_red = Integer.parseInt(color_of_border.getValue().toString().substring(2,4), 16);
            int border_blue = Integer.parseInt(color_of_border.getValue().toString().substring(4,6), 16);
            int border_green = Integer.parseInt(color_of_border.getValue().toString().substring(6,8), 16);
            message += "-BOC " +border_red + " " + border_blue + " " + border_green + " ";

            // if(color_of_bars.getValue().toString().equals("0xffffffff") && color_of_border.getValue() == Color.WHITE){
            // }else{
            //     System.out.println(color_of_bars.getValue());
            //     System.out.println(color_of_border.getValue());
            // }
            if(error != ""){
                ErrorBox.display("Error has occured.", error);
            } else {
                System.out.println(message);
                //Process p = Runtime.getRuntime().exec(message);
                //File f = new File("");
                // if (f != null) {
                //     openFile(f);
                // }
            }
        });
        
        grid.getChildren().addAll(title_name, author, input_label, openButton, previewButton, render_button, frame_rate_label, frame_rate_input, width_and_height);
        grid.getChildren().addAll(width_height_input, background_label, layout_types, bar_types, layout_label, bar_label, main_bar_label);
        grid.getChildren().addAll(width_of_border_label, width_of_border_slider, num_of_bars_label, num_of_bars_input, insert_image_label, select_color_label);
        grid.getChildren().addAll(color_of_bars_label, color_of_bars, color_of_border_label, color_of_border, border_value, swingNode);
        scene1 = new Scene(grid, 510,390);
        window.setScene(scene1);
        window.getIcons().add(new Image(getClass().getResourceAsStream("Syncorized Logo.png")));
        //primaryStage.titleProperty().bind(scene1.widthProperty().asString().concat(" : ").concat(scene1.heightProperty().asString()));
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
    private void openFile(File file) {
        try {
            desktop.open(file);
        } catch (IOException ex) {
        }
    }
}