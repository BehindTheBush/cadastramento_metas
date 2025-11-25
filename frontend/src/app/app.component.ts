import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet],
  template: `
    <div class="app-container">
      <h1>Sistema de Cadastramento de Metas</h1>
      <p>Aplicação configurada e pronta para desenvolvimento!</p>
      <router-outlet></router-outlet>
    </div>
  `,
  styles: [`
    .app-container {
      padding: 2rem;
      text-align: center;
    }
    h1 {
      color: #3b82f6;
    }
  `]
})
export class AppComponent {
  title = 'Sistema de Cadastramento de Metas';
}
