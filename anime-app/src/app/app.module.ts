import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { NgImageSliderModule } from 'ng-image-slider';

import { AppRoutingModule } from './app-routing.module';
import { JwtInterceptor, ErrorInterceptor } from './_helpers';
import { AppComponent } from './app.component';
import { AlertComponent } from './_components';
import { HomeComponent } from './home';
import { AnimesComponent } from './animes/animes.component';
import {RouterModule} from '@angular/router';
import { NgxPaginationModule } from 'ngx-pagination';
import { MatTabsModule } from '@angular/material/tabs';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AnimeDetailsComponent, SafeHtmlPipe, SafePipe } from './anime-details/anime-details.component';;
import { DescriptionComponent } from './description/description.component'
;

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    AppRoutingModule,
    CommonModule,
    NgImageSliderModule,
    NgxPaginationModule,
    BrowserAnimationsModule,
    MatTabsModule,
    RouterModule.forRoot([]),
  ],
  declarations: [
    AppComponent,
    AlertComponent,
    HomeComponent,
    AnimesComponent,
    AnimeDetailsComponent,
    DescriptionComponent,
    SafePipe,
    SafeHtmlPipe,
  ],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: JwtInterceptor, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {};
