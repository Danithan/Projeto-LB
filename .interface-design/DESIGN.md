---
name: Projeto LB-PRT
colors:
  surface: '#f9f9f7'
  surface-dim: '#dadad8'
  surface-bright: '#f9f9f7'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f4f2'
  surface-container: '#eeeeec'
  surface-container-high: '#e8e8e6'
  surface-container-highest: '#e2e3e1'
  on-surface: '#1a1c1b'
  on-surface-variant: '#3f4944'
  inverse-surface: '#2f3130'
  inverse-on-surface: '#f1f1ef'
  outline: '#6f7973'
  outline-variant: '#bfc9c2'
  surface-tint: '#246a51'
  primary: '#246a51'
  on-primary: '#ffffff'
  primary-container: '#6baf92'
  on-primary-container: '#00412e'
  inverse-primary: '#8fd5b6'
  secondary: '#356287'
  on-secondary: '#ffffff'
  secondary-container: '#a8d3fe'
  on-secondary-container: '#2e5b80'
  tertiary: '#63578a'
  on-tertiary: '#ffffff'
  tertiary-container: '#a89ad2'
  on-tertiary-container: '#3c3161'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#abf1d1'
  primary-fixed-dim: '#8fd5b6'
  on-primary-fixed: '#002115'
  on-primary-fixed-variant: '#00513a'
  secondary-fixed: '#cde5ff'
  secondary-fixed-dim: '#a0cbf5'
  on-secondary-fixed: '#001d32'
  on-secondary-fixed-variant: '#194a6e'
  tertiary-fixed: '#e8ddff'
  tertiary-fixed-dim: '#cdbef9'
  on-tertiary-fixed: '#1f1242'
  on-tertiary-fixed-variant: '#4b3f70'
  background: '#f9f9f7'
  on-background: '#1a1c1b'
  surface-variant: '#e2e3e1'
typography:
  display-lg:
    fontFamily: Quicksand
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Quicksand
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-lg-mobile:
    fontFamily: Quicksand
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  title-md:
    fontFamily: Quicksand
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Nunito Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Nunito Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Nunito Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-padding: 24px
  gutter: 20px
  stack-sm: 12px
  stack-md: 24px
  stack-lg: 48px
---

## Brand & Style

The design system is built upon the concept of "Clinical Softness." It bridges the gap between a high-functioning medical tool for therapists and a safe, non-threatening digital environment for children. The style is a blend of **Minimalism** and **Soft Modernism**, emphasizing clarity, reduction of cognitive load, and emotional stability.

The interface prioritizes an "Off-white" foundation to minimize eye strain during long clinical sessions. The visual language avoids the cold, sterile nature of corporate software by using organic shapes and a gentle color palette, while maintaining professional rigor through structured layouts and meticulous typography. Every interaction should feel intentional, supportive, and calm.

## Colors

The palette is anchored in muted, nature-inspired tones that promote focus and serenity.

- **Primary (Mint Green):** Used for primary actions and "Success" states. It represents growth and safety. (`#246A51` / Container: `#6BAF92`)
- **Secondary (Cerulean Blue):** Used for navigation and informative elements. It provides a grounded, trustworthy feel. (`#356287` / Container: `#A8D3FE`)
- **Tertiary (Soft Lavender):** Reserved for secondary highlights, accents, and specialized progress tracking. (`#63578A` / Container: `#A89AD2`)
- **Neutral (Off-White):** The canvas of the application (`#F9F9F7`). It reduces the harsh contrast of pure white, making the UI more accessible to neurodivergent users.
- **Text/Inks:** Deep charcoal (`#1A1C1B` / `#3F4944`) instead of pure black to maintain the "soft" visual hierarchy.

## Typography

This design system utilizes two highly legible, rounded sans-serifs to ensure a friendly yet professional tone.

- **Quicksand** is used for headlines. Its rounded terminals feel approachable to children and less intimidating than standard geometric sans-serifs.
- **Nunito Sans** handles the body text and functional labels. It offers superior readability for therapists reviewing clinical notes while maintaining the soft aesthetic.
- **Scale:** All font sizes are slightly oversized compared to standard SaaS products to ensure high legibility and an "obvious" information hierarchy.

## Layout & Spacing

The layout follows a **Fixed-Fluid Hybrid** model. Content is centered within a maximum width of 1200px on desktop to prevent eye-scanning fatigue, while elements within containers use a fluid 8px-based grid.

- **Margins:** Generous white space (stacking) is used to separate distinct therapeutic sections.
- **Mobile:** Transition to a single-column layout with 16px side margins.
- **Touch Targets:** Minimum height for interactive elements is 48px to accommodate developing motor skills in children and rapid data entry for therapists.

## Elevation & Depth

To maintain a "Sober and Clean" appearance, this design system avoids heavy drop shadows. Depth is communicated through:

- **Tonal Layers:** Using slightly darker neutral backgrounds (`#EFEEEA` / `#EEEEEC`) for sidebars or container wells.
- **Soft Outlines:** Elements like cards use a 1px border in a muted version of the primary or neutral color rather than shadows.
- **Active State:** When an item is selected or hovered, a very soft, diffused ambient shadow (8% opacity) may be applied to suggest "lifting" towards the user.

## Shapes

The shape language is consistently "Rounded" (0.5rem base). This choice removes the "sharpness" associated with aggressive corporate tools, creating a friendlier environment.

- **Cards:** Use `rounded-lg` (1rem) to create a soft frame for content.
- **Inputs & Buttons:** Use `rounded` (0.5rem) to balance a modern look with high touchability.
- **Icon Containers:** Often uses a full-circle (pill) shape to denote help or status.

## Components

- **Buttons:** Large, high-contrast surfaces. The "Primary" button uses the Mint Green background with dark text. "Secondary" buttons use a thick 2px outline. No "ghost" buttons—all actions must look clearly clickable.
- **Status Tags:** Pills with high-contrast backgrounds. "Done" uses the Primary Mint; "Pending" uses a soft Ochre; "Not Started" uses a light Neutral Gray. Text inside tags is always bold and Uppercase for instant recognition.
- **Cards:** Every clinical task or child profile is housed in a card with a subtle border. Content within cards should have a padding of at least 24px.
- **Input Fields:** Large text areas with 18px font size. Borders thicken (2px) and change color to Cerulean Blue on focus to provide immediate visual feedback.
- **Feedback Indicators:** Success/Error states should include both a color change and an icon (check/cross) to ensure accessibility and clarity for younger users.
- **Progress Bars:** Thick, rounded bars using the Tertiary Lavender to track session completion, making "progress" feel like a gentle achievement.
