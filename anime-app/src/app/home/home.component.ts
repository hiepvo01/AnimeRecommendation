import {HttpClient} from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { User } from '@app/_models';
import { AccountService } from '@app/_services';
import {environment} from '@environments/environment';
import * as d3 from 'd3';
import * as d3cloud from 'd3-cloud';
import { Planet } from '../_models/planet';
import { AnimeService } from '../_services/anime.service';
@Component({ templateUrl: 'home.component.html' })
export class HomeComponent implements OnInit {
  user: User;
  private svg;

  private cloudsvg;
  private cloudMargin = { top: 10, right: 10, bottom: 10, left: 10 };
  cloudWidth = 450 - this.cloudMargin.left - this.cloudMargin.right;
  cloudHeight = 450 - this.cloudMargin.top - this.cloudMargin.bottom;
  myWords = [
    { word: 'Running', size: 10 },
    { word: 'Surfing', size: 20 },
    { word: 'Climbing', size: 50 }, 
    { word: 'Kiting', size: 30 },
    { word: 'Sailing', size: 20 },
    { word: 'Snowboarding', size: 60 },
  ];

  // Constructs a new cloud layout instance. It run an algorithm to find the position of words that suits your requirements
  layout = d3cloud()
    .size([this.cloudWidth, this.cloudHeight])
    .words(
      this.myWords.map(function (d) {
        return { text: d.word, size:d.size };
      })
    )
    .padding(10)
    .fontSize(function(d) { return d.size; })

  private margin = 50;
  private width = 750 - this.margin * 2;
  private height = 400 - this.margin * 2;

  constructor(
    private accountService: AccountService,
    private http: HttpClient,
    private animes: AnimeService
  ) {
    this.user = this.accountService.userValue['user'];
    console.log(this.user);
    this.animes.getMostScore();
  }

  ngOnInit(): void {
    this.createSvg();
    d3.json<Planet[]>(`${environment.apiUrl}/planets`).then((data) =>
      this.drawBars(data)
    );
    this.wordSvg();
    this.layout.start();
    console.log(this.layout.words());
    this.draw(this.layout.words());
  }

  private createSvg(): void {
    this.svg = d3
      .select('figure#bar')
      .append('svg')
      .attr('width', this.width + this.margin * 2)
      .attr('height', this.height + this.margin * 2)
      .append('g')
      .attr('transform', 'translate(' + this.margin + ',' + this.margin + ')');
  }

  // append the svg object to the body of the page
  private wordSvg(): void {
    this.cloudsvg = d3
      .select('figure#wordcloud')
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
      .attr('text-anchor', 'middle')
      .attr('transform', function (d) {
        return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
      })
      .text(function (d) {
        return d.text;
      });
  }

  private drawBars(data: Planet[]): void {
    // Create the X-axis band scale
    const x = d3
      .scaleBand()
      .range([0, this.width])
      .domain(data.map((d) => d.planet_name))
      .padding(0.2);

    // Draw the X-axis on the DOM
    this.svg
      .append('g')
      .attr('transform', 'translate(0,' + this.height + ')')
      .call(d3.axisBottom(x))
      .selectAll('text')
      .attr('transform', 'translate(-10,0)rotate(-45)')
      .style('text-anchor', 'end');

    // Create the Y-axis band scale
    const y = d3.scaleLinear().domain([0, 5000]).range([this.height, 0]);

    // Draw the Y-axis on the DOM
    this.svg.append('g').call(d3.axisLeft(y));

    // Create and fill the bars
    this.svg
      .selectAll('bars')
      .data(data)
      .enter()
      .append('rect')
      .attr('x', (d) => x(d.planet_name))
      .attr('y', (d) => y(d.radius))
      .attr('width', x.bandwidth())
      .attr('height', (d) => this.height - y(d.radius))
      .attr('fill', '#d04a35');
  }
}
