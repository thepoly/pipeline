import { Component, Input } from '@angular/core';
import { Story } from './story';

@Component({
  selector: 'story-text',
  template: `
  <div *ngIf="story">
    <h2>{{story.title}} text!</h2>
    <div><label>id: </label>{{story.id}}</div>
    <div>
      <label>here sid: </label>
      <!--> put yo shit here<-->
    </div>
  </div>`
})
export class StoryTextComponent {
  @Input()
  story: Story;
}
