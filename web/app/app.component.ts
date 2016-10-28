import { Component } from '@angular/core';

export class Story {
  id: number;
  title: string;
}

const STORIES: Story[] = [
  { id: 11, title: 'tacos' },
  { id: 12, title: 'pizza' },
  { id: 13, title: 'bacon' },
  { id: 14, title: 'tequila mockingbird' },
  { id: 15, title: 'pupper' },
  { id: 16, title: 'enchilada' },
  { id: 17, title: 'egg roll' },
  { id: 18, title: 'sushis' },
  { id: 19, title: 'sugerz' },
  { id: 20, title: 'yum' }
];

@Component({
  selector: 'my-app',
  template: `
  <h1>{{title}}</h1>
  <h2>My Heroes</h2>
  <ul class="stories">
    <li *ngFor="let story of stories">
      <span class="badge">{{story.id}}</span>{{story.title}}
    </li>
  </ul>

  <h2>{{story.title}} details!</h2>
  <div><label>id: </label>{{story.id}}</div>
  <div><label>title: </label>
  <input [(ngModel)] = "story.title" placeholder = "title"> <!-->doesn't update to server??<-->
  </div>
  `
})

export class AppComponent {
  title = 'Pipeline';
  story: Story = {
  id: 1,
  title: 'Rex is a newb'
  };
  stories = STORIES;
}
