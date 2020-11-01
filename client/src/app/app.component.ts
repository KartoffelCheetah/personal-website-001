import { Component, OnInit } from '@angular/core';
import { ROUTING, getRoute } from '../environments/api-route';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.styl']
})
export class AppComponent implements OnInit {
  title = 'client';
  images: object[] = [];

  async ngOnInit() {
    const response = await fetch(getRoute(['RI', 'IMAGE', 'LIST']));
    if (response.ok) {
      this.images = (await response.json()).map( i => ({ ...i, resource: `${ROUTING.UPLOADS}/${i.resource}`}) );
    }
  }

}
