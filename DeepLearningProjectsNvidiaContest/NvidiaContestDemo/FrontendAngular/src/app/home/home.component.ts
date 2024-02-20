import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {

  isImageModuleActivated: boolean = false;
  isVideoModuleActivated: boolean = false;
  isIaChatActivated: boolean = false;



  showImageModule(): void {
    this.isImageModuleActivated = true;
    this.isVideoModuleActivated = false;
    this.isIaChatActivated = false;
  }

  showVideoModule(): void {
    this.isImageModuleActivated = false;
    this.isVideoModuleActivated = true;
    this.isIaChatActivated = false;
  }

  showIaChatModule(): void {
    this.isImageModuleActivated = false;
    this.isVideoModuleActivated = false;
    this.isIaChatActivated = true;
  }



}
