import { Injectable } from '@angular/core';
import { Headers, Http } from '@angular/http';

import 'rxjs/add/operator/toPromise';

import { Story } from './story';
// import { Observable } from 'rxjs/Observable';
// https://angular.io/docs/ts/latest/guide/server-communication.html#!#http-client
// to replace promise with observable

@Injectable()
export class StoryService {

  private headers = new Headers({'Content-Type': 'application/json'});
  private storiesUrl = 'https://poly.rpi.edu/pipeline_dev/api/stories';  // URL to web api

  constructor(private http: Http) { }

  getStories(): Promise<Story[]> {
    return this.http.get(this.storiesUrl)
               .toPromise()
               .then(response => response.json().stories as Story[])
               .catch(this.handleError);
  }


  getStory(id: number): Promise<Story> {
    const url = `${this.storiesUrl}/${id}`;
    return this.http.get(url)
      .toPromise()
      .then(response => response.json().story as Story)
      .catch(this.handleError);
  }

  delete(id: number): Promise<void> {
    const url = `${this.storiesUrl}/${id}`;
    return this.http.delete(url, {headers: this.headers})
      .toPromise()
      .then(() => null)
      .catch(this.handleError);
  }

  create(title: string): Promise<Story> {
    return this.http
      .post(this.storiesUrl, JSON.stringify({title: title}), {headers: this.headers})
      .toPromise()
      .then(res => res.json().story)
      .catch(this.handleError);
  }

  update(story: Story): Promise<Story> {
    const url = `${this.storiesUrl}/${story.id}`;
    return this.http
      .put(url, JSON.stringify(story), {headers: this.headers})
      .toPromise()
      .then(() => story)
      .catch(this.handleError);
  }

  private handleError(error: any): Promise<any> {
    console.error('An error occurred', error); // for demo purposes only
    return Promise.reject(error.message || error);
  }
}
