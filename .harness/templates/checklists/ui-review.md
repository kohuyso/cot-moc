# UI Review Checklist: Interactive Mockup & Prototype Specification

**Target Artifacts**: `artifacts/ui-mockup.html`, `artifacts/ui-spec.md`, `artifacts/ui-verdict.json`, `artifacts/ui-verdict.md`  
**Reviewer Role**: `sdlc-ui-reviewer` (Challenger / Independent UI Finish-Gate Reviewer)  
**Producer Role**: `sdlc-ui-designer` (UI/UX Designer)  
**Standards Alignment**: WCAG 2.1 AA Accessibility Guidelines, Atomic Design Principles, IEEE 1028 (Software Reviews and Audits)  
**Marker Semantics**: Mark `[x]` only when the UI deliverable passes objective and verifiable inspection.

---

> [!IMPORTANT]
> **Adversarial Gate & Deterministic UI Finish Policy**:
> Every user-facing feature with `has_ui == true` must undergo independent adversarial review before code implementation.
> - **Zero Self-Approval**: `sdlc-ui-reviewer` must NEVER review or approve prototypes it authored itself.
> - **Mandatory 4-State Validation**: Mockups MUST simulate all 4 core states (`normal`, `empty`, `loading`, `error`). If ANY state is missing or unimplemented, approval is strictly forbidden.
> - **Anti-AI-Slop Floor**: Generic AI aesthetics (default purple/cream palettes, unstyled cards, lorem ipsum placeholders) must be rejected with actionable pushback.
> - If ANY blocker/high defect exists, the reviewer MUST issue `pushback --loop UI_REVIEW` (`python -m sdlc_harness.cli transition --run-id <run-id> --action pushback --loop UI_REVIEW`).

---

## 1. SRS & Story Coverage
- [ ] `CHK-UI-001`: Are 100% of user-facing functional requirements (`FR-xxx`) from `artifacts/requirement-analysis.md` and `artifacts/requirement.json` mapped to concrete screens and itemized in `ui-verdict.json.requirements_covered`?
- [ ] `CHK-UI-002`: Do all primary user journeys and persona task flows defined in the requirements have clear, intuitive, and unbroken navigation paths?
- [ ] `CHK-UI-003`: Are all essential business data attributes, form controls, filters, status indicators, and call-to-action buttons represented accurately without missing functional scope?
- [ ] `CHK-UI-004`: Does `artifacts/ui-spec.md` provide a complete component hierarchy and screen inventory corresponding to the requirement specification?

## 2. 4 Mandatory States (Normal, Empty, Loading, Error)
- [ ] `CHK-UI-005`: **Normal / Success State (`states_validated.normal: true`)**: Are screens fully rendered with realistic business data, clear visual hierarchy, proper information density, and functional interaction targets?
- [ ] `CHK-UI-006`: **Empty State (`states_validated.empty: true`)**: When collections or tables have zero records, does the view present helpful explanatory messaging, relevant iconography, and an obvious Call-To-Action (CTA) guiding the user to create or import initial data?
- [ ] `CHK-UI-007`: **Loading / Skeleton State (`states_validated.loading: true`)**: Are layout-preserving skeleton loaders or progressive indicators displayed during data fetching to prevent jarring layout shifts (CLS) and keep the user informed?
- [ ] `CHK-UI-008`: **Error / Validation State (`states_validated.error: true`)**: Are form input validation errors, API failure banners, and system error dialogs explicitly simulated with clear, human-readable explanations and actionable retry/recovery actions?
- [ ] `CHK-UI-009`: **Interactive State Switcher**: Does `artifacts/ui-mockup.html` embed an interactive state toolbar allowing the reviewer and stakeholders to toggle seamlessly between Normal, Empty, Loading, and Error states on each screen?

## 3. Anti-Slop & Product Specificity
- [ ] `CHK-UI-010`: **Palette Authenticity**: Has the design avoided clichéd AI defaults (such as generic saturated purple-to-violet gradients, pastel cream card backgrounds, or indiscriminate rounded card bloat) in favor of a deliberate, brand-specific color system (4–6 hex tokens) defined in `ui-spec.md`?
- [ ] `CHK-UI-011`: **Realistic Domain Data**: Is the prototype completely free of lazy placeholder text (`lorem ipsum`, "Test User", "Item 1", dummy zeros)? Does it use domain-specific terminology, authentic currency/date formatting, and localized business data?
- [ ] `CHK-UI-012`: **Intentional Visual Hierarchy & Typography**: Are typography pairings and font scales functional, readable, and structured (H1, H2, body, caption) with an intentional 4/8px spacing grid?
- [ ] `CHK-UI-013`: **Micro-Interactions & Component Feedback**: Do buttons, links, inputs, and interactive rows have explicit hover, active, focus, and disabled states with visible feedback?

## 4. Responsive & Mobile Viewports (1280px & 375px)
- [ ] `CHK-UI-014`: **Desktop Viewport (1280px)**: Is the layout optimized for widescreen displays with clean multi-column layouts, persistent navigation bars/sidebars, and appropriate data density?
- [ ] `CHK-UI-015`: **Mobile Viewport (375px)**: Does the layout gracefully reflow into a clean single-column structure with mobile-friendly drawers/bottom navigation, stacked form controls, and zero horizontal scrolling?
- [ ] `CHK-UI-016`: **Viewport Switcher / Fluidity**: Does `artifacts/ui-mockup.html` provide responsive viewport controls (Desktop 1280px vs Mobile 375px) or demonstrate robust fluid responsive behavior without layout breakage?

## 5. Accessibility Floor (WCAG 2.1 AA & Touch Targets)
- [ ] `CHK-UI-017`: **WCAG AA Contrast Ratio**: Does all standard body text meet the minimum 4.5:1 contrast ratio against its background, and large headings/essential graphical controls meet at least 3:1?
- [ ] `CHK-UI-018`: **Touch Target Size**: Do all clickable buttons, touch targets, icon controls, and interactive form fields meet the minimum physical size of $44 \times 44\text{ px}$ on mobile viewports?
- [ ] `CHK-UI-019`: **Semantic HTML & Focusability**: Are semantic elements (`<header>`, `<nav>`, `<main>`, `<button>`, `<input>`) utilized rather than clickable `<div>` wrappers, with visible keyboard focus rings (`focus:ring`)?
- [ ] `CHK-UI-020`: **Accessibility Verdict**: Is the accessibility evaluation verified and recorded in `artifacts/ui-verdict.json` (`accessibility_passed: true`)?

## 6. Real Page Baseline, Target Components & Mode Switcher
- [ ] `CHK-UI-021`: **Real Page HTML Baseline**: Did the designer inspect the existing frontend codebase (`frontend/src/pages/`, `components/`) and extract the actual page HTML/DOM layout as the baseline (`Before`), instead of imagining a synthetic screen from scratch?
- [ ] `CHK-UI-022`: **Mode Switcher (Before vs After)**: Does `artifacts/ui-mockup.html` embed an interactive Mode Switcher toggle (`Before` vs `After`) with visual diff highlights showing added, modified, or removed/hidden components?
- [ ] `CHK-UI-023`: **Anti-Text-Card Enforcer**: Is the deliverable completely free of plain text card summaries (e.g. static white cards with bullet points describing changes)? Does it render the real interactive visual application interface?
- [ ] `CHK-UI-024`: **Target File & Component Transparency**: Does the prototype header and `ui-spec.md` explicitly list all target frontend file paths (e.g. `frontend/src/pages/BoothScreenPage.tsx`) being modified?

