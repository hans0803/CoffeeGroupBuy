# Changelog

All notable changes to the Coffee Group Buy project will be documented in this file.

## [Unreleased] - 2026-03

### Added
- **Mobile Bottom Navigation**: Introduced a sticky bottom navigation bar for viewports ≤ 768px, providing immediate access to Home, Products, Orders, and Cart.
- **Swipe-Dismissible Filter Sidebar**: Transformed the desktop sidebar filter into a modern, modal bottom-sheet on mobile.
- **Product Review System**: Added a modal/bottom-sheet system for users to write and view 5-star product reviews and comments.
- **"本次新品" (New Products) Tag**: Implemented backend logic to automatically flag and display products added in the most recent update batch.
- **Real-Time Sales Dashboard**: Replaced static dashboard visuals with dynamic Chart.js charts (Roast preference, Price distribution) that update immediately after order submission.

### Changed
- **Touch Target Accessibility**: Enforced a minimum touch target size of 44x44px for all interactive elements (add-to-cart buttons, quantity adjusters, checkout buttons) for improved mobile usability.
- **Mobile Filter UX**: Optimized the filter interaction on mobile using instant state toggles (`display: none` -> `block`) and removed transitions during page reload to eliminate visual flickering.

### Fixed
- **Home Page `TypeError`**: Fixed a critical error on the index route that caused server crashes when attempting to render legacy order items.
- **Sidebar Blocking Bug**: Fixed an issue where the closed mobile filter sidebar's invisible bounding box and shadow would cover and block clicks on the bottom navigation bar.
- **Submenu Animation Jitter**: Corrected CSS transition properties on bottom navigation submenus to prevent jittering when toggled rapidly.
