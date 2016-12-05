import { Component, OnInit } from '@angular/core';
import { Story } from './story';
import { StoryService } from './story.service';

@Component({
  selector: 'my-app',
  template: `
    <h1>{{title}}</h1>
    <h2>Stories</h2>
    <ul class="stories">
      <li *ngFor="let story of stories"
        [class.selected]="story === selectedStory"
        (click)="onSelect(story)">
        <span class="badge">{{story.id}}</span> {{story.title}}
      </li>
    </ul>
    <story-detail [story]="selectedStory"></story-detail>
    <story-text [story]="selectedStory"></story-text>
  `,
  styles: [`
    .selected {
      background-color: #dccfcf !important;
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
      background-color: #edc7c7 !important;
      color: white;
    }
    .stories li:hover {
      color: #e53b3b;
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
  `],
  providers: [StoryService]
})
export class AppComponent implements OnInit {
  title = 'pipeline';
  stories: Story[];
  selectedStory: Story;

  constructor(private storyService: StoryService) { }

  getStories(): void {
    this.storyService.getStories().then(stories => this.stories = stories);
  }

  ngOnInit(): void {
    this.getStories();
  }

  onSelect(story: Story): void {
    this.selectedStory = story;
  }
}
