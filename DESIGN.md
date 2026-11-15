---
name: Ron Systems AI
description: The Docket Rail. White thermal dockets on a stainless rail, printed in black with one red for work that now runs by itself.
colors:
  paper: "#F3F4F1"
  paper-2: "#E8EAE5"
  white: "#FFFFFF"
  ink: "#17171B"
  ink-2: "#45474F"
  ink-3: "#62656D"
  rule: "#D3D6CF"
  rule-strong: "#B9BDB5"
  red: "#D62839"
  red-deep: "#AE1C2B"
  red-wash: "#FCEBED"
  steel-hi: "#F8F9FA"
  steel-1: "#D9DDE1"
  steel-2: "#B4BBC2"
  steel-3: "#8B939B"
  steel-4: "#5E656C"
typography:
  display:
    fontFamily: "Big Shoulders Display, Arial Narrow, sans-serif"
    fontSize: "clamp(3.1rem, 6.6vw, 6rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.005em"
  headline:
    fontFamily: "Big Shoulders Display, Arial Narrow, sans-serif"
    fontSize: "clamp(2.4rem, 4.6vw, 4rem)"
    fontWeight: 800
    lineHeight: 0.94
    letterSpacing: "-0.005em"
  headline-m:
    fontFamily: "Big Shoulders Display, Arial Narrow, sans-serif"
    fontSize: "clamp(1.9rem, 3.2vw, 2.6rem)"
    fontWeight: 800
    lineHeight: 0.94
  title:
    fontFamily: "Big Shoulders Display, Arial Narrow, sans-serif"
    fontSize: "1.75rem"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "0.01em"
  lede:
    fontFamily: "Hanken Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(1.125rem, 1.6vw, 1.3rem)"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "Hanken Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Hanken Grotesk, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.78rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.07em"
  docket:
    fontFamily: "Martian Mono, ui-monospace, Cascadia Mono, Menlo, monospace"
    fontSize: "0.76rem"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "tnum"
  docket-bar:
    fontFamily: "Martian Mono, ui-monospace, Cascadia Mono, Menlo, monospace"
    fontSize: "0.76rem"
    fontWeight: 700
    lineHeight: 1.6
    letterSpacing: "0.05em"
rounded:
  none: "0px"
  hardware: "4px"
spacing:
  gutter: "clamp(16px, 4vw, 48px)"
  wrap: "1240px"
  section: "clamp(4.5rem, 10vw, 8.5rem)"
  docket-pad: "1.05rem"
  tooth: "14px"
components:
  button-primary:
    backgroundColor: "{colors.red}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "1.05rem 1.35rem 1rem"
  button-primary-hover:
    backgroundColor: "{colors.red-deep}"
    textColor: "{colors.white}"
  button-primary-small:
    backgroundColor: "{colors.red}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "0.7rem 1rem 0.65rem"
  icon-button:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    size: "48px"
  icon-button-hover:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
  docket:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    typography: "{typography.docket}"
    rounded: "{rounded.none}"
    padding: "0 1.05rem 1.9rem"
  docket-bar:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    typography: "{typography.docket-bar}"
    padding: "0.7rem 1.05rem 0.6rem"
  flag:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    rounded: "{rounded.none}"
    padding: "0.28em 0.6em"
  input:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.85rem 1rem"
  input-error:
    backgroundColor: "{colors.red-wash}"
    textColor: "{colors.ink}"
  filed-job-side:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    padding: "1.75rem 1.5rem"
  footer:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
---

# Design System: Ron Systems AI

## Overview

**Creative North Star: "The Docket Rail"**

Every manual task in a business is a printed docket. The site is a pass in a busy kitchen or a print shop: a cool paper ground, white thermal dockets clipped to a brushed-stainless rail, printed in black. A single printer red marks the moment work changes hands from a person to a system: the Result of a filed job and the one action that starts the job. The world is literal and material. Paper has grain, torn serrated edges, and a soft shadow. Steel has a brushed raster and a highlight. Nothing is glass, and no surface wears a decorative color gradient.

Density is a working counter's, not a gallery's. Big condensed display type in uppercase does the shouting. Hanken Grotesk carries plain-English explanation at a readable measure. Martian Mono appears only where a printer would have printed: on dockets, receipts, slips, filed jobs, and the done tag. The page is light only; there is no dark theme.

Motion is kept to a minimum. There are no entrance animations; the hero is still, centered type on the ledger grid. The one ambient exception is the tool strip under the hero: tool marks (never client logos) drift left in Light Print at a slow linear pace, pause on hover, fade at both ends with a mask, and sit as a static wrapped list under reduced motion. Every other element simply sits on the page.

