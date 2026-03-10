# Changelog

All notable changes to the Coffee Group Buy project will be documented in this file.

## [1.1.1] - 2026-03-11
### Added
- **New Products Filtering**: Enabled full support for roast level and price filters on the "本次新品" (New Products) sheet.
- **Extreme Mobile UX Fix**: Implemented the "Physical Removal" strategy for the product sidebar. Using `display: none` by default and a two-phase JS toggle to completely eliminate rendering flickers in Safari and other browsers.

## [1.1.0] - 2026-03-10
### Added
- **Hybrid Database Engine**: Added support for **PostgreSQL (Neon)** alongside local **SQLite**. The system automatically detects `DATABASE_URL` to switch modes.
- **Vercel Cloud Deployment**: Fully compatible with Vercel's serverless environment.
- **Remote Image Support**: Scraper now stores remote product image URLs, enabling deployment on platforms without persistent storage (like Vercel).
- **Dynamic Real-Time Stats**: Refactored the homepage statistics to calculate directly from the database, ensuring accurate charts in ephemeral cloud environments.

### Changed
- **Mobile Filter Performance**: Implemented "Instant Hide" logic for bottom sheets and navigation sub-menus to eliminate flickering during page reloads.

### Fixed
- **Historical Stats Restoration**: Recovered and synchronized missing historical purchase counts to the cloud database.
- **"本次新品" Logic Fix**: Corrected a bug where the cloud migration reset all timestamps, causing all products to appear as "New". Now correctly displays only the most recent batch.
- **Sidebar Click Blocking**: Fixed a CSS regression where the hidden filter sidebar would still capture clicks on mobile.

## [1.0.1] - 2026-03
### Added
- **Mobile Bottom Navigation**: Introduced a sticky bottom navigation bar for viewports ≤ 768px.
- **Product Review System**: Added a modal/bottom-sheet system for product reviews.
- **"本次新品" Tag**: Automarking products added in the most recent update batch.
- **Real-Time Sales Dashboard**: Dynamic Chart.js charts.

### Changed
- **Touch Target Accessibility**: Enforced minimum touch target size of 44x44px.
- **Mobile Filter UX**: Optimized interaction using instant state toggles.

### Fixed
- **Home Page TypeError**: Fixed server crash on index route.
- **Sidebar Blocking Bug**: Fixed click-blocking issue with hidden sidebar.
- **Submenu Animation Jitter**: Corrected CSS transitions on submenus.
