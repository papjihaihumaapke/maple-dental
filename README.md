# Maple Dental Vancouver: website

A static site with no framework or dependencies. Each page lives at `/<page>/index.html`, so URLs are clean: `/`, `/about/`, `/services/`, `/new-patients/`, `/contact/` and `/privacy-policy/`.

## Edit and rebuild

The shared header, footer, CTA band, icons and schema markup are defined once in `src/build.py`. To regenerate every page after an edit:

```
python3 src/build.py
```

To preview locally, run this from the project root, then open http://localhost:8765:

```
python3 -m http.server 8765
```

Links are root-relative, so opening the files directly with `file://` won't work.

## Settings to update (top of `src/build.py`)

| Setting | Current value | Replace with |
|---|---|---|
| `BOOKING_URL` | `tel:+16042614607` | [ONLINE BOOKING URL] |
| `REVIEWS_URL` | Correctly spelled Google Maps search | [CORRECT GOOGLE REVIEWS URL] (Google Business Profile) |
| `FORM_ACTION` | `#` (form inactive; tells visitors to call or email instead) | [FORM ENDPOINT] such as Formspree or Netlify Forms |

## Client content checklist

Placeholders appear on the site as yellow `[BRACKETED]` text.

**Home**
- [CLINIC INTERIOR OR DR. LI WITH A PATIENT] hero photo
- [EDUCATION AND YEARS IN PRACTICE]
- [CONFIRM after-hours process]
- [PASTE REAL REVIEWS]: genuine Google reviews only
- [DIRECT BILLING / INSURANCE DETAILS], [PAYMENT OR FINANCING OPTIONS]
- [PARKING / TRANSIT / ELEVATOR ACCESS]
- [CONFIRM: cleanings, exams, fillings?] decides whether to add a fifth "General & Preventive Care" card (see the HTML comment in the services section)

**About**
- [EDUCATION / BACKGROUND] for Dr. Li
- [TEAM PHOTOS AND NAMES]
- [CLINIC PHOTO GALLERY]: reception, treatment room, equipment

**Services**
- Service photos or illustrations (4)
- [AAID LOGO] (the ICOI logo is already in place)
- [ADDITIONAL SERVICES], or remove the block
- [IMPLANT FAQS FROM CLIENT] (5 accordion slots)

**New Patients**
- First-visit details, what to bring, cancellation policy

**Global**
- [SOCIAL LINKS] in the footer
- Privacy Policy text, which must reflect BC PIPA

## Notes

- Dr. Li's coat in the existing photo shows Université Laval. Confirm his education before adding it to the bio.
- The Single-Tooth and Multiple Implants descriptions and every "Who it's for" line are new, plain-language copy, because the current site lists these services without descriptions. Have the clinic review them.
- Accent colours: buttons use coral `#C4513D` with white text (4.57:1). Coral text on the off-white and teal-tint backgrounds only reaches about 4.1 to 4.3:1, so eyebrows and links use a slightly deeper `#A8402E` (at least 5.5:1 on all light backgrounds). On dark teal, eyebrows use a pale salmon tint `#F4B3A6` (6.8:1). The original `#EF8E7E` appears only in small decorative dots and lines.
