package com.example.demo.controllers;


import com.example.demo.models.ChatModel;
import com.example.demo.services.GeneralPurposeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.List;


@CrossOrigin
@RestController
@RequestMapping("/nvidia/api")
public class GeneralPurposeController {

    private String projectDirectoryPath = System.getProperty("user.dir");
    File currentDirectory = new File(projectDirectoryPath);

    File upperLevelDirectory = currentDirectory.getParentFile().getParentFile().getParentFile().getParentFile();

    String projectDirectoryPathGeneral = upperLevelDirectory.getPath();

    private static final String processImagePath = "DeepLearningProjectsNvidiaContest" + File.separator +
            "PythonEngineTensorRT" + File.separator +
            "Resnet18VImageferenceTensorRT";

    private static final String processVideoPath = "DeepLearningProjectsNvidiaContest" + File.separator +
            "PythonEngineTensorRT" + File.separator +
            "Resnet18VideoInferenceTensorRT";

    @Autowired
    private GeneralPurposeService generalPurposeService;

    @GetMapping("/trigger/nvidia/tensorrt")
    public void triggerNvidiaTensorRTPythonScript() throws IOException {
        String processImagePathCommand = projectDirectoryPathGeneral + File.separator + processImagePath;
        ProcessBuilder builder = new ProcessBuilder(
                "cmd.exe", "/c", "cd \"" + processImagePathCommand +"\" && python imageInferenceTensorTR.py");

        builder.redirectErrorStream(true);
        Process p = builder.start();
        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line;
        while (true) {
            line = r.readLine();
            if (line == null) {
                break;
            }
        }
    }

    @GetMapping("/original/images")
    public ResponseEntity<?> getOriginalImagesFromFolder() throws IOException {
        List<String> listOfOriginalImages = generalPurposeService.getOriginalImages();
        return ResponseEntity.status(HttpStatus.OK).body(listOfOriginalImages);
    }

    @GetMapping("/processed/images")
    public ResponseEntity<?> getProcessedImagesFromFolder() throws IOException {
        List<String> listOfProcessedImages = generalPurposeService.getProcessedImages();
        return ResponseEntity.status(HttpStatus.OK).body(listOfProcessedImages);
    }

    @GetMapping("/videos")
    public ResponseEntity<?> getVideoNames() throws IOException {
        List<String> listOfProcessedImages = generalPurposeService.getVideosNames();
        return ResponseEntity.status(HttpStatus.OK).body(listOfProcessedImages);
    }


    @GetMapping("/trigger/nvidia/tensorrt/video")
    public void triggerNvidiaTensorRTPythonScriptVideo(@RequestParam String videoName) throws IOException {
        String processVideoPathCommand = projectDirectoryPathGeneral + File.separator + processVideoPath;
        ProcessBuilder builder = new ProcessBuilder(
                "cmd.exe", "/c", "cd \""+ processVideoPathCommand +"\" && python videoInferenceTensorTR.py \"" + videoName + "\"");
        builder.redirectErrorStream(true);
        Process p = builder.start();
        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
        String line;
        while (true) {
            line = r.readLine();
            if (line == null) {
                break;
            }
        }
    }


    @PostMapping("/images")
    public ResponseEntity<?> saveImageIntoFolder(@RequestParam("images") List<MultipartFile> images) throws IOException {
        generalPurposeService.saveImages(images);
        ResponseEntity response = ResponseEntity.status(HttpStatus.OK).body(null);
        return response;
    }

    @PostMapping("/video")
    public ResponseEntity<?> saveVideoIntoFolder(@RequestParam("video") MultipartFile video) throws IOException {
        generalPurposeService.saveVideo(video);
        ResponseEntity response = ResponseEntity.status(HttpStatus.OK).body(null);
        return response;
    }

    @PostMapping("/chat/message")
    public ResponseEntity<?> postMessageToGenerativeChatIa(@RequestBody ChatModel chatModel) throws IOException, InterruptedException {
        return ResponseEntity.status(HttpStatus.OK).body(generalPurposeService.sendChatMessage(chatModel));
    }
}
