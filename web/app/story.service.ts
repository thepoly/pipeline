import { Injectable } from '@angular/core';

import { Story } from './story';
import { STORIES } from './mock-stories';

@Injectable()
export class StoryService {
  getStories(): Promise<Story[]> {
    return Promise.resolve(STORIES);
  }
}
