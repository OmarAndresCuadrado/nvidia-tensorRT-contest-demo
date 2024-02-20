import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoRecognitionComponent } from './video-recognition.component';

describe('VideoRecognitionComponent', () => {
  let component: VideoRecognitionComponent;
  let fixture: ComponentFixture<VideoRecognitionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [VideoRecognitionComponent]
    });
    fixture = TestBed.createComponent(VideoRecognitionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
