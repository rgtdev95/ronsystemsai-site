# 12 — Booking follow-up

What happens after someone books a discovery call, done by hand for now, and an idea for automating it later. **Status: manual. The automation is an idea, not built (as of 2026-11-08).**

## The problem

Bookings go through a Proton Calendar booking page (decision 15 in [08-open-decisions.md](08-open-decisions.md)). Its form only asks for **name and email**:

- The discovery call is a **phone call**, but Proton doesn't collect a phone number.
- There's no notes field, so the visitor can't tell you anything before the call (what the business does, the tools they use, what's slowing them down).
- Proton has no API or webhooks for bookings. A booking appears in your Proton calendar, and the visitor gets a confirmation email.

## For now: follow up by hand

1. **In the Proton booking page's notes** (shown to visitors before they book), add:
   > After you book, I'll email you to ask for the best number to call and anything you'd like me to know.
2. **After each booking,** reply to the person using the template below. You always have their email address, so this works every time.
3. **Before the call,** read their reply and note the number on the calendar event.

### Email template

> **Subject:** Your call with Ron Systems AI on {day}
>
> Hi {first name},
>
> Thanks for booking a call for {day and time}. Two quick things so we can make the most of the 30 minutes:
>
> 1. What's the best phone number to reach you, with the country code?
> 2. Anything you'd like me to know beforehand: what your business does, the tools you use, and what's slowing you down. A few lines is plenty.
>
> Talk soon,
> Ron

Save it as a template in Proton Mail so each follow-up takes a minute.

## Idea: automate it

```
Someone books on Proton
   → a booking email arrives in Ron's inbox (to be confirmed, see "Check first")
   → Proton Mail Bridge on the VPS gives the automation IMAP/SMTP access to the inbox
   → n8n (or a small Python worker) reads the visitor's name, email and time
   → it sends the email template above, filled in
   → when the visitor replies, AI turns the reply into a short pre-call brief and emails it to Ron
     ("12-person clinic, uses Xero and Google Sheets, wants to stop re-typing invoices, call +61…")
```

### Where AI fits, and where it doesn't

- **First email: no AI.** A fixed template with the name and time filled in is predictable and needs no judgment. An AI writing to prospects unsupervised can say odd things.
- **Pre-call brief: AI.** Summarizing a free-form reply into a few lines before the call is where it saves real time.

### Pieces to add

| Piece | Where | Notes |
|---|---|---|
| Proton Mail Bridge | New service in `docker/compose.yml` | Proton's IMAP/SMTP bridge. Built for desktops; on a server it runs from a community Docker image with a one-time interactive login. Needs a paid Proton plan. |
| n8n (or a Python worker) | New service in `docker/compose.yml` | Watches the inbox over IMAP, sends the email over SMTP, calls the AI. Keep its editor off the public internet (reach it through an SSH tunnel). |
| AI provider | API key in `.env` | Only for the pre-call brief. |
| Privacy page | `app/templates/pages/privacy.html` | Say that replies to booking emails are processed by an AI service to prepare for the call. Consider removing the phone number before sending text to the AI. |

### Check first

1. **What Proton sends you when someone books.** Book a test call on your own page from another email address and look at what arrives: sender, subject, and whether it includes the visitor's name, email and time. Proton's documentation only mentions the visitor's confirmation email and the calendar entry, so a usable email for you isn't guaranteed.
2. **Fallback if there's no usable email:** share the Proton calendar through a read-only link (an ICS feed) and have the automation check it for new events. Check whether the feed includes the attendee's email.
3. **Matching replies to bookings,** for example by subject line or email thread, so each brief belongs to the right call.
4. **Your Proton plan** supports Bridge (and SMTP submission if sending without Bridge).

### Why not now

With a few bookings a month, a manual reply takes about a minute each. The automation is worth building when follow-ups become a chore, or as a demo of your own automation services. It's exactly what you sell, and it could become a case study ([11-case-studies.md](11-case-studies.md)).

### Alternative: a booking tool that asks the questions itself

Cal.com (free) and Calendly can add a phone number field and custom questions to the booking form, which removes the follow-up step entirely. The catch: neither reads a Proton calendar directly, so people could book over other appointments. Cal.com's "ICS Feed" app might block busy times from Proton's shared calendar link, but that's unverified. Switching only needs a new `BOOKING_URL` in `.env` plus small text changes on `/book/`, the privacy page and the terms page.

## References

- [Proton: Calendar appointment scheduling](https://proton.me/support/calendar-appointment-scheduling)
- [Proton: appointment scheduling (blog)](https://proton.me/business/blog/appointment-scheduling)
- [Headless Proton Bridge guide](https://ndo.dev/posts/headless_protonbridge)
- [Proton Bridge Docker image (community)](https://hub.docker.com/r/capitandavide/proton-bridge)
- [Cal.com: phone meetings and booking questions](https://cal.com/blog/phone-meetings-made-easy-cal-com-s-flexible-scheduling-solution)
- [Calendly: invitee questions](https://help.calendly.com/hc/en-us/articles/226893168)
