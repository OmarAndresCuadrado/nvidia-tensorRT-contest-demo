package com.example.demo.services;

import com.example.demo.models.ChatModel;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.ArrayList;
import java.util.List;
import java.util.Stack;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class GeneralPurposeService {

    private String projectDirectoryPath = System.getProperty("user.dir");
    File currentDirectory = new File(projectDirectoryPath);

    File upperLevelDirectory = currentDirectory.getParentFile().getParentFile().getParentFile().getParentFile();

    String projectDirectoryPathGeneral = upperLevelDirectory.getPath();


    private static final String parentImagePath = "DeepLearningProjectsNvidiaContest" + File.separator +
            "PythonEngineTensorRT" + File.separator +
            "Resnet18VImageferenceTensorRT" + File.separator +
            "OriginalImages" + File.separator;

    private static final String parentProcessImagePath = "DeepLearningProjectsNvidiaContest" + File.separator +
            "PythonEngineTensorRT" + File.separator +
            "Resnet18VImageferenceTensorRT" + File.separator +
            "ProcessedImages" + File.separator;


    private static final String parentVideoPath = "DeepLearningProjectsNvidiaContest" + File.separator +
            "PythonEngineTensorRT" + File.separator +
            "Resnet18VideoInferenceTensorRT" + File.separator +
            "OriginalVideo" + File.separator;

    private static final String parentAngularPath = "DeepLearningProjectsNvidiaContest" + File.separator +
            "NvidiaContestDemo" + File.separator +
            "FrontendAngular" + File.separator +
            "src" + File.separator +
            "assets" + File.separator;

    private static final String parentIaChatPath = "DeepLearningProjectsNvidiaContest" + File.separator +
            "PythonEngineTensorRT" + File.separator +
            "GeneartiveIaChatTensorRT";

    private String originalImagePath = projectDirectoryPathGeneral + File.separator + parentImagePath;


    private String processImagePath = projectDirectoryPathGeneral + File.separator + parentProcessImagePath;

    private String originalVideoPath = projectDirectoryPathGeneral + File.separator + parentVideoPath;

    private String angularFolderPath = projectDirectoryPathGeneral + File.separator + parentAngularPath;
    private String chatResponsePath = projectDirectoryPathGeneral  + File.separator + parentIaChatPath;

    public void saveImages(List<MultipartFile> images) throws IOException {
        for (MultipartFile image : images) {

            String filename = image.getOriginalFilename();
            String angularPath = angularFolderPath + filename;
            String filePath = originalImagePath + filename;
            image.transferTo(new File(filePath));
            Files.copy(Paths.get(filePath), Paths.get(angularPath), StandardCopyOption.REPLACE_EXISTING);
        }
    }

    public void saveVideo(MultipartFile video) throws IOException {
        String filename = video.getOriginalFilename();
        String videoPath = originalVideoPath + filename;
        video.transferTo(new File(videoPath));
    }

    public List<String> getOriginalImages() throws IOException {
        List<String> listOfUrls = new ArrayList<>();
        File directory = new File(originalImagePath);
        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    listOfUrls.add(file.getName());
                }
            }
        }
        return listOfUrls;
    }

    public List<String> getProcessedImages() throws IOException {
        List<String> listOfUrls = new ArrayList<>();
        File directory = new File(processImagePath);
        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {
                    listOfUrls.add(file.getName());
                }
            }
        }
        return listOfUrls;
    }

    public Stack<String> getVideosNames() throws IOException {
        Stack<String> listOfUrls = new Stack<>();
        String regex = ".*\\.mp4$";
        Pattern pattern = Pattern.compile(regex);
        File directory = new File(angularFolderPath);
        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                String fileName = file.getName();
                Matcher matcher = pattern.matcher(fileName);
                if (matcher.matches()) {
                    listOfUrls.push(fileName);
                }
            }
        }
        return listOfUrls;
    }

    public String sendChatMessage(ChatModel chatModel) throws IOException, InterruptedException {
        // Ensure the command is correctly formatted, especially the path and inclusion of arguments
        Path filePath = Paths.get(chatResponsePath + "\\Responses\\" + File.separator + "chat_response.txt");
        String response = "";
        String command = String.format("cd \""+ chatResponsePath +"\" && python GenerativeIaQuestionAndAnswer.py \"%s\" \"%s\"",
                chatModel.getContext(), chatModel.getQuestion());
        ProcessBuilder builder = new ProcessBuilder(
                "cmd.exe", "/c", command);
        builder.redirectErrorStream(true);
        Process p = builder.start();
        BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
        StringBuilder output = new StringBuilder();
        String line;
        while ((line = r.readLine()) != null) {
            output.append(line).append("\n");
        }
        int exitVal = p.waitFor();
        if (exitVal == 0) {
            response = new String(Files.readAllBytes(filePath));
            Files.delete(filePath);
        } else {
            System.out.println("failed");
        }
        return response;
    }
}
