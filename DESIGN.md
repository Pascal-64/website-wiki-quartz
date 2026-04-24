# Design Systems

Source: Stitch MCP — Project `Technical Systems Portfolio` (`projects/16882277778253845806`)

---

## Design System: Structural Calm

- **Reference:** `assets/4fb05e4bd53a46f9b82983b4784855d9`
- **Version:** 1

### Theme Settings

| Property | Value |
| --- | --- |
| Color mode | `DARK` |
| Color variant | `FIDELITY` |
| Roundness | `ROUND_FOUR` |
| Spacing scale | `2` |
| Headline font | `SPACE_GROTESK` |
| Body font | `INTER` |
| Label font | `SPACE_GROTESK` |
| Primary override | `#003b5c` |
| Secondary override | `#00b4d8` |
| Tertiary override | `#2eb086` |
| Neutral override | `#0a0c10` |
| Custom color | `#003b5c` |

### Color Tokens

| Token | Hex |
| --- | --- |
| `background` | `#111318` |
| `on_background` | `#e2e2e8` |
| `surface` | `#111318` |
| `surface_dim` | `#111318` |
| `surface_bright` | `#37393e` |
| `surface_tint` | `#a0cbf3` |
| `surface_variant` | `#333539` |
| `surface_container_lowest` | `#0c0e12` |
| `surface_container_low` | `#1a1c20` |
| `surface_container` | `#1e2024` |
| `surface_container_high` | `#282a2e` |
| `surface_container_highest` | `#333539` |
| `on_surface` | `#e2e2e8` |
| `on_surface_variant` | `#c2c7ce` |
| `inverse_surface` | `#e2e2e8` |
| `inverse_on_surface` | `#2f3035` |
| `inverse_primary` | `#366285` |
| `primary` | `#a0cbf3` |
| `primary_container` | `#003b5c` |
| `primary_fixed` | `#cce5ff` |
| `primary_fixed_dim` | `#a0cbf3` |
| `on_primary` | `#003351` |
| `on_primary_container` | `#7aa5cc` |
| `on_primary_fixed` | `#001d31` |
| `on_primary_fixed_variant` | `#1a4a6c` |
| `secondary` | `#4cd6fb` |
| `secondary_container` | `#00b2d6` |
| `secondary_fixed` | `#b3ebff` |
| `secondary_fixed_dim` | `#4cd6fb` |
| `on_secondary` | `#003642` |
| `on_secondary_container` | `#003f4e` |
| `on_secondary_fixed` | `#001f27` |
| `on_secondary_fixed_variant` | `#004e5f` |
| `tertiary` | `#62dcaf` |
| `tertiary_container` | `#00402d` |
| `tertiary_fixed` | `#80f9ca` |
| `tertiary_fixed_dim` | `#62dcaf` |
| `on_tertiary` | `#003827` |
| `on_tertiary_container` | `#34b48a` |
| `on_tertiary_fixed` | `#002116` |
| `on_tertiary_fixed_variant` | `#00513b` |
| `error` | `#ffb4ab` |
| `error_container` | `#93000a` |
| `on_error` | `#690005` |
| `on_error_container` | `#ffdad6` |
| `outline` | `#8c9198` |
| `outline_variant` | `#42474e` |

---

## Design Strategy (designMd)

# Design System Strategy: The Technical Zen Garden

## 1. Overview & Creative North Star
The "Technical Zen Garden" is the guiding philosophy for this design system. It balances the cold, precise efficiency of a professional developer tool with the calm, intentional negative space of a high-end editorial publication.

The goal is to move away from the "generic template" look of portfolio sites. Instead of a standard 12-column grid, we utilize **Intentional Asymmetry**. Large, high-contrast typography scale is paired with deep, layered surfaces to create a sense of structural authority. The experience should feel like a custom-engineered dashboard—dense with information but light on visual noise.

**Creative North Star: The Digital Architect**
Everything is built on a foundation of structural clarity. We favor high-quality "invisible" design where the content is framed by the architecture, not buried under it.

---

## 2. Colors: Tonal Depth & The "No-Line" Rule
The palette is rooted in deep oceanic blues and technical neon accents, optimized for long-session readability and a premium "pro-tool" feel.

