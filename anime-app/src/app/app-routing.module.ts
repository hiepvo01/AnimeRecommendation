import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {AnimeDetailsComponent} from './anime-details/anime-details.component';
import {AnimesComponent} from './animes/animes.component';

import { HomeComponent } from './home';
import { AuthGuard } from './_helpers';
import { DescriptionComponent } from './description/description.component';

const accountModule = () => import('./account/account.module').then(x => x.AccountModule);
const usersModule = () => import('./users/users.module').then(x => x.UsersModule);

const routes: Routes = [
  { path: '', component: HomeComponent, canActivate: [AuthGuard] },
  { path: 'users', loadChildren: usersModule, canActivate: [AuthGuard] },
  { path: 'account', loadChildren: accountModule },
  { path: 'animes', component: AnimesComponent },
  { path: 'anime_detail/:anime_id', component: AnimeDetailsComponent },
  { path: 'description', component: DescriptionComponent },

  // otherwise redirect to home
  { path: '**', redirectTo: '' },
];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
