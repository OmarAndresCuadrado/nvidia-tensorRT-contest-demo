package com.example.demo.models;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.Setter;

@AllArgsConstructor
@Getter
@Setter
@Builder
public class GeneralPurposeModel {

    private String imageDetected;

    private Double detectionConfidence;

    private Double totalTimeGeneration;

    private String originalImageName;

    private String originalImagePath;

    private String processImageName;

    private String processImagePath;

    private String imageExtension;
}
