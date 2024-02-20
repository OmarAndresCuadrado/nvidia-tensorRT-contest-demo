import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GeneralPorpuseServiceService {

  localHostEndpoint: string = 'http://localhost:4090/nvidia/api'

  constructor(private http: HttpClient) { }


  getOriginalImages(): Observable<any> {
    let getOriginalImagesEndpoint = `${this.localHostEndpoint}/original/images`;
    return this.http.get<any>(getOriginalImagesEndpoint);
  }

  getProcessedImages(): Observable<any> {
    let getProcessedImagesEndpoint = `${this.localHostEndpoint}/processed/images`;
    return this.http.get<any>(getProcessedImagesEndpoint);
  }

  triggerNvidiaTensorRT(): Observable<any> {
    let triggerNvidiaTensorRTEndpoint = `${this.localHostEndpoint}/trigger/nvidia/tensorrt`;
    return this.http.get<any>(triggerNvidiaTensorRTEndpoint);
  }

  triggerNvidiaTensorRTVideo(videoName : string): Observable<any> {
    let triggerNvidiaTensorRTEndpoint = `${this.localHostEndpoint}/trigger/nvidia/tensorrt/video?videoName=${videoName}`;
    return this.http.get<any>(triggerNvidiaTensorRTEndpoint);
  }

  uploadImages(images: File): Observable<any> {
    let formData = new FormData();
    let uploadImagesEndpoint = `${this.localHostEndpoint}/images`;
    let imagesArray = Object.values(images);
    imagesArray.forEach(image => {
      formData.append("images", image);
    });
    return this.http.post<any>(uploadImagesEndpoint, formData);
  }

  uploadVideo(video: File): Observable<any> {
    let formData = new FormData();
    let uploadVideoEndpoint = `${this.localHostEndpoint}/video`;
    formData.append("video", video);
    return this.http.post<any>(uploadVideoEndpoint, formData);
  }

  getVideos() {
    let getVideosEndpoint = `${this.localHostEndpoint}/videos`;
    return this.http.get<any>(getVideosEndpoint);
  }

  sendMessageToIaChatBot(messageToChatIa: any) : Observable<string> {
    let sendMessageToIaChatBot = `${this.localHostEndpoint}/chat/message`;
    return this.http.post<string>(sendMessageToIaChatBot, messageToChatIa, { responseType: 'text' as 'json' });
  }
}
