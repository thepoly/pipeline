import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';
import { AppModule } from './app.module';
const platform = platformBrowserDynamic();
platform.bootstrapModule(AppModule);

// saw
// platformBrowserDynamic().bootstrapModule(AppModule);
// used in tutorial as well; does that work as well?
