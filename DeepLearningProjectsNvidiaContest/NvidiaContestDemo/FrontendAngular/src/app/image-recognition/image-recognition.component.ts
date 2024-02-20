import { Component, OnInit } from '@angular/core';
import { GeneralPorpuseServiceService } from '../services/general-porpuse-service.service';
import { timeout } from 'rxjs';
import Swal from 'sweetalert2'
import 'hammerjs';

// or via CommonJS

@Component({
  selector: 'app-image-recognition',
  templateUrl: './image-recognition.component.html',
  styleUrls: ['./image-recognition.component.css']
})
export class ImageRecognitionComponent implements OnInit {

  constructor(private generalService: GeneralPorpuseServiceService) {

  }

  imagesArray?: File;
  listOfOriginalImages: any[] = [];
  listOfPocessImages: any[] = [];
  zoomedImagePath!: string;
  isModalOpen: boolean = false;
  zoomScale: number = 1;
  isPanning: boolean = false;
  panStart: { x: number, y: number } = { x: 0, y: 0 };
  imagePosition: { x: number, y: number } = { x: 0, y: 0 };
  imageStyle? : any;
 

  ngOnInit(): void {
    this.getOriginalImages();
    this.getProcessedImages();
  }


  triggerNvidia(): void {
    this.generalService.triggerNvidiaTensorRT().subscribe(resp => {
      setTimeout(() => {
        this.getOriginalImages();
        this.getProcessedImages();
      }, 300);
    })
  }

  getOriginalImages() {
    this.generalService.getOriginalImages().subscribe(resp => {
      this.listOfOriginalImages = resp;
    });
  }

  getProcessedImages() {
    this.generalService.getProcessedImages().subscribe(resp => {
      this.listOfPocessImages = resp;
    });
  }

  selectImages(event:any) {
    this.imagesArray = event.target.files;
  }

  uploadMultipleImages() {
    this.generalService.uploadImages(this.imagesArray!).subscribe(resp => {
      Swal.fire({
        title: "Nvidia Contest",
        text: "Images uploaded successfully!",
        icon: "success"
      });
    });
  }

  openZoomModal(imagePath: string) {
    this.zoomedImagePath = 'assets/' + imagePath;
    this.isModalOpen = true; // Use this flag to control the modal display
  }

  closeModal() {
    this.isModalOpen = false; // Close the modal
    this.zoomScale = 1;
    this.panStart = { x: 0, y: 0 };
    this.imagePosition =  { x: 0, y: 0 };
  }


  startPanning(event: MouseEvent) {
    this.isPanning = true;
    this.panStart = { x: event.clientX - this.imagePosition.x, y: event.clientY - this.imagePosition.y };
  }
  
  panImage(event: MouseEvent) {
    if (this.isPanning) {
      event.preventDefault();
      this.imagePosition.x = event.clientX - this.panStart.x;
      this.imagePosition.y = event.clientY - this.panStart.y;
      this.updateImageStyle();
    }
  }
  
  stopPanning() {
    this.isPanning = false;
  }
  
  zoomImage(event: WheelEvent) {
    event.preventDefault();
    const zoomIntensity = 0.1;
    const wheelDelta = event.deltaY < 0 ? 1 : -1;
    this.zoomScale += wheelDelta * zoomIntensity;
    this.zoomScale = Math.max(1, this.zoomScale);
    this.updateImageStyle();
  }
  
  updateImageStyle() {
    this.imageStyle = `translate(${this.imagePosition.x}px, ${this.imagePosition.y}px) scale(${this.zoomScale})`;
  }


}
