import { Component, Input } from '@angular/core';
import { Story } from './story';

@Component({
  selector: 'story-detail',
  template: `
  <div *ngIf="story">
    <h2>{{story.title}} details!</h2>
    <div><label>id: </label>{{story.id}}</div>
    <div>
      <label>name: </label>
      <input [(ngModel)]="story.title" placeholder="title"/>
    </div>
  </div>`
})
export class StoryDetailComponent {
  @Input()
  story: Story;
}
