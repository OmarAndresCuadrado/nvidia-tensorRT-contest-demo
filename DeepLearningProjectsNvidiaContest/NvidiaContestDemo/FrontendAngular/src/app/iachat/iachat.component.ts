import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { GeneralPorpuseServiceService } from '../services/general-porpuse-service.service';

@Component({
  selector: 'app-iachat',
  templateUrl: './iachat.component.html',
  styleUrls: ['./iachat.component.css']
})
export class IachatComponent implements OnInit {

  historicalChats:any [] = [];
  chatResponse = '';
  isLoading: boolean = false;

  chatBotForm: FormGroup = this.formBuilder.group({
    context: [''],
    question: ['']
  });;

  get email() {
    return this.chatBotForm.get('context');
  }

  get password() {
    return this.chatBotForm.get('question');
  }

  constructor(private formBuilder: FormBuilder, private generalPorpuseService: GeneralPorpuseServiceService) { }

  ngOnInit(): void {
    this.historicalChats = [];
  }

  sendChatBotMessage() {
    this.isLoading = true;
    this.chatResponse = '';
    let messageToChatIa = {
      context: this.chatBotForm.value.context,
      question: this.chatBotForm.value.question,
    }
    this.generalPorpuseService.sendMessageToIaChatBot(messageToChatIa).subscribe(resp => {
      this.chatResponse = resp;
      let messageForHistorical = {
        ... messageToChatIa,
        chatResponse : this.chatResponse
      }
      this.historicalChats.push(messageForHistorical);
      this.chatBotForm.reset();
      this.isLoading = false;
    });
  }



}

