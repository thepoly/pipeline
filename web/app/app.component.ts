import { Component } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'my-app',
  template: `
    <h1>
      <img src="https://poly.rpi.edu/wp-content/themes/poly_new_testbed/images/logo_m.png">
    </h1>
    <nav>
      <a routerLink="/story-editor" routerLinkActive="active">Story Editor</a>
      <a routerLink="/story-search" routerLinkActive="active">Story Search</a>
    </nav>
    <router-outlet></router-outlet>
  `,
  styleUrls: ['app.component.css'],
})
export class AppComponent {
  // title = 'pipeline';
}