### The "No-Line" Rule
**Explicit Instruction:** Do not use 1px solid borders to section content. Traditional borders create visual clutter that breaks the "Zen" atmosphere.
- **Sectioning:** Define boundaries solely through background color shifts. For example, a `surface-container-low` section should sit directly against a `surface` background to define its territory.
- **Tonal Transitions:** Use the 8-step surface scale (`lowest` to `highest`) to imply hierarchy.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers.
*   **Base:** `surface` (#111318) for the main canvas.
*   **Secondary Sections:** `surface-container-low` (#1a1c20).
*   **Elevated Modules/Cards:** `surface-container-high` (#282a2e).

### The "Glass & Gradient" Rule
To elevate the "Technical" aspect into "Premium," use Glassmorphism for floating navigation elements or modal overlays.
- Use semi-transparent variants of `surface-container` (approx 70-80% opacity) with a `32px backdrop-blur`.
- **Signature Texture:** Apply a subtle linear gradient to main CTAs (from `primary` to `primary-container`) to give them a "machined" metallic sheen rather than a flat plastic feel.

---

## 3. Typography: Editorial Technicality
The system pairs **Space Grotesk** (a tech-leaning sans with geometric quirks) with **Inter** (the gold standard for functional legibility).

- **Display & Headlines (Space Grotesk):** These are the "hooks." Use `display-lg` (3.5rem) with tight letter-spacing (-0.02em) to create a bold, structural impact.
- **Body & Titles (Inter):** High-readability sans-serif. Use `body-lg` (1rem) for project descriptions to maintain an editorial quality.
- **Labels (Space Grotesk):** For technical data points, tags, and small metadata, use `label-md` in all-caps with increased letter-spacing (+0.05em) to mimic a professional IDE (Integrated Development Environment).

---

## 4. Elevation & Depth: Tonal Layering
We reject traditional drop shadows in favor of **Ambient Light** and **Tonal Stacking**.

- **The Layering Principle:** Depth is achieved by placing a darker surface (`surface-container-lowest`) inside a lighter section (`surface-container-low`). This "recessed" look feels more technical and precise than a floating shadow.
- **Ambient Shadows:** For elements that *must* float (like tooltips), use a tinted shadow: `0px 20px 40px rgba(0, 0, 0, 0.4)`. The shadow must never be pure black; it should feel like a soft occlusion of the background light.
- **The "Ghost Border" Fallback:** If a divider is required for accessibility, use the `outline-variant` token at **15% opacity**. This creates a "suggestion" of a line that only appears when the eye looks for it.

---

## 5. Components: Functional Precision

### Buttons
- **Primary:** Gradient from `primary` to `primary-container`. `border-radius: sm` (0.125rem) for a sharp, technical edge.
- **Secondary:** Transparent background with a `Ghost Border`. On hover, fill with `surface-container-highest`.
- **States:** Hover should trigger a subtle shift in `surface-brightness`. Active (click) should involve a 2% scale-down to feel tactile.

### Cards & Projects
- **Rule:** Forbid divider lines. Use `surface-container-low` as the card background against a `surface` page.
- **Interaction:** On hover, the card should transition to `surface-container-high` and the `secondary` (Turquoise) accent should appear as a 2px vertical "status bar" on the left edge.

### Chips & Tags
- Use `tertiary-container` for backgrounds with `on-tertiary-container` (#34b48a) for text. These should be `rounded-full` to contrast against the sharp-edged cards, signaling they are interactive "pills."

### Input Fields
- Understated and "ghostly." Background: `surface-container-lowest`. Bottom border only, using `outline-variant` at 20% opacity. Focus state: Border becomes 100% `primary` and text glows slightly.

### Additional Component: The "Status Indicator"
- For a portfolio site, include a "System Status" component in the footer or header: A small pulsing dot (`tertiary` Green) next to a `label-sm` text (e.g., "AVAILABLE FOR PROJECTS"). This reinforces the "Technical Dashboard" mood.

---

## 6. Do's and Don'ts

### Do:
- **Use "Space" as a tool:** Allow large gaps between sections (using `80px`, `120px`, or `160px` jumps) to emphasize the Zen Garden vibe.
- **Align to a Grid, but break it:** Place technical metadata in a sidebar that sits outside the main content column.
- **Use Monospace for Numbers:** Ensure all dates, version numbers, or stats use a monospaced font-weight to maintain the developer aesthetic.

### Don't:
- **Don't use pure black (#000):** It kills the depth. Stick to the `surface` tokens.
- **Don't use rounded corners (lg/xl):** Stay within `none`, `sm`, or `md` for structural elements. Large rounded corners feel "bubbly" and consumer-grade, not technical.
- **Don't use 100% white for body text:** Use `on-surface-variant` (#c2c7ce) for long-form text to reduce eye strain and look more sophisticated. Use `on-surface` (#e2e2e8) only for high-priority headings.
