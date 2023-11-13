import {HttpClient} from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import {environment} from '@environments/environment';
import {first} from 'rxjs/operators';
import { AnimeService } from '../_services/anime.service';

@Component({
  selector: 'app-animes',
  templateUrl: './animes.component.html',
  styleUrls: ['./animes.component.less'],
})
export class AnimesComponent implements OnInit{
  animes$;
  p: number = 1;
  anime_details;
  found = [];

  constructor(
    private animeService: AnimeService,
    private http: HttpClient,
  ) {
  }

  ngOnInit(): void {
    this.animeService.currentSearch.subscribe((search) => {
      if (search) {
        console.log(search.length);
        this.found = [];
        for (var s in search) {
          this.animeService.getAnime(search[s]['anime_id']).subscribe((data) => {
            this.found.push(data);
          });
        }
        this.animes$ = this.found;
      } else {
        this.animeService.getMostScore().subscribe((data) => (this.animes$ = data));
      }
    });
  }

  sortScore() {
    this.animes$ = this.http
      .get(`${environment.apiUrl}/animes/most_score`)
      .subscribe((data) => (this.animes$ = data));
  }
  sortEp() {
    this.animes$ = this.http
      .get(`${environment.apiUrl}/animes/most_episode`)
      .subscribe((data) => (this.animes$ = data));
  }
  sortYear() {
    this.animes$ = this.http
      .get(`${environment.apiUrl}/animes/most_recent`)
      .subscribe((data) => (this.animes$ = data));
  }
}
