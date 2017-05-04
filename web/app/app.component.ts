import { Component } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'my-app',
  template: `
    <div class="header">
      <img src="../pipeline_logo.png">
    </div>
    <nav class="navbar-navbar-default">
      <div class = "container-fluid">
          <a class = "navbar-left"routerLink="/story-editor/1" routerLinkActive="active">Story Editor</a>
          <a class = "navbar-right" routerLink="/story-search" routerLinkActive="active">Story Search</a>
      </div>
    </nav>
    <router-outlet></router-outlet>
  `,
  styleUrls: ['app.component.css'],
})
export class AppComponent {
  // title = 'pipeline';
}
