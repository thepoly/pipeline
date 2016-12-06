import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';

import { AppComponent }   from './app.component';
import { StoryEditorComponent} from './story-editor.component';
import { StoryDetailComponent } from './story-detail.component';
import { StoryTextComponent } from './story-text.component';
import { StorySearchComponent} from './story-search.component';
import { StoryService } from './story.service';

import { SafePipe } from './safepipe';

import { AppRoutingModule }     from './app-routing.module';

@NgModule({
  imports:      [
    BrowserModule,
    FormsModule,
    AppRoutingModule
 ],
  declarations: [
    AppComponent,
    StoryEditorComponent,
    StoryDetailComponent,
    StoryTextComponent,
    StorySearchComponent,
    SafePipe
  ],
  providers: [StoryService],
  bootstrap:    [ AppComponent ]
})

export class AppModule { }
