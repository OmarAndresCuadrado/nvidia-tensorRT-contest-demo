import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IachatComponent } from './iachat.component';

describe('IachatComponent', () => {
  let component: IachatComponent;
  let fixture: ComponentFixture<IachatComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [IachatComponent]
    });
    fixture = TestBed.createComponent(IachatComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
