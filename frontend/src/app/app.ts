import { Component } from '@angular/core';
import { DocumentCompareComponent } from './pages/document-compare/document-compare.component';

@Component({
  selector: 'app-root',
  imports: [DocumentCompareComponent],
  template: '<app-document-compare></app-document-compare>',
  styleUrls: ['./app.css']
})
export class App {}
