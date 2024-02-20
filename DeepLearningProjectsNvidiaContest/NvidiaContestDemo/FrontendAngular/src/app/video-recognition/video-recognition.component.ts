import { Component, OnInit } from '@angular/core';
import { GeneralPorpuseServiceService } from '../services/general-porpuse-service.service';
import Swal from 'sweetalert2'

@Component({
  selector: 'app-video-recognition',
  templateUrl: './video-recognition.component.html',
  styleUrls: ['./video-recognition.component.css']
})
export class VideoRecognitionComponent implements OnInit {

  
  constructor(private generalPorpuseService: GeneralPorpuseServiceService) {}

  videosArray: any[] = [];
  videoSelected: any;


  ngOnInit(): void {
    this.getVideos();
  }


  getVideos() {
    this.generalPorpuseService.getVideos().subscribe(resp => {
      this.videosArray = resp;
    });
  }

  triggerNvidiaVideo(): void {
    this.generalPorpuseService.triggerNvidiaTensorRTVideo(this.videoSelected.name).subscribe(resp => {
      setTimeout(() => {
        this.videosArray = [];
        this.getVideos();
      }, 1000);
    })
  }



  selectVideo(event:any) {
    this.videoSelected = event.target.files[0];
  }

  uploadVideo() {
    this.generalPorpuseService.uploadVideo(this.videoSelected).subscribe(resp => {
      Swal.fire({
        title: "Nvidia Contest",
        text: "Video uploaded successfully!",
        icon: "success"
      });
    });
  }

}
