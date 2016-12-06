import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { StorySearchComponent }   from './story-search.component';
import { StoryEditorComponent }      from './story-editor.component';
import { StoryDetailComponent }  from './story-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/story-editor', pathMatch: 'full' },
  { path: 'story-search',  component: StorySearchComponent },
  { path: 'detail/:id', component: StoryDetailComponent },
  { path: 'story-editor', component: StoryEditorComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
