import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';

import { AppComponent }   from './app.component';
import { StoryDetailComponent } from './story-detail.component';
import { StoryTextComponent } from './story-text.component';


@NgModule({
  imports:      [ BrowserModule, FormsModule ],
  declarations: [ AppComponent, StoryDetailComponent, StoryTextComponent ],
  bootstrap:    [ AppComponent ]
})

export class AppModule { }
