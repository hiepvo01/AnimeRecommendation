import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {environment} from '@environments/environment';
import { map } from 'rxjs/operators';
import { Anime } from '@app/_models';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

interface AnimeEp {
  ep_url: string;
}
@Injectable({
  providedIn: 'root',
})
export class AnimeService {
  search_result: any = new BehaviorSubject('');
  currentSearch = this.search_result.asObservable();

  constructor(private http: HttpClient) {}

  getMostScore() {
    return this.http.get(`${environment.apiUrl}/animes/most_score`);
  }

  getAnime(anime_id) {
    return this.http.get<Anime>(`${environment.apiUrl}/animes/${anime_id}`);
  }

  getAnimeReview(anime_id) {
    return this.http.get<Anime>(
      `${environment.apiUrl}/animes/${anime_id}/reviews`
    );
  }

  getWordCloud(anime_id) {
    return this.http.get<Anime>(
      `${environment.apiUrl}/animes/${anime_id}/wordcloud`
    );
  }

  resetSearch() {
    this.search_result = new BehaviorSubject('');
    this.currentSearch = this.search_result.asObservable();
  }

  getEp(anime_id, ep_num) {
    return this.http.get<AnimeEp>(
      `${environment.apiUrl}/animes/${anime_id}/episode/${ep_num}`
    );
  }

  getScore(anime_id) {
    return this.http.get<AnimeEp>(
      `${environment.apiUrl}/animes/${anime_id}/stats`
    );
  }

  getSimilars(anime_id) {
    return this.http.get(
      `${environment.apiUrl}/animes/${anime_id}/similar_animes`
    );
  }

  searchAnime(name) {
    this.http
      .post(`${environment.apiUrl}/search`, { partial_name: name })
      .subscribe((data) => {
        this.search_result.next(data);
      });
  }
}
