import 'rxjs/add/operator/switchMap';

// Keep the Input import for now, we'll remove it later:
import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Params }   from '@angular/router';
import { Location }                 from '@angular/common';

import { Story } from './story';
import { StoryService } from './story.service';


@Component({
  moduleId: module.id,
  selector: 'story-detail',
  templateUrl: 'story-detail.component.html',
  styleUrls: [ 'story-detail.component.css' ]
})
export class StoryDetailComponent implements OnInit{
  story: Story;

  constructor(
    private storyService: StoryService,
    private route: ActivatedRoute,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.route.params
      .switchMap((params: Params) => this.storyService.getStory(+params['id']))
      .subscribe(story => this.story = story);
  }

  goBack(): void {
    this.location.back();
  }
}
