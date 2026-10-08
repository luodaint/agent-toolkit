# Conditional readiness checklist

Select the sections that match the app. Start with shared basics, then relevant
surfaces and capabilities. Confirm each item's applicability and evidence; an
internal dashboard, API or CLI does not inherit a marketing site's requirements.

## Shared basics

- **Core journey:** can the intended user complete the main task from a fresh
  start? Check onboarding/setup, empty data, invalid inputs and recovery, not just
  the happy-path demo. Sample data and placeholders must be intentional.
- **Failures:** errors give an actionable next step without exposing internals.
  Timeouts, retries and duplicate submissions behave sensibly; success messages
  reflect actual completion rather than only a request being sent.
- **Release configuration:** required environment settings are documented by name,
  development defaults do not leak into release builds, credentials stay private,
  and advertised runtime/platform support matches tested configurations.
- **Meaningful checks:** the project's test/build/lint checks cover its main journey
  and important failure paths. Report unrun checks; do not assume CI exists or add
  a pipeline solely because this skill is used.
- **Support and trust:** there is a real, monitored contact/support or issue channel
  appropriate to the audience. Product claims, pricing and links match behavior;
  remove broken links, dead buttons and unintended sample contact details.
- **Data boundaries:** where data is stored or shared, basic ownership/access checks,
  retention and recovery are understood. Distinguish evidence of a problem from a
  recommendation for deeper security validation.

## Public web pages: marketing, content, ecommerce, public SaaS surfaces

- **Identity:** useful titles/descriptions for each relevant public page, favicon/app icons, brand assets and
  a meaningful not-found experience. Confirm invalid URLs return the intended HTTP
  status; a friendly error page with a 200 response can conceal broken routing.
- **Search visibility:** intentional indexing policy, appropriate robots directives,
  sitemap where useful, canonical URLs and correct production hostname. Check the
  framework's generated output and host configuration, including accidental preview
  `noindex` settings. A robots directive is not access control.
- **Sharing:** appropriate Open Graph/social title, description and image for shareable
  pages; check actual rendered metadata, resolvable URLs and image assets. Don't
  publish private application data in link previews or search metadata.
- **Mobile layout:** navigation, forms, dialogs and primary actions work at narrow
  widths and zoomed text, without horizontal overflow or inaccessible controls.
- **Accessibility:** keyboard navigation, visible focus, semantic headings, labelled
  inputs, meaningful link text, sufficient contrast and usable validation feedback.
  Give informative images appropriate alternatives; decorative images need empty
  alternatives rather than redundant descriptions.
- **Media and speed:** sensible image dimensions/compression and suitable formats
  such as WebP/AVIF for photos; SVG or other formats may suit different assets.
  Reserve layout space, avoid unnecessary blocking resources, and lazy-load only
  where it fits. Measure representative pages before proposing optimizations.
- **Interactions:** loading, empty, success and error states; disabled/duplicate-submit
  handling; form validation; usable unavailable/not-found states; recovery when
  navigation or network requests fail.
- **External obligations:** confirm needed terms, privacy disclosures, consent and
  contact details against business model, audience and data use. Don't assume every
  site needs a cookie banner or that adding policy pages proves compliance.
- **Learning from users:** decide whether analytics is needed and what question it
  answers. If used, verify relevant events, environment separation and privacy
  settings; never treat installing a tracking SDK as a universal launch requirement.

## Interactive web apps and internal tools

- Verify real entry points, deep links, refresh behavior, browser history and session
  expiry. Private routes should have intentional indexing and metadata policies.
- Check empty/loading/error states, unsaved changes, pagination/filter behavior and
  permission-denied recovery on actual user journeys.
- Test keyboard and mobile use appropriate to the audience. Confirm layout and
  form controls with realistic content, not just short demo strings.
- Check timezone, locale, date/number formatting and export/import behavior when
  those are product capabilities. An internal tool may need auditability and access
  control more urgently than public SEO or a social image.

## APIs, services and background workers

