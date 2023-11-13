import {
  AfterViewChecked,
  AfterViewInit,
  Component,
  OnInit,
  Pipe,
  PipeTransform,
  ViewEncapsulation,
} from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { ActivatedRoute } from '@angular/router';
import { AnimeService } from '@app/_services/anime.service';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '@environments/environment';
import { Anime, User } from '@app/_models';
import * as d3 from 'd3';
import * as d3cloud from 'd3-cloud';
import {AccountService} from '@app/_services';

@Pipe({ name: 'safe' })
export class SafePipe implements PipeTransform {

  constructor(private sanitizer: DomSanitizer) {}
  transform(url) {
    return this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}

@Pipe({
  name: 'safeHtml',
})
export class SafeHtmlPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(html) {
    return this.sanitizer.bypassSecurityTrustHtml(html);
  }
}

@Component({
  selector: 'app-anime-details',
  templateUrl: './anime-details.component.html',
  styleUrls: ['./anime-details.component.less'],
  encapsulation: ViewEncapsulation.None,
})
export class AnimeDetailsComponent implements AfterViewChecked {
  user: User;
  episode_url: any;
  score_url: any;
  anime_id = 0;
  anime: Anime;
  similars = [];
  reviews;
  layout;
  myStyle: SafeHtml;
  private cloudsvg;
  private cloudMargin = { top: 10, right: 10, bottom: 10, left: 10 };
  cloudWidth = 950 - this.cloudMargin.left - this.cloudMargin.right;
  cloudHeight = 550 - this.cloudMargin.top - this.cloudMargin.bottom;
  myWords;

  constructor(
    private accountService: AccountService,
    private route: ActivatedRoute,
    public animeService: AnimeService,
    private http: HttpClient,
    private sanitizer: DomSanitizer
  ) {
    this.myStyle = this.sanitizer.bypassSecurityTrustHtml(
      `<style>
        .score-stats {
          width: 900px;
        }
      }</style>`
    );
    this.accountService.user.subscribe((x) => {(this.user = x); console.log(this.user)});
    this.route.paramMap.subscribe((params) => {
      animeService.resetSearch();
      this.anime_id = +params.get('anime_id');

      animeService.getAnime(this.anime_id).subscribe((data) => {
        this.anime = data;
      });
      animeService.getWordCloud(this.anime_id).subscribe((data) => {
        this.myWords = data;
        // Constructs a new cloud layout instance. It run an algorithm to find the position of words that suits your requirements
        this.layout = d3cloud()
          .size([this.cloudWidth, this.cloudHeight])
          .words(
            this.myWords.map(function (d) {
              return { text: d.word, size: d.size };
            })
          )
          .padding(10)
          .fontSize(function (d) {
            return d.size;
          });
      });
      animeService.getAnimeReview(this.anime_id).subscribe((data) => {
        this.reviews = data;
      });
      animeService.getEp(this.anime_id, 1).subscribe((data) => {
        this.episode_url = data.ep_url;
      });
      animeService.getScore(this.anime_id).subscribe((data) => {
        this.score_url = data['score-table'];
      });
      animeService.getSimilars(this.anime_id).subscribe((data) => {
        for (var sim in data) {
          animeService.getAnime(data[sim]['anime_id']).subscribe((data) => {
            this.similars.push(data);
          });
        }
      });
    });
  }

  ngAfterViewChecked() {
    this.wordSvg();
    this.layout.start();
    this.draw(this.layout.words());
  }

  numSequence(n: number): Array<number> {
    return Array(n);
  }

  newEp(ep: number) {
    this.http
      .get(`${environment.apiUrl}/animes/${this.anime_id}/episode/${ep}`)
      .subscribe((data) => {
        this.episode_url = data['ep_url'];
      });
  }
  clear() {
    this.similars = [];
  }

  // append the svg object to the body of the page
  wordSvg(): void {
    d3.selectAll('figure#wordcloudd > *').remove();
    this.cloudsvg = d3
      .select('figure#wordcloudd')
      .append('svg')
      .attr(
        'width',
        this.cloudWidth + this.cloudMargin.left + this.cloudMargin.right
      )
      .attr(
        'height',
        this.cloudHeight + this.cloudMargin.top + this.cloudMargin.bottom
      )
      .append('g')
      .attr(
        'transform',
        'translate(' + this.cloudMargin.left + ',' + this.cloudMargin.top + ')'
      );
  }

  // This function takes the output of 'layout' above and draw the words
  // Better not to touch it. To change parameters, play with the 'layout' variable above
  private draw(words): void {
    let c = d3.scaleSequential(d3.interpolateInferno).domain([0, 35]);
    this.cloudsvg
      .append('g')
      .attr(
        'transform',
        'translate(' +
          this.layout.size()[0] / 2 +
          ',' +
          this.layout.size()[1] / 2 +
          ')'
      )
      .selectAll('text')
      .data(words)
      .enter()
      .append('text')
      .style('font-size', function (d) {
        return d.size + 'px';
      })
      .style('fill', function (d, i) {
        return c(i);
      })
      .attr('text-anchor', 'middle')
      .attr('transform', function (d) {
        return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
      })
      .text(function (d) {
        return d.text;
      });
  }
}
