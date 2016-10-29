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
  <h2>Stories</h2>
  <ul class="stories">
    <li *ngFor = "let story of stories" (click) = "onSelect(hero)">
      <span class = "badge">{{story.id}}</span>{{story.title}}
    </li>
  </ul>

  <div *ngIf = "selectedStory">
    <h2>{{selectedStory.title}} details!</h2>
    <div><label>id: </label>{{selectedStory.id}}</div>
    <div>
      <label>title: </label>
      <input [(ngModel)] = "selectedStory.title" placeholder = "title"> <!-->doesn't update to server??<-->
    </div>
  </div>
  `,
  styles: [`
  .selected {
    background-color: #CFD8DC !important;
    color: white;
  }
  .stories {
    margin: 0 0 2em 0;
    list-style-type: none;
    padding: 0;
    width: 15em;
  }
  .stories li {
    cursor: pointer;
    position: relative;
    left: 0;
    background-color: #EEE;
    margin: .5em;
    padding: .3em 0;
    height: 1.6em;
    border-radius: 4px;
  }
  .stories li.selected:hover {
    background-color: #BBD8DC !important;
    color: white;
  }
  .stories li:hover {
    color: #607D8B;
    background-color: #DDD;
    left: .1em;
  }
  .stories .text {
    position: relative;
    top: -3px;
  }
  .stories .badge {
    display: inline-block;
    font-size: small;
    color: white;
    padding: 0.8em 0.7em 0 0.7em;
    background-color: #DA1E05;
    line-height: 1em;
    position: relative;
    left: -1px;
    top: -4px;
    height: 1.8em;
    margin-right: .8em;
    border-radius: 4px 0 0 4px;
  }
`]

})

export class AppComponent {
  title = 'pipeline';
  selectedStory = Story;
  onSelect(story: Story): void {
    this.selectedStory = story;
  }
  stories = STORIES;
}
