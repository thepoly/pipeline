import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Params }   from '@angular/router';
import { Router } from '@angular/router';

import { Story } from './story';
import { StoryService } from './story.service';

import { StoryListComponent } from './story-list.component';
import { StoryDetailComponent } from './story-detail.component';

@Component({
  moduleId: module.id,
  selector: 'story-editor',
  templateUrl: 'story-editor.component.html',
  styleUrls: [ 'story-editor.component.css'],
  providers: [StoryService],
  directives: [StoryListComponent, StoryDetailComponent]
})
export class StoryEditorComponent implements OnInit {
  // stories: Story[];
  // selectedStory: Story;

  constructor(
    private router: Router,
    private storyService: StoryService) { }

  // getStories(): void {
  //   this.storyService.getStories().then(stories => this.stories = stories);
  // }

  // ngOnInit(): void {
  //   this.getStories();
  // }
}
