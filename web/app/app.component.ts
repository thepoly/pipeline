import { Component } from '@angular/core';

export class Story {
  id: number;
  title: string;
}

@Component({
  selector: 'my-app',
  template: `
  <h1>{{title}}</h1>
  <h2>{{story.title}} details!</h2>
  <div><label>id: </label>{{story.id}}</div>
  <div><label>title: </label>{{story.title}}</div>
  `
})

export class AppComponent {
  title = 'Pipeline';
  story: Story = {
  id: 1,
  title: 'Rex is a newb'
  };
}
