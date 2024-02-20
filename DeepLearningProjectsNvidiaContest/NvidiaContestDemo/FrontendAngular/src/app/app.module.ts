import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { HashLocationStrategy, LocationStrategy } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ImageRecognitionComponent } from './image-recognition/image-recognition.component';
import { VideoRecognitionComponent } from './video-recognition/video-recognition.component';
import { ButtonsComponent } from './buttons/buttons.component';
import { IachatComponent } from './iachat/iachat.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ImageRecognitionComponent,
    VideoRecognitionComponent,
    ButtonsComponent,
    IachatComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [ { provide: LocationStrategy, useClass: HashLocationStrategy }],
  bootstrap: [AppComponent]
})
export class AppModule { }
