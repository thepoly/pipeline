import { Component, OnInit } from '@angular/core';

import { Story } from './story';
import { StoryService } from './story.service';


@Component({
  moduleId: module.id,
  selector: 'story-search',
  templateUrl: 'story-search.component.html',
  styleUrls: [ 'story-search.component.css' ]
})

export class StorySearchComponent implements OnInit {

  stories: Story[] = [];

  constructor(private storyService: StoryService) { }

  ngOnInit(): void {
    this.storyService.getStories()
      .then(stories => this.stories = stories);
  }
}
