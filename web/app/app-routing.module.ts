import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { StorySearchComponent }   from './story-search.component';
import { StoryEditorComponent }      from './story-editor.component';
import { StoryListComponent }  from './story-list.component';
import { StoryDetailComponent }  from './story-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/story-editor/1', pathMatch: 'full' },
  { path: 'story-search',  component: StorySearchComponent },
  { path: 'detail/:id', component: StoryDetailComponent },
  { path: 'story-editor/:id', component: StoryEditorComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
