# House of Lions website

Sample redesign of [houseoflions.in](https://www.houseoflions.in): a static, five-page site (Home, About, Solutions, Insights, Contact) with no build tools needed to host it.

## Run it locally

Open `index.html` in a browser, or serve the folder:

```
python3 -m http.server 8000
```

## Publish on GitHub Pages

Repository **Settings → Pages → Deploy from a branch → `main` / root**. The site is live at `https://<username>.github.io/<repo>/` within a minute or two. Point `houseoflions.in` at it later by adding a `CNAME` file.

## Editing

The pages are generated from `build.py`, which holds all copy, case studies, capabilities, testimonials and team details in one place. Edit it, then run:

```
python3 build.py
```

Styles live in `assets/style.css`, behaviour (menu, the hero lion, filters, form) in `assets/main.js`.

## Before launch

- Connect the contact form to a backend (Formspree, Netlify Forms or HubSpot). It currently validates and shows a thank-you message but does not send anything.
- Replace the case-study artwork with real project photography where available, and add outcome figures the clients have approved.
- The six Perspectives essays are proposed topics; write or swap them before going live.
- Confirm testimonial wording, mentor bios and office locations with the people named.