- Provide the API/consumer setup contract: endpoint/version, authentication model,
  request/response examples, validation and consistent error/status behavior.
- Check authorization/resource ownership, payload limits and abuse/rate controls
  where exposure warrants them. CORS is a browser policy, not authorization.
- Verify timeouts, cancellation and retry/idempotency semantics for writes and
  integrations. Worker failures need bounded retries, visibility and a recovery path.
- Check health/readiness signals and documented dependencies; graceful shutdown
  should not lose accepted work. Confirm observability without logging credentials
  or sensitive request bodies.
- Verify migration/upgrade compatibility, persistence and an appropriate backup or
  recovery mechanism. Look for evidence of restore/recovery testing, not just the
  existence of a scheduled backup job.

## Mobile and desktop apps

- Check first-run onboarding, app icon, supported devices/OS versions, layout/text
  scaling, screen-reader access and primary navigation/input methods.
- Verify permission explanations, denial/revocation paths and minimal requested
  permissions. Determine whether offline mode, reconnect and local persistence
  matter; don't invent offline support as a requirement for every product.
- Check interrupted/background operations, resume, expired sessions and deep links
  where supported. Test update compatibility with existing user data and recovery
  after failed synchronization.
- If distributed through a store or installer, review packaging/signing, identifiers,
  version/build numbers, actual support/privacy URLs, required disclosures and
  store-specific release requirements using current official documentation.

## CLIs, libraries and developer tools

- Verify installation, quickstart and a minimal example on advertised runtimes/OSes.
  Check help/version output, configuration discovery and useful error/exit behavior
  for a CLI; check exported APIs and types where applicable for a library.
- Confirm package contents, license, dependency constraints and absence of private
  files or secrets. Ensure examples use published interfaces rather than unpublished
  local code, with release/version and compatibility guidance.
- Destructive operations need appropriate safeguards; diagnostics should avoid
  exposing credentials. For tools producing files, inspect overwrite behavior and
  preservation of unrelated user work.
- Recommend an issue/support channel and a reproducible bug-report path. Favicon,
  robots, cookie UI and social cards apply only to any separate public website.

## Capability checks: use only when present or required

### Accounts, organizations and user data

Check signup/login/logout, relevant email verification and password-reset or
identity-provider recovery flows, expired sessions and meaningful denied-access
states. Verify role/tenant boundaries and invitation lifecycle where they exist.
For account data, determine export/deletion and retention requirements; inspect
what actually happens instead of inferring it from a settings button.

### Payments, subscriptions and commerce

Check displayed pricing/currency/taxes against the actual checkout configuration,
payment failure/cancellation and entitlement state. Verify webhook authenticity,
retry/idempotency behavior, refunds or subscription cancellation where relevant,
and separation of test/live credentials. Use sandbox fixtures; don't make live
purchases or mutate real subscriptions as part of this review.

### Email, notifications and external integrations

Check relevant verification/reset/receipt messages, usable links, failure handling,
delivery configuration and sender identity. Inspect provider setup or sandbox
results; don't send real messages to prove a checkbox. Review recipient consent,
unsubscribe/preferences where appropriate, webhook validation and provider limits.

### Uploads and user-generated content

Check file size/type handling, storage access, private-file URLs and meaningful
rejection states. Determine whether moderation/reporting is needed for actual
content exposure, and whether dangerous files or rendered content cross a trust
boundary. Deletion and retention should include associated stored objects.

### Production hosting and operations

Check production domains/TLS, deploy configuration, secret management, error
visibility and an owned response path. Match uptime/monitoring requirements to
the product's actual commitments. Inspect deployment/rollback and data recovery
evidence; monitoring alone doesn't provide recovery. Don't deploy or change provider
settings during a review-only task.

### AI-powered features

When model calls are part of the product, check timeout/provider-error behavior,
cost/usage limits and sensitive-data handling. Treat generated output as untrusted
input, and preserve user/tenant permissions for tools or retrieved content. Verify
that the product communicates appropriate limits for its intended use; a chat demo
does not establish safe tool execution or predictable operating cost.