**Key Characteristics:**
- Cool paper ground, white textured dockets with serrated edges, brushed-steel rail and spikes.
- Print black plus one red; red means "changed or automated" and "act here", nothing else.
- Printer discipline on dockets: two sizes, rank by weight, caps, red ink, and reversed black bars.
- Square corners everywhere paper and ink meet; small radii only on steel hardware.
- Depth comes from paper lifting off paper (drop-shadow on the torn silhouette), not from cards.
- No entrance animation; the only ambient motion is the tool strip under the hero.

## Colors

Print black on cool paper, with steel for hardware and a single printer red held back for the automated state and the primary action.

### Primary
- **Printer Red** (`red`): the only chromatic color. Used for the tear-off stub background, the RON block in the wordmark, the error border on fields and alerts, text selection, and the caret.
- **Deep Printer Red** (`red-deep`): red as text on white or paper, where Printer Red would be too light for small type. The Result label in filed jobs, field error messages, alert text, and the stub hover.
- **Red Wash** (`red-wash`): the tint behind an errored field and an alert. Never decorative.

### Neutral
- **Cool Paper** (`paper`): the page ground and masthead.
- **Counter Paper** (`paper-2`): alternating section bands (services, work, FAQ, alt blocks), the scrollbar track, inline code.
- **Thermal White** (`white`): docket, receipt, slip, filed-job, and order-type surfaces, always under the paper-grain raster; also inputs and icon buttons at rest.
- **Print Black** (`ink`): headings, body text, docket bars, reversed flags and tags, filed-job side panels, the footer, focus outlines, and every hover fill.
- **Faded Print** (`ink-2`): secondary prose, ledes, descriptions.
- **Light Print** (`ink-3`): struck task text, captions, meta, placeholders, quiet underline color.
- **Hairline** (`rule`) and **Dashed Rule** (`rule-strong`): section dividers and the dashed rules between docket and list lines.
- **Brushed Steel** (`steel-hi` through `steel-4`): rail, docket clips, and spike rods. The rail's texture comes from `rail-steel.png` over `steel-2`.

### Named Rules
**The Red Means Automated Rule.** Red is reserved for the Result label in filed jobs, the tear-off stub, error states, text selection, and the RON wordmark block. Flags, checkmarks, step numbers, link underlines, and hovers are ink or reversed, never red. If a new element wants red, ask whether it shows work that now runs by itself or is the one action to take; if not, it is ink.

**The Reversed Bar Rule.** Emphasis is reversed printing (white on Print Black), not a new color. Docket bars, flags, tags, filed-job sides, and hover fills all reverse.

## Typography

**Display Font:** Big Shoulders Display (with Arial Narrow, sans-serif)
**Body Font:** Hanken Grotesk (with ui-sans-serif, system-ui)
**Label/Mono Font:** Martian Mono (with ui-monospace, Cascadia Mono, Menlo), docket surfaces only

**Character:** A condensed, heavy display face that reads like a stencilled order board, paired with a warm, plain grotesk for honest explanation. The mono is the printer's voice and only speaks on paper the printer produced.

All three families are self-hosted variable fonts.

### Hierarchy
- **Display** (800, clamp(3.1rem, 6.6vw, 6rem), 0.94): the hero headline and inner-page titles. Balanced wrapping.
- **Headline** (800, clamp(2.4rem, 4.6vw, 4rem), 0.94): section headings; a smaller step (clamp(1.9rem, 3.2vw, 2.6rem)) for secondary sections.
- **Title** (800, 1.5 to 1.9rem, 1 to 1.05, uppercase): docket titles, receipt item names, order-type names, filed-job titles, list and service-index headings, prose h2 (2rem).
- **Lede** (400, clamp(1.125rem, 1.6vw, 1.3rem), 1.55, `ink-2`): the paragraph under a page or section title, max 38em.
- **Body** (400, 1.0625rem, 1.6; 1rem under 640px): all prose, capped at 68ch (articles and videos: 90ch).
- **Label** (700, 0.7 to 0.78rem, 0.06 to 0.07em tracking, uppercase, Hanken Grotesk): field labels, footer heads, tools terms, meta lines, order-type format, flags and tags.
- **Docket** (Martian Mono, 0.66 to 0.8rem via a per-docket size variable, tabular numerals; bars and labels 700 uppercase at 0.05em): docket lines, bars, receipt head and total, slip heads, filed-job dt and tag, done tag.

