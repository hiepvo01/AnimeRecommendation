import { Component, OnInit  } from '@angular/core';
import { AccountService } from './_services';
import { User } from './_models';
import { AnimeService } from './_services/anime.service';
import {Router} from '@angular/router';

@Component({ selector: 'app', templateUrl: 'app.component.html' })
export class AppComponent implements OnInit{
  user: User; 
  search_result :any;

  constructor(
    private accountService: AccountService,
    private animeService: AnimeService,
    private router: Router,
  ) {
    this.accountService.user.subscribe((x) => (this.user = x));
  }
  ngOnInit() {
    (function(d, m) {
    var kommunicateSettings = {
      "appId": "24d4c8448813785f025a9377cf9ad4507",
      "popupWidget": true,
      "automaticChatOpenOnNavigation": true
      };

      var s = document.createElement("script");
      s.type = "text/javascript";
      s.async = true;
      s.src = "https://widget.kommunicate.io/v2/kommunicate.app";
      var h = document.getElementsByTagName("head")[0];
      h.appendChild(s);
      (window as any).kommunicate = m;
      m._globals = kommunicateSettings;
    })(document, (window as any).kommunicate || {});
    /* NOTE : Use web server to view HTML files as real-time update will not work if you directly open the HTML file in the browser. */
  }

  logout() {
    this.accountService.logout();
  }

  save(event) {
    this.animeService.searchAnime(event.target.value);
    this.router.navigate(['/animes']);
  }
}
