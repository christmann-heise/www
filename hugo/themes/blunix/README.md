# Hugo Theme Blunix

A professional, clean Hugo theme designed for consulting and service-based businesses. Features a flexible block-based page layout system, multilingual support, and modern responsive design.

## Preview

![Theme Screenshot](https://raw.githubusercontent.com/Blunix-GmbH/hugo-theme-blunix/main/images/screenshot.png)
![Theme Thumbnail](https://raw.githubusercontent.com/Blunix-GmbH/hugo-theme-blunix/main/images/tn.png)

## Features

- **Block-based page builder** — Compose pages from reusable content blocks
- **Multilingual support** — Built-in i18n with English and German translations
- **Responsive design** — Mobile-first with Tailwind CSS
- **SEO optimized** — OpenGraph, Twitter Cards, and semantic markup
- **Service business focused** — Pricing tables, contact sections, and FAQ blocks
- **Clean codebase** — Modular partials and well-organized templates

## Prerequisites

- **Hugo Extended** (v0.120.0 or later) — [Installation guide](https://gohugo.io/installation/)
- **Go** (v1.21 or later) — Required for Hugo Modules — [Installation guide](https://go.dev/doc/install)

No Node.js or npm required — CSS is pre-compiled.

## Installation

### As a Hugo Module (Recommended)

Initialize your site as a Hugo Module (if not already):

```bash
hugo mod init github.com/<your-username>/<your-site>
```

Add the theme to your `hugo.toml` (or `config/_default/hugo.toml`):

```toml
[module]
  [[module.imports]]
    path = "github.com/Blunix-GmbH/hugo-theme-blunix"
```

Then download the module:

```bash
hugo mod get -u
```

> **Note:** When using Hugo Modules, you do **not** need to set `theme = "..."` in your config. The module import replaces that directive.

### As a Git Submodule

From your Hugo site root:

```bash
git submodule add https://github.com/Blunix-GmbH/hugo-theme-blunix.git themes/hugo-theme-blunix
```

Then activate the theme in your `config.toml` or `config/_default/config.toml`:

```toml
theme = "hugo-theme-blunix"
```

### As a Local Theme Folder (No Modules/Submodules)

Copy or clone the theme directly into your site's `themes/` directory:

```bash
mkdir -p themes
git clone https://github.com/Blunix-GmbH/hugo-theme-blunix.git themes/hugo-theme-blunix
```

Then set the theme in your config:

```toml
theme = "hugo-theme-blunix"
```

### Cloning a Site That Uses This Theme as a Submodule

```bash
git clone --recurse-submodules <your-site-repo>
```

Or if you've already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Configuration

### Basic Configuration

Minimum required in `config/_default/config.toml`:

```toml
baseURL = 'https://example.com/'
languageCode = 'en'
title = 'Your Company Name'
```

### Parameters

Configure site parameters in `config/_default/params.toml`:

```toml
logo = '/images/logo.svg'
footer_logo = '/images/logo-full.svg'
featured_image = 'featured.webp'

[[contact]]
name = "contact@example.com"
icon = "fa-solid fa-envelope"
link = "mailto:contact@example.com"

[[contact]]
name = "+1 234 567 890"
icon = "fa-solid fa-phone"
link = "tel:+1234567890"
```

### Multilingual Setup

Configure languages in `config/_default/languages.toml`:

```toml
[en]
languageName = "English"
languageCode = "en-us"
contentDir = "content/en"
title = "Your Company"
weight = 1

[de]
languageName = "Deutsch"
languageCode = "de"
contentDir = "content/de"
title = "Ihr Unternehmen"
weight = 2
```

See the `exampleSite/` directory for a complete working example.

## Block-Based Page Layout

Pages are composed from reusable "blocks" defined in front matter. The theme loops through the `blocks` array and renders each block partial.

### How It Works

1. Define blocks in your page's front matter under the `blocks` key
2. Each block must have a `block` field matching a partial name in `layouts/partials/blocks/`
3. Blocks render in the order they appear in the array
4. Additional parameters are passed to the block partial

### Example Page

```yaml
---
title: "Our Services"
description: "Professional consulting services"

blocks:
  - block: hero-breadcrumb
    title: "Services"
    subtitle: "Expert Solutions for Your Business"
    background: "/images/services/hero.webp"
    breadcrumb: "Services"

  - block: text-image
    title: "Custom Solutions"
    text: "We provide tailored consulting services..."
    image:
      src: "/images/services/consulting.webp"
      alt: "Consulting services"
    reverse: false

  - block: features-grid
    title: "What We Offer"
    items:
      - icon: "fa-solid fa-server"
        title: "Infrastructure"
        description: "Scalable server solutions"
      - icon: "fa-solid fa-shield"
        title: "Security"
        description: "Enterprise-grade protection"

  - block: cta
    title: "Ready to Get Started?"
    text: "Contact us today for a consultation"
    button:
      text: "Get in Touch"
      link: "/contact/"
---
```

## Available Blocks

This streamlined theme build includes the following blocks:

- **`hero`** — Full-width hero section with image background
- **`hero-breadcrumb`** — Hero with breadcrumb navigation
- **`banner`** — Simple banner section
- **`about`** — About section with image and text columns
- **`text-image`** — Text alongside image (left/right configurable)
- **`text-image-bg`** — Text with image and section background styling
- **`features-grid`** — Grid of features with icons
- **`process-timeline`** — Process steps timeline
- **`faq`** — Accordion-style FAQ
- **`pricing-tabs`** — Tabbed pricing tables
- **`ethics-accordion`** — Expandable ethics/values section
- **`partners-scroller`** — Scrolling partner logos
- **`contact-standard`** — Contact information section
- **`cta`** — Call-to-action section

## Multilingual Support

The theme includes translation files in `i18n/`:

- `en.yaml` — English
- `de.yaml` — German

Use translations in templates:

```go-html-template
{{ i18n "read_more" }}
{{ i18n "contact_us" }}
```

Add custom translations by extending these files in your site's `i18n/` directory.

## Theme Structure

```
hugo-theme-blunix/
├── archetypes/          # Content templates
│   └── default.md
├── assets/              # Assets for Hugo Pipes processing
│   └── images/          # Theme images (logo, icons)
├── exampleSite/         # Demo site
│   ├── config/
│   └── content/
├── i18n/                # Translation files
│   ├── en.yaml
│   └── de.yaml
├── layouts/
│   ├── _default/        # Default templates
│   │   ├── baseof.html
│   │   ├── single.html
│   │   ├── list.html
│   │   └── _markup/     # Custom render hooks
│   ├── blog/            # Blog-specific templates
│   ├── partials/
│   │   ├── blocks/      # Block components (14 blocks)
│   │   ├── components/  # Reusable UI components
│   │   ├── helpers/     # Helper partials
│   │   ├── _funcs/      # Utility functions
│   │   ├── head.html
│   │   ├── header.html
│   │   └── footer.html
│   └── shortcodes/      # Custom shortcodes
├── static/              # Static assets
│   ├── css/             # Compiled CSS
│   ├── js/              # JavaScript (Alpine.js, Prism.js)
│   ├── fonts/           # Web fonts (Nunito, EB Garamond)
│   ├── libs/            # Third-party libraries
│   └── images/          # Static images
├── go.mod               # Hugo Modules definition
├── hugo.toml            # Module configuration
├── theme.toml           # Theme metadata
└── LICENSE
```

## Updating the Theme

### Hugo Modules

```bash
hugo mod get -u github.com/Blunix-GmbH/hugo-theme-blunix
```

To pin to a specific version:

```bash
hugo mod get github.com/Blunix-GmbH/hugo-theme-blunix@v1.0.0
```

### Git Submodule

```bash
git submodule update --remote --merge themes/hugo-theme-blunix
git add themes/hugo-theme-blunix
git commit -m "Update theme to latest version"
```

## Development

### Running the Example Site

```bash
cd exampleSite
hugo server --themesDir ../..
```

### Production Build

```bash
hugo --minify
```

Output goes to `public/` directory.

## Customization

### Override Templates

To customize a theme template, copy it from the theme's `layouts/` to your site's `layouts/` directory with the same path. Your version will take precedence.

```bash
mkdir -p layouts/partials
cp themes/hugo-theme-blunix/layouts/partials/footer.html layouts/partials/footer.html
```

### Override Styles

To customize styles, copy `static/css/style.css` to your site's `static/css/` directory and modify it. Your version will take precedence.

### Add Custom Blocks

Create new blocks in your site's `layouts/partials/blocks/` directory. They'll be available alongside theme blocks.

## Linux Support

For issues, questions, or contributions, please contact Blunix GmbH or open an issue in the theme repository.

Author information: [Blunix Ansible Role - Apache2](https://github.com/Blunix-GmbH/ansible-role-apache2?tab=readme-ov-file#author-information)

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Credits

Developed and maintained by [Blunix GmbH](https://www.blunix.com)