### Named Rules
**The Printer's Voice Rule.** Monospace appears only on docket surfaces (dockets, receipt, filed jobs, slips, done tag), prose table headers and inline code, and timeline dates. Labels anywhere else are Hanken Grotesk, uppercase, tracked. Explanatory sentences that sit on a docket (stage descriptions, agenda items) switch back to Hanken Grotesk.

**The Two Sizes Rule.** On a docket, rank by weight, caps, reversal, and red ink, not by adding sizes. A docket carries its mono size and at most one display title.

## Layout

Content sits in a 1240px wrap with a fluid gutter (clamp(16px, 4vw, 48px)), except the masthead and the home hero, which run full width with only the gutter as inset. The hero is a single centered column: headline, lede, and actions centered. The home hero lies on a ledger grid: 40px squares in 1px Print Black hairlines at 7.5% opacity, fading out toward the bottom of the hero with a mask. No other section carries the grid; sections breathe with a fluid vertical rhythm (clamp(4.5rem, 10vw, 8.5rem)). Most sections are asymmetric two-column grids (roughly 4:8 or 5:7) with a sticky intro column on wide screens; bands alternate between Cool Paper and Counter Paper, separated by hairlines.

The docket module is 42 characters of mono plus padding. Stage dockets on the process rail are 19rem wide in a horizontal scroll-snap track that bleeds to the viewport edge, with previous and next icon buttons. A full-bleed rail runs across the top of the hero, every page head, and the booking close, and dockets hang from it by a steel clip.

Breakpoints: 1100px (filed jobs stack to one column), 900px (nav collapses behind a Menu toggle into a paper drop-down), 860px (all two-column grids and order types stack), 640px (docket type and padding shrink).

## Elevation & Depth

Depth is physical: paper lifts off paper. Torn and serrated shapes are cut with a mask on a `::before` layer, and the shadow is a `filter: drop-shadow` on the element itself so it follows the torn silhouette instead of a rectangle. Steel hardware gets small, tight box-shadows and an inset highlight. There is no layered card elevation scale and no shadow on hover.

### Shadow Vocabulary
- **Paper lift** (`filter: drop-shadow(0 1px 0.5px rgba(23,23,27,.12)) drop-shadow(0 16px 18px rgba(23,23,27,.14))`): every paper surface: dockets, slips, receipt, filed jobs, order-type panel, portrait.
- **Rail** (`box-shadow: 0 1px 0 rgba(255,255,255,.8) inset, 0 7px 10px -6px rgba(23,23,27,.45)`): the stainless rail, plus a 3px fade beneath it.
- **Hardware** (`box-shadow: 0 2px 3px rgba(23,23,27,.3)` on clips; `2px 0 4px rgba(23,23,27,.22 to .3)` on spike rods): clips and spikes.
- **Stub lift** (`filter: drop-shadow(0 10px 12px rgba(174,28,43,.22))`): the full-size tear-off stub only.

### Named Rules
**The Torn Silhouette Rule.** A paper surface's edge is a mask, its shadow is a drop-shadow filter. Never box-shadow a torn edge.

## Shapes

Paper and ink are square: zero radius on dockets, slips, receipts, filed jobs, stubs, buttons, inputs, flags, and panels. Paper edges are serrated with a conic-gradient tooth (12 to 16px): dockets and slips on the bottom, the receipt on top and bottom, filed jobs on the right. The tear-off stub has two semicircular notches (7px radius) at the perforation, and the perforation itself is a dashed white line. Rounded corners belong only to steel hardware: clip bottoms (4px), spike rods and bases (3px), and the punched hole in each slip (a circle). Slips on the spike hang at small rotations (about -1.1 to 1.2 degrees); the stamp sits at -9 degrees.

## Components

### Buttons
Tactile and printed: the primary action is a ticket stub you tear off.
- **Shape:** square, with two semicircular notches at a dashed perforation near the right end.
- **Primary (tear-off stub):** Printer Red, white Big Shoulders Display 800 uppercase at 1.3rem with 0.04em tracking; the arrow sits in the torn-off end. It is the only red button, and there is one per view region (masthead, hero, close, booking).
- **Hover / Focus:** background deepens to Deep Printer Red and the stub end rotates 4 degrees and shifts 5px, as if being torn. Focus draws a 2px white outline inset 6px inside the label.
- **Small stub:** the masthead version: 1.05rem, no notches, no glow.
- **Icon button:** 48px square, white with a 1px ink border; hover reverses to ink. Disabled is 35% opacity.
- **Links:** Hanken Grotesk 600 with an `ink-3` underline (1.5px, 0.28em offset) that thickens to 3px in ink on hover; the arrow icon moves 4px right. Quiet links use a `rule-strong` underline.

### Chips (flags and tags)
- **Style:** reversed ink blocks, white Hanken Grotesk 700 uppercase at 0.7rem, 0.06em tracking, square. "Start here" and "Best place to start" flags ride inside a title; the "Example" tag leads the hero caption. Never red.

### Cards / Containers
The system has no generic cards. Containers are paper objects:
- **Docket:** white with grain, serrated bottom, steel clip on top, reversed ink bar (number left, title or "Free" right), dashed-rule lines, mono throughout. Variants: stage dockets on the process rail, and the booking ticket with a checklist, meta list, and stub.
- **Receipt:** serrated top and bottom, mono head with the display brand, double-rule dividers (3px double ink), each line a link with a display name, description, and a 44px arrow box that reverses and nudges on hover. Mono total and footer.
- **Slip on spike:** white slip with a punched hole, impaled on a steel rod, slight rotation, mono uppercase head, body text below.
- **Filed job:** a horizontal docket with a serrated right edge, reversed ink side panel (display title, mono tag), and a three-column body. Articles use it: every article in the homepage's Latest articles (up to three), and the newest article or video on its list page, with older items as plain rows below (title and date on the side; In short / What's inside / Read it, none in red). Case studies, when they return, use Problem / What I built / Result, where only the Result label is red.
- **Order-type panel:** one white strip divided into three by dashed vertical perforations, display names, and a ruled Hanken label for the format.

### Inputs / Fields
- **Style:** white, square, 1px `rule-strong` border with a 2px ink bottom rule; Hanken label above in uppercase tracked.
- **Focus:** the whole border turns ink with a 1px ink ring; no glow.
- **Error:** red border and bottom rule on a Red Wash fill, message below in Deep Printer Red 600. Alerts use Red Wash with a 2px red top rule.

### Navigation
- **Masthead:** Cool Paper, 76px tall. Wordmark in Big Shoulders Display 800 uppercase with RON reversed on a red block. Links in Hanken 600 with a 2px ink underline that draws from the left on hover and stays for the current page. The small stub closes the row.
- **Mobile (under 900px):** a bordered Menu toggle opens a full-width paper panel of ruled links, the current page underlined, and a centered stub.
- **Footer:** Print Black band, white wordmark rest, Hanken label heads, white links underlined on hover. Social profiles (YouTube, Facebook, LinkedIn, GitHub) sit under the email as 40px square outlined icon links that fill white on hover; all four always show, and one without a URL is a plain icon with no link or hover.

### Page head, steps, and FAQ
- **Page head:** full-bleed rail, optional back crumb, display title, lede.
- **Steps and checklists:** ruled lists with dashed separators; step numbers in Big Shoulders 900 ink; check icons in ink.
- **FAQ (details):** 2px ink top rule, 1.2rem Hanken 650 questions, a plus icon that rotates 45 degrees when open.

## Do's and Don'ts

### Do:
- **Do** put new content on paper objects that hang from or file off the rail: dockets, slips, receipts, filed jobs.
- **Do** cut paper edges with a conic-gradient mask on `::before` and shadow them with the paper-lift drop-shadow filter on the element.
- **Do** reverse to Print Black for emphasis, flags, bars, and hover fills.
- **Do** keep red to the eight reserved uses in The Red Means Automated Rule; use Deep Printer Red when red is small text on white.
- **Do** set dockets in Martian Mono with tabular numerals at the 42-column module, and switch explanatory sentences on them back to Hanken Grotesk.
- **Do** keep corners square on paper, ink, and controls; reserve small radii for steel hardware.
- **Do** ship any new motion as a finished state first, with a reduced-motion path that shows the end.

### Don't:
- **Don't** use red for flags, checkmarks, step numbers, link underlines, or hover states (the stub deepening to Deep Printer Red is the one red hover, because the stub is already red).
- **Don't** set labels in monospace off docket surfaces; use Hanken Grotesk uppercase tracked.
- **Don't** add entrance animations; all motion is state feedback (hovers, the stub tear, the FAQ plus, rail scrolling), plus the tool strip drift.
- **Don't** box-shadow a torn edge or add rectangular card shadows to paper.
- **Don't** introduce a second accent color, decorative color gradients, glass, or a dark theme. (Gradients used as drawing tools, such as perforations, masks, and the rail's shade, are native.)
- **Don't** add rounded corners to dockets, buttons, or inputs.
